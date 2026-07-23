"""Exploratory analysis of the engineer-share panel.

Runnable as a script (also openable as a notebook). It loads the analysis panel,
plots the long-run engineer share on a log scale, and runs the *assessment
machinery* — log-linear trend fits and anchor-to-anchor growth rates — that the
formal claim tests will build on.

IMPORTANT: with the numerator sources still egress-blocked, the panel is built
from provisional, literature-transcribed anchors (``confidence ==
'literature_unverified'``). Everything below is therefore a *methods
demonstration and preliminary read*, not a result. A formal changepoint test
(task A-03) needs the dense primary series (IPUMS/BLS/UIS/...), not a handful of
anchors.

Run:
    uv run python sections/engineering-workforce/notebooks/00_explore_panel.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from quasioptimal.data import load_processed
from quasioptimal.paths import processed_dir, section_dir
from quasioptimal.viz import new_axes

FIG_DIR = section_dir("engineering-workforce") / "notebooks" / "figures"


def load_panel() -> pd.DataFrame:
    return load_processed(processed_dir("engineering-workforce") / "panel.parquet")


def growth_between_anchors(df: pd.DataFrame) -> pd.DataFrame:
    """Compound annual growth rate of the share between consecutive anchors."""
    rows = []
    for (entity, definition), g in df.dropna(subset=["share_per_100k"]).groupby(
        ["entity", "definition"]
    ):
        g = g.sort_values("year")
        for (y0, s0), (y1, s1) in zip(
            g[["year", "share_per_100k"]].values[:-1],
            g[["year", "share_per_100k"]].values[1:],
            strict=False,
        ):
            if y1 > y0 and s0 > 0:
                cagr = (s1 / s0) ** (1 / (y1 - y0)) - 1
                rows.append((entity, definition, int(y0), int(y1), s0, s1, cagr))
    return pd.DataFrame(
        rows,
        columns=["entity", "definition", "year_from", "year_to", "share_from", "share_to", "cagr"],
    )


def fit_loglinear_trend(g: pd.DataFrame) -> dict | None:
    """OLS of log(share) on year; returns slope as an implied annual growth rate.

    Needs >= 3 points to be meaningful. Real structural-break testing (Bai-Perron
    / Bayesian changepoint) is deferred to the dense-series stage (task A-03).
    """
    g = g.dropna(subset=["share_per_100k"])
    g = g[g["share_per_100k"] > 0]
    if g["year"].nunique() < 3:
        return None
    x = g["year"].to_numpy(float)
    y = np.log(g["share_per_100k"].to_numpy(float))
    slope, intercept = np.polyfit(x, y, 1)
    return {"annual_growth": np.exp(slope) - 1, "n": len(g)}


def plot_longrun(df: pd.DataFrame) -> Path:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = new_axes(
        title="Engineers per 100,000 population (PROVISIONAL — literature anchors)",
        xlabel="Year",
        ylabel="Engineers per 100k (log scale)",
    )
    markers = {"contemporary": "o", "modern": "s"}
    for (entity, definition), g in df.dropna(subset=["share_per_100k"]).groupby(
        ["entity", "definition"]
    ):
        g = g.sort_values("year")
        ax.plot(
            g["year"],
            g["share_per_100k"],
            marker=markers.get(definition, "o"),
            label=f"{entity} ({definition})",
        )
    ax.set_yscale("log")
    ax.legend(fontsize=8, ncol=2)
    ax.figure.text(
        0.01,
        0.01,
        "Provisional literature_unverified anchors — not a result.",
        fontsize=7,
        style="italic",
        alpha=0.7,
    )
    out = FIG_DIR / "longrun_share_provisional.png"
    fig.savefig(out)
    return out


def main() -> int:
    df = load_panel()
    if len(df) == 0:
        print("Panel is empty — no numerators yet. Fill a G-* source and re-run the pipeline.")
        return 0

    n_prov = int((df["confidence"] == "literature_unverified").sum())
    print(f"Panel: {len(df)} rows ({n_prov} provisional literature_unverified).")
    if n_prov == len(df):
        print("!! ALL rows are provisional literature anchors. Preliminary read only. !!\n")

    print("Anchor-to-anchor growth in engineer share (per 100k):")
    print(growth_between_anchors(df).to_string(index=False))

    print("\nLog-linear trend fits (entities with >=3 anchors):")
    any_fit = False
    for entity, g in df.groupby("entity"):
        fit = fit_loglinear_trend(g)
        if fit:
            any_fit = True
            print(
                f"  {entity}: implied {fit['annual_growth'] * 100:.1f}%/yr over {fit['n']} points"
            )
    if not any_fit:
        print("  (none dense enough yet — formal trend/changepoint tests await primary data)")

    out = plot_longrun(df)
    print(f"\nFigure -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
