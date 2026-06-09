# Documentation for `test_resolution_to_filled.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_filled.py`
- Unit under test: `ResolutionToFilledCapability`
- Style: `unittest` with `patch`

## What This File Tests

This document describes the step that prepares input data for an already selected capability by using loaders and a parameter dependency evaluator.

## Documented Scenario

### `test_execute_fills_capability_inputs`

**What is tested**

- The context starts with `selected_capability_id` defined.
- `CapabilityLoader` returns the matching dummy capability.
- `DagParametersEvaluator` reports that no parameters are missing.
- The capability propagates the selection to the final identifier used by the flow.

**Expected result**

- The `capability_id` parameter is set to `org.example.capability.test`.
- The flow completes without requesting additional data and without error.

**What is mocked**

- `CapabilityLoader`.
- `ParameterLoader`.
- `DagParametersEvaluator`.

**What is not mocked**

- `ResolutionToFilledCapability`.
- `CliContextAdapter`.
- `DummyQueryCapability`, used as a simple concrete implementation.
- The real logic that writes `capability_id` into the context.

## Notes

- The test covers the minimal happy path.
- There is no coverage for scenarios where required parameters are missing.
