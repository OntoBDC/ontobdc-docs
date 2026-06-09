# Documentation for `test_resolution_to_language_defined.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_language_defined.py`
- Unit under test: `ResolutionToLanguageDefinedCapability`
- Style: `unittest` with `patch` and injected prompt

## What This File Tests

This document describes context language selection, covering reuse of an already defined language, reading available languages from configuration, prompting the user when multiple options exist, and failing when the flow is explicitly exited.

## Documented Scenarios

### `test_context_has_language_returns_it`

**What is tested**

- The context already contains `context_language = pt`.
- `_get_language()` must reuse that value without consulting external configuration.

**Expected result**

- The method returns `pt`.

**What is mocked**

- Nothing.

**What is not mocked**

- `ResolutionToLanguageDefinedCapability`.
- `CliContextAdapter`.
- The real priority logic for a language already present in the context.

### `test_config_has_one_language_returns_it`

**What is tested**

- The context does not have a defined language.
- Configuration returns exactly one available language.
- `_get_language()` must select that language automatically.

**Expected result**

- The method returns `en`.

**What is mocked**

- `ConfigDataAdapter`, to control `available_languages()`.

**What is not mocked**

- `ResolutionToLanguageDefinedCapability`.
- `CliContextAdapter`.
- `BaseResource`, used as a real object to represent languages.

### `test_config_has_multiple_languages_prompts_user`

**What is tested**

- The context does not have a defined language.
- Configuration returns two available languages.
- The capability must ask the user to choose one.

**Expected result**

- The method returns `English (en)`, exactly the value returned by the prompt.

**What is mocked**

- `ConfigDataAdapter`.
- The choice prompt, through `set_prompt_choice`.

**What is not mocked**

- `ResolutionToLanguageDefinedCapability`.
- `CliContextAdapter`.
- `BaseResource`.
- The real logic that enters interactive mode when multiple options exist.

### `test_execute_sets_language_parameter`

**What is tested**

- The main flow receives a context where the language is already defined.

**Expected result**

- The returned `cli_context` preserves `context_language = en`.
- Execution completes without error.

**What is mocked**

- Nothing.

**What is not mocked**

- `ResolutionToLanguageDefinedCapability`.
- `CliContextAdapter`.
- The real `execute()` flow.

### `test_execute_raises_exception_on_exit`

**What is tested**

- The context does not have a defined language.
- The prompt returns `Exit`, simulating explicit user cancellation.

**Expected result**

- Execution raises `Exception`.
- The flow is interrupted instead of continuing with an undefined language.

**What is mocked**

- The choice prompt, through `set_prompt_choice`.

**What is not mocked**

- `ResolutionToLanguageDefinedCapability`.
- `CliContextAdapter`.
- The real interruption rule when the user chooses to exit.

## Notes

- This file mixes tests for the internal method `_get_language()` and the public `execute()` method.
- The return value `English (en)` shows that the test validates the raw prompt output directly.
