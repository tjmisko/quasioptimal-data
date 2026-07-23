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
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, grangercausalitytests


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
# engineers vs covariates: merge helper
# --------------------------------------------------------------------------- #
def entity_frame(
    panel: pd.DataFrame,
    covariates: pd.DataFrame,
    entity: str,
    definition: str = "contemporary",
) -> pd.DataFrame:
    """Wide per-entity time series: engineers + population + each covariate by year."""
    e = panel[(panel["entity"] == entity) & (panel["definition"] == definition)]
    e = e[["year", "engineers", "population", "share_per_100k"]].dropna(subset=["engineers"])
    wide = covariates[covariates["entity"] == entity].pivot_table(
        index="year", columns="variable", values="value", aggfunc="first"
    )
    out = e.merge(wide, on="year", how="inner").sort_values("year").reset_index(drop=True)
    return out


# --------------------------------------------------------------------------- #
# H1: quasi-exponential growth
# --------------------------------------------------------------------------- #
def test_exponential_growth(df: pd.DataFrame, value_col: str, since: int = 1800) -> dict:
    """Is `value_col` growing quasi-exponentially since `since`?

    Fits log(value) ~ year (exponential) and log(value) ~ year + year^2. Exponential
    growth => high R^2 of the linear-in-log fit and an insignificant quadratic term
    (constant growth rate). Returns the implied annual growth (CAGR), R^2, and the
    quadratic-term p-value (curvature test).
    """
    d = df[df["year"] >= since].dropna(subset=[value_col])
    d = d[d[value_col] > 0]
    if len(d) < 6:
        return {"n": len(d), "insufficient": True}
    x = d["year"].to_numpy(float)
    y = np.log(d[value_col].to_numpy(float))
    xc = x - x.mean()
    lin = sm.OLS(y, sm.add_constant(xc)).fit()
    quad = sm.OLS(y, sm.add_constant(np.column_stack([xc, xc**2]))).fit()
    return {
        "n": int(len(d)),
        "since": int(since),
        "annual_growth": float(np.exp(lin.params[1]) - 1),
        "r2_loglinear": float(lin.rsquared),
        "quad_term_pvalue": float(quad.pvalues[2]),
        "constant_growth": bool(quad.pvalues[2] > 0.05),
    }


# --------------------------------------------------------------------------- #
# H2/H3: elasticity + cointegration (does E track GDP / capital?)
# --------------------------------------------------------------------------- #
def elasticity(df: pd.DataFrame, y_col: str, x_col: str) -> dict:
    """Log-log OLS elasticity d log(y)/d log(x), with an Engle-Granger cointegration
    check (ADF on the regression residuals) to guard against spurious level regression."""
    d = df.dropna(subset=[y_col, x_col])
    d = d[(d[y_col] > 0) & (d[x_col] > 0)]
    if len(d) < 12:
        return {"n": len(d), "insufficient": True}
    ly = np.log(d[y_col].to_numpy(float))
    lx = np.log(d[x_col].to_numpy(float))
    fit = sm.OLS(ly, sm.add_constant(lx)).fit()
    resid = ly - fit.predict(sm.add_constant(lx))
    adf_p = float(adfuller(resid, autolag="AIC")[1])
    ci = fit.conf_int()[1]
    return {
        "n": int(len(d)),
        "elasticity": float(fit.params[1]),
        "se": float(fit.bse[1]),
        "ci95": [float(ci[0]), float(ci[1])],
        "r2": float(fit.rsquared),
        "coint_adf_pvalue": adf_p,
        "cointegrated": bool(adf_p < 0.05),
    }


