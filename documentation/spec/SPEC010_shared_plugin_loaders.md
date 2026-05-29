# SPEC 010 - Shared Plugin Loaders

## Status

- **Status**: Working specification of the current shared plugin loader model
- **Scope**: `src/ontobdc/shared/adapter/plugin.py`
- **Audience**: maintainers and contributors working on plugin discovery, dynamic loading, CLI commands, and runtime extensibility

## 1. Purpose

This specification describes the current shared plugin loading model implemented in `src/ontobdc/shared/adapter/plugin.py`.

The module exists to provide a common discovery mechanism for runtime-extensible resources across OntoBDC.

It currently defines loaders for:

- capabilities
- CLI context parameter strategies
- CLI commands

This document explains:

- how plugin package discovery works
- how each loader filters and instantiates resources
- which runtime areas currently depend on these loaders
- the error-tolerance model of plugin loading
- current inconsistencies and limitations

## 2. Source Of Truth

This specification is derived from the current implementation under:

- `src/ontobdc/shared/adapter/plugin.py`
- `src/ontobdc/run/domain/port/resource.py`
- `src/ontobdc/cli/domain/port/command.py`
- `src/ontobdc/run/domain/resource/capability.py`
- `src/ontobdc/run/domain/port/context.py`

Current known consumers include:

- `src/ontobdc/list/list.py`
- `src/ontobdc/run/run.py`
- `src/ontobdc/run/adapter/context.py`
- `src/ontobdc/run/domain/machine/dag.py`
- `src/ontobdc/run/plugin/capability/resolution_to_filled.py`
- `src/ontobdc/cli/adapter/command.py`

## 3. Runtime Role

The shared plugin loaders are the dynamic discovery boundary between:

- the importable OntoBDC package tree
- runtime components that need extensibility without hardcoded registries

They allow the system to discover plugin resources by convention rather than by explicit static import lists.

In practice, this means the module is responsible for:

- locating plugin package roots
- walking subpackages under known plugin folders
- importing modules dynamically
- selecting compatible classes
- returning discovered resources as classes or instantiated objects

## 4. Core Model

The module defines one shared base adapter and three concrete loaders:

- `PluginResource`
- `CapabilityLoader`
- `ParameterLoader`
- `CommandLoader`

All three loaders rely on folder conventions rooted under `ontobdc`.

## 5. Base Discovery Model

### 5.1 `PluginResource`

`PluginResource` extends `PluginResourcePort` and provides the reusable folder discovery logic used by the concrete loaders.

Its central helper is:

- `_list_plugin_folder(resource: str) -> List[str]`

The abstract method:

- `get_all(resource: str)`

is left to the concrete loaders.

The convenience method:

- `get(resource: str, id: str)`

iterates over `get_all(resource)` and tries to match `capability.METADATA.id == id`.

This makes `get()` effectively tailored to capability-like resources even though it lives in the generic base loader.

### 5.2 Package Root Resolution

`_list_plugin_folder()` uses:

- `ontobdc.cli.get_script_dir()`

to resolve the effective package root of the current OntoBDC installation.

That root is then used as the scanning base for plugin discovery.

### 5.3 Directory Scanning Rules

The base scanner walks immediate child directories under:

- the OntoBDC root package
- `ontobdc/module` when that directory exists

For each child directory, it looks for:

- `plugin/<resource>/`

If that directory exists, the scanner appends:

- `ontobdc.<component>.plugin`

or, for module-based extensions:

- `ontobdc.module.<component>.plugin`

to the list of discovered plugin package names.

### 5.4 Directory Exclusions

The scanner ignores entries whose names:

- start with `.`
- start with `_`
- are `__pycache__`

It also ignores non-directory entries.

### 5.5 Error Tolerance

The base directory scan is intentionally tolerant.

Current behavior:

- scanning errors inside a directory are swallowed
- top-level scan failures return `[]`

This means plugin discovery prefers resilience over strict visibility into failures.

## 6. Capability Loader

### 6.1 Role

`CapabilityLoader` discovers capability classes exposed through plugin packages.

It is the main dynamic discovery mechanism behind capability cataloging and capability execution selection.

### 6.2 Discovery Algorithm

