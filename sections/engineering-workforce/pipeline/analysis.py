"""Analysis library for the engineer-share panel — panel-agnostic.

Everything here operates on a tidy panel with columns ``entity, year,
definition, share_per_100k`` (plus optional ``confidence``), so it runs
identically on the synthetic panel today and the real panel later.

Contents:
- ``series()``            — extract one clean (year, share) series.
- ``detect_changepoints()`` — piecewise-log-linear structural breaks via
  dynamic programming, model order chosen by BIC. Dates the inflections
  (industrial takeoff, later regime shifts).
- ``fit_regimes()``      — growth rate within each regime (between breaks).
- ``growth_table()``     — regimes for every entity/definition in a panel.
- ``cross_country_snapshot()`` — level comparison at a given year.
- ``counterfactual_modern_share()`` — bounded pre-1900 "modern-standard"
  scenario estimate (explicit assumptions, low/central/high band), for task A-02.

These are the mechanics the first claim's formal test (A-03) calls. They are
unit-tested to recover known breaks from the synthetic ground truth.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# series extraction
# --------------------------------------------------------------------------- #
def series(panel: pd.DataFrame, entity: str, definition: str) -> pd.DataFrame:
    """Return a sorted, positive-share (year, share_per_100k) frame for one series."""
    g = panel[(panel["entity"] == entity) & (panel["definition"] == definition)].copy()
    g = g.dropna(subset=["share_per_100k"])
    g = g[g["share_per_100k"] > 0].sort_values("year")
    return g[["year", "share_per_100k"]].reset_index(drop=True)


# --------------------------------------------------------------------------- #
# structural-break detection (piecewise linear on log share)
# --------------------------------------------------------------------------- #
def _segment_costs(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """cost[i, j] = SSR of an OLS line fit to points i..j (inclusive)."""
    n = len(x)
    cost = np.full((n, n), np.inf)
    for i in range(n):
        for j in range(i, n):
            if j - i < 1:
                cost[i, j] = 0.0
                continue
            xs, ys = x[i : j + 1], y[i : j + 1]
            a, b = np.polyfit(xs, ys, 1)
            resid = ys - (a * xs + b)
            cost[i, j] = float(resid @ resid)
    return cost


def _best_partition(cost: np.ndarray, m: int) -> tuple[float, list[int]]:
    """Min-SSR partition of n points into m contiguous segments (DP).

    Returns (total_cost, break_indices) where break_indices are the first index
    of each segment after the first (length m-1).
    """
    n = cost.shape[0]
    # dp[k][j] = best cost to cover points 0..j with k segments
    dp = np.full((m + 1, n), np.inf)
    prev = np.full((m + 1, n), -1, dtype=int)
    dp[1] = cost[0]
    for k in range(2, m + 1):
        for j in range(k - 1, n):
            for i in range(k - 2, j):
                c = dp[k - 1][i] + cost[i + 1][j]
                if c < dp[k][j]:
                    dp[k][j] = c
                    prev[k][j] = i
    # backtrack
    breaks: list[int] = []
    j = n - 1
    k = m
    while k > 1:
        i = prev[k][j]
        breaks.append(i + 1)
        j = i
        k -= 1
    return float(dp[m][n - 1]), sorted(breaks)


@dataclass
class BreakModel:
    n_regimes: int
    break_years: list[int]
    bic: float
    ssr: float


def detect_changepoints(df: pd.DataFrame, max_regimes: int = 4, min_size: int = 8) -> BreakModel:
    """Detect structural breaks in log(share) over time; pick #regimes by BIC.

    ``df`` has columns (year, share_per_100k). Fits piecewise-linear models with
    1..max_regimes segments and selects the order minimising BIC. Returns the
    break *years*.
    """
    d = df.dropna().sort_values("year")
    x = d["year"].to_numpy(float)
    y = np.log(d["share_per_100k"].to_numpy(float))
    n = len(x)
    if n < 2 * min_size:
        return BreakModel(1, [], np.nan, float("nan"))
    cost = _segment_costs(x, y)
    max_regimes = max(1, min(max_regimes, n // min_size))

    best: BreakModel | None = None
    for m in range(1, max_regimes + 1):
        if m == 1:
            ssr, breaks = float(cost[0][n - 1]), []
        else:
            ssr, idx = _best_partition(cost, m)
            # enforce minimum segment size
            bounds = [0, *idx, n]
            if any((bounds[t + 1] - bounds[t]) < min_size for t in range(len(bounds) - 1)):
                continue
            breaks = [int(x[i]) for i in idx]
        params = 2 * m + (m - 1)  # slope+intercept per segment + break locations
        sigma2 = max(ssr / n, 1e-12)
        bic = n * np.log(sigma2) + params * np.log(n)
        if best is None or bic < best.bic:
            best = BreakModel(m, breaks, float(bic), float(ssr))
    return best if best is not None else BreakModel(1, [], np.nan, float(cost[0][n - 1]))


# --------------------------------------------------------------------------- #
# growth regimes
# --------------------------------------------------------------------------- #
@dataclass
class Regime:
    year_from: int
    year_to: int
    annual_growth: float
    start_share: float
    end_share: float


def fit_regimes(df: pd.DataFrame, break_years: list[int]) -> list[Regime]:
    """Annualised growth of the share within each regime defined by break_years."""
    d = df.dropna().sort_values("year").reset_index(drop=True)
    x = d["year"].to_numpy(float)
    y = np.log(d["share_per_100k"].to_numpy(float))
    edges = [x[0], *break_years, x[-1] + 1]
    regimes: list[Regime] = []
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        mask = (x >= lo) & (x < hi)
        if mask.sum() < 2:
            continue
        slope, _ = np.polyfit(x[mask], y[mask], 1)
        regimes.append(
            Regime(
                year_from=int(x[mask][0]),
                year_to=int(x[mask][-1]),
                annual_growth=float(np.exp(slope) - 1),
                start_share=float(np.exp(y[mask][0])),
                end_share=float(np.exp(y[mask][-1])),
            )
        )
    return regimes


def growth_table(panel: pd.DataFrame, **kw) -> pd.DataFrame:
    """Detect breaks + growth regimes for every (entity, definition) in a panel."""
    rows = []
    for (entity, definition), _ in panel.groupby(["entity", "definition"]):
        s = series(panel, entity, definition)
        if len(s) < 4:
            continue
        model = detect_changepoints(s, **kw)
        for r in fit_regimes(s, model.break_years):
            rows.append(
                {
                    "entity": entity,
                    "definition": definition,
                    "year_from": r.year_from,
                    "year_to": r.year_to,
                    "annual_growth_pct": 100 * r.annual_growth,
                    "start_share": r.start_share,
                    "end_share": r.end_share,
                    "break_years": ",".join(map(str, model.break_years)),
                }
            )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# cross-country comparison
# --------------------------------------------------------------------------- #
def cross_country_snapshot(
    panel: pd.DataFrame, year: int, definition: str, tol: int = 3
) -> pd.DataFrame:
    """Engineer share for every entity at (nearest year within tol) `year`."""
    rows = []
    for entity, g in panel[panel["definition"] == definition].groupby("entity"):
        g = g.dropna(subset=["share_per_100k"])
        if g.empty:
            continue
        nearest = g.iloc[(g["year"] - year).abs().argmin()]
        if abs(int(nearest["year"]) - year) <= tol:
            rows.append(
                {
                    "entity": entity,
                    "year": int(nearest["year"]),
                    "share_per_100k": float(nearest["share_per_100k"]),
                }
            )
    cols = ["entity", "year", "share_per_100k"]
    if not rows:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows).sort_values("share_per_100k", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# pre-1900 "modern-standard" counterfactual (task A-02)
# --------------------------------------------------------------------------- #
def counterfactual_modern_share(
    technical_workforce_share: float,
    engineer_fraction_of_technical: dict[str, float],
) -> dict[str, float]:
    """Bounded estimate of the *modern-standard* engineer share in a pre-modern era.

    The pre-1900 "would they qualify as a modern engineer?" count is a
    counterfactual, so we express it as an explicit scenario band rather than a
    point estimate. Given the share of the workforce in technical/mechanical
    trades and a low/central/high assumption for what fraction of them would meet
    a modern engineering bar, return engineers per 100k population under each
    scenario. (Assumes labour-force participation ~40% of population as a rough,
    documented constant; callers should sensitivity-test it.)

    This is scaffolding: plug real trade-share estimates in when available.
    """
    lf_participation = 0.40
    out = {}
    for scenario, frac in engineer_fraction_of_technical.items():
        engineers_per_capita = lf_participation * technical_workforce_share * frac
        out[scenario] = engineers_per_capita * 1e5
    return out
