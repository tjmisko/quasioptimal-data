"""Shared helpers for claim test scripts (data loading + provenance banner)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from quasioptimal.data import load_processed
from quasioptimal.paths import processed_dir, section_dir

sys.path.insert(0, str(section_dir("engineering-workforce") / "pipeline"))


def default_paths(real: bool) -> tuple[Path, Path]:
    pdir = processed_dir("engineering-workforce")
    suffix = "" if real else "_synth"
    return pdir / f"panel{suffix}.parquet", pdir / f"covariates_long{suffix}.parquet"


def load(panel_path: Path, cov_path: Path | None = None):
    panel = load_processed(panel_path)
    cov = load_processed(cov_path) if cov_path and Path(cov_path).exists() else None
    return panel, cov


def provenance(df: pd.DataFrame) -> str:
    conf = set(df.get("confidence").dropna().unique()) if "confidence" in df else set()
    if "synthetic" in conf:
        return "SYNTHETIC (demonstration only — not a result)"
    if "literature_unverified" in conf:
        return "PROVISIONAL (unverified anchors — not a result)"
    return "REAL"
