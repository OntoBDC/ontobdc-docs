# 🚀 OntoBDC (Ontology-Based Data Capabilities)

| Category   | Badges |
|------------|--------|
| License    | [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE) |
| Python     | [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) |
| Standards  | [![Frictionless](https://img.shields.io/badge/frictionless-data-black)](https://frictionlessdata.io/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) |
| State      | [![Sismic](https://img.shields.io/badge/statecharts-sismic-blue)](https://sismic.readthedocs.io/) |
| Status     | [![Status](https://img.shields.io/badge/status-active-success)]() |

**OntoBDC** (Ontology-Based Data Capabilities) is a capability-driven runtime for executing ontology-aware data operations on portable datasets. It bridges the gap between static data storage and dynamic semantic execution.

When data is described by **RO-Crate** and **Frictionless Data Packages**, it becomes self-describing. OntoBDC leverages this metadata to automatically discover and execute available **Capabilities** (operations) relevant to the data context.

Use OntoBDC to manage the lifecycle of your data projects. The runtime orchestrates **L1 Capabilities** (Discovery), **L2 Actions** (Transformation), and **L3 Use Cases** (State Transitions) while maintaining a rigorous **Event Sourcing** backbone (System Crate).

**Table of contents**

- [Project Focus](#project-focus)
- [Principles](#principles)
- [Architecture](#architecture)
- [Getting started](#getting-started)
- [Installation](#installation)
- [Useful Links](#useful-links)
- [Open Source](#open-source)
- [Contributing](#contributing)
- [Who uses OntoBDC?](#who-uses-ontobdc)

## 🎯 Project Focus

OntoBDC works best with **decentralized, portable data projects**. Unlike monolithic systems that lock data into specific databases, OntoBDC assumes data lives in portable packages (Zip/Folder/WEB/API/FTP) that can be moved between local storage, cloud, and edge devices without losing semantic meaning or operational capability.

OntoBDC is commonly used to:

- **Standardize** data exchange between diverse engineering disciplines (BIM, GIS, Documents).
- **Execute** context-aware operations (e.g., "Extract Entities from PDF", "Validate IFC Model") without hardcoded pipelines.
- **Track** every modification in a project's history via an immutable event log (System Crate).

## 💡 Principles

- **Semantic**: Data is not just bytes; it has meaning defined by ontologies and metadata (RO-Crate).
- **Modular**: Capabilities are isolated plugins. You can add new operations without changing the core runtime.
- **Portable**: The entire runtime and data package are self-contained. Run it on a laptop, a server, or inside a container.
- **Event-Sourced**: State is derived from a sequence of events, ensuring auditability and time-travel debugging.

## 🏗️ Architecture

OntoBDC is built on three pillars:

1.  **Physical Layer**: [Frictionless Data Package](https://frictionlessdata.io/) for file organization.
2.  **Context Layer**: [RO-Crate](https://www.researchobject.org/ro-crate/) for semantic metadata and relationships.
3.  **System Layer**: **System Crate** for event sourcing and operational memory, implementing a robust **Finite State Machine (FSM)**.

The **Capability Runtime** binds these layers together, dynamically resolving which tools (CLI strategies) apply to the current data state.

## ⚡ Capabilities

Capabilities are the core units of execution in OntoBDC. They are categorized into three levels of power and responsibility, ensuring safety and clarity for autonomous agents:

| Level | Name | Scope & Power | Side Effects? | Example |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Capability** | **Read-Only / Discovery.** Pure interface to query the environment. | **NO.** Must be idempotent and safe to retry infinite times. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformation / Creation.** Takes input data and produces new data/files without changing business state logic. | **Local Only.** Can create/write files but does not advance workflow state. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **State Transition.** Orchestrates L1 and L2 to move the business process forward. | **YES.** Changes the "truth" of the system. | `process_chat_folder` (Raw -> Processed), `publish_dataset`. |

This structure allows granular control over what an agent can do, separating "sensing" (L1) from "doing" (L2) and "deciding" (L3).

## 📦 Installation

OntoBDC is typically deployed via pip. Install it to start using the CLI:

```bash
pip install ontobdc

# After installation, you can run the CLI like this:
ontobdc --help
```

## 🔗 Useful Links

| Resource | Link |
|----------|------|
| 📘 Documentation | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## ❤️ Open Source

OntoBDC is a free and open-source initiative, licensed under the **Apache License 2.0**.
We believe in the power of community-driven development to solve complex data interoperability challenges.

## 🤝 Contributing

OntoBDC is an open initiative. Contributions are welcome!

## 🏢 Who uses OntoBDC?

OntoBDC is the core engine behind **InfoBIM**, powering semantic data interoperability for complex engineering projects.

---
<p align="center">Proudly developed in Brazil 🇧🇷</p>
