# UC05 - Manage Storage (`ontobdc storage`)

## Description
This use case manages the local storage index for OntoBDC datasets. It allows the user to list registered datasets, initialize a local storage path, and remove datasets from the index.

## Actors
- **User**: Needs to manage local datasets and storage repositories.
- **System (OntoBDC)**: Interacts with storage adapters to manage the local storage index, enabling listing, adding, removing, and refreshing dataset resources.

## Pre-conditions
- The project is initialized.
- The `storage` module dependencies (like `datapackage`, `rocrate`) are available.

## Flow of Events
1. The user runs `ontobdc storage` (no arguments).
2. The system checks whether a storage index exists (`.__ontobdc__/storage.rdf`).
3. If the index does not exist, the system warns that no storage has been initialized and suggests `ontobdc storage --local [path]`.
4. If the index exists, the system parses it and prints the registered datasets.
5. Optionally, the user runs `ontobdc storage --local [path]` to initialize/register a local storage path (default: project root when omitted).
6. The system resolves the provided path (relative paths are resolved against the project root) and validates that it exists and is a directory.
7. The system creates the storage index if needed, then registers the dataset location in the index and persists it to `storage.rdf`.
8. The system ensures the dataset has the expected RO-Crate/ICDD structure (creating `.__icdd__/payload/triples/ro-crate-metadata.json` when missing).
9. Optionally, the user runs `ontobdc storage --remove <dataset_id>` to remove a dataset.
10. The system removes the dataset entry from the index, saves the updated index, and reports success (or warns if the dataset is not found).

## Post-conditions
- The storage index is updated or displayed.
