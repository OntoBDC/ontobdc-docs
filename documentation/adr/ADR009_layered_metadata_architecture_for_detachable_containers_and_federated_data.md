# ADR 009: Adopt A Layered Metadata Architecture For Detachable Containers And Federated Data

## Status

Accepted

## Context

Across engineering, industrial operations, research, analytics, and other data-intensive domains, projects routinely handle a highly heterogeneous set of digital artifacts.

Typical examples include:

- 3D models and CAD files
- spreadsheets and CSV tables
- PDFs and technical documents
- schedules, logs, and reports
- domain-specific binary formats

These artifacts are operationally valuable in their native form, but they do not all behave the same way from a data architecture perspective.

The previous storage model in OntoBDC exposed several structural problems:

- storage portability was weak because containers depended too heavily on a centralized control graph
- raw files had no intrinsic semantic contract beyond their physical presence
- tabular sources such as spreadsheets and CSV files were structurally fragile and often lacked strict typing, schema validation, and durable row identity
- semantic linking across heterogeneous artifacts was possible in principle, but too brittle when built directly on unstable file layouts or ad hoc table structures

As a result, the platform needed a storage and data architecture that could support all of the following at the same time:

- infrastructure governance
- detachable and self-descriptive containers
- strict validation of tabular datasets
- semantic federation across heterogeneous resources

## Decision Drivers

The decision is driven by the following requirements:

- FAIR-oriented data handling, so assets remain findable, accessible, interoperable, and reusable
- detachability, so a container can be moved between OntoBDC instances without losing its local integrity
- separation of concerns, so internal control artifacts do not pollute user-facing domain manifests
- resilience to structural change, so semantic links do not silently collapse when files or tables evolve
- compatibility with native user artifacts, so users can keep working with the formats already used in their domain

## Decision

OntoBDC adopts a layered metadata architecture in which each layer has a narrow and explicit responsibility.

The architecture is organized around three complementary scopes:

1. a container governance layer for packaging, provenance, and transport metadata
2. a tabular formalization layer for schema validation, typing, and stable record identity
3. a semantic federation layer for explicit RDF-based links across heterogeneous artifacts

This decision intentionally avoids forcing every artifact into one monolithic RDF graph.

Instead, the platform preserves native files, adds validation where needed, and introduces semantic linking only where it adds explicit architectural value.

## Layered Architecture

### Layer 1: Storage Container Governance

The storage container is the physical unit on the filesystem.

Its governance is represented through internal metadata under `.__ontobdc__/`.

This layer includes:

- `ro-crate-metadata.json` for package-level provenance and transport-oriented metadata
- `storage.rdf` for OntoBDC control and local container rehydration

These two artifacts do not serve the same purpose.

`ro-crate-metadata.json` exists to describe transportable digital assets and external package metadata.

`storage.rdf` exists to represent OntoBDC storage control information, including the local metadata needed for detachability.

The local `storage.rdf` inside a container acts as a controlled projection of the information needed to reconstruct container registration in another OntoBDC instance.

This makes the container self-descriptive enough to be detached and later reattached without depending on the original root storage graph as the only source of truth.

### Layer 2: Formal Tabular Datasets

Tabular files such as spreadsheets and CSVs are not treated as semantically reliable merely because they exist as files.

When tabular content must participate in governed data flows, it is formalized as a validated dataset package with explicit contracts such as:

- schema
- primary keys
- field types
- structural validation rules

This layer gives unstable tabular inputs a stricter operational model.

Instead of relying on implicit spreadsheet conventions, the platform can expose tabular data as typed records with durable row identity.

That identity is essential when table records must be referenced by downstream semantic links, automation, or cross-resource queries.

### Layer 3: Semantic Federation

Semantic meaning is expressed through explicit RDF links rather than by overloading raw files or assuming semantics from directory layout alone.

This layer is responsible for:

- linking records across heterogeneous sources
- expressing cross-document relationships
- enabling federated semantic queries

The semantic layer can safely reference validated table rows, document fragments, model elements, or other governed resources because the lower layers provide stable storage context and structured identifiers.

## Rationale

### Avoid A Monolithic RDF Storage Model

Converting every artifact into a single central RDF graph would over-centralize the architecture, increase performance and maintenance risk, and weaken the role of native user files.

The selected approach keeps native artifacts intact while introducing metadata only where it is needed.

### Keep Containers Detachable

