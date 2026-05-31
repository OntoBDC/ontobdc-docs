# TEST 005 - Storage Component Tests

## Purpose

This document describes the automated tests that currently validate the `storage` component behavior implemented in:

- `wip/src/ontobdc/storage`

The focus of this document is the current storage contract around:

- container creation
- root and container metadata separation
- RO-Crate behavior
- storage-specific checks and hotfixes

## Targeted Components

The current storage-related tests directly exercise these implementation areas:

- `wip/src/ontobdc/storage/adapter/repository.py`
- `wip/src/ontobdc/storage/plugin/command/create.py`
- `wip/src/ontobdc/storage/plugin/check/has_container_config_file/check.py`
- `wip/src/ontobdc/storage/plugin/check/is_root_set/check.py`
- `wip/src/ontobdc/storage/plugin/check/is_crate_healthy/hotfix.py`
- `test/stubs/rocrate/rocrate.py`

## Test Inventory

The current storage-focused automated tests documented here are:

- `test/src/ontobdc/storage/test_repository.py`
- `test/src/ontobdc/storage/test_checks.py`
- `test/src/ontobdc/storage/plugin/command/test_create.py`

These tests are included in the standard runner through:

- `test/config.yaml`

## 1. Repository-Level Crate Tests

### File

- `test/src/ontobdc/storage/test_repository.py`

### What It Tests

This test file validates the current behavior of `LoadedStorageContainerCrate`.

It covers:

- serialization when the caller provides a metadata file path
- refresh behavior for container-local crate metadata
- exclusion of internal storage files from the crate payload listing

### Scenario Coverage

#### 1.1 Serialize With Metadata File Path

- creates a temporary crate directory
- loads `LoadedStorageContainerCrate`
- calls `serialize()` with `ro-crate-metadata.json` as destination
- expects the crate to be written successfully by using the parent directory as the real target

#### 1.2 Refresh Excludes Internal Files

- creates a temporary crate directory
- adds `storage.rdf`
- runs `refresh()`
- expects:
  - `storage.rdf` not to be indexed as crate payload
  - hidden files not to be indexed
  - the crate to remain valid

### What Part Of Storage This Covers

- repository adapter behavior
- RO-Crate load and write semantics
- the rule that `storage.rdf` is not payload

## 2. Storage Check And Hotfix Tests

### File

- `test/src/ontobdc/storage/test_checks.py`

### What It Tests

This test file validates the current check/hotfix behavior under `storage/plugin/check`.

It covers:

- isolated root validation
- isolated container-config validation
- RO-Crate hotfix creation behavior

### Scenario Coverage

#### 2.1 Root Check Is Isolated

- patches the storage graph loader with a test double
- returns a valid root container
- expects `is_root_set/check.py` to succeed without depending on child-container validity

#### 2.2 Container Config Check Requires Local `storage.rdf`

- patches the storage graph loader with one registered child container
- expects `has_container_config_file/check.py` to fail when the child `storage.rdf` is missing
- then creates the child file
- expects the same check to pass

#### 2.3 Crate Hotfix Creates Metadata

- patches the storage graph loader with one registered child container
- runs `is_crate_healthy/hotfix.py`
- expects:
  - `ro-crate-metadata.json` to be created
  - `storage.rdf` not to appear as crate payload

### What Part Of Storage This Covers

- check isolation by responsibility
- container metadata repair
- RO-Crate repair behavior

## 3. Storage Create Command Tests

### File

- `test/src/ontobdc/storage/plugin/command/test_create.py`

### What It Tests

This existing test file validates the command-level behavior of `StorageCreateCommand`.

It covers:

- command acceptance rules
- response structure
- success and failure flows for container creation

### Why It Matters

The current storage behavior depends on `--create` as the command that materializes:

- the container-local `.__ontobdc__`
- the container-local `storage.rdf`
- the container-local `ro-crate-metadata.json`

That makes `test_create.py` the command-surface complement to the repository and check tests documented above.

## Coverage Summary

### Covered

- RO-Crate loading from a directory-based source
- RO-Crate serialization to directory targets
- exclusion of `storage.rdf` from crate payload
- isolated root check behavior
- isolated container-config check behavior
- crate hotfix creation behavior
- command-level container creation behavior

### Not Covered Well

- full end-to-end CLI invocation of `ontobdc storage --create`
- `storage --delete`
- `storage --list`
- full integration with the real external `rocrate` package instead of the test stub
- multi-container repair orchestration in one end-to-end CLI flow

## Operational Note

The storage test area now uses a layered strategy:

- unit-like tests for repository behavior
- focused tests for check/hotfix logic
- command-level tests for the storage plugin surface

This matches the current implementation split of the `storage` component:

- adapters own structured metadata behavior
- check plugins own integrity verification and repair
- command plugins own the CLI-facing action surface
