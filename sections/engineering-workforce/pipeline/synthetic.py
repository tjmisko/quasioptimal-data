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


# --- ground-truth causal parameters (what the econometrics should recover) ---
GT = {
    "gdp_elasticity_wrt_engineers": 0.85,  # d log GDP / d log E
    "capital_elasticity_wrt_engineers": 1.05,  # d log K / d log E
    "patent_elasticity_wrt_engineers": 1.10,  # d log patents / d log E
    "patent_lag_years": 12,  # engineers LEAD patents -> Granger E -> patents
    "patent_depreciation": 0.04,  # perpetual-inventory decay for patent stock
    "causal_direction": "engineers -> {gdp, capital, patents}; patents do NOT cause engineers",
}
_SCALES = {"gdp_real": 5e6, "capital_stock": 1.6e7, "patents_flow": 0.075}


def _covariates_for(cfg: EntityConfig, engineers: np.ndarray, rng) -> list[dict]:
    """GDP, capital, and patents generated FROM the engineer stock with the GT
    elasticities and an engineers->patents lag, so causal tests have ground truth."""
    logE = np.log(np.clip(engineers, 1e-6, None))
    gdp = _SCALES["gdp_real"] * np.exp(
        GT["gdp_elasticity_wrt_engineers"] * logE + rng.normal(0, 0.05, len(logE))
    )
    capital = _SCALES["capital_stock"] * np.exp(
        GT["capital_elasticity_wrt_engineers"] * logE + rng.normal(0, 0.05, len(logE))
    )
    lag = GT["patent_lag_years"]
    logE_lag = np.concatenate([np.full(lag, logE[0]), logE[:-lag]])
    patents_flow = _SCALES["patents_flow"] * np.exp(
        GT["patent_elasticity_wrt_engineers"] * logE_lag + rng.normal(0, 0.08, len(logE))
    )
    delta = GT["patent_depreciation"]
    patents_stock = np.empty_like(patents_flow)
    patents_stock[0] = patents_flow[0]
    for i in range(1, len(patents_flow)):
        patents_stock[i] = (1 - delta) * patents_stock[i - 1] + patents_flow[i]
    investment = np.clip(np.gradient(capital) + 0.05 * capital, 1.0, None)

    variables = {
        "gdp_real": (gdp, "constant int$ (synthetic)"),
        "capital_stock": (capital, "constant int$ (synthetic)"),
        "investment": (investment, "constant int$/yr (synthetic)"),
        "patents_flow": (patents_flow, "count/yr (synthetic)"),
        "patents_stock": (patents_stock, "count (synthetic)"),
    }
    rows = []
    for var, (arr, unit) in variables.items():
        for y, v in zip(YEARS, arr, strict=True):
            rows.append(
                {
                    "entity": cfg.entity,
                    "iso3": cfg.iso3,
                    "year": int(y),
                    "variable": var,
                    "value": float(v),
                    "unit": unit,
                    "source_id": "synthetic",
                    "confidence": "synthetic",
                    "notes": "SYNTHETIC — not real data",
                }
            )
    return rows


def build() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    pop_rows, eng_rows, cov_rows = [], [], []
    ground_truth: dict = {"breaks": {}, "causal": GT}

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
        ground_truth["breaks"][cfg.entity] = {}
        contemporary_engineers = None
        for definition, ceiling, modern in (
            ("contemporary", cfg.ceiling_contemporary, False),
            ("modern", cfg.ceiling_modern, True),
        ):
            share = _regime_share(cfg, ceiling, modern, rng)
            engineers = share / 1e5 * pop
            if definition == "contemporary":
                contemporary_engineers = engineers
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
            ground_truth["breaks"][cfg.entity][definition] = [int(takeoff), int(cfg.break2)]

        cov_rows.extend(_covariates_for(cfg, contemporary_engineers, rng))

    pop_df = schema.validate_population(pd.DataFrame(pop_rows))
    eng_df = schema.validate_engineers(pd.DataFrame(eng_rows))
    cov_df = schema.validate_covariates(pd.DataFrame(cov_rows))
    return pop_df, eng_df, cov_df, ground_truth


def main() -> int:
    pop_df, eng_df, cov_df, ground_truth = build()
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
        notes="NOT REAL DATA. confidence=synthetic. Ground-truth in the sidecar.",
    )
    save_processed(
        cov_df,
        pdir / "covariates_long_synth.parquet",
        source="SYNTHETIC generative model (pipeline/synthetic.py)",
        description="SYNTHETIC GDP, capital stock, investment, and patents (flow+stock).",
        notes=(
            "NOT REAL DATA. Generated FROM the engineer stock with known elasticities and an "
            "engineers->patents lag so causal/cointegration tests have ground truth. Mirrors the "
            "real covariates being sourced (Maddison/PWT GDP+capital, OWID/WIPO patents)."
        ),
    )
    panel = schema.build_panel(eng_df, pop_df)
    save_processed(
        panel,
        pdir / "panel_synth.parquet",
        source="Join of SYNTHETIC engineers + population.",
        description="SYNTHETIC analysis panel (share_per_100k) for developing the stack.",
        notes="NOT REAL DATA. Use to build/validate analysis + report; swap in real panel later.",
    )
    (pdir / "panel_synth.breaks.json").write_text(json.dumps(ground_truth, indent=2))

    print(f"Wrote SYNTHETIC panel ({len(panel)} rows) + covariates ({len(cov_df)} rows).")
    print(f"Ground-truth (breaks + causal params) -> {pdir / 'panel_synth.breaks.json'}")
    print(f"Covariate variables: {sorted(cov_df['variable'].unique())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
