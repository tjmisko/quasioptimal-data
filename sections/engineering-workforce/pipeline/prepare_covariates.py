"""Build the REAL ``processed/covariates_long.parquet`` (GDP, capital, patents).

Sources (GitHub-reachable mirrors, see sources.yaml):
- pwt-1001               -> gdp_real (rgdpna), capital_stock (rnna)   [1950-2019]
- worldbank-patents-*    -> patents_flow (RESD + NRES office intake)  [1960-2013]
                            + patents_stock (perpetual-inventory cumulation)

These are the real covariates the H2/H3/patent claims consume. They cover the
same countries as the engineer numerators; the binding constraint on running the
causal claims for real is still a DENSE engineer series (IPUMS, task G-US-01) that
overlaps these years.

Run:
    uv run python sections/engineering-workforce/pipeline/prepare_covariates.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import registry  # noqa: E402
import schema  # noqa: E402

from quasioptimal.data import save_processed  # noqa: E402
from quasioptimal.paths import processed_dir  # noqa: E402

CANON = schema.CANONICAL_ENTITIES
ISO_TO_ENTITY = {v: k for k, v in CANON.items()}
PATENT_DEPRECIATION = 0.0  # patents don't obviously depreciate; 0 = pure cumulation


def _raw(source_id: str) -> Path:
    src = registry.get_source(source_id)
    if src.raw_file is None or not src.raw_file.exists():
        raise SystemExit(f"Raw for {source_id} missing ({src.raw_file}). Run fetch.py.")
    return src.raw_file


def _pwt() -> pd.DataFrame:
    p = pd.read_csv(_raw("pwt-1001"), encoding="utf-8-sig")
    p = p[p["countrycode"].isin(ISO_TO_ENTITY)]
    rows = []
    for var, col, unit in (
        ("gdp_real", "rgdpna", "mn 2017 US$ (PWT rgdpna)"),
        ("capital_stock", "rnna", "mn 2017 US$ (PWT rnna)"),
    ):
        d = p[["countrycode", "year", col]].dropna()
        rows.append(
            pd.DataFrame(
                {
                    "entity": d["countrycode"].map(ISO_TO_ENTITY),
                    "iso3": d["countrycode"],
                    "year": d["year"].astype(int),
                    "variable": var,
                    "value": d[col].astype(float),
                    "unit": unit,
                    "source_id": "pwt-1001",
                    "confidence": "primary",
                    "notes": "",
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


def _wb_patents() -> pd.DataFrame:
    def _long(source_id: str) -> pd.DataFrame:
        w = pd.read_csv(_raw(source_id))
        w = w[w["Country Code"].isin(ISO_TO_ENTITY)]
        year_cols = [c for c in w.columns if c.isdigit()]
        m = w.melt(
            id_vars=["Country Code"],
            value_vars=year_cols,
            var_name="year",
            value_name="value",
        ).dropna(subset=["value"])
        m["year"] = m["year"].astype(int)
        return m.rename(columns={"Country Code": "iso3"})

    resd = _long("worldbank-patents-resd")
    nres = _long("worldbank-patents-nres")
    total = (
        pd.concat([resd, nres])
        .groupby(["iso3", "year"], as_index=False)["value"]
        .sum()  # office intake = residents + non-residents
    )
    flow = pd.DataFrame(
        {
            "entity": total["iso3"].map(ISO_TO_ENTITY),
            "iso3": total["iso3"],
            "year": total["year"],
            "variable": "patents_flow",
            "value": total["value"].astype(float),
            "unit": "applications/yr (WB RESD+NRES)",
            "source_id": "worldbank-patents-resd",
            "confidence": "primary",
            "notes": "residents + non-residents (office intake)",
        }
    )
    # perpetual-inventory patent stock per country
    stock_rows = []
    for iso3, g in flow.sort_values("year").groupby("iso3"):
        s = 0.0
        for _, r in g.iterrows():
            s = (1 - PATENT_DEPRECIATION) * s + r["value"]
            stock_rows.append(
                {
                    "entity": r["entity"],
                    "iso3": iso3,
                    "year": int(r["year"]),
                    "variable": "patents_stock",
                    "value": float(s),
                    "unit": "cumulative applications (delta=0)",
                    "source_id": "worldbank-patents-resd",
                    "confidence": "primary",
                    "notes": "perpetual-inventory cumulation of office intake",
                }
            )
    return pd.concat([flow, pd.DataFrame(stock_rows)], ignore_index=True)


def build() -> pd.DataFrame:
    out = pd.concat([_pwt(), _wb_patents()], ignore_index=True)
    out = out[np.isfinite(out["value"])]
    return schema.validate_covariates(
        out.sort_values(["variable", "entity", "year"]).reset_index(drop=True)
    )


def main() -> int:
    df = build()
    dest = processed_dir("engineering-workforce") / "covariates_long.parquet"
    save_processed(
        df,
        dest,
        source="PWT 10.01 (rgdpna, rnna) + World Bank IP.PAT.RESD/NRES, via GitHub mirrors.",
        description="Real covariates: GDP, capital stock, and patents (flow + stock) by country-year.",
        notes=(
            "gdp_real/capital_stock from PWT 1950-2019; patents from WB 1960-2013 (RESD+NRES, "
            "office intake; applications not grants; post-1985 surge). Causal claims need a dense "
            "engineer series overlapping these years (IPUMS, task G-US-01)."
        ),
    )
    print(f"Wrote {dest} ({len(df)} rows)")
    print(df.groupby("variable")["year"].agg(["min", "max", "count"]).to_string())
    print(df.groupby(["variable", "entity"]).size().unstack(fill_value=0).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
