# TEST 002 - CLI Init Entrypoint Test

## Purpose

This document describes the single automated test dedicated to the OntoBDC CLI initialization entrypoint:

- `src/ontobdc/test_cli_init.sh`

The scope of this document is limited to that file and to the behavior of `ontobdc init`.

## Targeted Components

The test directly exercises these implementation files:

- `wip/src/ontobdc/cli/__init__.py`
- `wip/src/ontobdc/cli/init.py`
- `wip/src/ontobdc/cli/message_box.sh`
- `wip/src/ontobdc/check/check.sh`

## Test File

- `src/ontobdc/test_cli_init.sh`

## What The Test Covers

- the initial uninitialized state, with no `.__ontobdc__/config.yaml`
- the error path triggered when a CLI command is executed before `ontobdc init`
- the `Not Initialized` error metadata rendered through the message box contract
- the styling of the `Not Initialized` guidance message
- rejection of the removed legacy command `ontobdc init context`
- execution of `ontobdc init venv`
- successful exit code for `ontobdc init venv`
- creation of `.__ontobdc__/config.yaml`
- persistence of `engine: venv`
- persistence of `directory.root.absolute_path`
- execution of the real post-init `check` flow
- absence of the `Root Directory Not Configured` error after initialization
- presence of `Infra: Root Absolute Path Configured` in the init output

## How The Test Works

1. Resolves the project root from the test file location.
2. Resolves `wip/src` as the Python import root.
3. Locates the CLI entrypoint at `wip/src/ontobdc/cli/__init__.py`.
4. Locates the original `wip/src/ontobdc/cli/message_box.sh`.
5. Creates a temporary backup of `message_box.sh`.
6. Replaces `message_box.sh` with a small capture script.
7. Executes `ontobdc check` in a fresh temporary directory before initialization.
8. Verifies that the command fails and emits the `Not Initialized` error contract.
9. Independently renders the original `message_box.sh` with the expected `Not Initialized` body.
10. Verifies message styling:
    - `OntoBDC is not initialized.` in gray
    - `Please run` in gray
    - `ontobdc init` in bold white
    - `to setup the project configuration.` back in gray
11. Restores the original `message_box.sh`.
12. Executes `ontobdc init context` in the same temporary directory.
13. Verifies that the command fails as an invalid engine and does not create `ro-crate-metadata.json`.
14. Executes `ontobdc init venv` in the same temporary directory.
15. Verifies exit code `0`.
16. Verifies creation of `.__ontobdc__/config.yaml`.
17. Verifies `engine: venv` in the generated config.
18. Verifies `directory.root.absolute_path` points to the initialized project root.
19. Verifies the init output does not contain `Root Directory Not Configured`.
20. Verifies the init output contains `Infra: Root Absolute Path Configured`.

## Expected Result

- a non-initialized directory must fail before setup
- the pre-init failure must be reported as `Not Initialized`
- only `ontobdc init` must be emphasized in the guidance message
- the removed legacy command `ontobdc init context` must be rejected
- `ontobdc init venv` must exit successfully
- `.__ontobdc__/config.yaml` must be created
- the config must persist both engine and root absolute path
- the post-init check flow must not emit `Root Directory Not Configured`
- the init output must confirm the root absolute path check

## What Part Of The CLI This Covers

- `main()` dispatch for `init`
- `main()` pre-init guard for non-init commands
- `init_main()`
- `init_engine_main()`
- rejection of the removed legacy `context` mode
- message-box invocation for the `Not Initialized` error
- styled rendering of the `Not Initialized` body
- creation of `.__ontobdc__/config.yaml`
- persistence of `directory.root.absolute_path`
- integration with the real `check.sh` flow after initialization

## What This Test Does Not Cover

- automatic engine detection without explicit `venv`
- invalid engine handling
- repeated `ontobdc init` on an already initialized directory
- detailed behavior of all individual checks beyond the root path assertion

## Coverage Summary

### Covered

- pre-init failure path
- `Not Initialized` message contract
- `Not Initialized` message styling
- rejection of the removed legacy `context` mode
- init success path with `venv`
- config file creation
- root absolute path persistence
- avoidance of the root directory misconfiguration regression

### Not Covered

- engine auto-detection flow
- invalid engine flow
- already initialized flow
