# SPEC - Country Dataset Container

## Status

- **Status**: Working specification of the current result
- **Scope**: `docs/ontology/social/ds/country`
- **Dataset version**: `0.1.0`

## 1. Purpose

This specification describes the current country dataset package stored under:

- `docs/ontology/social/ds/country`

The package combines:

- a container metadata graph in `index.rdf`
- a tabular source in CSV
- a minimal RDF graph in `payload/triples/nid.rdf`
- a Frictionless Data Package descriptor in `linkset/resources/datapackage.json`
- local copies of the Container and Linkset ontologies as normative references

The goal is to keep the package layered:

- `index.rdf` describes the package and its internal documents
- the CSV preserves the source table
- `nid.rdf` carries the semantic country node plus the link back to the CSV
- `datapackage.json` formalizes the CSV schema

Within this directory, `ds` means **dataset**.

The broader design intent is not limited to one country example. The idea is to build a dataset from living documents and easily manipulable formats that, together, describe an entity as a whole while preserving multiple complementary views of the same subject:

- a semantic view
- a tabular or raw operational view
- a package/container view
- a schema view

In this sense, the package is not just "using" ISO 21597. It is extending the ISO 21597 container and linkset ideas toward a more general dataset-oriented application profile, suitable for datasets composed of heterogeneous but coordinated documents.

## 2. Physical Structure

```text
docs/ontology/social/ds/
  country/
    index.rdf
    ontology/
      resources/
        Container.rdf
        Linkset.rdf
    payload/
      documents/
        country-identifier-iso3166-1-alpha-2-en.csv
      triples/
        nid.rdf
    linkset/
      resources/
        datapackage.json
```

## 3. Main Artifacts

- `index.rdf`
  - package-level metadata graph
  - declares the internal CSV document and the internal RDF document
- `payload/documents/country-identifier-iso3166-1-alpha-2-en.csv`
  - source table with columns `Name` and `Code`
- `payload/triples/nid.rdf`
  - current semantic graph
  - currently contains modeled individuals for all countries present in the source CSV
- `linkset/resources/datapackage.json`
  - Frictionless descriptor for the CSV resource and its schema
- `ontology/resources/Container.rdf`
  - local reference copy of the ISO Container ontology
- `ontology/resources/Linkset.rdf`
  - local reference copy of the ISO Linkset ontology

## 4. Current Logical Model

### 4.1 Container Layer

`index.rdf` plays the role of container description.

It declares:

- one publisher individual: `#OntoBDC`
- one CSV internal document: `#country-identifier`
- one RDF internal document: `#country-list`
- one `ct:ContainerDescription`

It also records:

- publication metadata
- version metadata
- provenance with `prov:wasDerivedFrom`
- source distribution with `dcat:downloadURL`

### 4.2 Tabular Layer

The CSV file is the operational source dataset:

- `payload/documents/country-identifier-iso3166-1-alpha-2-en.csv`

Current fields:

- `Name`
- `Code`

The current semantic mapping deliberately uses the logical key `Code`, not the physical row number.

### 4.3 RDF Layer

`nid.rdf` currently contains one modeled individual for each country present in the CSV source.

Representative example:

- `#BR`

This resource is intentionally modeled as both:

- `schema:Country`
- `ls:Directed1toNLink`

This means the same stable IRI acts as:

- the semantic country node
- the mini-container that carries the outbound mapping to other resources

The current `nid.rdf` also types this resource as:

- `prov:Entity`

This is conceptually coherent with the idea that the country node is a managed data entity inside the dataset.

### 4.4 Mapping Layer

The mapping is encoded inside `nid.rdf` using the Linkset vocabulary.

For `#BR`, the graph contains:

- one anonymous `ls:LinkElement` on the RDF side
- one anonymous `ls:LinkElement` on the CSV side
- one anonymous `ls:URIBasedIdentifier` for the RDF-side reference
- one anonymous `ls:StringBasedIdentifier` for the CSV-side reference

The CSV-side identifier currently uses:

- `ls:identifierField = "Code"`
- `ls:identifier = "BR"`

This is the current core design decision: the graph points to the source record through the logical key field, without duplicating `Name` or `Code` inside the semantic node.

## 5. Why It Was Modeled This Way

### 5.1 Keep Package Metadata Separate From Domain Data

