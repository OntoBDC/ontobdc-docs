# SPEC 002 - Automated Tests

## Status

- **Status**: Working specification of the current automated testing setup
- **Scope**: repository-level automated tests for OntoBDC core
- **Primary sources**:
  - `test/`
  - `wip/pyproject.toml`
  - `wip/.github/workflows/pypi-publish.yml`

## 1. Purpose

This specification describes the current automated testing landscape of the repository.

It covers:

- where automated tests live
- how they are executed
- which frameworks are used
- which suites are currently included in the standard runner
- which supporting stubs and fixtures exist
- what is automated in CI and what is not
- the current strengths, weaknesses, and gaps of the testing setup

## 2. Current Test Topology

The repository currently has a dedicated top-level test workspace:

- `test/`

This workspace contains:

- test sources under `test/src/ontobdc`
- dependency stubs under `test/stubs`
- a YAML selection file under `test/config.yaml`
- a repository test runner script under `test/test`

The main automated test focus is the OntoBDC core currently developed under:

- `wip/src/ontobdc`

There are also test-like files outside the main automated path.

Those should not be treated as part of the main automated core test suite unless explicitly adopted later.

## 3. Frameworks And Execution Model

The current automated testing setup uses a mixed model:

- `pytest` as the main Python test runner
- `unittest` style assertions inside some Python test files
- shell-based tests for selected CLI and infrastructure behaviors

This means the project does not currently rely on a single test authoring style. Instead, it combines:

- shell scripts for command-line behavior
- `pytest` collection and execution for Python test files
- `unittest.TestCase` classes executed through `pytest`

## 4. Declared Test Dependencies

In `wip/pyproject.toml`, the development extra currently declares:

- `pytest`
- `coverage`

This means the intended development installation path for testing is:

```bash
pip install -e ".[dev]"
```

However, the current repository runner is more permissive in practice:

- if `pytest` is missing, the runner attempts to install `pytest` and `pytest-cov` on demand

Important nuance:

- `coverage` is declared as a development dependency
- `pytest-cov` is installed opportunistically by the test runner
- but no explicit coverage command is currently used in the standard execution flow

## 5. Standard Test Runner

The current repository-level test runner is:

- `test/test`

### 5.1 Runner Responsibilities

The script currently:

- reads `test/config.yaml`
- separates shell tests from Python tests
- runs shell tests immediately
- accumulates Python tests and executes them together with `pytest`
- sets up `PYTHONPATH` so tests resolve:
  - `wip/src`
  - `test/stubs`
- prefers `.venv/bin/python` when available
- falls back to `python3` otherwise

### 5.2 Python Execution Behavior

For Python suites, the runner effectively executes:

```bash
python -m pytest <selected python test files>
```

with a custom `PYTHONPATH` including:

- `test/stubs`
- `wip/src`

### 5.3 Shell Execution Behavior

Shell tests are executed directly with:

```bash
bash <test_script>
```

This is used for selected command-level or environment-level checks.

## 6. Standard Included Test Suites

The standard automated selection is currently defined in:

- `test/config.yaml`

The following suites are explicitly included there.

### 6.1 Shell Suites

- `test_cli_help.sh`
- `test_dev_dev_sh.sh`
- `check/infra/test_is_engine_installed.sh`

### 6.2 Python Suites

- `test_cli_python.py`
- `a3/adapter/test_guardrail.py`
- `a3/test_transformation_to_translated.py`
- `a3/test_transformation_to_validated.py`
- `a3/test_transformation_to_reasoned.py`
- `a3/test_transformation_to_dispatched.py`
- `test_capability_structure.py`
- `run/adapter/test_context.py`
- `run/adapter/test_context_config.py`
- `run/core/strategy/test_action_only.py`
- `run/core/strategy/test_capability.py`
- `run/core/strategy/test_export.py`
- `run/core/strategy/test_file_filter.py`
- `run/core/strategy/test_help.py`
- `run/core/strategy/test_include_action.py`
- `run/core/strategy/test_json_export.py`
- `run/core/strategy/test_pagination.py`
- `run/core/strategy/test_root_path.py`
- `storage/test_storage.py`

## 7. Current Test Coverage Areas

Based on the included suites, the automated tests currently cover these main areas.

### 7.1 CLI Behavior

Covered by:

- `test_cli_help.sh`
- `test_cli_python.py`
- `test_dev_dev_sh.sh`

This area focuses on:

- top-level CLI help behavior
- shell wrapper behavior
- developer command entry behavior

### 7.2 Check Infrastructure

Covered by:

- `check/infra/test_is_engine_installed.sh`

This area focuses on:

- selected environment/infrastructure check behavior

### 7.3 Run Context And Parameter Strategies

Covered by:

- `run/adapter/test_context.py`
- `run/adapter/test_context_config.py`
- `run/core/strategy/test_action_only.py`
- `run/core/strategy/test_capability.py`
- `run/core/strategy/test_export.py`
- `run/core/strategy/test_file_filter.py`
- `run/core/strategy/test_help.py`
- `run/core/strategy/test_include_action.py`
- `run/core/strategy/test_json_export.py`
- `run/core/strategy/test_pagination.py`
- `run/core/strategy/test_root_path.py`

