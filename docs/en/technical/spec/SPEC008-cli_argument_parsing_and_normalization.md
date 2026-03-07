---
title: SPEC008 - CLI Argument Parsing and Normalization
status: Accepted
author: Elias M. P. Junior
created_at: 2026-03-06
---

# SPEC008 - CLI Argument Parsing and Normalization

## Context

The OntoBDC CLI (`ontobdc run`) serves as a unified entry point for executing Capabilities and Actions. Previously, the argument parser enforced a rigid structure where the Capability ID had to be the first positional argument or explicitly defined before other flags. Additionally, there was a disconnect between CLI conventions (kebab-case, e.g., `--file-type`) and Python/Internal conventions (snake_case, e.g., `file_type`) defined in Capability Schemas.

This led to two main issues:
1.  **Ordering Failures**: Commands like `ontobdc run --file-type yaml --id <ID>` failed because the parser expected the ID before strategy-specific flags.
2.  **Discovery Failures**: Capabilities requiring `file_type` in their schema were not listed when the user provided `--file-type`, because the runner only registered the kebab-case key.

## Decision

We have adopted a flexible parsing strategy and automatic normalization layer in the core runner (`ontobdc/run/run.py`).

### 1. Flexible Argument Ordering

The runner now performs a preprocessing pass on `sys.argv` to reconstruct the argument list before handing it over to the specific Capability Strategy parser.

- **Mechanism**: The runner extracts the Capability ID (whether provided positionally or via `--id`) and ensures it is placed as the *first* positional argument in the list passed to `argparse`.
- **Result**: All other flags are preserved and passed after the ID, regardless of their original position in the command line.

### 2. Automatic Key Normalization

To bridge the gap between CLI and Python standards:
- **Mechanism**: When parsing CLI arguments for the discovery/filtering phase, the runner now stores both the original key (e.g., `file-type`) and its snake_case variant (e.g., `file_type`) in the `capabilities_attrs` dictionary.
- **Result**: A Capability Schema defining `required: ["file_type"]` will be satisfied by a CLI argument `--file-type`.

## Expected Behavior

### Command Line Usage
Users can provide arguments in any logical order. The following commands are now equivalent and valid:

```bash
# ID as flag, after arguments
ontobdc run --file-type yaml --id org.ontobdc.capability.list

# ID as flag, before arguments
ontobdc run --id org.ontobdc.capability.list --file-type yaml

# ID positional, before arguments
ontobdc run org.ontobdc.capability.list --file-type yaml
```

### Schema Definition
Developers should follow Python conventions for schema properties:

```python
input_schema={
    "type": "object",
    "properties": {
        "file_type": {  # Use snake_case here
            "type": "array",
            "required": True
        }
    }
}
```

The CLI Strategy should define the flag in kebab-case (standard `argparse` behavior):

```python
parser.add_argument("--file-type", dest="type", ...)
```

## Constraints and "Don'ts"

### 1. Do Not Assume Positional Index for Flags
Do not write scripts or wrappers that rely on flags being at specific indices (e.g., `sys.argv[2]`). The preprocessor may shift arguments to satisfy `argparse` requirements.

### 2. Avoid Ambiguous Flag Values
The parser distinguishes flags from values. Ensure values for flags are explicit.
- **Good**: `--type yaml` or `--type=yaml`
- **Bad**: `--type --other-flag` (if `type` expects a value, it might consume `--other-flag` as a string value).

### 3. Do Not Mix Schema Conventions
- **Schema**: Always use `snake_case` for property names (e.g., `user_id`, `file_name`).
- **CLI Flags**: Always use `kebab-case` for user-facing flags (e.g., `--user-id`, `--file-name`).
- The framework handles the mapping. Do not define `file-type` (kebab-case) directly in the Input Schema unless strictly necessary for legacy reasons, as it breaks Python variable naming conventions when mapped to code.

## Technical Implementation Details

The `run.py` script uses a manual reconstruction loop:
1. Identifies `capability_id`.
2. Creates a new list starting with `[capability_id]`.
3. Iterates through original arguments, skipping the `run` command, the `--id` flag, and the `capability_id` value itself (to avoid duplication).
4. Appends all other recognized flags to the new list.
5. Passes this sanitized list to `real_parser.parse_known_args()`.

This ensures compatibility with `argparse`'s expectation of `prog [positional] [optional]` structure while offering users a modern, flexible CLI experience.
