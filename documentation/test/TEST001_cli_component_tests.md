# TEST 001 - CLI Component Tests

## Purpose

This document lists the automated tests in `test/` that directly exercise the OntoBDC CLI component implemented in:

- `wip/src/ontobdc/cli/__init__.py`
- `wip/src/ontobdc/cli/init.py`
- `wip/src/ontobdc/cli/message_box.sh`
- `wip/src/ontobdc/cli/print_log.sh`

The focus of this document is the CLI entrypoint behavior, not the full behavior of downstream components such as `dev`, `run`, or `storage`.

## Scope

The following tests currently have direct CLI relevance:

- `test/src/ontobdc/test_cli_help.sh`
- `test/src/ontobdc/test_cli_python.py`
- `test/src/ontobdc/test_dev.sh`

Important note:

- `test_dev.sh` is mainly a test of the `dev` component.
- Even so, two checks inside that file call `wip/src/ontobdc/cli/__init__.py` directly, so they also validate part of the CLI entrypoint behavior.

## Test Inventory

### 1. `test_cli_help.sh`

**File**

- `test/src/ontobdc/test_cli_help.sh`

**What it tests**

- basic execution of the Python CLI entrypoint with `--help`
- successful exit code for the help path
- presence of the main help content rendered by `print_help()`

**How it works**

1. Resolves the project root.
2. Resolves `wip/src` as the Python import root.
3. Executes:
   - `python3 wip/src/ontobdc/cli/__init__.py --help`
4. Captures stdout.
5. Verifies that the command exits with code `0`.
6. Checks that the output contains the expected help markers.

**Expected output markers**

- `OntoBDC`
- `CLI Help`
- `init`
- `check`
- `run`
- `list`

**Expected result**

- the CLI should print help successfully
- the process should exit with code `0`
- the basic command catalog should be visible

**What part of the CLI this covers**

- `main()` help dispatch
- `print_help()`
- fallback execution of the Python CLI entrypoint without shell wrapper dependency

## 2. `test_cli_python.py`

**File**

- `test/src/ontobdc/test_cli_python.py`

**What it tests**

- Python-level execution of the CLI entrypoint with `--help`
- successful subprocess invocation with controlled `PYTHONPATH`
- presence of key help text in stdout

**How it works**

1. Computes the project root from the test file location.
2. Builds `wip/src` as the CLI import path.
3. Resolves `wip/src/ontobdc/cli/__init__.py`.
4. Executes the CLI in a subprocess using:
   - `sys.executable`
   - the CLI file path
   - `--help`
5. Captures stdout and stderr.
6. Asserts exit code `0`.
7. Validates the presence of help strings in stdout.

**Expected output markers**

- `OntoBDC`
- `CLI Help`
- `check`
- `run`
- `init`

**Expected result**

- the Python CLI entrypoint must run as a subprocess without crashing
- help output must be rendered to stdout
- the command must terminate successfully

**What part of the CLI this covers**

- Python subprocess invocation path
- `main()` command dispatch for `--help`
- import/path resolution for the CLI component

**Why it is not redundant with `test_cli_help.sh`**

- `test_cli_help.sh` validates the shell-oriented execution path
- `test_cli_python.py` validates the same behavior from a Python test harness using `subprocess.run`

Together, they give both shell-level and pytest-level confidence for the help entrypoint.

## 3. CLI-Relevant Assertions Inside `test_dev.sh`

**File**

- `test/src/ontobdc/test_dev.sh`

**Primary purpose of the file**

- validate the `dev` component shell behavior

**CLI-relevant portions**

This file contains two explicit checks against:

- `wip/src/ontobdc/cli/__init__.py`

Those checks matter because they validate that the CLI entrypoint correctly dispatches:

- `ontobdc dev commit ...`

### 3.1 CLI Dispatch Fails When `dev.tool` Is Disabled

**What it tests**

- the Python CLI entrypoint should reject `dev commit` when local configuration does not enable the developer tool

**How it works**

1. Creates an isolated temporary OntoBDC-like project structure.
2. Writes a minimal `.__ontobdc__/config.yaml` without enabling `dev.tool`.
3. Executes:
   - `python3 wip/src/ontobdc/cli/__init__.py dev commit "test python cli"`
4. Captures exit code and output.
5. Verifies that the command fails.
6. Verifies that the output reports:
   - `dev.tool is not enabled`

**Expected result**

- non-zero exit code
- error message informing that `dev.tool` is not enabled

**What part of the CLI this covers**

- `main()` command dispatch to `dev`
- `dev_command()`
- configuration lookup through `config_data()`
- gating logic for `dev commit`

### 3.2 CLI Dispatch Succeeds When `dev.tool` Is Enabled

**What it tests**

- the Python CLI entrypoint should correctly route `dev commit` when configuration is valid

**How it works**

1. Creates an isolated temporary OntoBDC-like project structure.
2. Writes a valid `.__ontobdc__/config.yaml` with:
   - `dev.tool: enabled`
3. Executes:
   - `python3 wip/src/ontobdc/cli/__init__.py dev commit "test python cli"`
4. Captures exit code and output.
5. Verifies that the command does not fail.
6. Verifies that the output contains:
   - `Starting commit process`

**Expected result**

- exit code `0`
- delegated execution of `commit.sh`
- no `Not Initialized` error

**What part of the CLI this covers**

- root/config discovery through `get_root_dir()`
- valid config loading through `config_data()`
- successful delegation from `dev_command()` to `commit.sh`

## 4. What Is Currently Not Covered Well

The current CLI-oriented tests cover help rendering and a slice of `dev` dispatch, but they do not cover the full CLI command surface.

Significant gaps remain for:

- `ontobdc init`
- `ontobdc check`
- `ontobdc run`
- `ontobdc list`
- `ontobdc plan`
- `ontobdc storage`
- `ontobdc a3`
- unknown command handling
- `--version`
- message-box fallback behavior when shell scripts are missing
- error path when the project is not initialized

## 5. Coverage Summary

### Covered

- help entrypoint via shell
- help entrypoint via Python subprocess
- CLI dispatch to `dev commit` with invalid config
- CLI dispatch to `dev commit` with valid config

### Partially covered

- CLI configuration resolution
- CLI-to-shell delegation for the `dev` command

### Not covered

- end-to-end CLI coverage for the rest of the command groups
- version command
- unknown command behavior
- initialization error handling across the full command set
