"""Tests for the engineering-workforce analysis library.

These build small in-memory series with known structure so they don't depend on
the generated synthetic parquet, and assert that the changepoint detector,
regime fitter, and counterfactual behave correctly.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from quasioptimal.paths import section_dir

sys.path.insert(0, str(section_dir("engineering-workforce") / "pipeline"))

import analysis  # noqa: E402


def _piecewise_series(break_year: int, g_pre: float, g_post: float) -> pd.DataFrame:
    years = np.arange(1700, 2021)
    log_share = np.empty(len(years), dtype=float)
    log_share[0] = np.log(0.1)
    for i in range(1, len(years)):
        g = g_pre if years[i] < break_year else g_post
        log_share[i] = log_share[i - 1] + g
    return pd.DataFrame({"year": years, "share_per_100k": np.exp(log_share)})


def test_detect_changepoints_recovers_known_break():
    df = _piecewise_series(break_year=1870, g_pre=0.001, g_post=0.05)
    model = analysis.detect_changepoints(df, max_regimes=3)
    assert model.n_regimes == 2
    assert len(model.break_years) == 1
    assert abs(model.break_years[0] - 1870) <= 5


def test_detect_changepoints_flat_series_has_one_regime():
    years = np.arange(1500, 1801)
    df = pd.DataFrame({"year": years, "share_per_100k": np.full(len(years), 0.5)})
    model = analysis.detect_changepoints(df, max_regimes=3)
    assert model.n_regimes == 1
    assert model.break_years == []


def test_fit_regimes_orders_growth_correctly():
    df = _piecewise_series(break_year=1870, g_pre=0.001, g_post=0.05)
    regimes = analysis.fit_regimes(df, [1870])
    assert len(regimes) == 2
    assert regimes[0].annual_growth < 0.01  # near-flat pre-industrial
    assert regimes[1].annual_growth > 0.03  # takeoff


def test_cross_country_snapshot_picks_nearest_year_and_sorts():
    panel = pd.DataFrame(
        {
            "entity": ["A", "A", "B"],
            "definition": ["contemporary"] * 3,
            "year": [1899, 1905, 1900],
            "share_per_100k": [10.0, 12.0, 20.0],
        }
    )
    snap = analysis.cross_country_snapshot(panel, 1900, "contemporary", tol=3)
    assert list(snap["entity"]) == ["B", "A"]  # sorted descending by share
    assert int(snap[snap["entity"] == "A"]["year"].iloc[0]) == 1899  # nearest


def test_counterfactual_band_is_monotone():
    band = analysis.counterfactual_modern_share(0.05, {"low": 0.002, "central": 0.01, "high": 0.03})
    assert band["low"] < band["central"] < band["high"]


def _covariate_frame(g_eng=0.05, gdp_elasticity=0.85, patent_lag=10):
    """engineers grow exponentially; gdp = f(engineers^elasticity); patents lag engineers."""
    years = np.arange(1800, 2021)
    engineers = np.exp(g_eng * (years - 1800)) * 100
    gdp = 5e6 * engineers**gdp_elasticity
    patents = np.empty_like(engineers)
    patents[:patent_lag] = engineers[0]
    patents[patent_lag:] = engineers[:-patent_lag]
    return pd.DataFrame(
        {"year": years, "engineers": engineers, "gdp_real": gdp, "patents_flow": patents}
    )


def test_exponential_growth_recovers_rate():
    df = _covariate_frame(g_eng=0.05)
    res = analysis.test_exponential_growth(df, "engineers", since=1800)
    assert res["r2_loglinear"] > 0.999
    assert abs(res["annual_growth"] - 0.05) < 0.002
    assert res["constant_growth"] is True


def test_elasticity_recovers_known_value():
    df = _covariate_frame(gdp_elasticity=0.85)
    res = analysis.elasticity(df, "gdp_real", "engineers")
    assert abs(res["elasticity"] - 0.85) < 0.02


def test_lead_lag_recovers_direction_and_lag():
    df = _covariate_frame(patent_lag=10)
    res = analysis.lead_lag(df, "engineers", "patents_flow", max_lag=30)
    assert res["best_lag"] == 10  # engineers lead patents by the injected lag
