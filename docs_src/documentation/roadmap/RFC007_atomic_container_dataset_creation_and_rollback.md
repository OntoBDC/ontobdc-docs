# RFC 007 - Atomic Container Dataset Creation And Rollback

## Status

- **Status**: requested
- **Scope**: container-local dataset creation workflow
- **Primary surface**: `wip/src/ontobdc/storage/plugin/command/dataset.py`

## Purpose

This RFC proposes that dataset creation inside a storage container should become atomic from the user point of view.

The goal is to prevent partial success scenarios in which the filesystem is mutated but the container-local `storage.ttl` fails to persist the corresponding dataset metadata.

## Context

The current command flow already aligns with the main storage architecture defined in:

- [ADR009_layered_metadata_architecture_for_detachable_containers_and_federated_data.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR009_layered_metadata_architecture_for_detachable_containers_and_federated_data.md)

Today, dataset creation already:

- resolves the target container through the root storage graph
- loads the container-local `storage.ttl`
- creates the dataset directory inside the container
- writes `hasPart`, `isPartOf`, and `prov:atLocation` in the container-local graph
- avoids RO-Crate synchronization during dataset creation

That direction is correct.

However, the current mutation order still allows a partial-failure window:

1. the dataset folder is created on disk
2. RDF persistence is attempted afterward
3. if RDF persistence fails, the command returns an error but the folder remains

This leaves behind a physical dataset directory that is not represented in the container-local source of truth.

## Motivation

ADR009 treats the container-local `storage.ttl` as the operational source of truth for managed dataset registration inside a container.

That means the command should not leave managed storage artifacts in a state where:

- the physical directory exists
- but the local storage graph does not acknowledge it

Such a split state weakens:

- local consistency
- auditability
- detachability guarantees
- predictable repair behavior

## Proposal

Make container dataset creation atomic at the command boundary.

The implementation may satisfy this in either of these ways:

1. **Create then rollback on persistence failure**
   - create the physical directory
   - attempt graph persistence
   - if persistence fails, remove the just-created directory before returning the error

2. **Stage then commit**
   - compute and validate everything first
   - persist through a staged or temporary workflow
   - expose the final directory only when the metadata write is guaranteed

The first version does not need a complex transaction framework.

A focused rollback rule is enough if it guarantees that a failed command does not leave a newly created orphan dataset directory behind.

## Constraints

The final behavior should:

- preserve the container-local `storage.ttl` as the authoritative registration record
- avoid orphan physical dataset directories created by failed commands
- keep error behavior deterministic and testable
- avoid reintroducing root-graph persistence for dataset state

It should not:

- silently tolerate divergence between the filesystem and container-local storage metadata
- delegate consistency recovery to later manual cleanup when the command itself can prevent the inconsistency

## Expected Impact

If implemented, this RFC would likely affect:

- `wip/src/ontobdc/storage/plugin/command/dataset.py`
- storage command tests under `test/src/ontobdc/storage/plugin/command`

Likely new or updated tests:

- forced failure during `storage.ttl` serialization
- assertion that the dataset directory does not remain after failure
- assertion that no dataset triples are left behind in the container graph after rollback

## Correlation With ADR009

ADR009 defines the container-local `storage.ttl` as the local governance artifact for managed dataset state.

This RFC refines the operational consequence of that rule:

- command failure must not leave a physical managed dataset without matching local registration

In other words:

- `ADR009` defines the local source of truth
- `RFC007` defines the failure-handling behavior needed to preserve that truth during mutation

## Open Questions

- Is rollback sufficient, or does the storage component need a broader transaction helper?
- Should the rollback cover only new directories, or also future dataset bootstrapping artifacts?
- How should the command behave if rollback itself fails?
- Should a later storage check/hotfix explicitly scan for orphan dataset directories as a defense-in-depth mechanism?

## Follow-Up

If accepted, the next step should be to define:

- the precise rollback boundary
- the expected error contract when persistence fails
- the cleanup behavior when rollback itself encounters an error
- the regression tests that force and verify the failure path