def multiple_regression(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> dict:
    """Log-log multiple regression: partial elasticities of y wrt each x (controls)."""
    cols = [y_col, *x_cols]
    d = df.dropna(subset=cols)
    for c in cols:
        d = d[d[c] > 0]
    if len(d) < 12:
        return {"n": len(d), "insufficient": True}
    y = np.log(d[y_col].to_numpy(float))
    X = np.column_stack([np.log(d[c].to_numpy(float)) for c in x_cols])
    fit = sm.OLS(y, sm.add_constant(X)).fit()
    return {
        "n": int(len(d)),
        "params": dict(zip(["const", *x_cols], map(float, fit.params), strict=True)),
        "pvalues": dict(zip(["const", *x_cols], map(float, fit.pvalues), strict=True)),
        "r2": float(fit.rsquared),
    }


# --------------------------------------------------------------------------- #
# causality direction (Granger, on stationary differenced logs)
# --------------------------------------------------------------------------- #
def granger_direction(df: pd.DataFrame, a_col: str, b_col: str, maxlag: int = 6) -> dict:
    """Test Granger-causality both ways between a and b (log, differenced to
    stationarity). Returns the best (smallest) p-value in each direction and the
    inferred lead. Small p for a->b means past a helps predict b."""
    d = df.dropna(subset=[a_col, b_col])
    d = d[(d[a_col] > 0) & (d[b_col] > 0)]
    if len(d) < maxlag * 3 + 5:
        return {"n": len(d), "insufficient": True}
    la = np.diff(np.log(d[a_col].to_numpy(float)))
    lb = np.diff(np.log(d[b_col].to_numpy(float)))

    def _best_p(cause: np.ndarray, effect: np.ndarray) -> float:
        data = np.column_stack([effect, cause])  # tests whether col2 causes col1
        res = grangercausalitytests(data, maxlag=maxlag, verbose=False)
        return min(res[lag][0]["ssr_ftest"][1] for lag in res)

    p_a_to_b = _best_p(la, lb)
    p_b_to_a = _best_p(lb, la)
    direction = (
        f"{a_col} -> {b_col}"
        if p_a_to_b < 0.05 <= p_b_to_a
        else f"{b_col} -> {a_col}"
        if p_b_to_a < 0.05 <= p_a_to_b
        else "bidirectional"
        if p_a_to_b < 0.05 and p_b_to_a < 0.05
        else "inconclusive"
    )
    return {
        "n": int(len(d)),
        f"p_{a_col}_causes_{b_col}": p_a_to_b,
        f"p_{b_col}_causes_{a_col}": p_b_to_a,
        "direction": direction,
    }


def lead_lag(df: pd.DataFrame, a_col: str, b_col: str, max_lag: int = 40) -> dict:
    """Cross-correlate growth rates to find the lag at peak correlation.

    Returns ``best_lag`` where a positive value means `a_col` LEADS `b_col` by that
    many years (past a predicts b) — a robust direction diagnostic for smooth,
    co-trending series where Granger tests are ambiguous.
    """
    d = df.dropna(subset=[a_col, b_col])
    d = d[(d[a_col] > 0) & (d[b_col] > 0)].sort_values("year")
    if len(d) < max_lag + 10:
        return {"n": len(d), "insufficient": True}
    ga = np.diff(np.log(d[a_col].to_numpy(float)))
    gb = np.diff(np.log(d[b_col].to_numpy(float)))
    ga = (ga - ga.mean()) / (ga.std() + 1e-12)
    gb = (gb - gb.mean()) / (gb.std() + 1e-12)
    best_lag, best_corr = 0, -np.inf
    for k in range(-max_lag, max_lag + 1):
        if k >= 0:
            x, y = ga[: len(ga) - k], gb[k:]
        else:
            x, y = ga[-k:], gb[: len(gb) + k]
        if len(x) < 10:
            continue
        corr = float(np.corrcoef(x, y)[0, 1])
        if corr > best_corr:
            best_corr, best_lag = corr, k
    leader = a_col if best_lag > 0 else b_col if best_lag < 0 else "contemporaneous"
    return {
        "n": int(len(d)),
        "best_lag": best_lag,
        "peak_corr": best_corr,
        "interpretation": f"{leader} leads by {abs(best_lag)} yr"
        if best_lag
        else "contemporaneous",
    }


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
