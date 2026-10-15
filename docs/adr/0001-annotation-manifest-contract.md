# ADR 0001: Make the specification manifest the public contract

- **Status:** Proposed; no API, schema, generator, or runtime adapter implemented.
- **Date:** 2026-10-15
- **Authority:** [DTSpect specification](../../DTSpect.md)

## Context

DTSpect has moved from BPMN modelling with DTS testing toward contract-aware,
code-first workflow engineering. The manifest is a product in its own right:
the shared, machine-readable description of workflow identities, semantic
mappings, model associations, and version correspondence. It should support
independent tools in the same architectural role an OpenAPI document serves,
without claiming OpenAPI format compatibility.

Code, business steps, and diagram elements have different identities. A
reusable activity can appear in several orchestrations or several positions
in one process, and can execute repeatedly. Static annotations can describe
intent and discoverable relationships, but cannot establish every possible
runtime path. A build that validates mappings has not proven conformance.

## Proposed decision

Use explicit annotations and Roslyn discovery to generate a public,
versioned **DTSpect specification manifest**. Treat it as the shared contract
for mapping validators, future modellers, test runners, conformance evaluators,
and third-party tooling. Keep runtime evidence separate and reference the
exact contract/model bundle from that evidence.

This ADR proposes boundaries and invariants. Every API spelling and technical
mechanism remains a design hypothesis until a working slice validates it.

### 1. Annotations and stable identities

`[DtspectOrchestration]` would associate an implementation with a stable
orchestration identity, semantic process ID, and one or more BPMN projections.
`[DtspectStep]` would associate activity implementations with stable business
step IDs. These complement native DTS attributes/registration and do not
change how DTS executes the workflow.

Proposed identity rules:

- Process and orchestration IDs are explicit, namespaced strings with defined
  uniqueness within a manifest bundle; exact syntax is still open.
- Semantic step IDs are scoped to a process. Diagram labels and C# names are
  locators or presentation, never silently substituted for semantic IDs.
- A rename/refactor preserves an ID if business meaning is unchanged. A
  materially different meaning requires an explicit identity/version decision.
- BPMN element IDs are scoped by model fingerprint and process ID. Two model
  projections can map one semantic step to different model elements.
- An activity definition, a semantic use/call site, and an invocation/attempt
  are separate concepts. Mapping one activity to multiple business roles
  requires an explicit contextual binding; discovery must not choose arbitrarily.
- Repeating the same semantic step in a loop creates new runtime occurrences,
  not new static step IDs. Distinct business roles need distinct semantic IDs
  even when they reuse the same activity implementation.

Illustrative C# only: these attributes do not exist, the class bodies omit
native DTS declarations, and this is not a compilable or runnable sample.
Attribute targets and signatures remain open.

```csharp
[DtspectOrchestration("document-processing",
    ProcessId = "documents.intake",
    Models = new[] { "models/document-processing.bpmn" })]
class DocumentProcessing { /* native DTS implementation omitted */ }

[DtspectStep("documents.validate")]
class ValidateDocument { /* native DTS activity implementation omitted */ }
```

Discovery can inventory the reusable activity above. Membership in a specific
process and mapping to a specific BPMN element still require an unambiguous
relationship or explicit binding. Attributes cannot be placed on arbitrary C#
invocation expressions; a call-site wrapper, generated API, or binding file
needs a separate design and replay-safety validation.

### 2. Discovery, export, and consumer contract

Propose Roslyn analysis of symbols and annotations. Evaluate incremental source
generation where it helps, but do not assume a source generator should write
arbitrary files during compilation. Compare a build task, a command-line export,
and generated metadata with a deterministic export step before selecting one.

The manifest should contain stable identities, implementation locators,
semantic bindings and their provenance, BPMN associations, version references,
diagnostics, and tool provenance. Explicit, uniquely discovered, and suggested
bindings must be distinguishable. Ambiguous candidates must remain unresolved.

The following is a **shape sketch**, not a schema or valid generated artifact.
Paths and symbols are hypothetical; angle-bracket values are placeholders.
`draft-0` reserves no released format or compatibility promise.

```json
{
  "formatVersion": "draft-0",
  "generator": { "name": "DTSpect", "version": "<tool-version>" },
  "implementation": {
    "orchestrationVersion": "<runtime-version>",
    "buildFingerprint": "<immutable-build-fingerprint>"
  },
  "orchestrations": [
    {
      "id": "document-processing",
      "processId": "documents.intake",
      "symbol": "Example.DocumentProcessing",
      "models": [
        {
          "path": "models/document-processing.bpmn",
          "bpmnProcessId": "DocumentProcess",
          "fingerprint": "<model-fingerprint>"
        }
      ],
      "steps": [
        {
          "id": "documents.validate",
          "activitySymbol": "Example.ValidateDocument",
          "bindings": [
            {
              "modelPath": "models/document-processing.bpmn",
              "bpmnProcessId": "DocumentProcess",
              "elementId": "Task_Validate",
              "provenance": "explicit"
            }
          ]
        }
      ]
    }
  ],
  "validation": { "policy": "validate", "diagnostics": [] },
  "manifestFingerprint": "<generated-contract-fingerprint>"
}
```

A future published schema needs compatibility rules, fixtures, and a consumer
that reads it without loading application code. Generation should be
reproducible, with stable ordering and normalized repository-relative paths;
exclude machine paths, timestamps, and secrets from the canonical contract.
Define canonicalization and hash inputs explicitly, excluding the fingerprint
field itself to avoid circular hashing. Algorithm and artifact packaging remain
open. Source locators should not accidentally make unrelated machine-specific
changes alter semantic identity.