For each package name returned by `_list_plugin_folder(resource)`:

1. Import the plugin package.
2. Skip it if it cannot be imported.
3. Skip it if it is not package-like, meaning it has no `__path__`.
4. Walk all submodules under the plugin package.
5. Import each discovered submodule.
6. Inspect all members of the module.
7. Keep objects that:
   - are classes
   - expose `METADATA`
   - have truthy `METADATA`
   - have truthy `METADATA.id`
   - subclass `Capability`

The loader returns:

- a list of capability classes

It does not instantiate the capability classes during discovery.

### 6.3 Error Model

`CapabilityLoader` is the most verbose loader in the module.

When a submodule fails to load:

- it attempts to log a warning through `cli/print_log.sh`
- if that script is not available, it prints a warning to `stderr`
- loading continues with the next module

This behavior makes capability loading relatively observable compared with the other loaders.

### 6.4 Current Runtime Usage

Known current uses include:

- `ontobdc list`
- `ontobdc run`
- DAG planning and resolution flows

## 7. Parameter Loader

### 7.1 Role

`ParameterLoader` discovers CLI context parameter strategy implementations.

These strategies are used to parse and enrich CLI input for `ontobdc run`.

### 7.2 Discovery Algorithm

For each package name returned by `_list_plugin_folder("parameter")`:

1. Import the plugin package.
2. Skip it on `ImportError`.
3. Skip it if it has no `__path__`.
4. Import the nested resource package:
   - `<plugin_package>.parameter`
5. Skip it on `ImportError`.
6. Skip it if it has no `__path__`.
7. Walk submodules under that package.
8. Import each submodule.
9. Inspect module members.
10. Keep objects that:
    - are classes
    - subclass `CliContextStrategyPort`
    - are not `CliContextStrategyPort` itself
11. Instantiate each discovered strategy immediately.

The loader returns:

- a list of instantiated strategy objects

### 7.3 Instantiation Model

Unlike `CapabilityLoader`, `ParameterLoader` returns instances rather than classes.

This reflects the current runtime model in which context resolution executes concrete strategy objects directly.

### 7.4 Error Model

`ParameterLoader` is highly tolerant and mostly silent.

Current behavior:

- import failures are ignored
- submodule load failures are ignored
- no warning is emitted for skipped or broken strategies

This keeps the runtime resilient but makes debugging harder.

### 7.5 Current Runtime Usage

Known current consumers include:

- `src/ontobdc/run/adapter/context.py`
- `src/ontobdc/run/plugin/capability/resolution_to_filled.py`

This loader underpins the built-in plugin parameter model documented in `SPEC006`.

## 8. Command Loader

### 8.1 Role

`CommandLoader` is the experimental shared loader for CLI command plugins.

It is intended to discover command objects that implement:

- `CliCommandPort`

### 8.2 Constructor State

`CommandLoader` currently stores:

- `logical_component`

through its constructor.

However, in the current implementation, this state is not used by `get_all()`.

This means the loader currently does not filter commands by logical component even though its API suggests that it should.

### 8.3 Discovery Algorithm

For each package name returned by `_list_plugin_folder("command")`:

1. Import the plugin package.
2. Skip it on `ImportError`.
3. Skip it if it has no `__path__`.
4. Import the nested resource package:
   - `<plugin_package>.command`
5. Skip it on `ImportError`.
6. Skip it if it has no `__path__`.
7. Walk submodules under that package.
8. Import each submodule.
9. Inspect module members.
10. Keep objects that:
    - are classes
    - subclass `CliCommandPort`
    - are not `CliCommandPort` itself
11. Instantiate each discovered command immediately.

The loader returns:

- a list of instantiated command objects

### 8.4 Current Characteristics

The current implementation contains signs of work-in-progress behavior:

- `logical_component` is stored but unused
- `get_all()` prints each discovered plugin package name directly
- no compatibility filtering beyond `CliCommandPort` is currently applied

This suggests the command plugin model is being introduced incrementally and is not yet fully integrated.

### 8.5 Error Model

Like `ParameterLoader`, command loading is mostly silent.

Current behavior:

- import failures are ignored
- submodule load failures are ignored
- no structured logging is emitted

