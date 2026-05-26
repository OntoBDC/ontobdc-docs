# TEST 004 - Check Component Tests

## Purpose

This document describes the automated tests in `test/` that currently validate behavior related to the OntoBDC `check` component.

The scope of this document includes:

- direct test coverage of the `check` infrastructure logic
- direct CLI help coverage for `ontobdc check -h | --help`
- indirect coverage of `ontobdc check` behavior through the CLI initialization flow

It does not treat all references to `check` as equivalent.

In particular, this document distinguishes between:

- tests that exercise `check` logic directly
- tests that only touch `check` as part of another command flow

## Targeted Components

The current check-related tests touch these implementation areas:

- `src/ontobdc/check/check.sh`
- `src/ontobdc/check/config.json`
- `src/ontobdc/check/infra/is_engine_installed/init.sh`
- `src/ontobdc/check/infra/is_venv_active/init.sh`
- `src/ontobdc/cli/__init__.py`
- `src/ontobdc/cli/init.py`
- `src/ontobdc/cli/message_box.sh`

## Test Inventory

The current check-related automated tests are:

- `test/src/ontobdc/check/infra/test_is_engine_installed.sh`
- `test/src/ontobdc/test_cli_check_help.sh`
- `test/src/ontobdc/test_cli_init.sh`

## 1. Direct Check Test: `test_is_engine_installed.sh`

### File

- `test/src/ontobdc/check/infra/test_is_engine_installed.sh`

### What It Tests

This is the main direct automated test of the `check` component currently present in `test/`.

It validates the infrastructure check script:

- `src/ontobdc/check/infra/is_engine_installed/init.sh`

More specifically, it validates:

- failure when no `.__ontobdc__/config.yaml` exists
- failure when `engine` is invalid
- success when `engine: venv` is configured
- hotfix behavior when a virtual environment is active

### How It Works

1. Resolves the project root.
2. Locates:
   - `src/ontobdc/check/infra/is_engine_installed/init.sh`
   - `src/ontobdc/check/config.json`
3. Creates a temporary test workspace.
4. Rebuilds a minimal check-oriented directory structure inside that temporary workspace.
5. Copies:
   - `is_engine_installed/init.sh`
   - `is_venv_active/init.sh`
   - `check/config.json`
6. Adds a simple stub for `is_colab`.
7. Sources the copied `init.sh` directly and executes its shell functions.

### Scenario Coverage

#### 1.1 No Config Present

- the test runs `check` with no `.__ontobdc__/config.yaml`
- expected result: failure

#### 1.2 Invalid Engine

- the test writes `engine: invalid_engine`
- expected result: failure

#### 1.3 Valid Engine

- the test writes `engine: venv`
- expected result: success

#### 1.4 Hotfix Path

- the test removes the config file again
- it exports `VIRTUAL_ENV` to simulate an active virtual environment
- it runs `hotfix`
- expected result:
  - `.__ontobdc__/config.yaml` is created
  - the file contains `engine: venv`

### Expected Result

- the direct engine-installed infrastructure check must reject missing or invalid configuration
- it must accept a valid `venv` engine
- its hotfix path must be able to create a usable config in the simulated venv case

### What Part Of `check` This Covers

- infra-level check script behavior
- engine value validation against the check configuration model
- hotfix behavior for venv setup

### Limitations

- this is not a full end-to-end `ontobdc check` CLI test
- it tests a single infrastructure check in isolation
- it does not validate the rendered overall `check.sh` summary output

## 2. Dedicated Check Help Test: `test_cli_check_help.sh`

### File

- `test/src/ontobdc/test_cli_check_help.sh`

### Why It Matters

This is the dedicated CLI entrypoint test for the `check` help surface.

It exists to ensure that `ontobdc check -h` and `ontobdc check --help` do not fall back to the raw `argparse` output and instead follow the standard OntoBDC CLI help contract.

### What It Covers

It validates these `check` help behaviors:

