"""Patents/IP claim: engineers LEAD the accumulation of patents.

Distinct from the GDP/capital claims: here the question is directional — does the
engineering workforce drive intellectual-property output (patents), and with what
lag? Uses lead-lag cross-correlation (robust for smooth series) plus Granger.

Swap-in ready (synthetic today, real via --panel/--covariates later). See README for H0.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _common  # noqa: E402
import analysis  # noqa: E402


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
    if cov is None or "patents_flow" not in set(cov.get("variable", [])):
        print(f"No patents covariate available — cannot test. [{prov}]")
        return 0

    frame = analysis.entity_frame(panel, cov, args.entity, args.definition)
    lead = analysis.lead_lag(frame, "engineers", "patents_flow")
    granger = analysis.granger_direction(frame, "engineers", "patents_flow")
    elas = analysis.elasticity(frame, "patents_flow", "engineers")

    print(f"Data provenance: {prov}")
    print(f"Series: {args.entity} ({args.definition}) engineers vs patents_flow")
    print("lead-lag:", lead)
    print("granger:", granger)
    print("elasticity (patents wrt engineers):", elas)

    # engineers lead patents by a positive lag => engineers drive IP accumulation
    supported = not lead.get("insufficient") and lead["best_lag"] > 0
    print(
        f"\nCLAIM {'SUPPORTED' if supported else 'NOT SUPPORTED'}  [{prov}]  "
        f"({lead.get('interpretation')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
