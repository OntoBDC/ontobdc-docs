# SPEC 011 - Deprecating ADRs And SPECs

## Status

- **Status**: Working specification
- **Scope**: `docs/documentation`
- **Audience**: maintainers and contributors of the OntoBDC project

## 1. Purpose

This specification describes how to deprecate Architecture Decision Records (ADRs) and Specifications (SPECs) in the OntoBDC project documentation.

This document answers:

- how to mark an ADR or SPEC as deprecated
- how to preserve historical content
- how to link deprecated documents to their legacy notes

## 2. Source Of Truth

This specification is derived from the current project structure under:

- `docs/documentation/adr/`
- `docs/documentation/spec/`
- `docs/documentation/legacy/`

## 3. Deprecation Process

### 3.1 Keep The Original File

Never delete the original ADR or SPEC file from its directory (`adr/` or `spec/`). Always keep the original file in place.

### 3.2 Update The Original File

For the original file:

1. Change the status to "Deprecated"
2. Add a "Deprecation Note" section immediately after the status
3. Include:
   - the version when it was deprecated
   - a brief explanation of why it was deprecated
4. Update the "Related Files" section to link to the corresponding legacy note

#### Example - ADR

```markdown
# ADR 002: Build CLI Help From `pyproject.toml` Metadata

## Status

Deprecated

## Deprecation Note

This ADR is deprecated as of version 0.9.0. The project is no longer using `pyproject.toml` to document CLI commands.

## Related Files

- [pyproject.toml](pyproject.toml)
- [Legacy Note](../legacy/OLD003_cli_help_from_pyproject_metadata_adr.md)
```

#### Example - SPEC

```markdown
# SPEC 002 - CLI Help From `pyproject.toml` Metadata

## Status

- **Status**: Deprecated
- **Scope**: `src/ontobdc/cli` and `pyproject.toml`
- **Audience**: maintainers and contributors of the OntoBDC core CLI

## Deprecation Note

This specification is deprecated as of version 0.9.0. The project is no longer using `pyproject.toml` to document CLI commands.

## Related Files

- [pyproject.toml](pyproject.toml)
- [Legacy Note](../legacy/OLD004_cli_help_from_pyproject_metadata_spec.md)
```

### 3.3 Create A Legacy Note

Create a new file in `docs/documentation/legacy/` with:

1. Prefix `OLD` followed by the next available number
2. Suffix indicating whether it's an ADR or SPEC
3. Content structure:
   - Title: `OLD XXX - Legacy Note - [Original Title]`
   - Purpose section
   - Removal Status section
     - Status
     - Removed in version
   - Why It Was Removed section
   - Historical Content section with the full original content

#### Example Legacy Note Filenames

- `OLD003_cli_help_from_pyproject_metadata_adr.md`
- `OLD004_cli_help_from_pyproject_metadata_spec.md`

#### Example Legacy Note Structure

```markdown
# OLD 003 - Legacy Note - Build CLI Help From `pyproject.toml` Metadata

## Purpose

This note summarizes the ADR for building CLI help from `pyproject.toml` metadata.

## Removal Status

- **Status**: removed from the active documentation
- **Removed in version**: `0.9.0`

## Why It Was Removed

The project is no longer using `pyproject.toml` to document CLI commands.

## Historical Content

---

[Full original content here]
```

## 4. Related Files

- `docs/documentation/legacy/`