### 8.6 Current Runtime Usage

The current known consumer is:

- `src/ontobdc/cli/adapter/command.py`

At this stage, command loading appears to be under active construction rather than fully operational.

## 9. Structural Conventions

The loader model relies on a convention-based package layout.

The expected shape is roughly:

```text
ontobdc/
  <component>/
    plugin/
      capability/
      parameter/
      command/
```

or, for module-based extensions:

```text
ontobdc/
  module/
    <component>/
      plugin/
        capability/
        parameter/
        command/
```

The loader layer does not use a central registry file.

Discovery is inferred from the presence of these folders and from importable Python modules inside them.

## 10. Type And Instantiation Contract

The three loaders currently use different output contracts.

### 10.1 `CapabilityLoader`

Returns:

- classes

Selection criteria:

- subclass of `Capability`
- valid `METADATA.id`

### 10.2 `ParameterLoader`

Returns:

- instances

Selection criteria:

- subclass of `CliContextStrategyPort`

### 10.3 `CommandLoader`

Returns:

- instances

Selection criteria:

- subclass of `CliCommandPort`

This means the module does not expose one single uniform loader output model.

Consumers must know whether a given loader returns:

- classes
- or already-instantiated objects

## 11. Error Handling Summary

The current loaders share a resilience-first posture but differ in observability.

### 11.1 Shared Traits

- missing packages are tolerated
- broken plugin modules do not abort full discovery
- discovery continues after individual failures

### 11.2 Differences

`CapabilityLoader`:

- warns when module loading fails

`ParameterLoader`:

- fails silently on module-level issues

`CommandLoader`:

- also fails silently, but still contains direct `print()` output for package names

## 12. Design Implications

The current loader model enables several important behaviors.

### 12.1 Convention Over Registration

Contributors can add new plugin resources by placing modules under the expected `plugin/<resource>` folders without editing a central registry.

### 12.2 Runtime Extensibility

Capabilities, parameter strategies, and commands can be discovered dynamically from the importable package tree.

### 12.3 Loose Coupling

Execution and CLI layers can depend on abstract ports and plugin conventions rather than hardcoded imports.

### 12.4 Asymmetric Maturity

The loader family is not equally mature across all resource types:

- capabilities are operational and broadly used
- parameters are operational and strategy-driven
- commands are present but still transitional

## 13. Current Limitations

The current implementation has several notable limitations.

### 13.1 Generic Base With Capability-Specific `get()`

`PluginResource.get()` assumes a `METADATA.id` contract, which is not truly generic across all possible plugin resource types.

### 13.2 Silent Failure In Parameter And Command Loading

Broken strategy or command modules can disappear from runtime discovery without clear diagnostics.

### 13.3 Unused `logical_component` In `CommandLoader`

The command loader API suggests logical command scoping, but the current implementation does not apply that filter.

### 13.4 Mixed Return Shapes

Some loaders return classes while others return instances, which makes the API family less uniform.

### 13.5 Debug Print Residue

`CommandLoader.get_all()` currently prints package names directly, which looks like temporary debugging output rather than a stable contract.

### 13.6 Narrow Directory Scan Scope

The scanner only looks at immediate child directories of the OntoBDC root and `ontobdc/module`.

This means the model depends on a relatively strict package layout.

## 14. Guidance For Contributors

When introducing a new plugin resource under the current design:

1. Place it under a component-local `plugin/<resource>` folder.
2. Ensure the package is importable from the active OntoBDC package tree.
3. Match the expected type contract:
   - `Capability` for capability plugins
   - `CliContextStrategyPort` for parameter plugins
   - `CliCommandPort` for command plugins
4. Avoid import-time side effects when possible.
5. Prefer explicit, stable class definitions over dynamic exports.

When debugging discovery issues:

- verify the package folder structure first
- verify importability second
- verify type inheritance third
- remember that parameter and command loading may fail silently

## 15. Related Specifications

- `docs/documentation/spec/SPEC005_ontobdc_list_component.md`
- `docs/documentation/spec/SPEC006_run_cli_context_resolution.md`
- `docs/documentation/spec/SPEC007_cli_init_component.md`
