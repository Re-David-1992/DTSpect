# Contributing to DTSpect

DTSpect is at the specification stage. Help refine the public manifest
contract, stable identifiers, mapping policies, and small validation experiments
before proposing a full BPMN editor. Read the [specification](DTSpect.md),
[ADR 0001](docs/adr/0001-annotation-manifest-contract.md), and
[roadmap](docs/ROADMAP.md) first.

## Discuss and scope a change

Use [GitHub issues](https://github.com/Re-David-1992/DTSpect/issues) for a concrete
problem, design question, or proposal. Small documentation fixes can go straight
to a pull request. For larger work, describe the use case, affected contract,
acceptance evidence, and unresolved decisions before adding dependencies.

Keep proposed APIs visibly marked as proposals. Do not advertise runnable
examples, supported integrations, or passing conformance tests that do not
exist. Update the authoritative specification when direction changes, then
align the README, ADRs, and roadmap. Record accepted architectural changes in
an ADR; distinguish design acceptance from implementation status.

## Make a pull request

1. Fork or clone the repository and create a feature branch from `main`.
2. Make a focused change. Preserve stable semantic IDs unless the change
   deliberately changes meaning and explains migration/version implications.
3. Run the documentation checks below and inspect the diff for credentials,
   local paths, sensitive payloads, and accidental generated artifacts.
4. Commit and open a PR against `main` with the problem, resulting behaviour,
   validation performed, and any remaining limitations. Link a related issue
   when one exists. Maintainers review before merging.

Use UTF-8, LF line endings, and the repository's `.editorconfig`. Keep examples
small, use synthetic data, and label conceptual snippets that cannot compile.

## Validate the current content

Prerequisites: Git and Python 3.11 or later. No third-party Python dependencies
or .NET/Node installation are required for this documentation foundation.
From the repository root:

```sh
python scripts/check_docs.py
git diff --check
```

The checker checks required foundation files, UTF-8/LF/final-newline hygiene,
trailing whitespace, relative inline Markdown file/directory links, and fenced
JSON syntax. It excludes the canonical license text from whitespace rules.
It does not check heading fragments, external URLs, reference-style links,
BPMN semantics, C# compilation, or a manifest schema. Review those manually
where applicable. GitHub Actions runs the same checker on PRs and pushes.

There is no application build or runtime test suite yet. When implementation
arrives, add reproducible tests for actual behaviour and document the SDK,
hosting prerequisites, and validated limits. Useful early cases include
duplicate IDs, ambiguous activity reuse, stale model fingerprints, incomplete
evidence, and replay-safe invocation correlation.

## Research references

Use current primary documentation and record the SDK/host version behind a
technical claim. The [Azure Skills project](https://github.com/microsoft/azure-skills)
provides Azure guidance for development agents, and the
[Microsoft Learn MCP guide](https://learn.microsoft.com/en-us/training/support/mcp-get-started)
describes agent access to official documentation. These are optional research
tools, not DTSpect runtime dependencies or evidence that a proposed integration
works. Consult the [DTS documentation](https://learn.microsoft.com/en-us/azure/durable-task/scheduler/durable-task-scheduler)
for platform facts and verify assumptions with a targeted experiment.

## License and conduct

Contributions intentionally submitted for inclusion are under the repository's
[Apache-2.0 license](LICENSE). Submit only work you have the right to contribute
and preserve required third-party attribution. This project does not currently
require a separate contributor license agreement.

Follow the [Code of Conduct](CODE_OF_CONDUCT.md). The initial maintainer is
[@Re-David-1992](https://github.com/Re-David-1992); no broader governance or
review-response service level is implied.
