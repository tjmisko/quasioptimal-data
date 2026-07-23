"""H1: the NUMBER of engineers has grown quasi-exponentially since ~1800.

Swap-in ready (synthetic today, real via --panel later). See README for H0.

Run:
    uv run python sections/engineering-workforce/claims/exponential-growth-since-1800/test.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _common  # noqa: E402
import analysis  # noqa: E402

# pre-registered decision rule
R2_MIN = 0.95  # log-linear fit must explain >=95% of variation
GROWTH_MIN = 0.02  # sustained annual growth above 2%/yr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default=None)
    ap.add_argument("--entity", default="United States")
    ap.add_argument("--definition", default="contemporary")
    ap.add_argument("--since", type=int, default=1800)
    ap.add_argument("--real", action="store_true")
    args = ap.parse_args()

    panel_path, _ = _common.default_paths(args.real)
    panel, _ = _common.load(Path(args.panel) if args.panel else panel_path)
    prov = _common.provenance(panel)

    # use the engineer COUNT, not the share, for this claim
    d = panel[(panel["entity"] == args.entity) & (panel["definition"] == args.definition)]
    d = d[["year", "engineers"]].dropna()
    res = analysis.test_exponential_growth(d, "engineers", since=args.since)

    print(f"Data provenance: {prov}")
    print(f"Series: {args.entity} ({args.definition}) engineer count since {args.since}")
    print(res)
    supported = (
        not res.get("insufficient")
        and res["r2_loglinear"] >= R2_MIN
        and res["annual_growth"] >= GROWTH_MIN
    )
    print(
        f"\nlog-linear R^2={res.get('r2_loglinear'):.3f}, "
        f"annual growth={res.get('annual_growth', float('nan')) * 100:.2f}%/yr, "
        f"constant-growth={res.get('constant_growth')}"
    )
    print(f"CLAIM {'SUPPORTED' if supported else 'NOT SUPPORTED'}  [{prov}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
