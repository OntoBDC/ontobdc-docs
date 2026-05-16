# UC04 - List Capabilities (`ontobdc list`)

## Description
This use case discovers and lists all available Capabilities (Query and Actions) registered in the current OntoBDC installation. It provides metadata such as ID, Version, Name, Description, and Schemas.

## Actors
- **User**: Wants to explore available tools and their usage schemas.
- **System (OntoBDC)**: Discovers installed Capabilities, extracts their metadata, and renders the result as Rich UI output or JSON.

## Pre-conditions
- None (works globally or within an initialized project).

## Flow of Events
1. The user runs `ontobdc list` (optionally with `--json`).
2. The system scans all python packages and modules for classes inheriting from `Capability` (`Query` or `Action`).
3. The system extracts the `METADATA` attribute from each discovered class.
4. The system formats the output as Rich UI cards or JSON if requested.

## Post-conditions
- The user sees a complete directory of available tools to use with `ontobdc run`.
