---
code: SPEC009
title: Test Strategy and Directory Structure
status: Accepted
author: Elias M. P. Junior
date: 2026-03-08
tags: architecture, testing, structure, quality-assurance
---

# SPEC009: Test Strategy and Directory Structure

This document defines the standard for organizing, implementing, and registering tests within the OntoBDC architecture. It enforces a strict separation between production code and test code to maintain repository cleanliness and build integrity.

## 1. Directory Structure

### 1.1 Separation of Concerns
Production code and test code MUST reside in separate root directories.
- **Production Code**: `ontobdc-stack/wip/src/` (or relevant source root).
- **Test Code**: `ontobdc-stack/test/`.

**Prohibited**: Placing `tests/` folders inside `src/` or `wip/`.

### 1.2 Mirroring Structure
The internal structure of the `test/` directory MUST mirror the package structure of the source code being tested.

**Example**:
- Source: `src/ontobdc/run/adapter/contex.py`
- Test: `test/src/ontobdc/run/adapter/test_contex.py`

## 2. Test Registration

Tests are NOT automatically discovered by scanning directories. They MUST be explicitly registered to be executed by the CI/CD or test runner.

### 2.1 Configuration File
The registry file is located at `ontobdc-stack/test/config.yaml`.

### 2.2 Registration Format
Tests are listed under the `shell` key (legacy name, now includes Python tests). Paths are relative to `test/src/ontobdc/` (or the configured test root).

```yaml
shell:
  - test_run_capabilities.py
  - run/adapter/test_contex.py
  - run/core/strategy/test_action_only.py
```

## 3. Implementation Guidelines

### 3.1 Unit Tests
- Use `unittest` or `pytest`.
- Mock external dependencies (filesystem, network, database) using `unittest.mock`.
- Do not rely on the actual state of the `wip/` directory unless integration testing explicitly requires it.

### 3.2 Integration Tests
- Should be clearly distinguished from unit tests.
- May require setup/teardown of temporary directories or Docker containers.

## 4. Rationale

1.  **Cleanliness**: Prevents test artifacts (temporary files, mocks) from polluting production builds.
2.  **Explicit Execution**: Forcing registration prevents "dead" or obsolete tests from running silently and consuming resources, and ensures that every running test is intentional.
3.  **Deployment**: Simplifies packaging by allowing the exclusion of the entire `test/` directory without complex include/exclude patterns.
