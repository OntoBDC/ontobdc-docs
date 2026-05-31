# SPEC 012 - Storage Component Behavior

## Status

- **Status**: Working specification of the current storage behavior
- **Scope**: `src/ontobdc/storage`
- **Primary sources**:
  - `src/ontobdc/storage/__init__.py`
  - `src/ontobdc/storage/adapter/container.py`
  - `src/ontobdc/storage/adapter/repository.py`
  - `src/ontobdc/storage/plugin/command/create.py`
  - `src/ontobdc/storage/plugin/check`

## 1. Purpose

This specification describes the current runtime contract of the `storage` component.

It focuses on:

- the root storage index
- container-local metadata artifacts
- RO-Crate behavior per container
- storage integrity checks and hotfixes
- the current boundaries between root metadata and container-local metadata

## 2. Storage Model

The current `storage` component is organized around one root registry plus one local metadata area per registered container.

### 2.1 Root Storage Index

The root storage index is:

- `.__ontobdc__/storage.rdf`

Its role is to:

- register the root storage container
- register each local storage container
- keep the canonical RDF description of each registered container

The root graph is the source of truth for container registration.

### 2.2 Container-Local Metadata Area

Each registered local container has:

- `<container>/.__ontobdc__/storage.rdf`
- `<container>/.__ontobdc__/ro-crate-metadata.json`

These files are operational projections of the root registration, not independent registries.

Their role is to make each container self-describing and locally inspectable.

## 3. Artifacts

### 3.1 Root-Level Artifacts

- `.__ontobdc__/storage.rdf`
  - canonical container registry

### 3.2 Container-Level Artifacts

- `<container>/.__ontobdc__/storage.rdf`
  - RDF projection of the container triples registered in the root graph
- `<container>/.__ontobdc__/ro-crate-metadata.json`
  - RO-Crate metadata file for the container-local directory

## 4. Root Graph Behavior

`LoadedStorageGraph` is the main reader abstraction over the root storage graph.

### 4.1 `containers`

`LoadedStorageGraph.containers` iterates registered child containers and yields:

- container subject
- container config directory
- container-local `storage.rdf`

Important current rule:

- the `::ROOT::` container is excluded from `containers`

This means child-container iteration and root-container discovery are intentionally separate operations.

### 4.2 `get_root_container()`

`LoadedStorageGraph.get_root_container()` resolves the root container directly from the graph by the identifier:

- `::ROOT::`

This isolates root validation from child-container validity.

## 5. Container Creation Contract

The current `ontobdc storage --create <path>` flow behaves as follows:

1. Normalize the target path relative to the project root.
2. Create the target directory if necessary.
3. Load the root `.__ontobdc__/storage.rdf`.
4. Create and persist a new local container entry in the root graph.
5. Create `<path>/.__ontobdc__` if it does not exist.
6. Create `<path>/.__ontobdc__/storage.rdf` if it does not exist.
7. Copy the registered container triples from the root graph into the container-local `storage.rdf`.
8. Create `<path>/.__ontobdc__/ro-crate-metadata.json` if it does not exist.
9. Refresh the RO-Crate metadata so the crate file is current.

## 6. Container RO-Crate Behavior

The current RO-Crate behavior is implemented by `LoadedStorageContainerCrate`.

### 6.1 Loading

The crate is loaded from the container metadata directory using:

- `ROCrate(source=self.root_dir, gen_preview=False)`

This means the adapter treats the metadata directory as the load root, not the metadata file as a `read()` target.

### 6.2 Dictionary View

The current dictionary view returned by the adapter is the generated JSON-LD payload from:

- `self._crate.metadata.generate()`

### 6.3 Serialization

`LoadedStorageContainerCrate.serialize()` writes the crate to a directory, not to the metadata file path directly.

Current rule:

- if the provided destination looks like a file path, the adapter writes to its parent directory

This avoids treating `ro-crate-metadata.json` as an output directory.

### 6.4 Refresh

`LoadedStorageContainerCrate.refresh()` rescans the container metadata directory and rewrites the RO-Crate metadata.

Current exclusions are:

- hidden files
- `ro-crate-metadata.json`
- `storage.rdf`

This means the crate metadata does not index:

- the crate metadata file itself as a payload file
- the container-local RDF projection

The current intent is that `storage.rdf` remains an internal storage-control artifact, not container payload.

## 7. Integrity Checks

The current storage-specific checks are:

- `has_container_config_file/check.py`
- `is_root_set/check.py`
- `is_crate_healthy/check.py`

### 7.1 Container Config Check

`has_container_config_file/check.py` validates:

- the existence of the root `storage.rdf`
- each child container as a valid `URIRef`
- the existence of each child container `.__ontobdc__`
- the existence of each child container `storage.rdf`

It does not use the global `LoadedStorageGraph.is_valid()` gate.

### 7.2 Root Check

`is_root_set/check.py` validates:

- the existence of the root `storage.rdf`
- successful loading of the root graph
- the presence of `::ROOT::` through `get_root_container()`

It is intentionally isolated from child-container validity.

### 7.3 RO-Crate Check

`is_crate_healthy/check.py` validates:

- the existence and readability of each child container `ro-crate-metadata.json`
- the generated crate JSON-LD shape through `LoadedStorageContainerCrate.is_valid()`

## 8. Hotfix Behavior

The current storage hotfixes repair only the scope owned by their check.

### 8.1 Container Config Hotfix

`has_container_config_file/hotfix.py`:

- creates missing container `.__ontobdc__`
- creates missing container `storage.rdf`
- synchronizes registered root triples into the container-local RDF

### 8.2 Root Hotfix

`is_root_set/hotfix.py`:

- creates the root `storage.rdf` when missing
- ensures the `::ROOT::` container exists

### 8.3 RO-Crate Hotfix

`is_crate_healthy/hotfix.py`:

- creates missing `ro-crate-metadata.json`
- refreshes the container crate metadata
- preserves the current exclusion of `storage.rdf`

## 9. Design Characterization

The current `storage` behavior uses a layered metadata strategy:

- one root RDF registry
- one container-local RDF projection
- one container-local RO-Crate file

This is not a separate architecture from the rest of the CLI.

It is an implementation refinement inside the existing architecture defined by:

- shell wrappers as stable operational interface
- Python as the primary structured logic layer
- plugin-based command handling for the `storage` CLI surface

## 10. ADR Assessment

No new ADR is required for the current `storage` changes.

Reason:

- the recent changes are corrective and behavioral
- they clarify loading, writing, refresh, and validation rules inside an already accepted architecture
- they do not introduce a new architectural boundary, extension mechanism, or decision record-worthy trade-off

The current changes are therefore best captured as:

- updated working specifications
- updated test documentation

not as a new architectural decision.

## 11. Summary

The current `storage` component behaves as a layered metadata system with:

- a root RDF registry in `.__ontobdc__/storage.rdf`
- one container-local RDF projection per registered container
- one container-local `ro-crate-metadata.json` per registered container

Its current integrity rules are:

- root validation is isolated from child-container validity
- container-config validation is scoped to config artifacts
- crate health validation is scoped to crate metadata
- container RO-Crates exclude `storage.rdf` from payload indexing

This is the current working contract of `src/ontobdc/storage`.