`index.rdf` exists to describe:

- what the dataset package is
- which documents belong to it
- who publishes it
- where it came from

It does not need to carry country-level semantic mapping.

### 5.2 Keep Source Data In The Source File

The CSV is the source of truth for tabular values.

That is why the current `nid.rdf` does **not** duplicate:

- `schema:name`
- `schema:identifier`
- CSV field/value pairs such as `Code = BR`

Instead, it links back to the CSV using a logical field/value identifier.

### 5.3 Use The Country Node As The Stable Anchor

The current design intentionally uses the country resource itself as the stable reference:

- `#BR a schema:Country`
- `#BR a ls:Directed1toNLink`

This avoids scattering the model across extra named helper nodes such as `#BR-map`, `#BR-rdf`, or `#BR-csv`.

### 5.4 Prefer Logical Matching Over Physical Row Addressing

The current model uses:

- `identifierField = Code`
- `identifier = BR`

instead of:

- row `32`

This is preferable because row numbers are fragile under sorting, filtering, insertion, and regeneration. The `Code` column is the intended stable semantic key.

## 6. Advantages

- **Lower redundancy**: semantic RDF does not repeat data that already exists in the CSV.
- **Clear anchoring**: one IRI per country can act as both domain node and mapping anchor.
- **Better resilience**: logical identification by `Code` survives tabular reordering.
- **Cleaner layering**: container metadata, source data, semantic graph, and schema remain distinct.
- **Incremental growth**: the same pattern can be repeated for every country later.

## 7. Trade-Offs

- **Heavier semantics per node**: the same resource is both `schema:Country` and `ls:Directed1toNLink`, which is concise but conceptually denser.
- **Linkset verbosity**: even the minimal Linkset pattern still requires `LinkElement` and identifier structures.
- **Identifier indirection**: the CSV link still depends on a field/value indirection instead of carrying a direct row address.
- **Mixed concerns in one RDF file**: `nid.rdf` currently carries both the country node and the cross-document mapping.
- **Application-profile choices**: some modeling decisions intentionally generalize ISO 21597 beyond its narrower document-container usage into a broader dataset profile.

## 8. Current `datapackage.json` Role

The Frictionless descriptor currently declares:

- one table resource
- relative path to the CSV file
- `text/csv` media type
- `utf-8` encoding
- field schema:
  - `Name: string`
  - `Code: string`

The current descriptor also adds semantic typing at field level:

- `Name -> rdfType = http://schema.org/name`
- `Code -> rdfType = http://schema.org/identifier`

Its role is currently schema-oriented, not link-oriented.

In the current state of the model, `nid.rdf` does **not** directly point to `datapackage.json`.

An additional improvement worth keeping in scope is explicit language metadata for textual columns, especially the `Name` field, since the current file is effectively an English country label table.

## 9. Normative Alignment

### 9.1 ISO 21597 Container

The package is structurally aligned with the Container vocabulary because `index.rdf` uses:

- `ct:ContainerDescription`
- `ct:InternalDocument`
- `ct:containsDocument`
- container-oriented document metadata such as filename, type, format, and version

Compliance level:

- **Partial but meaningful alignment**

Reason:

- the vocabulary is used consistently for package description
- the result is a project-specific profile that expands the container idea toward a broader dataset packaging use

### 9.2 ISO 21597 Linkset

The current mapping in `nid.rdf` uses:

- `ls:Directed1toNLink`
- `ls:LinkElement`
- `ls:hasFromLinkElement`
- `ls:hasToLinkElement`
- `ls:hasDocument`
- `ls:hasIdentifier`
- `ls:URIBasedIdentifier`
- `ls:StringBasedIdentifier`

Compliance level:

- **Partial and structurally aligned**

Reason:

- the current graph respects the basic modeling intent of document-to-element linking
- the CSV side now uses the vocabulary in a simpler and more normative way through field/value identification
- the current profile also pushes the linkset idea toward a generalized dataset entity model, where a semantic resource can simultaneously act as the stable anchor of a mini-container

### 9.3 Frictionless Data Package

`datapackage.json` is practically aligned with Frictionless because it declares:

- resource path
- format
- media type
- encoding
- field schema
- field-level `rdfType` annotations

Compliance level:

- **Good practical alignment**

Reason:

