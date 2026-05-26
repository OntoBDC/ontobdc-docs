# TEST 003 - CLI List Entrypoint Test

## Purpose

This document describes the single automated test dedicated to the OntoBDC CLI list entrypoint:

- `test/src/ontobdc/test_cli_list.sh`

The scope of this document is limited to that file and to the behavior of `ontobdc list`.

## Targeted Components

The test directly exercises these implementation files:

- `wip/src/ontobdc/cli/__init__.py`
- `wip/src/ontobdc/list/list.py`
- `wip/src/ontobdc/cli/message_box.sh`
- `wip/src/ontobdc/shared/adapter/plugin.py`

## Test File

- `test/src/ontobdc/test_cli_list.sh`

## What The Test Covers

- execution of `ontobdc list --help`
- execution of `ontobdc list`
- execution of `ontobdc list --json`
- successful exit code for all three paths
- help metadata rendered through the message box contract
- help usage text for the `list` subcommand
- rich output when at least one capability is available
- JSON output when at least one capability is available
- discovery of a temporary fake capability through the standard plugin loader
- presence of the fake capability in both rich and JSON outputs

## How The Test Works

1. Resolves the project root from the shell test location.
2. Resolves `wip/src` as the Python import root.
3. Locates the CLI entrypoint at `wip/src/ontobdc/cli/__init__.py`.
4. Locates and temporarily replaces `wip/src/ontobdc/cli/message_box.sh` with a capture script.
5. Creates a temporary fake plugin under `wip/src/ontobdc/zz_testplugin/plugin/capability`.
6. Declares one fake capability with stable metadata:
   - id
   - name
   - description
   - version
   - input schema
7. Executes `ontobdc list --help`.
8. Verifies that help exits with code `0`.
9. Verifies the message-box contract for help:
   - `COLOR=GRAY`
   - `TITLE_TYPE=OntoBDC`
   - `TITLE_TEXT=List Help`
10. Verifies that help output contains:
   - `ontobdc list [OPTIONS]`
   - `--json`
11. Restores the real `message_box.sh`.
12. Executes `ontobdc list`.
13. Verifies rich output contains:
   - `Capabilities`
   - the fake capability name
   - the fake capability id
   - the fake capability description
14. Executes `ontobdc list --json`.
15. Verifies exit code `0`.
16. Parses JSON from stdout.
17. Verifies the fake capability is present in the JSON payload with the expected metadata.
18. Removes the temporary plugin and restores the original message box on exit.

## Expected Result

- `ontobdc list --help` must exit with code `0`
- `ontobdc list` must exit with code `0`
- `ontobdc list --json` must exit with code `0`
- help must render the expected list usage and options
- rich output must show the discovered fake capability
- JSON output must be valid and include the discovered fake capability

## What Part Of The CLI This Covers

- `main()` dispatch for `list`
- `list.main()`
- `list.show_help()`
- help message-box invocation for the list subcommand
- capability discovery through `CapabilityLoader`
- rich card rendering path in `list.py`
- JSON serialization path in `list.py`

## What This Test Does Not Cover

- unknown argument handling for `ontobdc list`
- failure path when capability loading raises fatal exceptions
- behavior with multiple real plugins from different environments
- formatting details of every rich panel field
- renderer components outside the `list` entrypoint

## Coverage Summary

### Covered

- `list --help`
- `list` rich output
- `list --json`
- plugin discovery through the standard loader
- presence of capability metadata in both render modes

### Not Covered

- unknown-argument warning path
- empty capability catalog behavior
- fatal error path in list execution
- deep renderer formatting assertions
