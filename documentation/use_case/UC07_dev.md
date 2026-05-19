# UC07 - Developer Tools (`ontobdc dev`)

## Description
This use case encompasses developer utilities that enforce project conventions, such as standardized semantic commits (`ontobdc dev commit`) and branch management (`ontobdc dev branch`).

## Actors
- **User (Contributor/Developer)**: Needs to commit code or manage branches according to project rules.
- **System (OntoBDC)**: Provides developer utilities that enforce project conventions, validating configuration and invoking underlying Git operations when rules are satisfied.

## Pre-conditions
- The project is initialized.
- The `dev.tool` is enabled in `.__ontobdc__/config.yaml`.
- The user is inside a Git repository.

## Flow of Events
1. The user runs `ontobdc dev commit "<message>"`.
2. The system verifies if the dev tool is enabled.
3. The system validates the commit message against semantic commit rules and language requirements (English).
4. If valid, the system executes the underlying `git commit` command.
5. If invalid, the system rejects the commit and provides feedback.

## Post-conditions
- Code is committed to the repository adhering strictly to project standards.