- the descriptor is minimal but useful
- it currently serves as schema metadata for the CSV rather than a full publication workflow
- it is also being used as a bridge between tabular structure and semantic interpretation

### 9.4 Schema.org

The RDF graph currently aligns with Schema.org in a minimal way through:

- `schema:Country`

Compliance level:

- **Minimal but valid alignment**

Reason:

- the class use is appropriate
- the current graph intentionally avoids duplicating descriptive properties that already live in the CSV

### 9.5 Provenance And Distribution

The package also uses:

- `prov:wasDerivedFrom`
- `prov:generatedAtTime`
- `dcat:downloadURL`

This improves traceability of the package as a whole.

## 10. Current Gaps

- `nid.rdf` is now populated for all countries in the current CSV source, but the pattern still depends on the stability of that source table.
- `nid.rdf` still contains OWL-generated declaration noise that could be reduced later.
- The mapping currently assumes that `Code` is the stable key of the CSV resource.
- `datapackage.json` is present as schema metadata, but is not yet explicitly integrated into the RDF mapping.
- `datapackage.json` semantically types the fields with `rdfType`, but explicit language metadata for textual columns is still missing.

## 11. Recommended Next Steps

- Decide whether the OWL-generated declarations in `nid.rdf` should be kept or simplified.
- Decide whether the long-term design keeps domain data and link mappings in the same RDF file.
- Add explicit language metadata for the relevant textual fields in `datapackage.json`, especially the `Name` column.

## 12. Summary

The current result under `docs/ontology/social/ds/country` is a layered dataset package composed of:

- a container metadata graph in `index.rdf`
- a source CSV document
- a Frictionless schema descriptor
- an RDF graph in `nid.rdf` populated for all countries currently present in the source CSV

The key current modeling choice is this:

- the country node itself is the stable semantic anchor
- the CSV remains the source of truth for tabular values
- the semantic mapping points back to the CSV logically through `identifierField = Code` and `identifier = BR`

Holistically, the package is meant to work as a dataset made of living documents in easy-to-handle formats, each one contributing a different but coordinated perspective over the same entity:

- the container perspective
- the semantic perspective
- the raw/tabular perspective
- the schema perspective

This produces a result that is:

- compact
- traceable
- low in redundancy
- standards-aligned at the vocabulary level

but still intentionally lightweight and project-specific.

More specifically, it can be understood as a generalization of ISO 21597 from a document-container pattern to a broader dataset pattern, where multiple coordinated documents describe a full entity without forcing all meanings into a single serialization.

## Reference
`Linkset.rdf` defines the ontology used to represent links between documents and between elements within those documents.

### Classes

- `ls:Link`: base link class; groups two or more `ls:LinkElement` instances.
- `ls:BinaryLink`: specialization of `ls:Link` with exactly 2 linked elements.
- `ls:DirectedLink`: link with semantic direction, separating source and target.
- `ls:DirectedBinaryLink`: directed link with exactly 1 source and 1 target.
- `ls:Directed1toNLink`: directed link with 1 source and multiple targets.
- `ls:LinkElement`: represents the "point" that participates in the link, usually pointing to a document and, optionally, to an internal identifier.
- `ls:Identifier`: abstract class for the mechanism used to identify an element within a document.
- `ls:StringBasedIdentifier`: string-based identifier.
- `ls:QueryBasedIdentifier`: identifier obtained through a query expression.
- `ls:URIBasedIdentifier`: URI-based identifier.
### Object Properties

- `ls:hasLinkElement`: links a `Link` to its `LinkElement` instances.
- `ls:hasFromLinkElement`: subproperty of `hasLinkElement` used to indicate source.
- `ls:hasToLinkElement`: subproperty of `hasLinkElement` used to indicate target.
- `ls:hasDocument`: links a `LinkElement` to a `ct:Document` from the Container ontology.
- `ls:hasIdentifier`: links a `LinkElement` to an `Identifier`.
### Datatype Properties

- `ls:identifier`: textual value of the identifier in `StringBasedIdentifier`.
- `ls:identifierField`: name of the field where this identifier should be looked up.
- `ls:queryLanguage`: language used by `QueryBasedIdentifier`.
- `ls:queryExpression`: query expression.
- `ls:uri`: URI used in `URIBasedIdentifier`.
