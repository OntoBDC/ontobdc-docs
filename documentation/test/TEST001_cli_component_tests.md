# TEST 001 - CLI Help Entrypoint Test

## Purpose

This document describes the single automated test in `test/` that currently exercises the OntoBDC CLI help entrypoint:

- `test/src/ontobdc/test_cli_help.sh`

The scope of this document is limited to that file and to the CLI help behavior it validates.

## Targeted Components

The test directly exercises these implementation files:

- `wip/src/ontobdc/cli/__init__.py`
- `wip/src/ontobdc/cli/message_box.sh`

It validates the behavior of the CLI help entrypoint and the message-box rendering contract used by the help output.

## Test File

- `test/src/ontobdc/test_cli_help.sh`

## What The Test Covers

- execution of `ontobdc --help`
- execution of `ontobdc` with no arguments
- successful exit code for both help entry paths
- equality between the outputs of `ontobdc --help` and `ontobdc`
- presence of the main help content rendered by `print_help()`
- use of the semantic message-box color `INFO`
- help title metadata:
  - `OntoBDC`
  - `CLI Help`
- rendered help header format:
  - `>_ OntoBDC CLI Help`
- rendered header styling:
  - `OntoBDC` in bold blue
- rendered usage styling:
  - `Usage:` in bold white
  - `<command>` in cyan

## How The Test Works

1. Resolves the project root from the location of the shell test.
2. Resolves `wip/src` as the Python import root.
3. Locates the CLI entrypoint at `wip/src/ontobdc/cli/__init__.py`.
4. Locates the original `wip/src/ontobdc/cli/message_box.sh`.
5. Creates a temporary backup of `message_box.sh`.
6. Replaces `message_box.sh` with a small capture script that records:
   - `COLOR`
   - `TITLE_TYPE`
   - `TITLE_TEXT`
7. Executes the CLI twice:
   - `python3 wip/src/ontobdc/cli/__init__.py --help`
   - `python3 wip/src/ontobdc/cli/__init__.py`
8. Verifies that both invocations exit with code `0`.
9. Verifies that both outputs contain the expected help markers.
10. Verifies that both outputs are identical.
11. Verifies that the captured message-box contract uses:
   - `COLOR=INFO`
   - `TITLE_TYPE=OntoBDC`
   - `TITLE_TEXT=CLI Help`
12. Independently executes the original backed-up `message_box.sh` with a controlled sample help body.
13. Verifies the rendered header and styled usage lines in the original message-box output.
14. Restores the original `message_box.sh` on exit.

## Expected Output Markers

The test expects the CLI help output to contain at least these text markers:

- `OntoBDC`
- `CLI Help`
- `init`
- `check`
- `run`
- `list`

It also expects these styled fragments to be present in the help output:

- `Usage:` in bold white
- `<command>` in cyan

## Expected Result

- `ontobdc --help` must exit with code `0`
- `ontobdc` with no arguments must exit with code `0`
- both invocations must produce the same help output
- the help output must expose the expected command catalog markers
- the CLI must delegate help rendering to the message box using `INFO`
- the rendered header must contain `>_ OntoBDC CLI Help`
- the rendered header must show `OntoBDC` in bold blue
- the rendered usage block must preserve:
  - `Usage:` in bold white
  - `<command>` in cyan

## What Part Of The CLI This Covers

- `main()` dispatch for `--help`
- `main()` behavior when no command is provided
- `print_help()`
- message-box invocation contract for help rendering
- header rendering in `message_box.sh`
- styled body rendering in `message_box.sh`

## What This Test Does Not Cover

This test is intentionally limited to the help entrypoint. It does not validate:

- `ontobdc init`
- `ontobdc check`
- `ontobdc run`
- `ontobdc list`
- `ontobdc plan`
- `ontobdc storage`
- `ontobdc a3`
- `ontobdc --version`
- unknown command handling
- project initialization side effects
- downstream command execution beyond help rendering

## Coverage Summary

### Covered

- CLI help entrypoint via `--help`
- CLI help entrypoint with no arguments
- help output contract passed to `message_box.sh`
- rendered header styling for the help box
- rendered usage styling inside the help box

### Not Covered

- end-to-end execution of non-help CLI commands
- initialization flow
- error flows outside the help path
- version handling
- unknown command behavior
