# RFC 006 - Container Dataset Identifier To Physical Name Contract

## Status

- **Status**: requested
- **Scope**: `ontobdc storage --container-id <container_id> --create <dataset_id>`
- **Primary surface**: `src/ontobdc/storage/plugin/command/dataset.py`

## Purpose

This RFC proposes a stricter contract between the logical dataset identifier and the physical folder name created inside a storage container.

The goal is to prevent the dataset creation command from accepting a logical identifier shape that can accidentally produce an invalid or unintended physical path.

## Context

The current dataset creation flow already follows the main architectural direction recorded in:

- [ADR009_layered_metadata_architecture_for_detachable_containers_and_federated_data.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR009_layered_metadata_architecture_for_detachable_containers_and_federated_data.md)

That means:

- dataset metadata is stored in the container-local `storage.ttl`
- the root storage graph is used for container discovery, not as the source of truth for datasets
- RO-Crate is not part of dataset registration

However, one contract remains underspecified.

The command currently accepts a dataset value that may be:

- a short identifier
- a URN
- or, more generally, any URI with a scheme

At the same time, the command still derives the physical folder name using string splitting against the OntoBDC dataset URN prefix.

This creates a mismatch between:

- the logical identifier contract
- and the filesystem path contract

## Motivation

ADR009 establishes that managed dataset state belongs to the container and must be governed locally.

That design assumes the dataset folder inside the container is a controlled local artifact.

If the command accepts arbitrary URIs and derives the physical folder name through a partial string operation, the resulting folder can become:

- semantically ambiguous
- structurally invalid
- or physically inconsistent with the intended dataset naming model

This weakens the local-governance guarantees that ADR009 is trying to enforce.

## Proposal

Define an explicit rule for how a dataset creation request becomes a physical folder name.

The implementation should choose one of these two models and document it clearly:

1. **Local identifier only for creation**
   - `--create` accepts only a local dataset identifier
   - the command always expands it to `urn:ontobdc:storage/dataset/<identifier>`
   - the physical folder name is exactly `<identifier>`

2. **URI accepted, but canonical physical-name extraction**
   - `--create` may accept a URI
   - the command extracts a canonical local dataset name through an explicit normalization rule
   - unsupported URI shapes are rejected instead of being turned into filesystem paths implicitly

The command should not derive the physical folder name through ad hoc string splitting that only works safely for a subset of accepted inputs.

## Constraints

The resulting contract should:

- keep the logical identifier and physical folder name semantically related
- remain deterministic
- remain container-local
- avoid accidental nested paths or malformed folder names
- be documented as part of the command behavior

It should not:

- treat arbitrary URI text as if it were already a safe filesystem segment
- rely on partial prefix stripping as the only normalization mechanism

## Expected Impact

If implemented, this RFC would likely affect:

- `src/ontobdc/storage/plugin/command/dataset.py`
- `src/ontobdc/storage/plugin/parameter/dataset.py`
- storage command documentation and storage specs

Likely new or updated tests:

- creation with short identifier
- creation with OntoBDC dataset URN
- rejection or normalization of non-OntoBDC URIs
- guarantees that the physical folder remains a single controlled local name

## Correlation With ADR009

ADR009 defines that datasets are managed locally inside the container and recorded in the container-local `storage.ttl`.

This RFC refines one operational consequence of that decision:

- if a dataset is local to the container, its physical directory name must also follow an explicit local contract

In other words:

- `ADR009` defines where dataset truth lives
- `RFC006` defines how the creation command should materialize that truth on disk safely

## Open Questions

- Should `--create` accept only local identifiers and URNs, or any URI at all?
- If URIs remain accepted, what is the canonical mapping from URI to physical folder name?
- Should the physical folder name be validated against a restricted character set?
- Should the command reject ambiguous inputs even if they can technically be represented on disk?

## Follow-Up

If accepted, the next step should be to define:

- the canonical input contract for `--create`
- the normalization rule from logical identifier to folder name
- the rejection rules for unsupported identifier shapes
- the regression tests that lock this behavior down
