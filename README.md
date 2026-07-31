# CAID site (Jekyll · Just the Docs)

Same shape as The Autonomous Stack: a standalone GitHub-Pages repo. Markdown
pages themed by Just the Docs (nav + search), one standalone interactive page
for the report cards, and a GitHub Action that regenerates the report-card data
from the cross-tab and commits it — the analogue of TAS's `generate-catalog.yml`.

## Layout

```
_config.yml                         remote_theme just-the-docs, search on
index.md                            Home (layout: home)
docs/standard.md                    The Assessment Standard
docs/findings.md                    Findings, uncertainty, limitations
report-cards.html                   standalone interactive: 35-model chart
data/v1_3_crosstab_v1_6_final.csv   the site's data input (canonical cross-tab)
data.json                           derived dataset (embedded in report-cards.html)
build.py                            regenerates data.json + reinjects into report-cards.html
.github/workflows/                  auto-regenerate + CI gate
```

This is a **standalone repo**, like TAS. Its data input — the cross-tab — lives
in the repo (in `data/`), the same way TAS keeps its catalog markdown in-repo.
That co-location is what makes the auto-update trigger possible: a push that
changes the cross-tab regenerates the derived report cards.

## Deploy (GitHub Pages)

No Gemfile needed; GitHub Pages builds Jekyll with the remote theme. Push to
`main`, then Settings -> Pages -> Source: `main` / `/` (root). The theme, nav and
search come from `remote_theme`. `build.py`, `data/`, `.github/` and this README
are excluded from the built site via `_config.yml`.

## Automatic update (the workflow)

`.github/workflows/generate-report-cards.yml` runs on any push that changes
`data/v1_3_crosstab_v1_6_final.csv` (or `build.py`), and on manual dispatch. It:

1. runs `python3 build.py`, which rewrites `data.json` and reinjects it into
   `report-cards.html`;
2. **aborts (non-zero exit) if the medians no longer reproduce REPORT_v1.3**
   (+53.3 all / +52.2 n>=20) — so a cross-tab that drifted from the report
   **fails the job and is never shipped**, rather than silently publishing wrong
   headline numbers;
3. commits the refreshed `report-cards.html` + `data.json` with `[skip ci]`.

The GitHub Pages Jekyll build is separate and already automatic on every push —
the workflow only keeps the report-card data in sync with the cross-tab.

### To publish new results

Drop the new `v1_3_crosstab_v1_6_final.csv` into `data/` and push. The workflow
regenerates the report cards, or fails loudly if the numbers no longer match the
report. If the corpus legitimately changed, update `EXPECT_MEDIAN_*` in
`build.py` and the report first. The two closed-model fields (disclosed rate,
rank) are not in the cross-tab; they live in the `ENRICH` dict in `build.py`.

The prose pages (`docs/*.md`) are edited by hand.

## Notes

- **Explorer** (raw responses + verdicts) is a placeholder, held until the
  public/private battery split is designated (Goodhart / defeat-device).
- **Per-model catalog** — a themed page per model in the TAS catalog style,
  generated from the cross-tab — is the natural next expansion; not built yet.
- **No composite score**; report cards are norm-referenced to the open-model
  composite. **Open core only** — operator assets are not part of this site.
- If you would rather keep the cross-tab single-sourced in `caid-benchmark`
  instead of a copy here, the workflow can be switched to fetch it cross-repo on
  dispatch/schedule — a few more moving parts than the in-repo trigger above.
