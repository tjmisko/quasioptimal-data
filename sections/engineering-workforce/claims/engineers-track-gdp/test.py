"""H2: the engineer stock tracks real GDP (cointegrated, positive elasticity).

Swap-in ready (synthetic today, real via --panel/--covariates later). See README for H0.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _common  # noqa: E402
import analysis  # noqa: E402

COVARIATE = "gdp_real"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default=None)
    ap.add_argument("--covariates", default=None)
    ap.add_argument("--entity", default="United States")
    ap.add_argument("--definition", default="contemporary")
    ap.add_argument("--real", action="store_true")
    args = ap.parse_args()

    panel_path, cov_path = _common.default_paths(args.real)
    panel, cov = _common.load(
        Path(args.panel) if args.panel else panel_path,
        Path(args.covariates) if args.covariates else cov_path,
    )
    prov = _common.provenance(panel)
    if cov is None:
        print(f"No covariates table available — cannot test (need {COVARIATE}). [{prov}]")
        return 0

    frame = analysis.entity_frame(panel, cov, args.entity, args.definition)
    elas = analysis.elasticity(frame, "engineers", COVARIATE)
    mreg = analysis.multiple_regression(frame, "engineers", [COVARIATE, "capital_stock"])
    lead = analysis.lead_lag(frame, "engineers", COVARIATE)

    print(f"Data provenance: {prov}")
    print(f"Series: {args.entity} ({args.definition}) engineers vs {COVARIATE}")
    print("elasticity:", elas)
    print("multiple regression (control for capital):", mreg)
    print("lead-lag:", lead)

    supported = (
        not elas.get("insufficient")
        and elas["cointegrated"]
        and elas["ci95"][0] > 0  # positive, significant elasticity
    )
    print(
        f"\nCLAIM {'SUPPORTED' if supported else 'NOT SUPPORTED'}  [{prov}]  "
        f"(elasticity={elas.get('elasticity'):.3f}, cointegrated={elas.get('cointegrated')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
