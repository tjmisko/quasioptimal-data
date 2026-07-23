"""Build ``processed/population_long.parquet`` (the denominator) from raw pop data.

Layers several GitHub-reachable mirrors with explicit precedence (first wins on
a duplicate entity-year):

1. owid-co2-population  — OWID annual population, World + countries, 1750-2024.
2. maddison-2020        — country benchmark years before 1750 (deep country history).
3. world-historical     — World totals before 1750 ("Average" of standard estimates).
4. california-population — California 1900+ (fills the state gap Maddison lacks).
5. worldbank-population  — final fill for any year after owid-co2 ends.

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

CANON = schema.CANONICAL_ENTITIES


def _raw(source_id: str) -> Path:
    src = registry.get_source(source_id)
    if src.raw_file is None or not src.raw_file.exists():
        raise SystemExit(f"Raw for {source_id} missing ({src.raw_file}). Run fetch.py.")
    return src.raw_file


def _owid_co2() -> pd.DataFrame:
    d = pd.read_csv(_raw("owid-co2-population"), usecols=["country", "year", "population"])
    d = d[d["country"].isin(CANON) & d["population"].notna()]
    return pd.DataFrame(
        {
            "entity": d["country"],
            "iso3": d["country"].map(CANON),
            "year": d["year"].astype(int),
            "population": d["population"].astype(float),
            "source_id": "owid-co2-population",
            "notes": "",
        }
    )


def _maddison_pre1750() -> pd.DataFrame:
    m = pd.read_csv(_raw("maddison-2020"))
    m = m[m["Entity"].isin(CANON) & m["Population"].notna() & (m["Year"] < 1750)]
    return pd.DataFrame(
        {
            "entity": m["Entity"],
            "iso3": m["Entity"].map(CANON),
            "year": m["Year"].astype(int),
            "population": m["Population"].astype(float),
            "source_id": "maddison-2020",
            "notes": "pre-1750 benchmark estimate (wide uncertainty)",
        }
    )


def _world_historical() -> pd.DataFrame:
    w = pd.read_csv(_raw("world-historical-population"))
    w = w[(w["Year"] < 1750) & w["Average"].notna()]
    return pd.DataFrame(
        {
            "entity": "World",
            "iso3": "WLD",
            "year": w["Year"].astype(int),
            "population": w["Average"].astype(float) * 1e6,  # file is in millions
            "source_id": "world-historical-population",
            "notes": "consensus 'Average' of standard world-population estimates",
        }
    )


def _california() -> pd.DataFrame:
    c = pd.read_csv(
        _raw("california-population"), header=None, names=["state", "year", "population"]
    )
    c = c[c["state"] == "CA"]
    return pd.DataFrame(
        {
            "entity": "California",
            "iso3": "US-CA",
            "year": c["year"].astype(int),
            "population": c["population"].astype(float),
            "source_id": "california-population",
            "notes": "US Census state estimates",
        }
    )


def _worldbank() -> pd.DataFrame:
    w = pd.read_csv(_raw("worldbank-population"))
    code_to_entity = {v: k for k, v in CANON.items()}
    w = w[w["Country Code"].isin(code_to_entity)]
    return pd.DataFrame(
        {
            "entity": w["Country Code"].map(code_to_entity),
            "iso3": w["Country Code"],
            "year": w["Year"].astype(int),
            "population": w["Value"].astype(float),
            "source_id": "worldbank-population",
            "notes": "final fill",
        }
    )


def build() -> pd.DataFrame:
    # precedence order: earlier layers win on duplicate (iso3, year)
    layers = [
        _owid_co2(),
        _maddison_pre1750(),
        _world_historical(),
        _california(),
        _worldbank(),
    ]
    out = pd.concat(layers, ignore_index=True)
    out = out[out["population"] > 0]
    out = out.drop_duplicates(["iso3", "year"], keep="first").sort_values(["entity", "year"])
    return schema.validate_population(out.reset_index(drop=True))


def main() -> int:
    df = build()
    dest = processed_dir("engineering-workforce") / "population_long.parquet"
    save_processed(
        df,
        dest,
        source="Layered GitHub mirrors: owid-co2 (OWID/HYDE/Gapminder/UN) + Maddison 2020 "
        "+ world-historical + JoshData state population + World Bank. See sources.yaml.",
        description="Long-run population denominator, World + target countries + California.",
        notes=(
            "Annual 1750-2024 (owid-co2); pre-1750 country benchmarks (Maddison) and World "
            "totals (historical 'Average'); California 1900+ (US Census state estimates). "
            "Pre-1900 figures are era estimates with wide uncertainty; California pre-1900 "
            "still missing (Census historical, task G-US-06)."
        ),
    )
    print(f"Wrote {dest} ({len(df)} rows)")
    print(df.groupby("entity")["year"].agg(["min", "max", "count"]).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
