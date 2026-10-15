# DTSpect specification

**Model it. Specify it. Prove it.**

**Status: proposed product specification, revised 15 October 2026.**
This is the authoritative specification for this repository. It incorporates
the updated architectural direction and supersedes the original BPMN-first
project brief. It describes intended behaviour, not delivered software.
All APIs and technical mechanisms remain hypotheses until implemented and
validated. Architectural proposals belong in ADRs; acceptance does not imply
implementation.

## Vision and positioning

DTSpect is a proposed open-source, code-first workflow specification,
behaviour-driven testing, and process-conformance framework specifically for
Microsoft Durable Task Scheduler (DTS).

**Swagger/OpenAPI meets SpecFlow/Reqnroll and BPMN, built for durable
orchestrations.** The comparison describes the intended developer experience;
it does not imply OpenAPI compatibility or a dependency on SpecFlow.

The architectural centre is **contract-aware, code-first workflow engineering**.
The **DTSpect specification manifest** is an explicit product concept: a
versioned, machine-readable contract that independent tools, including the
BPMN modeller, test runner, and conformance evaluator, could consume. It is
not merely an internal generator output or a substitute for execution history.

## Principles

- DTS and application code execute workflows. DTSpect does not introduce a
  second orchestration engine or generate executable workflows from BPMN.
- Specifications describe permitted behaviour; observations describe what
  happened in a particular execution. Neither replaces the other.
- Discover relationships where possible, preserve explicit intent, and expose
  ambiguity rather than silently guessing mappings.
- Keep stable business identities separate from code names, diagram labels,
  runtime instance identifiers, and version fingerprints.
- Build-time validation checks mapping integrity. Runtime evidence and
  scenario assertions are needed to assess observed behaviour.
- Retain model, implementation, and manifest correspondence across versions.
- Prefer identifiers and metadata to business payloads in evidence and reports.

## 1. Attribute-driven specifications

Proposed C# attributes complement native DTS attributes and registration:

- `[DtspectOrchestration]` identifies an orchestration, its semantic process
  identity, and associated BPMN models. One orchestration may have multiple
  model projections at different levels of business detail.
- `[DtspectStep]` associates a DTS activity with a stable business-process
  identifier. Activity reuse requires additional context: an activity
  definition, a semantic use within a process, and a runtime invocation are
  distinct identities.

Identifiers should survive implementation renames and diagram layout changes.
The exact attribute targets, constructor signatures, multiple-use semantics,
and call-site binding mechanism are open decisions. Attributes alone must not
be assumed to reconstruct complete orchestration control flow.

## 2. Discovery and the specification manifest

Roslyn-based build-time discovery is the proposed approach, potentially using
incremental source generation alongside analyzers. The export mechanism must
be validated rather than assumed to be a supported generator side effect.

The manifest should represent:

- A manifest format version and generator/tool provenance.
- Orchestration identities, semantic process IDs, and implementation locators.
- Semantic step-to-implementation mappings, their scope and provenance, and
  unresolved or ambiguous relationships.
- BPMN model associations, process/element identities, and model fingerprints.
- Implementation/orchestration versions and immutable build correspondence.
- A generated specification-manifest fingerprint and validation diagnostics.

It should be independently consumable without executing the target workflow
or requiring the modeller. Reproducible serialization, fingerprint rules,
schema publication, compatibility, and consumer negotiation need a design
and fixtures before a stable contract is promised. No formal manifest schema
is published in this foundation.

## 3. Mapping detection and validation

Discovery and validation should detect missing, ambiguous, duplicated, stale,
or inconsistent mappings across annotations, implementation, manifest, and
BPMN. Discovery should distinguish explicit bindings, uniquely resolved
relationships, and suggestions requiring confirmation.

Progressively stricter policies should support adoption:

| Proposed policy | Intended behaviour |
| --- | --- |
| Discover | Inventory implementation and mappings; expose gaps and uncertainty. |
| Validate | Fail invalid or conflicting declared bindings; report unbound implementation elements. |
| Strict | Require mapping coverage within an explicitly selected business-process scope, with documented exclusions. |

