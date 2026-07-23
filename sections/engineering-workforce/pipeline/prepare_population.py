"""Build ``processed/population_long.parquet`` (the denominator) from raw pop data.

Primary source: Maddison Project Database 2020 (population back to 1500 for our
target countries; World from 1820). The World Bank mirror is kept as a modern
cross-check but Maddison is authoritative here for the long run.

Run:
    uv run python sections/engineering-workforce/pipeline/prepare_population.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import registry  # noqa: E402
import schema  # noqa: E402

from quasioptimal.data import save_processed  # noqa: E402
from quasioptimal.paths import processed_dir  # noqa: E402


def _maddison() -> pd.DataFrame:
    src = registry.get_source("maddison-2020")
    raw = src.raw_file
    if raw is None or not raw.exists():
        raise SystemExit(f"Raw file {raw} missing. Run pipeline/fetch.py first ({src.id}).")
    m = pd.read_csv(raw)
    m = m[m["Entity"].isin(schema.CANONICAL_ENTITIES)].copy()
    m = m[m["Population"].notna() & (m["Population"] > 0)]
    return pd.DataFrame(
        {
            "entity": m["Entity"],
            "iso3": m["Entity"].map(schema.CANONICAL_ENTITIES),
            "year": m["Year"].astype(int),
            "population": m["Population"].astype(float),
            "source_id": src.id,
            "notes": "",
        }
    )


def _worldbank_recent(after_year: int) -> pd.DataFrame:
    """World Bank population for years Maddison 2020 does not cover (post-2018)."""
    src = registry.get_source("worldbank-population")
    raw = src.raw_file
    if raw is None or not raw.exists():
        return pd.DataFrame(columns=schema.POPULATION_COLUMNS)
    w = pd.read_csv(raw)
    code_to_entity = {v: k for k, v in schema.CANONICAL_ENTITIES.items()}
    w = w[w["Country Code"].isin(code_to_entity)].copy()
    w = w[w["Year"] > after_year]
    return pd.DataFrame(
        {
            "entity": w["Country Code"].map(code_to_entity),
            "iso3": w["Country Code"],
            "year": w["Year"].astype(int),
            "population": w["Value"].astype(float),
            "source_id": src.id,
            "notes": "world-bank fill for post-Maddison years",
        }
    )


def build() -> pd.DataFrame:
    maddison = _maddison()
    wb = _worldbank_recent(after_year=int(maddison["year"].max()))
    out = pd.concat([maddison, wb], ignore_index=True)
    # California is not in Maddison or the WB country file; documented gap (task G-US-06).
    out = out.drop_duplicates(["iso3", "year"]).sort_values(["entity", "year"])
    return schema.validate_population(out.reset_index(drop=True))


def main() -> int:
    df = build()
    dest = processed_dir("engineering-workforce") / "population_long.parquet"
    save_processed(
        df,
        dest,
        source="Maddison Project Database 2020 (Bolt & van Zanden), via owid/owid-datasets mirror",
        description="Long-run population (denominator) for World + target countries, 1500–2018.",
        notes=(
            "Maddison population estimates. World total only from 1820 (use HYDE for "
            "earlier world denominator, task G-POP-02). California not covered (task "
            "G-US-06). Pre-1820 country figures are sparse era estimates with wide "
            "uncertainty (e.g. US 1500/1700 reflect contested indigenous-population estimates)."
        ),
        source_id="maddison-2020",
    )
    print(f"Wrote {dest} ({len(df)} rows, entities: {sorted(df['entity'].unique())})")
    print(df.groupby("entity")["year"].agg(["min", "max", "count"]).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
