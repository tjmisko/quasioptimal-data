"""Join engineers (stock) to population -> ``processed/panel.parquet``.

The panel is the analysis table: one row per (entity, year, definition, source),
with ``share_per_100k = 1e5 * engineers / population``. Only ``metric == 'stock'``
rows get a share (a share of an annual graduate flow is meaningless).

Run (after prepare_population and prepare_engineers):
    uv run python sections/engineering-workforce/pipeline/build_panel.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import schema  # noqa: E402

from quasioptimal.data import load_processed, save_processed  # noqa: E402
from quasioptimal.paths import processed_dir  # noqa: E402


def main() -> int:
    pdir = processed_dir("engineering-workforce")
    pop = load_processed(pdir / "population_long.parquet")
    eng = load_processed(pdir / "engineers_long.parquet")

    if len(eng) == 0:
        print("engineers_long is empty — no numerators yet. Panel will be empty.")
        panel = pd.DataFrame(columns=schema.PANEL_COLUMNS)
    else:
        panel = schema.build_panel(eng, pop)
        missing_pop = panel["population"].isna().sum()
        if missing_pop:
            print(
                f"WARNING: {missing_pop} engineer rows had no matching population "
                "(entity/year not in population_long). They have NaN share."
            )

    dest = pdir / "panel.parquet"
    save_processed(
        panel,
        dest,
        source="Join of engineers_long (numerator) and population_long (denominator).",
        description="Analysis panel: engineers, population, and share_per_100k by entity/year/definition.",
        notes=(
            "share_per_100k = 1e5 * engineers / population, stock rows only. Rows inherit "
            "the numerator's `confidence`; provisional literature_unverified rows must not "
            "back a claim until replaced by primary data."
        ),
    )
    print(f"Wrote {dest} ({len(panel)} rows).")
    if len(panel):
        cols = [
            "entity",
            "year",
            "definition",
            "engineers",
            "population",
            "share_per_100k",
            "confidence",
        ]
        print(panel[cols].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
