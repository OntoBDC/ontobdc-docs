# 🚀 OntoBDC (Ontology-Based Data Capabilities)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/OntoBDC/ontobdc-core/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) [![Status](https://img.shields.io/badge/status-active-success)](https://github.com/OntoBDC)

**OntoBDC** (Ontology-Based Data Capabilities) is a domain-driven data architecture and capability runtime for executing ontology-aware data operations on portable datasets. It bridges the gap between static data storage and dynamic semantic execution.

When data is described by **RO-Crate**, it becomes self-describing. OntoBDC leverages this metadata to automatically discover and execute available operations relevant to the data context.

Use OntoBDC to manage the lifecycle of your engineering data projects. The runtime orchestrates **L1 Queries** (Discovery), **L2 Actions** (Transformation), and **L3 Use Cases** (State Transitions) to provide reproducible and auditable workflows.

**Table of contents**

- [Project Focus](#project-focus)
- [Principles](#principles)
- [Architecture](#architecture)
- [Capabilities](#capabilities)
- [Getting Started](#getting-started)
- [Entity Framework](#entity-framework)
- [Useful Links](#useful-links)
- [Open Source](#open-source)
- [Contributing](#contributing)
- [Who uses OntoBDC?](#who-uses-ontobdc)

## Project Focus

OntoBDC works best with **decentralized, portable data projects**. Unlike monolithic systems that lock data into specific databases, OntoBDC assumes data lives in portable packages (Zip/Folder/Local Storage) that can be moved between local environments, cloud, and edge devices without losing semantic meaning or operational capability.

OntoBDC is commonly used to:

- **Standardize** data exchange between diverse engineering disciplines (BIM, GIS, Documents).
- **Execute** context-aware operations and automated checks without hardcoded pipelines.
- **Validate** engineering data against defined capabilities and rules ensuring reproducibility.

## Principles

- **Semantic**: Data is not just bytes; it has meaning defined by ontologies and metadata (RO-Crate).
- **Modular**: Capabilities are isolated plugins. You can add new operations without changing the core runtime.
- **Portable**: The entire runtime and data package are self-contained. Run it on a laptop, a server, or inside a container.

## Architecture

OntoBDC is built on core semantic layers:

1.  **Context Layer**: [RO-Crate](https://www.researchobject.org/ro-crate/) for semantic metadata and relationships.

The **Capability Runtime** binds these layers together, dynamically resolving which tools (CLI strategies) apply to the current data state.

## Capabilities

Capabilities are the core units of execution in OntoBDC. They are categorized into three levels of power and responsibility, ensuring safety and clarity for autonomous agents:

| Level | Name | Scope & Power | Side Effects? | Example |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Query** | **Read-Only / Discovery.** Pure interface to query the environment. | **NO.** Must be idempotent and safe to retry infinite times. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformation / Creation.** Takes input data and produces new data/files without changing business state logic. | **Local Only.** Can create/write files but does not advance workflow state. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **State Transition.** Orchestrates L1 and L2 to move the business process forward. | **YES.** Changes the "truth" of the system. | `process_chat_folder` (Raw -> Processed), `publish_dataset`. |

This structure allows granular control over what an agent can do, separating "sensing" (L1) from "doing" (L2) and "deciding" (L3).

## Getting Started

OntoBDC requires Python 3.11+ and pip. Install it to start using the CLI:

```bash
pip install ontobdc
```

After installation, you can initialize a project context:

```bash
ontobdc init
```

This creates the local configuration (`.__ontobdc__` directory) automatically detecting the environment (e.g., `venv` or `Google Colab`).

To execute capabilities interactively:

```bash
ontobdc run
```

To validate engineering data against defined rules:

```bash
ontobdc check --repair
```

## Entity Framework

The Entity Framework is a local structure that helps you manage **Entities** (ELOFs) and their ontology façade files under `.__ontobdc__/ontology/entity/`, indexed by `.__ontobdc__/entity.rdf`.

Enable it (also prepares `.__ontobdc__/payload/*` and downloads ISO 21597 container ontologies when needed):

```bash
ontobdc entity --enable true
```

Create and list entities:

```bash
ontobdc entity --create org.example.my_entity
ontobdc entity --list
```

Disable and purge all local Entity Framework state:

```bash
ontobdc entity --enable false
ontobdc entity --purge
```

## Useful Links

| Resource | Link |
|----------|------|
| 📘 Documentation | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## Open Source

OntoBDC is a free and open-source initiative, licensed under the **Apache License 2.0**.
We believe in the power of community-driven development to solve complex data interoperability challenges.

## Contributing

We are always on the lookout for contributors to help us fix bugs, create new features, or improve project documentation. If you are interested, feel free to open a PR or issue on GitHub.

## Who uses OntoBDC?

OntoBDC is the core engine behind **InfoBIM**, powering semantic data interoperability for complex engineering projects.

---
<p align="center">Proudly developed in Brazil 🇧🇷</p>