- `-h` and `--help` both exit successfully
- both variants render through the `message_box` contract
- the help requests `INFO` color
- the help uses `OntoBDC` as title type
- the help uses `Check Help` as title text
- both variants return the same rendered output
- the rendered content comes from the metadata-driven command description

### How It Works

1. Resolves the project root and source paths.
2. Replaces `src/ontobdc/cli/message_box.sh` with a test double that captures:
   - color
   - title type
   - title text
   - body
3. Creates a temporary initialized workspace with `.__ontobdc__/config.yaml`.
4. Executes:
   - `ontobdc check -h`
   - `ontobdc check --help`
5. Verifies the captured message-box contract and the rendered output.

### Expected Result

- both help variants must exit with code `0`
- both must request `INFO`
- both must request `OntoBDC` / `Check Help`
- both must render identical output
- the output must include the metadata-defined usage lines, description, and option descriptions

### What Part Of `check` This Covers

- CLI-level `check` help interception before the operational runner executes
- metadata-driven help rendering for the `check` command
- message-box formatting contract for the `check` help entrypoint

### Limitations

- this test validates the `check` help entrypoint, not the operational execution path
- it does not validate `check.sh` success or failure summaries
- it does not execute the infra checks themselves

## 3. Indirect Check Coverage Inside `test_cli_init.sh`

### File

- `test/src/ontobdc/test_cli_init.sh`

### Why It Matters

This is primarily an `init` test, not a dedicated `check` test.

Even so, it contains meaningful assertions about `ontobdc check` behavior and about the post-init interaction between `init` and `check`.

### What It Covers

It validates two important `check`-related behaviors:

- pre-init `ontobdc check` failure
- successful post-init execution of the real `check.sh` flow

### Scenario Coverage

#### 3.1 `ontobdc check` Before Initialization

The test executes `ontobdc check` in a fresh temporary directory with no `.__ontobdc__/config.yaml`.

Expected result:

- the command fails
- the CLI emits the `Not Initialized` error through the message box contract

This validates the guard path around `check` at the CLI level.

#### 3.2 `check` After `ontobdc init venv`

The test then executes `ontobdc init venv`, which triggers the real post-init `check` flow.

Expected result:

- the init output does not contain `Root Directory Not Configured`
- the init output does contain `Infra: Root Absolute Path Configured`

This validates that initialization produces configuration compatible with the current `check` expectations.

### What Part Of `check` This Covers

- CLI-level gating before initialization
- real integration with `src/ontobdc/check/check.sh`
- root absolute path compatibility between `init` and `check`

### Limitations

- the test does not focus on `check` options such as:
  - `--repair`
  - `--scope`
  - `--only`
  - `--ignore-warnings`
  - `--compact`
- it does not act as a dedicated `check` command test file

## Coverage Summary

### Covered

- direct shell validation of `is_engine_installed`
- invalid and valid engine handling at the infra check level
- venv-oriented hotfix behavior
- dedicated CLI validation of `ontobdc check -h | --help`
- metadata-driven help rendering for `check`
- message-box contract validation for `check` help
- CLI rejection of `ontobdc check` before initialization
- integration between `ontobdc init` and the real post-init `check.sh` flow
- validation of the root absolute path check after initialization

### Not Covered Well

- dedicated end-to-end CLI tests for `ontobdc check`
- `ontobdc check --repair`
- `ontobdc check --scope <name>`
- `ontobdc check --only <check>`
- `ontobdc check --ignore-warnings`
- `ontobdc check --compact`
- full multi-check aggregation behavior
- success and failure message-box summaries of the complete `check.sh` runner

## Operational Note

The current repository contains direct check-related coverage, but the standard suite selection in `test/config.yaml` is still selective.

That means a check-related test may exist in `test/` without currently being enabled by default in the YAML selection file.

This distinction matters when discussing:

- test presence in the tree
- test execution in the default runner

At the moment, `test/src/ontobdc/test_cli_check_help.sh` is included in the default shell suite selection.
