# UC01 - Initialize Configuration (`ontobdc init`)

## Description
This use case is responsible for initializing the OntoBDC configuration for a given project. It sets up the environment and creates the necessary configuration files, specifying the execution engine (e.g., `venv` or `colab`).

## Actors
- **User**: Executes the CLI command to initialize the project.
- **System (OntoBDC)**: Creates and populates the local OntoBDC project configuration (`.__ontobdc__/config.yaml`), selecting and persisting the execution engine and default settings.

## Pre-conditions
- OntoBDC is installed.
- The user is in the root directory of their project.

## Flow of Events
1. The user runs `ontobdc init`.
2. The system checks if the `.__ontobdc__` folder and `config.yaml` exist.
3. If they don't exist, the system generates them with default configurations.
4. The system prompts the user or defaults to an engine (like `venv`).
5. The project is marked as initialized and ready for execution.

## Post-conditions
- The `.__ontobdc__/config.yaml` file is created and populated with valid initialization data.
