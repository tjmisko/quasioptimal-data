"""Formal test for the 'engineer-share takeoff' claim.

Swap-in ready: runs on the synthetic panel today; point ``--panel`` at the real
panel later and the same test executes unchanged. The verdict is only meaningful
once the panel is real (``confidence == 'primary'``); on synthetic/provisional
data it is a wired-up demonstration.

Test logic (see the claim README for H0 and the pre-registered decision rule):
  1. Detect structural breaks in log(share) with BIC-selected model order.
  2. Fit growth regimes; identify the industrial-takeoff break as the one where
     annual growth jumps from < PRE_MAX to > POST_MIN.
  3. Reject H0 (no takeoff) iff such a break exists in the plausible window.

Run:
    uv run python sections/engineering-workforce/claims/engineer-share-takeoff/test.py
    uv run python .../test.py --panel sections/engineering-workforce/data/processed/panel.parquet \
        --entity "United States" --definition contemporary
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from quasioptimal.data import load_processed
from quasioptimal.paths import processed_dir, section_dir

sys.path.insert(0, str(section_dir("engineering-workforce") / "pipeline"))
import analysis  # noqa: E402

# pre-registered decision-rule thresholds
PRE_MAX = 0.010  # pre-takeoff annual growth must be below 1.0%/yr (near-flat)
POST_MIN = 0.030  # post-takeoff annual growth must exceed 3.0%/yr
WINDOW = (1700, 2000)  # plausible industrial-takeoff window


def run(panel, entity: str, definition: str) -> dict:
    s = analysis.series(panel, entity, definition)
    model = analysis.detect_changepoints(s)
    regimes = analysis.fit_regimes(s, model.break_years)

    takeoff = None
    for a, b in zip(regimes[:-1], regimes[1:], strict=False):
        if (
            a.annual_growth < PRE_MAX
            and b.annual_growth > POST_MIN
            and WINDOW[0] <= b.year_from <= WINDOW[1]
        ):
            takeoff = {
                "break_year": b.year_from,
                "pre_growth": a.annual_growth,
                "post_growth": b.annual_growth,
            }
            break

    return {
        "entity": entity,
        "definition": definition,
        "n_regimes": model.n_regimes,
        "break_years": model.break_years,
        "takeoff": takeoff,
        "reject_H0": takeoff is not None,
        "regimes": regimes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--panel", default=str(processed_dir("engineering-workforce") / "panel_synth.parquet")
    )
    ap.add_argument("--entity", default="United States")
    ap.add_argument("--definition", default="contemporary")
    args = ap.parse_args()

    panel = load_processed(Path(args.panel))
    conf = set(panel.get("confidence").dropna().unique()) if "confidence" in panel else set()
    provenance = (
        "SYNTHETIC (demonstration only)"
        if "synthetic" in conf
        else "PROVISIONAL (unverified anchors)"
        if "literature_unverified" in conf
        else "REAL"
    )

    res = run(panel, args.entity, args.definition)
    print(f"Data provenance: {provenance}")
    print(f"Series: {res['entity']} ({res['definition']})")
    print(f"Regimes selected (BIC): {res['n_regimes']}; breaks at {res['break_years']}")
    for r in res["regimes"]:
        print(
            f"  {r.year_from}-{r.year_to}: {r.annual_growth * 100:6.2f}%/yr  "
            f"({r.start_share:.2f} -> {r.end_share:.1f} per 100k)"
        )
    verdict = "SUPPORTED" if res["reject_H0"] else "NOT SUPPORTED"
    if res["takeoff"]:
        t = res["takeoff"]
        print(
            f"\nTakeoff break at {t['break_year']}: "
            f"{t['pre_growth'] * 100:.2f}%/yr -> {t['post_growth'] * 100:.2f}%/yr"
        )
    print(
        f"\nH0 (no takeoff / constant growth): {'REJECTED' if res['reject_H0'] else 'not rejected'}"
    )
    print(f"CLAIM {verdict}  [{provenance}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
