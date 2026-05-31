# UC 001: Task Prioritization with OntoBDC

## Status

Proposed

## Objective

Allow a user to use OntoBDC to analyze a set of tasks registered in a dataset and obtain a prioritization aligned with operational criteria, without manually handling queries, graphs, or internal rules.

## Context

Engineering, operations, product, research, and administrative teams often maintain task lists in spreadsheets, RDF files, local repositories, or datasets structured inside containers.

In practice, the challenge is not only listing tasks, but deciding:

- what should be done first
- what can wait
- what is blocked
- what brings the highest impact

OntoBDC acts as a capability layer over these data sources, allowing the user to interact through natural language or structured commands while the system resolves context, finds the correct dataset, queries the relevant data, and produces a decision-oriented response.

## Actors

- Analyst user
- Manager user
- OntoBDC CLI
- Task dataset
- Query and prioritization capability

## Trigger

The use case starts when the user wants to prioritize tasks from a dataset and invokes OntoBDC to obtain an ordering, classification, or focus recommendation.

## Preconditions

- the project is initialized with OntoBDC
- the storage component is enabled
- at least one registered container exists besides the root container
- a task dataset is available in the intended context
- the dataset contains enough information to distinguish priority, impact, deadline, dependency, blockage, or an equivalent criterion

## Postconditions

- the user receives a response with the task prioritization
- the response may indicate applied criteria, detected constraints, and blocked tasks
- the execution context may remain materialized for auditing, traceability, or later reuse

## Main Flow

1. The user tells OntoBDC that task prioritization is needed.
2. OntoBDC resolves the execution context, including language, objective, and target dataset.
3. The system identifies the relevant container and dataset for the query.
4. OntoBDC loads the task data from the selected dataset.
5. The system interprets explicit or implicit prioritization criteria.
6. OntoBDC evaluates relevant task attributes such as deadline, impact, urgency, dependencies, blockages, or category.
7. The system orders or classifies the tasks according to the applicable strategy.
8. OntoBDC returns a response with the prioritized list and a brief explanation of the ordering.

## Alternative Flows

### AF1: Dataset not explicitly provided

1. The user asks for prioritization without specifying the dataset.
2. OntoBDC attempts to infer the dataset from the current context.
3. If ambiguity remains, the system asks for clarification or requires a dataset identifier.

### AF2: Insufficient data for prioritization

1. OntoBDC finds the dataset, but the tasks do not contain enough attributes to calculate priority.
2. The system informs the user that prioritization cannot be performed with confidence.
3. The user may enrich the dataset or request only a simple listing.

### AF3: There are blocked or dependent tasks

1. The system detects highly important tasks that cannot be executed immediately.
2. OntoBDC highlights the blockage and adjusts the response to separate:
   - potential priority
   - currently executable priority

### AF4: The user provides a specific criterion

1. The user requests something like "prioritize by urgency", "prioritize by impact", or "prioritize what is due today".
2. OntoBDC restricts the analysis to the requested criterion.
3. The response makes clear which criterion was applied.

## Business Rules

- the prioritization must be explainable to the user
- blocked tasks must not be treated as immediately executable without qualification
- when the user provides an explicit criterion, it takes precedence over default heuristics
- in the absence of an explicit criterion, the system may apply a documented default strategy
- the selected dataset must be treated as the source of truth for the tasks considered in the response

## Involved Data

Task data may include, for example:

- task identifier
- title or description
- deadline
- status
- impact
- urgency
- dependency
- blockage
- responsible party
- category

## Expected Result

The user obtains a useful response for decision-making, for example:

- ordered task list
- grouping by priority level
- highlight of critical tasks
- signaling of blocked tasks
- brief justification of the recommendation

## Architecture Notes

- the use case depends on correct context and dataset resolution
- the dataset must be treated as a domain work entity rather than only as a physical folder
- the flow may be initiated by structured CLI, natural language text, or an internal capability execution pipeline
- the exact prioritization method may vary according to the implemented capability, as long as the response preserves explainability and traceability
