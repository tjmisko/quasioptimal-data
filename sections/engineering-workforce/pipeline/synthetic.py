"""Generate a DENSE, fully synthetic panel for developing the analysis + outputs.

This exists so the whole downstream stack (analysis library, figures, report,
the first claim's formal test) can be built and validated *now*, then populated
with real data later by swapping the input path — nothing downstream changes.

The synthetic series are deliberately shaped like the hypothesis: an engineer
share that is ~0 and flat for centuries, then takes off after industrialization
with a couple of growth regimes. The regime-change years are the GROUND TRUTH
that the changepoint test should recover; they are written to a sidecar so the
analysis tests can assert recovery.

QUARANTINE: every row is tagged ``confidence == 'synthetic'`` and
``source_id == 'synthetic'``; outputs are written to ``*_synth.parquet`` (never
the real ``population_long``/``engineers_long``/``panel`` files). Nothing here is
data about the world.

Run:
    uv run python sections/engineering-workforce/pipeline/synthetic.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import schema  # noqa: E402

from quasioptimal.data import save_processed  # noqa: E402
from quasioptimal.paths import processed_dir  # noqa: E402

YEARS = np.arange(1500, 2026)
SEED = 20260723


@dataclass
class EntityConfig:
    entity: str
    iso3: str
    pop_1500: float
    pop_2025: float
    takeoff: int  # first industrial-era growth regime begins
    break2: int  # second regime (maturation / acceleration) begins
    ceiling_contemporary: float  # target share per 100k at 2025
    ceiling_modern: float
    # growth rates (per year) for the three regimes: pre-industrial, takeoff, mature
    growth: tuple[float, float, float] = (0.0008, 0.055, 0.014)


CONFIGS: list[EntityConfig] = [
    EntityConfig("World", "WLD", 0.46e9, 8.0e9, 1870, 1970, 380, 900),
    EntityConfig("United States", "USA", 2.0e6, 335e6, 1860, 1965, 520, 1600),
    EntityConfig("California", "US-CA", 3.0e5, 39e6, 1885, 1975, 800, 2400),
    EntityConfig(
        "China", "CHN", 1.03e8, 1.41e9, 1955, 1999, 300, 1200, growth=(0.0006, 0.045, 0.030)
    ),
    EntityConfig("United Kingdom", "GBR", 3.9e6, 68e6, 1800, 1960, 430, 1500),
    EntityConfig("Germany", "DEU", 1.2e7, 84e6, 1845, 1960, 560, 2300),
    EntityConfig("France", "FRA", 1.5e7, 68e6, 1820, 1965, 460, 1700),
]


def _logistic_population(cfg: EntityConfig) -> np.ndarray:
    """Smooth monotone population from pop_1500 to pop_2025 (synthetic denominator)."""
    t = (YEARS - 1500) / (2025 - 1500)
    # accelerating growth, most of it after 1800
    shape = (np.exp(3.2 * t) - 1) / (np.exp(3.2) - 1)
    return cfg.pop_1500 + (cfg.pop_2025 - cfg.pop_1500) * shape


def _regime_share(cfg: EntityConfig, ceiling: float, modern: bool, rng) -> np.ndarray:
    """Piecewise-log-linear share (per 100k) with breaks at takeoff and break2.

    Baseline is anchored LOW at 1500 and the takeoff/maturation growth rates are
    solved so the series reaches ``ceiling`` at 2025 with the takeoff regime
    growing faster than the maturation regime. This keeps the pre-industrial
    share near-zero and flat (the hypothesis) instead of inflating the baseline.
    """
    g_pre = cfg.growth[0]
    # modern definition: small counterfactual baseline exists, takes off a
    # generation sooner, and reaches a higher ceiling.
    takeoff = cfg.takeoff - (25 if modern else 0)
    baseline = np.log(0.05 if modern else 0.02)  # per-100k share in 1500

    pre_years = takeoff - 1500
    take_years = cfg.break2 - takeoff
    mature_years = 2025 - cfg.break2
    # solve growth so cumulative log-rise hits the ceiling; takeoff 3x maturation.
    target = np.log(ceiling) - baseline - g_pre * pre_years
    rate_take, rate_mature = 1.0, 0.33
    scale = target / (rate_take * take_years + rate_mature * mature_years)
    g_take, g_mature = scale * rate_take, scale * rate_mature

    log_share = np.empty_like(YEARS, dtype=float)
    log_share[0] = baseline
    for i in range(1, len(YEARS)):
        y = YEARS[i]
        g = g_pre if y < takeoff else (g_take if y < cfg.break2 else g_mature)
        log_share[i] = log_share[i - 1] + g
    noise = rng.normal(0.0, 0.06, size=log_share.shape)
    return np.exp(log_share + noise)


def build() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    pop_rows, eng_rows = [], []
    ground_truth_breaks: dict[str, dict[str, list[int]]] = {}

    for cfg in CONFIGS:
        pop = _logistic_population(cfg)
        for y, p in zip(YEARS, pop, strict=True):
            pop_rows.append(
                {
                    "entity": cfg.entity,
                    "iso3": cfg.iso3,
                    "year": int(y),
                    "population": float(p),
                    "source_id": "synthetic",
                    "notes": "SYNTHETIC",
                }
            )
        ground_truth_breaks[cfg.entity] = {}
        for definition, ceiling, modern in (
            ("contemporary", cfg.ceiling_contemporary, False),
            ("modern", cfg.ceiling_modern, True),
        ):
            share = _regime_share(cfg, ceiling, modern, rng)
            engineers = share / 1e5 * pop
            for y, e in zip(YEARS, engineers, strict=True):
                eng_rows.append(
                    {
                        "entity": cfg.entity,
                        "iso3": cfg.iso3,
                        "year": int(y),
                        "definition": definition,
                        "metric": "stock",
                        "engineers": float(e),
                        "method": "estimate",
                        "source_id": "synthetic",
                        "source_definition": f"SYNTHETIC {definition} generative model",
                        "confidence": "synthetic",
                        "notes": "SYNTHETIC — not real data",
                    }
                )
            takeoff = cfg.takeoff - (25 if definition == "modern" else 0)
            ground_truth_breaks[cfg.entity][definition] = [int(takeoff), int(cfg.break2)]

    pop_df = schema.validate_population(pd.DataFrame(pop_rows))
    eng_df = schema.validate_engineers(pd.DataFrame(eng_rows))
    return pop_df, eng_df, ground_truth_breaks


def main() -> int:
    pop_df, eng_df, breaks = build()
    pdir = processed_dir("engineering-workforce")

    save_processed(
        pop_df,
        pdir / "population_long_synth.parquet",
        source="SYNTHETIC generative model (pipeline/synthetic.py)",
        description="SYNTHETIC dense population denominator for developing analysis/outputs.",
        notes="NOT REAL DATA. Quarantined; swap for real population_long when available.",
    )
    save_processed(
        eng_df,
        pdir / "engineers_long_synth.parquet",
        source="SYNTHETIC generative model (pipeline/synthetic.py)",
        description="SYNTHETIC dense engineer counts, both definitions, 1500-2025.",
        notes="NOT REAL DATA. confidence=synthetic. Ground-truth breaks in breaks sidecar.",
    )
    panel = schema.build_panel(eng_df, pop_df)
    save_processed(
        panel,
        pdir / "panel_synth.parquet",
        source="Join of SYNTHETIC engineers + population.",
        description="SYNTHETIC analysis panel (share_per_100k) for developing the stack.",
        notes="NOT REAL DATA. Use to build/validate analysis + report; swap in real panel later.",
    )
    (pdir / "panel_synth.breaks.json").write_text(json.dumps(breaks, indent=2))

    print(f"Wrote SYNTHETIC panel: {len(panel)} rows, entities={sorted(panel['entity'].unique())}")
    print(f"Ground-truth breaks -> {pdir / 'panel_synth.breaks.json'}")
    print(
        panel.query("entity == 'United States' and definition == 'contemporary'")
        .iloc[::80][["year", "engineers", "population", "share_per_100k"]]
        .to_string(index=False)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