Keep the manifest format version, runtime orchestration version, immutable
build reference, BPMN fingerprint, and manifest fingerprint separate. A human
model version can aid navigation but does not replace content correspondence.
Retain the bundle used for an execution. A missing bundle or mismatch must not
fall back silently to the current model or receive an unqualified pass.

### 3. Mapping discovery and progressive policies

| Condition | Proposed diagnostic behaviour |
| --- | --- |
| Missing | Identify an unresolved declared model/element/implementation reference; separately report unbound implementation elements. |
| Ambiguous | Show candidate relationships and require disambiguation before treating the binding as authoritative. |
| Duplicated | Detect conflicting identities within their defined scope; legitimate reuse across projections is not a duplicate error. |
| Stale | Detect renamed/removed targets or model/build fingerprints that no longer correspond. |
| Inconsistent | Detect conflicting process association, model element kind, semantic identity, or explicit bindings. |

Start with an inventory-oriented **discover** policy, progress to **validate**
for declared bindings, and allow **strict** coverage within an explicitly
selected process scope. Strict policy must support documented exclusions for
technical helpers. Invalid or ambiguous references remain visible under every
policy; changing severity cannot make them trusted bindings. An exploratory
export can contain diagnostics, but consumers must reject unresolved bindings
needed for a conformance claim. Policy vocabulary and severity levels are open.

Model element existence, uniqueness, reference integrity, supported element
kinds, and version correspondence are build-time checks. They cannot prove
that a branch executes, that a technical helper is a business violation, or
that all valid runtime paths have been modelled. Unsupported BPMN constructs
require an explicit diagnostic, not an invented interpretation.

### 4. Runtime evidence and conformance

Investigate native history, tags, and OpenTelemetry. Validate each source's
availability, completeness, correlation fields, permissions, and retention
against the selected SDK/host. No history endpoint, tag propagation behaviour,
or telemetry interceptor is assumed available.

Proposed normalized evidence should carry the manifest/model/build references,
source provenance and completeness, task-hub/environment scope, orchestration
instance and execution-generation identity, semantic step identity when known,
invocation identity, retry attempt, event identity/type, and causal relationships.
Unknown fields must be explicit. Do not synthesize causality from timestamps.

- Replay must not double-count recorded business events or introduce
  nondeterministic side effects into orchestration execution.
- Repeated invocations and retries must be separable from duplicate delivery
  or replay of the same event. Deduplication requires a tested stable event key.
- Concurrent branches require partial-order semantics; a timestamp-sorted list
  alone cannot prove their ordering or conformance.
- Waiting/running, failed, and completed observations need distinct handling.
  Missing evidence or unsupported semantics can make a result inconclusive.
- A pass is scoped to evaluated assertions and observed behaviour. A violation
  needs affirmative evidence under supported semantics; absence in an
  incomplete trace does not prove that an activity never ran.

Default evidence should contain metadata rather than payloads. Review even
instance IDs/tags for sensitive data. Decide redaction, retention, and explicit
opt-in capture before introducing collection. A visual overlay must display
uncertainty and version provenance rather than imply complete coverage.

### 5. BPMN and BDD consumers

A future modeller consumes the manifest as discovery metadata, then allows
explicit business bindings. Decide where those bindings live and how edits
survive regeneration; generated output should not become an untracked second
source of truth. BPMN describes permitted behaviour; DTS executes code.

A Gherkin/Reqnroll-inspired harness should execute real orchestration logic
with controlled dependencies, assert scenario expectations, and feed versioned
evidence into conformance evaluation. Hosting and mocking seams must be
validated. First implement a small declared BPMN subset and a simple report;
do not start with a full editor or infer complete control flow from annotations.

## Consequences and alternatives

- A public contract lets tools evolve independently but creates a real schema
  compatibility and version-retention responsibility.
- Discovery reduces manual mapping work but cannot eliminate explicit business
  intent, ambiguity, or incomplete runtime evidence.
- Stable explicit IDs survive refactoring but need governance and migration
  rules; IDs derived only from code names were rejected as the default.
- A BPMN-first editor would delay validation of the central contract. Defer it.
- Trace-only diagram generation cannot specify unobserved permitted behaviour.
- A completely manual mapping catalogue misses useful discovery; entirely
  inferred mappings can misrepresent reused activities. Propose a hybrid.

## Open decisions and validation work

1. Which .NET SDK/host and native attribute targets form the first supported slice?
2. How are step scope, multiple semantic roles, call-site identity, and external
   activities represented without changing runtime behaviour?
3. Which Roslyn/generation/export mechanism produces a deterministic artifact?
4. What are the public schema, ID grammar, fingerprint algorithm, canonical form,
   compatibility policy, and bundle storage/migration rules?
5. Where do explicit BPMN bindings live, and how are modeller edits reconciled?
6. Which diagnostics and policy defaults are actionable without excessive noise?
7. Which BPMN subset and causal semantics can the first evaluator prove correctly?
8. Which native evidence sources expose sufficient correlation across replay,
   retries, concurrency, sub-orchestrations, and execution generations?
9. Which BDD runner/host and dependency-control seams execute real logic reliably?
10. What data collection, access, redaction, and retention controls are required?

Use the [roadmap gates](../ROADMAP.md) to resolve these with working examples
and negative cases. This ADR remains proposed until reviewed; implementation
claims require independent evidence beyond accepting the design.

## Technical background

Microsoft documents durable orchestration identity, history/replay, and
parallel workflow patterns in the [durable orchestrations overview](https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-orchestrations).
The [DTS overview](https://learn.microsoft.com/en-us/azure/durable-task/scheduler/durable-task-scheduler)
describes the runtime service. These inform questions to test; they do not
establish that a DTSpect evidence adapter or generator exists.
