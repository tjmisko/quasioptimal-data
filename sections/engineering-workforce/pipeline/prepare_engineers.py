"""Build ``processed/engineers_long.parquet`` (the numerator).

Every authoritative numerator source (IPUMS, BLS, Census, Eurostat, UNESCO,
China MOE/NBS, I-CeM, ...) is currently **blocked by the session egress policy**
(see sources.yaml `reachable: blocked_egress` and the G-* task cards). Until a
raw file for one of them lands in ``data/raw/``, this script has nothing primary
to transform.

So today it assembles the numerator from two places:

1. Any real raw numerator files present in ``data/raw/`` — each gets a dedicated
   ``prepare_<source>()`` transform (documented below; they raise if the raw is
   absent, and are skipped). This is where verified primary data will flow in.
2. A small, explicitly-flagged SEED of anchor points transcribed from the
   literature review (``data_acquisition/seed/engineers_anchors.csv``), tagged
   ``confidence == 'literature_unverified'``. These let us compute a *provisional*
   long-run picture now; they are NOT verified data and must be replaced by
   primary pulls before backing any claim.

Run:
    uv run python sections/engineering-workforce/pipeline/prepare_engineers.py
    uv run python .../prepare_engineers.py --no-seed   # primary sources only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import registry  # noqa: E402
import schema  # noqa: E402

from quasioptimal.data import save_processed  # noqa: E402
from quasioptimal.paths import processed_dir  # noqa: E402


class SourceNotAvailable(Exception):
    """Raised when a source's raw file is not present yet (blocked/not fetched)."""


# --- primary-source transforms (fill in as raw files become available) -------
#
# Each returns rows in the ENGINEERS_COLUMNS shape. They deliberately raise
# SourceNotAvailable until the documented raw file exists, so `collect_primary`
# can skip them cleanly. The transform logic is specified so an agent/human can
# implement it the moment the egress block is lifted or a file is dropped in.


def prepare_ipums_usa() -> pd.DataFrame:
    """IPUMS USA extract -> US & California engineer STOCK, both definitions.

    Expected raw: data/raw/ipums-usa-extract.csv.gz with columns YEAR, STATEFIP,
    PERWT, OCC1950 (and OCC for post-1950 detail). Steps:
      * contemporary: sum PERWT where OCC1950 in the engineer codes valid that
        year; modern: restrict to detailed engineering occupations (exclude
        'engineer' meaning stationary-engine operator).
      * national totals and STATEFIP == 6 (California) separately.
      * one row per (year, definition) with method='census'.
    """
    src = registry.get_source("ipums-usa")
    if src.raw_file is None or not src.raw_file.exists():
        raise SourceNotAvailable(f"{src.id}: {src.raw_file} not present ({src.task})")
    raise NotImplementedError("Implement once the IPUMS extract is available (task G-US-01).")


def prepare_bls_oews() -> pd.DataFrame:
    """BLS OEWS mirror -> US modern engineer STOCK (SOC 17-2000), May 2021.

    Currently the mirror is a single national-year file; when the full
    year-by-state OEWS series is obtained (task G-US-02), extend this to emit all
    years and California (AREA_TITLE == 'California').
    """
    src = registry.get_source("bls-oews")
    if src.raw_file is None or not src.raw_file.exists():
        raise SourceNotAvailable(f"{src.id}: {src.raw_file} not present ({src.task})")
    b = pd.read_csv(src.raw_file, dtype=str)
    row = b[(b["OCC_CODE"] == "17-2000") & (b["AREA_TITLE"].str.contains("U.S.", na=False))]
    if row.empty:
        row = b[b["OCC_CODE"] == "17-2000"]
    emp = float(row.iloc[0]["TOT_EMP"].replace(",", ""))
    return pd.DataFrame(
        [
            {
                "entity": "United States",
                "iso3": "USA",
                "year": 2021,
                "definition": "modern",
                "metric": "stock",
                "engineers": emp,
                "method": "census",
                "source_id": "bls-oews",
                "source_definition": "BLS OEWS SOC 17-2000 'Engineers', national employment",
                "confidence": "primary",
                "notes": "Mirror of BLS OEWS national May-2021 (single year).",
            }
        ]
    )


PRIMARY_TRANSFORMS = {
    "ipums-usa": prepare_ipums_usa,
    "bls-oews": prepare_bls_oews,
    # add: nces-ipeds, unesco-uis, ilostat, eurostat-*, china-*, uk-icem, ...
}


def collect_primary() -> list[pd.DataFrame]:
    frames = []
    for source_id, fn in PRIMARY_TRANSFORMS.items():
        try:
            frames.append(fn())
            print(f"[primary] {source_id}: ingested")
        except SourceNotAvailable as exc:
            print(f"[skip]    {source_id}: {exc}")
        except NotImplementedError as exc:
            print(f"[todo]    {source_id}: {exc}")
    return frames


def load_seed() -> pd.DataFrame:
    path = registry._section_dir() / "data_acquisition" / "seed" / "engineers_anchors.csv"
    df = pd.read_csv(path)
    print(f"[seed]    {len(df)} provisional literature anchor(s) loaded from {path.name}")
    return df


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-seed", action="store_true", help="exclude provisional literature anchors")
    args = ap.parse_args()

    frames = collect_primary()
    if not args.no_seed:
        frames.append(load_seed())

    if not frames:
        print(
            "\nNo numerator data available yet. All sources blocked; run with seed "
            "(default) or unblock a source. Writing empty table."
        )
        empty = pd.DataFrame(columns=schema.ENGINEERS_COLUMNS)
        df = empty
    else:
        df = schema.validate_engineers(pd.concat(frames, ignore_index=True))

    dest = processed_dir("engineering-workforce") / "engineers_long.parquet"
    n_unverified = int((df.get("confidence") == "literature_unverified").sum()) if len(df) else 0
    save_processed(
        df,
        dest,
        source="Mixed; see source_id per row and sources.yaml. Seed = literature anchors.",
        description="Engineer counts (numerator) by entity-year, definition, and metric.",
        notes=(
            f"{len(df)} rows; {n_unverified} are provisional literature_unverified anchors "
            "([VERIFY]) — NOT primary data. Replace with primary pulls (G-* tasks) before "
            "using in any claim. All primary numerator sources are egress-blocked as of 2026-07-23."
        ),
    )
    print(f"\nWrote {dest} ({len(df)} rows; {n_unverified} provisional).")
    if len(df):
        print(
            df[["entity", "year", "definition", "engineers", "confidence"]].to_string(index=False)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
