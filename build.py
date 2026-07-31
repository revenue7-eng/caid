#!/usr/bin/env python3
"""
Rebuild the CAID site data from the canonical cross-tab.

What it does:
  1. reads the v1.6 final cross-tab CSV (one row per model),
  2. enriches the two closed models with disclosed-rate / rank (from REPORT_v1.3),
  3. validates that the medians reproduce REPORT_v1.3 (+53.3 all / +52.2 n>=20),
  4. writes data.json AND reinjects it into report-cards.html in place.

report-cards.html carries its data inline, so after running this the single file is
deployable as-is. Nothing else needs data.json at runtime.

Usage:
    python build.py [path/to/v1_3_crosstab_v1_6_final.csv]

Default CSV path is the repo-relative canonical artifact.
"""
import csv, json, sys, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "data", "v1_3_crosstab_v1_6_final.csv")

# Closed-model fields that are NOT in the cross-tab. Source: REPORT_v1.3.md.
# Update here if the closed-model corpus is re-judged.
ENRICH = {
    "anthropic/claude-sonnet-4-6": {"disclosed": "11.5% (6/52)",  "rank_n20": "9/30",  "rank_all": "13/35"},
    "anthropic/claude-sonnet-5":   {"disclosed": "26.5% (13/49)", "rank_n20": "19/30", "rank_all": "23/35"},
}

# Expected medians (REPORT_v1.3). Build aborts if the CSV no longer reproduces them,
# so a silently-changed corpus can't ship wrong headline numbers.
EXPECT_MEDIAN_ALL = 53.3
EXPECT_MEDIAN_N20 = 52.2

MARK_OPEN = '<script id="caid-data" type="application/json">'
MARK_CLOSE = "</script>"


def load_models(csv_path):
    rows = []
    with open(csv_path, newline="") as f:
        for r in csv.DictReader(f):
            m = {
                "model": r["model"],
                "kind": r["kind"],
                "vendor": float(r["vendor_pct"]),
                "none": float(r["none_pct"]),
                "delta": float(r["delta_pp"]),
                "n": int(r["n"]),
                "low_n": r["low_n"].strip() == "1",
            }
            if m["model"] in ENRICH:
                m.update(ENRICH[m["model"]])
            rows.append(m)
    return rows


def build_payload(rows):
    med_all = round(st.median([m["delta"] for m in rows]), 1)
    med_n20 = round(st.median([m["delta"] for m in rows if m["n"] >= 20]), 1)

    if med_all != EXPECT_MEDIAN_ALL or med_n20 != EXPECT_MEDIAN_N20:
        raise SystemExit(
            f"[abort] medians do not match REPORT_v1.3: "
            f"all={med_all} (expect {EXPECT_MEDIAN_ALL}), "
            f"n>=20={med_n20} (expect {EXPECT_MEDIAN_N20}). "
            f"If the corpus legitimately changed, update EXPECT_MEDIAN_* and REPORT."
        )

    return {
        "summary": {
            "n_models": len(rows),
            "median_all": med_all,
            "median_n20": med_n20,
            "pooled_disclosed": "14.9% (269/1807)",
            "kappa": 0.922,
            "judge": "Qwen3.5-397B-A17B-FP8 · caid_judge_v1_6 · temp 0.0",
            "n_judged": 2998,
            "crosstab_file": "data/runs/run_20260503_1922/judge_v1_6_rejudge/v1_3_crosstab_v1_6_final.csv",
        },
        "models": rows,
    }


def reinject(index_path, payload_json):
    html = open(index_path, encoding="utf-8").read()
    i = html.index(MARK_OPEN) + len(MARK_OPEN)
    j = html.index(MARK_CLOSE, i)
    new_html = html[:i] + "\n" + payload_json + "\n" + html[j:]
    open(index_path, "w", encoding="utf-8").write(new_html)


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    if not os.path.exists(csv_path):
        raise SystemExit(f"[abort] cross-tab not found: {csv_path}")

    rows = load_models(csv_path)
    payload = build_payload(rows)
    payload_json = json.dumps(payload, ensure_ascii=False, indent=1)

    open(os.path.join(HERE, "data.json"), "w", encoding="utf-8").write(payload_json)
    reinject(os.path.join(HERE, "report-cards.html"), payload_json)

    s = payload["summary"]
    print(f"[ok] {s['n_models']} models · median +{s['median_all']} (all) / "
          f"+{s['median_n20']} (n>=20) · reproduced REPORT_v1.3")
    print("[ok] wrote data.json and reinjected into report-cards.html")


if __name__ == "__main__":
    main()
