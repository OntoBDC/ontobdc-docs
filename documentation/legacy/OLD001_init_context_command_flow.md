# OLD 001 - Legacy Note - `ontobdc init context`

## Purpose

This note summarizes the main code paths behind the `ontobdc init context` command.

## Removal Status

- **Status**: removed from the core CLI surface
- **Removed in version**: `0.9.0`

## Why It Was Removed

`ontobdc init context` was removed from the core distribution because RO-Crate is no longer intended to be a mandatory concern of the OntoBDC core application.

The current direction is to keep the core focused on the essential command surface and runtime responsibilities of OntoBDC itself, such as initialization, checks, execution, listing, planning, storage, and developer tooling.

RO-Crate support is instead planned to move to a future companion package built on top of the core distribution.

In this context, a *companion package* means an additional package that extends the core application with specialized features without making those features part of the minimal core installation or core maintenance boundary.

That future package is expected to:

- depend on the OntoBDC core package
- reuse the core CLI and project structure where appropriate
- provide RO-Crate-specific commands, adapters, and dependencies as an optional extension layer

This separation reduces coupling inside the core, keeps the core dependency surface smaller, and leaves RO-Crate functionality available as a complementary capability for users who explicitly need it.

## Historical Dispatch

Before removal, the `init` command switched to a dedicated `init_context_main()` path when the second CLI argument was `context`.

```python
def init_main():
    if len(sys.argv) >= 3 and sys.argv[2] == "context":
        init_context_main()
        return

    init_engine_main()
```

## Historical Implementation

The legacy command logic lived in a dedicated `init_context_main()` function.

```python
def init_context_main() -> None:
    print("")
    log("INFO", "Initializing OntoBDC context creation.")

    cwd = os.getcwd()
    log("INFO", "Found current directory...", f"path={cwd}")

    existing_context_path = os.path.join(cwd, ".__ontobdc__", "ro-crate-metadata.json")
    if os.path.exists(existing_context_path):
        message_box(
            "RED",
            "Error",
            "Context Already Declared",
            f"Context already exists in this directory.\n\nPath: {existing_context_path}",
        )
        sys.exit(1)

    confirmed = _confirm_context_creation(cwd)
    if not confirmed:
        message_box(
            "YELLOW",
            "Warning",
            "Context Creation Cancelled",
            f"Operation cancelled.\n\npath={cwd}",
        )
        return

    try:
        from ontobdc.module.resource.adapter.folder import LocalFolderAdapter
        from ontobdc.module.resource.adapter.repository import LocalObjectDatasetRepository
        from ontobdc.module.resource.adapter.crate import RoCrateDatasetAdapter
    except Exception:
        message_box(
            "RED",
            "Error",
            "Dependencies Missing",
            "Could not import RO-Crate dependencies.\n\nRun:\n  ontobdc check --repair",
        )
        sys.exit(1)

    folder = LocalFolderAdapter(path=cwd)
    repo = LocalObjectDatasetRepository(folder, ensure_path=True)

    try:
        adapter = RoCrateDatasetAdapter(repo)
        adapter.create_ro_crate(output_dir=cwd)
    except Exception as e:
        message_box("RED", "Error", "Init Context Failed", str(e))
        sys.exit(1)

    message_box(
        "GREEN",
        "Success",
        "Context Created",
        f"RO-Crate created at:\n\n{os.path.join(cwd, '.__ontobdc__', 'ro-crate-metadata.json')}",
    )
```

## CLI Entry Point

At the top-level CLI, `ontobdc init` delegated to `init_main()`, which then selected the legacy context branch when applicable.

```python
project_root: Optional[str] = get_root_dir()

if cmd == "init":
    from ontobdc.cli.init import init_main
    init_main()
    sys.exit(0)
```

## Behavioral Summary

- `ontobdc init context` is a special `init` mode, separate from engine initialization.
- It checks whether `.__ontobdc__/ro-crate-metadata.json` already exists.
- It asks the user to confirm context creation.
- It imports the local RO-Crate-related adapters.
- It creates a local RO-Crate structure in the current directory.
- It reports success or failure through the message box interface.
