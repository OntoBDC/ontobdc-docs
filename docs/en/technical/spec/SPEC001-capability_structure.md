---
code: SPEC001
title: Capability Structure Specification
status: Accepted
author: Elias M. P. Junior
date: 2026-02-25
tags: architecture, capability, standard
---

# SPEC001: Capability Structure Specification

This document defines the standard structure for implementing a **Capability** in the OntoBDC architecture. A Capability represents a discrete, executable unit of business logic that can be invoked via various interfaces (CLI, API, etc.).

## 1. File Location
Capabilities should be placed within the `module/<domain>/plugin/capability/` directory.
Example: `ontobdc/module/resource/plugin/capability/list_documents.py`

## 2. Class Definition
A Capability is a Python class that inherits from `ontobdc.run.core.capability.Capability`.

```python
from typing import Any, Dict
from ontobdc.run.core.capability import Capability, CapabilityMetadata

class MyCapability(Capability):
    """
    Docstring describing what the capability does.
    """
    ...
```

## 3. Metadata
The `METADATA` attribute is mandatory and must be an instance of `CapabilityMetadata`. It defines identity, documentation, and interface contracts.

```python
    METADATA = CapabilityMetadata(
        id="org.domain.capability.unique_id",
        version="0.1.0",
        name="Human Readable Name",
        description="Detailed description of functionality.",
        author=["Author Name"],
        tags=["tag1", "tag2"],
        supported_languages=["en", "pt_BR"],
        
        # INPUT CONTRACT
        input_schema={
            "type": "object",
            "properties": {
                "input_key": {
                    "type": ExpectedType,  # Python Type or "string", "integer"
                    "required": True,
                    "uri": "org.ontobdc.domain.resource.input.key", # MANDATORY if required=True
                    "description": "Description of the input",
                    "check": [VerificationStrategy] # Optional list of verification strategies
                },
                # ...
            },
        },
        
        # OUTPUT CONTRACT
        output_schema={
            "type": "object",
            "properties": {
                "output_key": {
                    "type": "array", # or "string", "integer", "object"
                    "description": "Description of the output",
                },
            },
        },
        
        # ERROR CONTRACT
        raises=[
            {
                "code": "org.domain.exception.code",
                "python_type": "ValueError",
                "description": "When this error occurs",
            }
        ],
    )
```

## 4. Execution Logic
The `execute` method contains the core business logic. It **must not** contain interface-specific logic (like `argparse`, `print`, or `input`).
It receives a validated `inputs` dictionary and returns a dictionary matching `output_schema`.

```python
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Extract inputs (safe to assume they are validated/typed)
        repo = inputs.get("input_key")
        
        # 2. Perform business logic (delegate to Ports/Entities)
        result = repo.do_something()
        
        # 3. Return results
        return {
            "output_key": result
        }
```

## 5. CLI Strategy (Adapter)
To support CLI execution, the capability should implement `get_default_cli_strategy`. The strategy class itself should reside in `module/<domain>/adapter/cli_strategy.py` to keep the capability file clean.

## 6. Parameter Requirements
- **URI for Required Parameters**: Every parameter defined in `input_schema` that is marked as `"required": True` **MUST** have a `uri` field defined. This URI is used by the context resolver to map CLI arguments and environment variables to the capability input.
