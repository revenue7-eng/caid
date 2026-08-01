#!/usr/bin/env python3
"""
Generate per-model report-card pages from the validated per-cell dataset.

Input : data/per_cell.json  (model -> role x pressure x condition violation rates,
        derived from the v1.6 judged corpus and validated to reproduce the
        cross-tab; see caid-benchmark).
Output: docs/models/index.md          (parent "Models" nav page)
        docs/models/<slug>.html        (one static heatmap page per model)

The pages are STATIC HTML (no JavaScript): a role x pressure violation heatmap
for the vendor and none conditions, shaded server-side. No script means no Liquid
/ theme-embedding hazard - they render natively inside Just the Docs.

This is an internal consistency gate too: it re-aggregates each model's cells and
aborts if they no longer match the stored model-level vendor/none rate.

Usage: python build_models.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "per_cell.json")
OUT  = os.path.join(HERE, "docs", "models")

ROLES = ["Sales / financial", "Compliance / PII", "Medical / PHI",
         "Financial advisor", "Legal / privileged"]
PRESS = ["neutral", "mild", "direct", "emotional", "authority"]

def slug(m):
    return m.replace("/", "-").replace(":", "-").replace(" ", "-").replace("_", "-")

def shade(rate):
    """pale -> oxblood; returns (bg, fg)."""
    t = max(0.0, min(1.0, rate / 100.0))
    s = (242, 244, 245); e = (158, 27, 50)
    bg = tuple(round(s[i] + t * (e[i] - s[i])) for i in range(3))
    fg = "#ffffff" if t > 0.55 else "#16232e"
    return f"rgb({bg[0]},{bg[1]},{bg[2]})", fg

def heatmap(cells_cond):
    head = "".join(f'<th style="padding:6px 8px;font:600 11px/1.2 monospace;'
                   f'color:#5c6b74;text-align:center">{p}</th>' for p in PRESS)
    rows = ""
    for role in ROLES:
        tds = ""
        rc = cells_cond.get(role, {})
        for p in PRESS:
            c = rc.get(p)
            if not c:
                tds += ('<td style="padding:0;text-align:center;color:#aab4ba;'
                        'border:1px solid #fff;background:#f0f2f3">&ndash;</td>')
                continue
            bg, fg = shade(c["rate"])
            tds += (f'<td style="padding:9px 6px;text-align:center;border:1px solid #fff;'
                    f'background:{bg};color:{fg}">'
                    f'<div style="font:600 13px/1.1 monospace">{c["rate"]:.0f}%</div>'
                    f'<div style="font:400 9px/1.3 monospace;opacity:.75">n {c["n"]}</div></td>')
        rows += (f'<tr><th style="padding:6px 10px 6px 0;font:500 12px/1.3 '
                 f'-apple-system,sans-serif;color:#16232e;text-align:left;white-space:nowrap">'
                 f'{role}</th>{tds}</tr>')
    return (f'<table style="border-collapse:collapse;margin:2px 0 6px">'
            f'<tr><th></th>{head}</tr>{rows}</table>')

def page(model, d, rank):
    v, n, delta, N = d["vendor_pct"], d["none_pct"], d["delta"], d["n"]
    kind = d["kind"]
    stat = (f'<div style="display:flex;gap:22px;flex-wrap:wrap;margin:4px 0 20px;'
            f'font:500 13px/1.4 monospace">'
            f'<span style="color:#5c6b74">vendor <b style="color:#9e1b32">{v:.1f}%</b></span>'
            f'<span style="color:#5c6b74">baseline <b style="color:#33708f">{n:.1f}%</b></span>'
            f'<span style="color:#5c6b74">effect <b style="color:#16232e">+{delta:.1f} pp</b></span>'
            f'<span style="color:#5c6b74">n <b style="color:#16232e">{N}</b></span>'
            f'<span style="color:#5c6b74">type <b style="color:#16232e">{kind}</b></span></div>')
    body = f'''---
layout: default
title: "{model}"
parent: "Models"
nav_order: {rank}
---
<h1 style="font:500 22px/1.2 'IBM Plex Serif',Georgia,serif;margin:0 0 2px">{model}</h1>
<p style="color:#5c6b74;margin:0 0 6px">Violation rate by role and pressure. Each cell is the share of undisclosed recommendations on a denied action; darker is worse.</p>
{stat}
<h3 style="font:600 13px/1.2 monospace;letter-spacing:.06em;text-transform:uppercase;color:#9e1b32;margin:18px 0 4px">Under a vendor prompt</h3>
{heatmap(d["cells"]["vendor"])}
<h3 style="font:600 13px/1.2 monospace;letter-spacing:.06em;text-transform:uppercase;color:#33708f;margin:22px 0 4px">Clean baseline &mdash; no vendor prompt</h3>
{heatmap(d["cells"]["none"])}
<p style="color:#8d9aa1;font-size:12.5px;margin-top:18px">Derived from the v1.6 judged corpus; aggregates reproduce the <a href="../evidence.html">Report Cards</a> figures. &ndash; = no sample in that cell.</p>
'''
    return body

def main():
    data = json.load(open(DATA, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)

    # internal consistency gate
    bad = []
    for m, d in data.items():
        for cond, target in (("vendor", d["vendor_pct"]), ("none", d["none_pct"])):
            tot_v = tot_n = 0
            for role in d["cells"][cond].values():
                for c in role.values():
                    tot_v += c["viol"]; tot_n += c["n"]
            got = 100 * tot_v / tot_n if tot_n else 0
            if abs(got - target) > 0.6:
                bad.append((m, cond, got, target))
    if bad:
        raise SystemExit(f"[abort] per-cell aggregate != model rate: {bad[:5]}")

    order = sorted(data.items(), key=lambda kv: -kv[1]["delta"])

    # parent index
    idx = ['---', 'title: "Models"', 'nav_order: 4', 'has_children: true',
           'has_toc: false', '---', '',
           '# Models', '',
           'The vendor effect across all models is on the [Report Cards overview](../evidence.html). '
           'Each model below is broken down by **role and pressure**.', '',
           '| Model | Vendor effect | n | Type |', '|---|--:|--:|:--|']
    for m, d in order:
        idx.append(f'| [{m}]({slug(m)}.html) | +{d["delta"]:.1f} pp | {d["n"]} | {d["kind"]} |')
    open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(idx))

    # per-model pages
    for i, (m, d) in enumerate(order):
        open(os.path.join(OUT, slug(m) + ".html"), "w", encoding="utf-8").write(page(m, d, i+1))

    print(f"[ok] generated {len(order)} model pages + index; consistency gate passed")

if __name__ == "__main__":
    main()
