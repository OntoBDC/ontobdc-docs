# UC07 - Developer Tools (`ontobdc dev`)

## Description
This use case covers the developer-oriented command group exposed by `ontobdc dev`. It centralizes repository workflows such as enabling the dev tool, creating semantic commits, inspecting or creating branches, checking out branches, and persisting repository SSH key settings in the local project configuration.

## Actors
- **User (Contributor/Developer)**: Needs to commit code or manage branches according to project rules.
- **System (OntoBDC)**: Provides developer utilities that enforce project conventions, validating configuration and invoking underlying Git operations when rules are satisfied.

## Pre-conditions
- The project is initialized.
- The user is inside a Git repository for branch and commit operations.
- The `dev.tool` flag is required for most developer commands and can be enabled from the CLI.

## Supported Commands
- `ontobdc dev`
- `ontobdc dev --help`
- `ontobdc dev --enable-dev-tool`
- `ontobdc dev commit "<message>"`
- `ontobdc dev branch`
- `ontobdc dev branch --create <name>`
- `ontobdc dev checkout <name>`
- `ontobdc dev repo --add-ssh-key <path>`
- `ontobdc dev repo --rm-ssh-key`

## Main Flows

### Flow A - Enable the Dev Tool
1. The user runs `ontobdc dev --enable-dev-tool`.
2. The system verifies that the flag was passed alone.
3. The system writes `dev.tool: enabled` to `.__ontobdc__/config.yaml`.
4. The system confirms that developer commands are now enabled for the current project.

### Flow B - Create a Semantic Commit
1. The user runs `ontobdc dev commit "<message>"`.
2. The system verifies that `dev.tool` is enabled.
3. The system validates the provided commit message according to the project's semantic commit rules.
4. If valid, the system delegates the operation to the commit script, which performs the repository commit workflow.
5. If invalid, the system rejects the message and shows usage guidance.

### Flow C - Inspect or Create Branches
1. The user runs `ontobdc dev branch`.
2. The system verifies that `dev.tool` is enabled.
3. The system delegates to the branch management script.
4. The script lists repositories/submodules and reports branch-related Git status.
5. Optionally, the user runs `ontobdc dev branch --create <name>`.
6. The system creates and pushes the requested branch across the configured repositories.

### Flow D - Checkout an Existing Branch
1. The user runs `ontobdc dev checkout <name>`.
2. The system verifies that `dev.tool` is enabled.
3. The system delegates to the branch script using checkout mode.
4. The target branch is checked out across the participating repositories.

### Flow E - Persist Repository SSH Key Settings
1. The user runs `ontobdc dev repo --add-ssh-key <path>`.
2. The system verifies that `dev.tool` is enabled.
3. The system writes the path to `dev.repo.ssh.key_path` in `.__ontobdc__/config.yaml`.
4. Optionally, the user runs `ontobdc dev repo --rm-ssh-key`.
5. The system removes the stored SSH key path from the local configuration.

## Alternative and Error Flows
1. If `dev.tool` is not enabled and the user runs a protected dev command, the system aborts and instructs the user to run `ontobdc dev --enable-dev-tool`.
2. If `--enable-dev-tool` is combined with other arguments, the system rejects the call.
3. If `commit` is called without a message, the system aborts and prints the correct usage.
4. If `repo` is called without a supported option or with invalid arguments, the system aborts and prints the accepted syntax.
5. If a branch or commit operation fails in the underlying Git scripts, the system propagates the failure to the user.

## Post-conditions
- The local project configuration may be updated with developer settings.
- Commits and branch states may be changed in the target repositories.
- The user receives guided feedback when a developer command is disabled or called incorrectly.
