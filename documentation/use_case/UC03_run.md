# UC03 - Run Capability (`ontobdc run`)

## Description
This is the core use case of the OntoBDC stack. It executes a specific Capability (Query or Action) dynamically loaded from the available modules.

## Actors
- **User**: Wants to perform an operation (e.g., fetch a web link, extract data, transform schema).
- **System (OntoBDC)**: Resolves the requested Capability, validates CLI arguments against its schema, delegates execution to the appropriate strategy, and returns the produced output.

## Pre-conditions
- The project is initialized.
- Infrastructure checks have passed.
- The target capability is installed and available.

## Flow of Events
1. The user runs `ontobdc run <capability_id> [arguments]`.
2. The system resolves the requested capability via `CapabilityLoader` .
3. The system maps the provided CLI arguments to the `input_schema` defined in the capability's `METADATA`.
4. The system delegates execution to the appropriate `CliStrategy` (e.g., `CapabilityStrategy`).
5. The Capability executes, manipulating data, or interacting with the network.
6. The system captures the output (e.g., a Knowledge Graph or JSON data) and presents it to the user.

## Post-conditions
- The capability's logic is fully executed.
- Resulting data is returned or saved depending on the capability's design.
