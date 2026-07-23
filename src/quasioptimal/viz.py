"""Shared plotting defaults so figures across claims look consistent."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt


def set_style() -> None:
    """Apply the repository's default matplotlib style (idempotent)."""
    mpl.rcParams.update(
        {
            "figure.figsize": (9, 5.5),
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "font.size": 11,
        }
    )


def new_axes(title: str = "", xlabel: str = "", ylabel: str = ""):
    """Return a styled ``(fig, ax)`` with common labels set."""
    set_style()
    fig, ax = plt.subplots()
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    return fig, ax