Containers must be movable and reusable across environments.

That requirement cannot be satisfied if a container depends exclusively on a central root graph that is external to the container itself.

The local `storage.rdf` exists precisely to preserve enough control metadata for reattachment and operational continuity.

### Separate Governance From Semantic Meaning

Transport metadata, storage control metadata, dataset validation metadata, and semantic federation metadata are different concerns.

They should not be collapsed into one undifferentiated manifest.

This separation reduces conceptual overload and makes each layer easier to audit, repair, and evolve.

### Protect Semantic Links From Weak Tabular Inputs

Spreadsheets and CSVs are practical and ubiquitous, but they are structurally weak unless governed by explicit contracts.

If the platform creates semantic links directly against unstable rows or informal columns, those links become brittle.

The tabular formalization layer reduces that risk by introducing stricter schemas and durable identifiers before semantic federation occurs.

## Responsibilities Mapping

### Root Storage Graph

The root storage graph sees the ecosystem of registered containers.

Its role is central orchestration and discovery, not exclusive ownership of all container knowledge.

### Container `storage.rdf`

The container-local `storage.rdf` sees the container and its internal managed storage metadata.

Its role is detachability, local control projection, and container rehydration in another OntoBDC environment.

### RO-Crate

The RO-Crate layer sees package-level assets intended for transport and external metadata exchange.

Its role is provenance, authorship, licensing, and package description.

It must not be treated as the source of truth for internal storage control.

Managed internal storage artifacts should remain excluded from automated crate refresh behavior when they belong to OntoBDC control concerns rather than transportable user-facing assets.

### Tabular Dataset Package

The tabular package layer sees the internal structure of spreadsheets and tabular files.

Its role is validation, typing, schema enforcement, and stable record identity.

### Semantic Federation Layer

The semantic federation layer sees meaning and relationships across heterogeneous artifacts.

Its role is cross-resource linking, semantic interoperability, and federated query support.

## Consequences

### Positive

- containers become detachable and more self-descriptive
- native user files remain first-class artifacts instead of being replaced by a monolithic RDF projection
- tabular data gains stricter contracts before participating in semantic workflows
- semantic links become more robust because they can rely on validated and stable identifiers
- governance concerns, validation concerns, and semantic concerns become easier to isolate operationally
- verification and repair workflows can target each layer independently

### Negative

- the architecture introduces multiple metadata layers that contributors must understand
- synchronization rules between layers must be explicit and well documented
- tabular formalization adds operational overhead compared with treating spreadsheets as opaque files
- semantic federation remains dependent on the quality of identifiers and mappings defined above it

### Neutral

- the root graph still exists as the central registry of containers
- containers still participate in a broader OntoBDC ecosystem even though they are locally rehydratable
- not every file must be elevated into a semantic resource

## Alternatives Considered

### Single Central RDF Monolith

Rejected because it would:

- concentrate too much responsibility in one graph
- weaken the role of native artifacts
- increase migration and performance risk
- reduce practical portability of detached containers

### Opaque File Storage With No Formal Dataset Or Semantic Layer

Rejected because it would preserve files physically but leave the platform without:

- strict validation for tabular data
- durable record identity
- robust semantic linking across heterogeneous sources

### Flat Metadata Model With One Manifest For Everything

Rejected because governance, storage control, tabular validation, and semantic federation have different lifecycles and should not be forced into one undifferentiated abstraction.

## Implementation Notes

The current implementation direction in OntoBDC reflects this decision through the following principles:

- the root storage graph is used for container discovery and orchestration
- container-local `storage.rdf` files preserve local storage knowledge needed for detachability
- dataset metadata for a container is stored in the container-local storage graph rather than in the root graph
- automated RO-Crate refresh behavior excludes internal OntoBDC control artifacts and managed dataset paths when those paths belong to internal storage control rather than transport packaging
- semantic and dataset-related processing should use explicit metadata contracts rather than infer meaning from filesystem structure alone

## Risks And Constraints

This decision depends on disciplined boundaries between layers.

The main risks are:

- leaking internal storage control concerns into package manifests
- allowing semantic links to depend on unstable tabular structure
- rebuilding hidden coupling to a centralized root graph
- creating duplicate sources of truth without clear synchronization rules

These risks are acceptable only if each layer keeps a narrow responsibility and the platform continues to enforce that separation in commands, repositories, checks, and repair flows.
