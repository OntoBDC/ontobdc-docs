# Documentation for `test_resolution_to_planned.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_planned.py`
- Unit under test: `ResolutionToPlannedCapability`
- Style: `unittest` with `patch` and a real temporary directory

## What This File Tests

This document describes the planning stage for the selected capability, consuming the previously saved canonical intent and preparing the state required for execution.

## Documented Scenario

### `test_execute_plans_capability`

**What is tested**

- The test creates a real canonical intent file in the temporary directory.
- The context provides `selected_capability_id`.
- `CapabilityLoader` returns the matching dummy capability.
- `DagParametersEvaluator` returns an empty filled set.
- The capability runs the flow that reads persisted state and plans the capability.

**Expected result**

- The `capability_id` parameter is set to `org.example.capability.test`.
- The previously saved JSON file is consumed without error.
- The main flow completes successfully.

**What is mocked**

- `CapabilityLoader`.
- `ParameterLoader`.
- `DagParametersEvaluator`.
- `get_config_dir`, to point to the temporary directory.

**What is not mocked**

- `ResolutionToPlannedCapability`.
- `CliContextAdapter`.
- `IntentScoreResponse`, used for real to serialize the input file.
- Real JSON file reads and writes in the temporary directory.
- `DummyQueryCapability`, used as a simple concrete implementation.

## Notes

- The test exercises a small local integration with the file system.
- There is no assertion about planned parameters, only about the selected capability propagated into the context.
