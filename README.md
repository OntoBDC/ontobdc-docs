# 🚀 OntoBDC (Ontology-Based Data Capabilities)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/OntoBDC/ontobdc-core/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) [![Status](https://img.shields.io/badge/status-active-success)](https://github.com/OntoBDC)

**OntoBDC** (Ontology-Based Data Capabilities) is a domain-driven data architecture and capability runtime for executing ontology-aware data operations. It bridges the gap between static data storage and dynamic semantic execution, making your data smart, portable, and actionable.

Use OntoBDC to manage the lifecycle of your engineering and data projects. The runtime orchestrates **L1 Queries** (Discovery), **L2 Actions** (Transformation), and **L3 Use Cases** (State Transitions) to provide reproducible and auditable workflows directly from your terminal.

**Table of contents**

- [Principles](#principles)
- [Architecture & Modules](#architecture--modules)
- [Capabilities](#capabilities)
- [Getting Started](#getting-started)
- [Managing Dependencies](#managing-dependencies)
- [Ontologies Catalog](#ontologies-catalog)
- [Exceptions Catalog](#exceptions-catalog)
- [Open Source](#open-source)

## Principles

- **Semantic First**: Data is not just bytes; it has meaning defined by ontologies.
- **Modular by Design**: Capabilities are isolated plugins grouped by domains (Core, Storage, A3, Social, Dev). You can add new operations without changing the core runtime.
- **Portable**: The entire runtime and data package are self-contained. Run it on a laptop, a server, or inside a Google Colab notebook.

## Architecture & Modules

OntoBDC is built upon a modular architecture. Instead of installing a monolithic package, you can enable only the modules you need for your specific context.

- **Core / Run / CLI**: The heart of the system. Manages the execution engine, dynamic capability loading, and CLI interactions.
- **Storage**: Provides adapters and capabilities for physical file manipulation, ICDD containers, and local data querying.
- **A3**: Specialized capabilities for Agent-to-Agent Architecture and LLM data extraction/transformation (means AI Anchor Agent).
- **Social**: Tools for web scraping and semantic data extraction from public URLs (e.g., generating Knowledge Graphs from HTML/RDFa).
- **Plan / Check**: Workflow DAG orchestration and environment validation checks.
- **Dev**: Tooling for semantic commits and branch management.

## Capabilities

Capabilities are the core units of execution in OntoBDC. They are categorized into three levels of power and responsibility, ensuring safety and clarity for autonomous agents:

| Level | Name | Scope & Power | Side Effects? | Example |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Query** | **Read-Only / Discovery.** Pure interface to query the environment. | **NO.** Must be idempotent and safe to retry infinite times. | `list_documents`, `extract_transform_raw_text`. |
| **L2** | **Action** | **Transformation / Creation.** Takes input data and produces new data/files without changing business state logic. | **Local Only.** Can create/write files but does not advance workflow state. | `unzip_file`, `convert_pdf_to_png`. |
| **L3** | **Use Case** | **State Transition.** Orchestrates L1 and L2 to move the business process forward. | **YES.** Changes the "truth" of the system. | `process_chat_folder` (Raw -> Processed). |

## Getting Started

OntoBDC requires Python 3.10+ and pip. Install the base system to start using the CLI:

```bash
pip install ontobdc
```

After installation, you can initialize a project context and set up the execution engine (e.g., `venv` or `colab`):

```bash
ontobdc init
```

To execute capabilities interactively, you can invoke the run command and pass the capability ID. The system will dynamically prompt you for the required parameters or read them from CLI flags:

```bash
ontobdc run --id <capability_id>
```

To validate the environment, engine, and dependencies:

```bash
ontobdc check --repair
```

## Managing Dependencies

OntoBDC uses a smart optional dependency system (Extras). Instead of installing heavy packages you don't need, you can enable specific modules. The CLI dynamically checks if the required module is enabled before executing a capability.

To install the full suite of development tools (pytest, coverage):
```bash
pip install -e ".[dev]"
```

To enable specific domain modules (e.g., A3 for LLMs or Storage for file manipulation):
```bash
pip install -e ".[a3,storage]"
```

## Ontologies Catalog

### Storage Capabilities
{{ render_ontology('ontology/nid/storage/capability.ttl') }}

## Exceptions Catalog

This catalog is generated automatically from our semantic Knowledge Graph (RDF):

{% for error in get_rdf_exceptions() %}
### {{ error.code }}
- **Type**: `{{ error.python_type }}`
- **Description**: {{ error.description }}
{% endfor %}

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