This is currently one of the strongest automated areas of the core.

### 7.4 A3 Transformations And Guardrails

Covered by:

- `a3/adapter/test_guardrail.py`
- `a3/test_transformation_to_translated.py`
- `a3/test_transformation_to_validated.py`
- `a3/test_transformation_to_reasoned.py`
- `a3/test_transformation_to_dispatched.py`

This area focuses on:

- transformation stages
- validation behavior
- JSON/schema-oriented guardrail logic

### 7.5 Storage Behavior

Covered by:

- `storage/test_storage.py`

This area focuses on:

- storage listing
- JSON storage output
- local registration attempts
- removal behavior

### 7.6 Capability Structure

Covered by:

- `test_capability_structure.py`

This area focuses on:

- structural expectations of capability organization

## 8. Supporting Test Infrastructure

### 8.1 Stub Packages

The directory:

- `test/stubs`

currently contains stub packages for:

- `datapackage`
- `rocrate`

This allows tests to run without requiring the full external packages in all cases.

These stubs reduce test friction for optional dependency scenarios and help isolate core behavior.

### 8.2 Temporary Workspace Style

Some tests create temporary directories and simulate a minimal OntoBDC workspace by writing:

- `.__ontobdc__/config.yaml`
- mock RDF storage metadata

This pattern appears especially in:

- `storage/test_storage.py`

### 8.3 Subprocess-Based CLI Validation

Some tests validate behavior by spawning subprocesses rather than calling functions directly.

This is visible in:

- `test_cli_python.py`
- `storage/test_storage.py`

This style is useful for command realism, but tends to be slower and more environment-sensitive than pure unit tests.

## 9. Tests Present But Not In The Standard Runner

Not every test-like artifact currently participates in the standard automated flow.

Examples include:

- `test/test_a3_etl.sh`
- files under `triage/`

This means the repository has a distinction between:

- tests present in the tree
- tests selected by `test/config.yaml`

The configuration file is therefore the operational definition of the standard suite.

## 10. CI And Automation Status

The currently visible GitHub Actions workflow under `wip/.github/workflows` is:

- `pypi-publish.yml`

That workflow:

- builds the package
- publishes to PyPI on release

It does **not** currently run the automated test suite before publishing.

This is an important current characteristic of the repository:

- local automated tests exist
- but there is no active test execution workflow in the main visible CI path described here

## 11. Strengths

- **Dedicated test workspace**: the repository has a clear top-level `test/` area.
- **Mixed practical strategy**: shell and Python tests cover both CLI realism and internal logic.
- **Capability and strategy focus**: important execution-strategy logic is already covered.
- **Optional dependency handling**: `test/stubs` helps reduce friction for extras-based dependencies.
- **Runnable repository script**: `test/test` provides a single operational entrypoint.

## 12. Weaknesses And Gaps

- **No visible test CI workflow**: tests are not currently enforced in the visible GitHub Actions flow.
- **Mixed test styles**: `pytest`, `unittest`, and shell tests coexist without a single documented style guide.
- **No explicit coverage reporting flow**: `coverage` is declared, but coverage measurement is not part of the standard runner.
- **Selection is config-driven and partial**: only tests listed in `test/config.yaml` are run by default.
- **Environment sensitivity**: subprocess and shell tests can be more brittle across machines.
- **Sparse project-level documentation**: the test strategy is discoverable from code, but not yet fully formalized in user-facing documentation.

## 13. Normative Characterization

The current automated testing setup is best described as:

- a practical repository-level test harness
- centered on `pytest` execution
- augmented with shell-level behavior checks
- optimized for local development rather than CI-first enforcement

It is not currently:

- a fully centralized `pytest`-only test architecture
- a coverage-driven gate
- a CI-enforced release quality gate

## 14. Recommended Next Steps

- Add a dedicated CI workflow that runs `test/test` or an equivalent `pytest` command before publish and merge.
- Decide whether shell tests and Python tests should continue to coexist in the same orchestration model.
- Formalize a preferred authoring style:
  - `pytest` functions
  - `unittest.TestCase`
  - or a documented mix by purpose
- Add optional coverage reporting to the standard runner.
- Review whether tests present outside `test/config.yaml` should be promoted into the standard suite or explicitly marked as experimental.
- Add a short developer-facing guide explaining how to run the tests locally.

## 15. Summary

The current OntoBDC automated testing setup is centered on a dedicated `test/` workspace, a YAML-driven repository runner, and a mixed strategy using shell checks plus `pytest`-executed Python tests.

Its strongest current areas are:

- run parameter strategies
- A3 transformations and guardrails
- storage behavior
- selected CLI behavior

Its main operational gap is clear:

- automated tests exist locally
- but they are not currently enforced in the visible release automation workflow

Overall, the test system is functional and useful for development, but it still needs stronger CI integration and a more formal testing policy to become a full repository quality gate.
