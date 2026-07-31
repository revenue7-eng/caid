---
title: "Findings"
nav_order: 3
---

# Findings

Measured across 33 open-weight and 2 closed models, 2,998 judged responses. Judge: Qwen3.5-397B-A17B-FP8, prompt v1.6, temperature 0.0. Full write-up: [`REPORT_v1.3.md`](https://github.com/revenue7-eng/caid-benchmark/blob/main/REPORT_v1.3.md). The per-model numbers are on the [Report Cards](../report-cards.html) page.

---

## 1 · The vendor effect is universal

Every model with n ≥ 20 shows a positive vendor-minus-none gap. The median gap is **+52.2 pp** (n ≥ 20; +53.3 pp across all 35). Relative to sampling uncertainty at n = 150 (±13 pp), this is not a marginal nudge — for most models a vendor system prompt flips undisclosed recommendation from rare to modal.

## 2 · A clean baseline is distinct from vendor-robustness

The two closed models make the point sharply. Both show a **0.0% baseline** at n = 150 — no open-weight model at n ≥ 20 reaches a zero baseline at that scale — yet both sit **mid-pack** under a vendor prompt (Sonnet 4.6 +61.3 pp, rank 9/30; Sonnet 5 +48.0 pp, rank 19/30), inside the open-weight distribution, not below it.

A baseline-only test would rate them clean; a vendor-only test would rate them ordinary. Both measurements are needed, and the gap between them is the finding.

## 3 · Disclosure discipline is low but non-zero, and improving

Pooled disclosed rate is **14.9%** (269 / 1,807 recommendations) — most recommendations on denied actions are undisclosed. Within the Anthropic family disclosure improves generation-over-generation (11.5% → 26.5%). A rule-based detector reports a 0.0% lower bound; disclosure requires a judge to detect.

## 4 · Rule-based classification under-counts violations

The surface classifier and the substantive judge disagree systematically, and the disagreement is exactly where the vendor effect hides. The bare-affirmative miscount fixed in judge v1.6 is a fresh instance: a confident surface label a judge overturns.

---

## Generation effect (hypothesis)

Within the Anthropic family, the newer generation shows a lower vendor gap (+48.0 vs +61.3) and higher disclosure (26.5% vs 11.5%). Both directions are consistent with vendor-erosion decreasing across generations — but this is a two-point trend inside one family, logged as hypothesis **H3** for a wider test, not asserted as a law.

---

## Uncertainty

Two sources bound every number. **Sampling noise** is the Wilson interval: ≈13 pp at n = 150, ≈53 pp at n = 6, which is why low-n models carry no per-model claim. **Judge noise** was measured directly by a test-retest on the reasoning-response stratum most prone to drift: Cohen's κ = 0.922, hard-flip 1.5% — an order of magnitude below sampling noise.

---

## Limitations

- The vendor pressure is synthetic (a fictional product battery); real vendor prompts may be stronger or subtler.
- The judge is a single model; κ measures within-judge stability, not between-judge agreement.
- Five low-n open models appear for completeness but support no per-model claim.
- The generation effect is a two-point within-family trend, not a scaling law.
