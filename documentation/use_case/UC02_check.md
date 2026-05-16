# UC02 - Run Infrastructure Checks (`ontobdc check`)

## Description
This use case runs a series of infrastructure checks defined in the `check` module. It verifies dependencies, active environments, required engines, internet connection, and specific configurations for the project.

## Actors
- **User**: Wants to verify if their environment is ready.
- **System (OntoBDC)**: Internally calls this use case before running capabilities to ensure safety.

## Pre-conditions
- The project must be initialized (`.__ontobdc__/config.yaml` exists).

## Flow of Events
1. The user or the system invokes `ontobdc check`.
2. The system reads the global `config.json` and local `config.yaml` to determine which checks are enabled (`auto: true`).
3. The system executes each check sequentially (e.g., `is_venv_active`, `is_connected_to_internet`, `is_engine_installed`).
4. If `--repair` is passed, the system attempts to fix failing checks (e.g., installing Python dependencies).
5. The system reports the final status of all checks.

## Post-conditions
- The user is informed about the environment's health.
- If errors exist, the process halts, preventing runtime failures in capabilities.
