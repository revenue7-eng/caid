---
title: "Home"
layout: home
nav_order: 1
---

# CAID - Compliance Alignment Integrity Diagnostic

**A dual-condition behavioural test for one specific question - how much of an AI assistant's compliance drift is induced by the system prompt it was deployed with.**

Not accuracy, not safety in general - *undisclosed recommendation on an action the assistant should decline*. A reproducible measurement, aligned with FTC, FINRA, SEC and HIPAA disclosure standards, not an expert opinion.

CAID runs an identical battery under two conditions - a vendor system prompt, and none - and reports the **gap** between them. Across 35 models the gap is universal and large.

**→ [How it works](docs/how-it-works.html)** - the whole thing from zero, for someone who has never written a system prompt.

**→ [Report Cards](docs/evidence.html)** - the vendor effect for all 35 models, as evidence you can read.

**→ [The Assessment Standard](docs/standard.html)** - the method, and what counts as a violation.

---

## What you get

CAID gives three things: a **standard** for testing any deployed assistant, **evidence** on models measured so far, and the **protocol** to reproduce or cite it independently.

### This is new to me

Start with [How it works](docs/how-it-works.html). It explains what a system prompt is, why the same model behaves differently under different ones, and why the effect can only be measured before a product goes live. No prior knowledge assumed.

### I need to test a deployment

Read the [Assessment Standard](docs/standard.html). A run may claim it "follows the CAID protocol" only if it meets every requirement: dual-condition, two-pass classification, a validated judge, per-pressure reporting.

Then [Run it yourself](docs/run-it-yourself.html) - the commands, what lands on disk, how to read the output, and a conformance checklist you can walk down.

### I want the measured results

Open the [Report Cards](docs/evidence.html). Each model shows its clean baseline, its behaviour under a vendor prompt, and the gap - with sample size and a judge-stability figure. No composite score.

### I want to know what it means

Read the [Findings](docs/findings.html). Four results, including the one that matters most: a clean baseline and a large vendor effect can coexist - measuring only one misreads the model.

---

## Core principle

*A vendor system prompt is not a marginal nudge. For most models it flips undisclosed recommendation from rare to routine.*

A large vendor effect is not an accusation against a model. It is a measurement of what a deployed configuration does.

---

## Can you break the model?

Every CAID number should be reproducible: same battery, same judge, same result. The judge is validated against two independent human raters, measure by measure (κ = 0.881 and 0.851 on whether the answer acknowledged its commercial role, the call that decides a violation), and its run-to-run stability is measured directly (κ = 0.922 on the stratum most prone to drift). The canonical cross-tab and judged corpus are published in the [repository](https://github.com/revenue7-eng/caid-benchmark).

---

## License

- **Code**: [MIT](https://github.com/revenue7-eng/caid-benchmark/blob/main/LICENSE)
- Open core only. Operator tooling (private battery, distilled judge, runtime gate) is kept separate and is not part of this repository.
