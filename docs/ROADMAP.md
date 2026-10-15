# DTSpect roadmap

All implementation milestones below are **planned**, not delivered or dated
commitments. The [specification](../DTSpect.md) is authoritative. Each milestone
should produce reviewable evidence before the next capability is claimed.

## Foundation: specification and collaboration

This initial contribution provides the specification, proposed
[ADR 0001](adr/0001-annotation-manifest-contract.md), community files, and docs CI.
Review the contract boundaries and open questions before accepting the ADR.
The maintainer should also establish a confidential conduct-reporting channel
before expanding community participation.

## 1. Annotation and manifest contract

- Select one .NET/DTS hosting model and compatible SDK for a discovery spike.
- Specify semantic ID scope, activity reuse, and attribute targets.
- Draft a public manifest schema with positive and negative fixtures,
  deterministic serialization, fingerprints, and format compatibility rules.
- Prototype Roslyn discovery and choose a reproducible artifact export path.

**Gate:** a decorated sample generates the same manifest for the same semantic
inputs; renames preserve explicit IDs; duplicate/ambiguous IDs are diagnosed;
an independent consumer can parse the artifact without loading application code.
Document exactly which APIs and SDK versions were validated.

## 2. BPMN bindings and progressive validation

- Select a small BPMN 2.0 subset, initially considering sequential tasks and
  exclusive branches; explicitly reject or mark other constructs unsupported.
- Resolve model/process/element references against the generated manifest.
- Implement discover, validate, and strict policy semantics with scoped exclusions.
- Choose how modeller-authored bindings are stored and merged during generation.

**Gate:** fixtures distinguish missing, ambiguous, duplicate, stale, and
inconsistent mappings; an unmapped technical helper is reported without being
misclassified as a runtime conformance failure. Changed model/build versions
cannot silently reuse an incompatible manifest.

## 3. BDD execution and evidence

- Choose the test host, runner, and Reqnroll integration through a working spike.
- Execute real orchestration logic with controlled activity dependencies.
- Investigate native execution history, tags, and OpenTelemetry availability.
- Prove correlation for repeated activities, retries, replay, and execution
  generations; record any unsupported cases explicitly.

**Gate:** positive and negative Gherkin scenarios produce assertions plus
version-associated, payload-minimized evidence. Missing or sampled evidence
is visible; replay does not double-count a business execution. No fabricated
trace is presented as an integration test against DTS.

## 4. Conformance and minimal visual evidence

- Evaluate the supported BPMN subset with causal ordering where required.
- Distinguish a violation from incomplete evidence, unsupported semantics,
  version mismatch, or an instance still waiting/running.
- Render a small model overlay/report with evidence provenance and limitations.

**Gate:** the full slice runs from decorated orchestration to manifest, binding
validation, BDD execution, conformance result, and visual evidence. Include a
valid route, an observed forbidden route, and an inconclusive case. A pass
claims only the behaviour actually checked, not full process-path coverage.

## 5. Modeller and wider semantics

Only after the contract and vertical slice are demonstrated, consider a full
interactive BPMN modeller consuming the same manifest. Expand concurrency,
timers, loops, failure semantics, coverage reporting, and instance inspection
through separate ADRs and executable fixtures. React/TypeScript and `bpmn-js`
remain candidates, not selected dependencies.