An unmapped implementation detail is not automatically a conformance
violation. Unresolved identities must never be presented as proven bindings,
even if a policy permits export. Policy names and exact diagnostic severity
rules are provisional. Missing/stale models and incompatible versions must
remain visible to consumers.

## 4. BPMN as a living specification

BPMN 2.0 describes permitted business-process behaviour. A future modeller
should consume the manifest, present discovered metadata, and support explicit
binding to implementation elements. Binding edits must have a defined source
of truth and regeneration path; hand-editing generated output is not a settled
workflow.

The initial supported BPMN subset must be explicit. Gateways, loops, timers,
exceptions, and parallel branches need defined conformance semantics before
support is claimed. Unsupported constructs must yield a diagnostic or an
inconclusive result, not silent success. A trace is not a complete model of
all possible paths.

## 5. Behaviour-driven testing

Gherkin scenarios and Reqnroll-inspired .NET bindings should express
acceptance criteria. The intended harness executes real orchestration logic
against controlled dependencies, records observable behaviour, and evaluates
both scenario expectations and BPMN constraints.

The hosting approach, SDK version, dependency-control seams, test runner, and
Reqnroll integration remain open. Passing a test would support only the
assertions and observed paths exercised, not prove all possible executions.

## 6. Runtime observability and conformance

Investigate native DTS execution history, tags, and OpenTelemetry as evidence
sources. Their completeness, access, correlation, and version support must be
tested. No particular history API or instrumentation hook is promised.

Evidence should distinguish orchestration instances and execution generations,
semantic steps, repeated activity invocations, retry attempts, and causal
relationships. Replay must not create false business executions. Concurrent
events must not be reduced to an arbitrary timestamp order.

Instance overlays should eventually show observed branches, failures, waits,
and retries where instrumentation permits. Incomplete evidence, an active
wait, an unsupported construct, and an observed violation need distinct
interpretation. Inconclusive results must be possible; absence from a partial
trace cannot establish that a step never ran.

Default evidence should exclude business inputs, outputs, secrets, and
sensitive identifiers. Collection, redaction, retention, and export controls
need design before runtime collection is introduced.

## 7. Version correspondence

Keep these concepts separate:

| Identity/version | Purpose |
| --- | --- |
| Semantic process/step ID | Stable business meaning across compatible refactors. |
| DTS implementation/orchestration version | Runtime implementation identity; also record an immutable build reference. |
| BPMN model version/fingerprint | Exact specification associated with an implementation. |
| Manifest format version | Interpretation and compatibility of the machine-readable contract. |
| Specification-manifest fingerprint | Exact generated contract used by a consumer or execution. |

An execution must be evaluated against its associated contract/model bundle,
not automatically against the latest files. Unknown, missing, or mismatched
versions must be diagnosed and prevent an unqualified conformance pass.
Fingerprint canonicalization and migration rules remain open.

## 8. MVP and sequencing

**Decorated DTS orchestration → Generated manifest → BPMN binding validation
→ BDD test execution → Conformance result → Visual evidence**

Prioritize annotations, discovery, the public manifest contract, and mapping
validation before a full visual modeller. The first slice should demonstrate
one small orchestration, one explicitly supported BPMN model, and controlled
BDD scenarios with positive and negative evidence. A simple report can precede
an interactive editor.

See the [roadmap](docs/ROADMAP.md) for evidence-based milestone gates and the
[first ADR](docs/adr/0001-annotation-manifest-contract.md) for the proposed
contract architecture and open decisions.

## Current implementation status

This repository contains specifications, contribution guidance, and documentation
checks only. There is no DTSpect attribute library, Roslyn analyzer/generator,
formal manifest schema, DTS adapter, BDD harness, conformance engine, package,
or BPMN UI yet. Candidate technologies do not constitute supported integrations.
