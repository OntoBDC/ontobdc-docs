# UC03 - Run Capability (`ontobdc run`)

## Description
This is the core use case of the OntoBDC stack. It executes a specific Capability (Query or Action) dynamically loaded from the available modules.

## Actors
- **User**: Wants to perform an operation (e.g., fetch a web link, extract data, transform schema).
- **System (OntoBDC)**: Resolves the requested Capability, validates CLI arguments against its schema, delegates execution to the appropriate strategy, and returns the produced output.

## Pre-conditions
- The project is initialized.
- Infrastructure checks have passed.
- The target capability is installed and available.

## Flow of Events
1. The user runs `ontobdc run <capability_id> [arguments]`.
2. The system resolves the requested capability via `CapabilityLoader` .
3. The system maps the provided CLI arguments to the `input_schema` defined in the capability's `METADATA`.
4. The system delegates execution to the appropriate `CliStrategy` (e.g., `CapabilityStrategy`).
5. The Capability executes, manipulating data, or interacting with the network.
6. The system captures the output (e.g., a Knowledge Graph or JSON data) and presents it to the user.

## Post-conditions
- The capability's logic is fully executed.
- Resulting data is returned or saved depending on the capability's design.



**Cadeia exata que gera a mensagem**
- O `ontobdc run` monta a lista `all_capabilities` chamando `get_all_capabilities()`; ali ele percorre os pacotes retornados por `load_capability_packages()` e usa `CapabilityLoader.load_from_package(pkg)` para varrer/importar módulos e coletar classes com `METADATA.id` ([run.py](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/wip/src/ontobdc/run/run.py#L80-L196), [loader.py](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/wip/src/ontobdc/run/adapter/loader.py#L11-L50)).
- Quando você passa `--id`, ele procura esse ID dentro de `all_capabilities`; se não achar, imprime exatamente “Capability Not Found …” e sai com erro ([run.py](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/wip/src/ontobdc/run/run.py#L183-L196)).

**Por que essa capability específica não entra em `all_capabilities`**
- A sua capability existe e define o ID exatamente como no erro ([transformation_to_sanitized.py](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/wip/src/ontobdc/a3/plugin/capability/transformation_to_sanitized.py#L8-L24)).
- Só que o “descobridor” **só varre os pacotes** retornados por `load_capability_packages()`. E, quando não existe configuração, ele usa um *default* que **não inclui** `ontobdc.a3.plugin` (apenas `ontobdc.module` e `ontobdc.storage.plugin`) ([util.py](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/wip/src/ontobdc/run/util.py#L33-L102)).
- No seu `.__ontobdc__/config.yaml` não existe a seção `capability: package: ...` para adicionar `ontobdc.a3.plugin`, então ele cai nesse default ([config.yaml](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/.__ontobdc__/config.yaml#L1-L20)).
