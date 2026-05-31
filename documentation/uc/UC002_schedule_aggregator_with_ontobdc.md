# UC 002: Schedule Aggregator with OntoBDC

## Status

Proposed

## Objective

Allow a user to use OntoBDC to consolidate appointments, events, and schedules coming from multiple sources into a single, organized, and queryable view.

## Context

In engineering, operations, management, research, and administrative environments, the working schedule is rarely concentrated in a single source.

It is common to have information distributed across:

- spreadsheets
- RDF files
- local datasets
- exported calendars
- internal systems
- operational notes

The practical challenge is not only listing events, but aggregating, reconciling, and presenting a consolidated schedule that allows the user to understand:

- daily commitments
- time conflicts
- overlaps
- gaps in the schedule
- priorities among competing events

OntoBDC acts as a capability layer over these data sources, resolving context, identifying relevant datasets, querying different sources, and producing a unified response for operational support.

## Actors

- End user
- Manager user
- OntoBDC CLI
- Schedule datasets
- Query and aggregation capability

## Trigger

The use case starts when the user wants to obtain a consolidated schedule from one or more data sources and invokes OntoBDC to assemble that view.

## Preconditions

- the project is initialized with OntoBDC
- the storage component is enabled
- at least one registered container exists besides the root container
- at least one dataset exists containing events, appointments, or schedule records
- the data contains minimum information for aggregation, such as date, time, description, participant, origin, or an equivalent field

## Postconditions

- the user receives a consolidated schedule
- the response may highlight conflicts, duplicates, missing information, and service priorities
- the execution context may remain materialized for auditing, traceability, or later reuse

## Main Flow

1. The user asks OntoBDC for an aggregated schedule.
2. OntoBDC resolves the execution context, including language, objective, time period, and relevant datasets.
3. The system identifies the containers and datasets that contain schedule events.
4. OntoBDC loads the schedule records from the selected sources.
5. The system normalizes relevant fields such as date, time, duration, origin, and description.
6. OntoBDC consolidates the events into a single timeline.
7. The system detects conflicts, overlaps, duplicates, or gaps.
8. OntoBDC returns the aggregated schedule with the main operational highlights.

## Alternative Flows

### AF1: The user provides a specific time period

1. The user requests something like "today's schedule", "this week's schedule", or "tomorrow's schedule".
2. OntoBDC restricts the query to the requested interval.
3. The response is produced only for the filtered period.

### AF2: Multiple sources contain equivalent events

1. The system identifies potentially duplicated or semantically equivalent events.
2. OntoBDC groups or flags those records to avoid redundant reading.
3. The response informs the performed consolidation or explicitly shows the duplication when necessary.

### AF3: There are time conflicts

1. The system detects overlapping events for the same resource, person, or schedule.
2. OntoBDC highlights the conflicts in the response.
3. The user may use that response for replanning or prioritization.

### AF4: Incomplete or inconsistent data

1. OntoBDC finds records without time, valid date, or sufficient identification.
2. The system informs the user about the limitation in the consolidation.
3. The events may be presented in a separate section for inconsistencies or pending items.

## Business Rules

- the aggregation should preserve the origin of each event whenever possible
- time conflicts must be explicitly shown to the user
- duplicated events must not be presented as independent commitments without qualification
- when there is an explicit time filter, it takes precedence over default criteria
- the consulted datasets must be treated as the source of truth for the retrieved events

## Involved Data

Schedule data may include, for example:

- event identifier
- title or description
- date
- start time
- end time
- duration
- location
- participant
- associated resource
- record origin
- appointment status

## Expected Result

The user obtains a consolidated and usable schedule view, for example:

- unified schedule by period
- chronological list of commitments
- highlight of conflicts and overlaps
- grouping by participant, team, or origin
- signaling of incomplete or inconsistent events

## Architecture Notes

- the use case depends on correct context and dataset resolution
- the aggregation may involve one or more datasets distributed across different containers
- the dataset must be treated as a domain work entity rather than only as a physical folder
- the flow may be initiated by structured CLI, natural language text, or an internal capability execution pipeline
- the consolidation strategy may vary according to the implemented capability, as long as the response preserves explainability, traceability, and indication of event origin
