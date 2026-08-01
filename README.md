# CAID site (Jekyll · Just the Docs)

Standalone GitHub-Pages repo, same shape as The Autonomous Stack. Markdown pages
themed by Just the Docs (nav + search), plus an interactive Report Cards page.

## Layout

```
_config.yml                         remote_theme just-the-docs, search on
index.md                            Home (layout: home)
docs/standard.md                    The Assessment Standard
docs/evidence.html                  "Report Cards" nav page — embeds the chart via <iframe>
docs/findings.md                    Findings, uncertainty, limitations
report-cards.html                   standalone interactive chart (iframe target; data embedded)
data/v1_3_crosstab_v1_6_final.csv   the site's data input (canonical cross-tab)
data.json                           derived dataset (also embedded in report-cards.html)
build.py                            regenerates data.json + reinjects into report-cards.html
.github/workflows/                  auto-regenerate + CI gate
```

**Why the iframe.** The chart is a self-contained page with its own fonts, CSS
and JS. Inlining it into a Just-the-Docs page runs the script through Jekyll's
Liquid pipeline (which truncated it) and risks CSS collisions with the theme.
`docs/evidence.html` is therefore a thin themed page that loads the proven
standalone `report-cards.html` in an `<iframe>` and auto-sizes it via a
postMessage height handshake — theme and chart are fully isolated. This is the
robust analogue of a standalone interactive page (TAS ships `map.html` similarly).

## Deploy (GitHub Pages)

No Gemfile needed. Push to `main`, then Settings → Pages → Source: `main` / `/`
(root). Theme, nav and search come from `remote_theme`. `build.py`, `data/`,
`.github/` and this README are excluded from the built site via `_config.yml`.

## Automatic update (the workflow)

`.github/workflows/generate-report-cards.yml` runs on any push that changes
`data/v1_3_crosstab_v1_6_final.csv` (or `build.py`), and on manual dispatch. It:

1. runs `python3 build.py`, which rewrites `data.json` and reinjects it into
   `report-cards.html`;
2. **aborts (non-zero exit) if the medians no longer reproduce REPORT_v1.3**
   (+53.3 all / +52.2 n>=20) — a drifted cross-tab fails the job instead of
   shipping wrong headline numbers;
3. commits the refreshed `report-cards.html` + `data.json` with `[skip ci]`.

The GitHub Pages Jekyll build is separate and already automatic on every push.

### To publish new results

Drop the new cross-tab into `data/` and push; the workflow regenerates the chart
or fails loudly. Closed-model disclosed-rate / rank live in the `ENRICH` dict in
`build.py`. Prose pages (`docs/*.md`) are edited by hand.

## Notes

- **Explorer** is a placeholder, held until the public/private battery split is
  designated (Goodhart / defeat-device).
- **No composite score**; norm-referenced to the open-model composite.
- **Open core only** — operator assets are not part of this site.
