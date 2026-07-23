"""Smoke tests for path resolution and the provenance-aware data helpers."""

from __future__ import annotations

import pandas as pd

from quasioptimal import data as qdata
from quasioptimal import paths


def test_repo_root_has_expected_markers():
    root = paths.repo_root()
    assert (root / "pyproject.toml").is_file()
    assert (root / "sections").is_dir()


def test_engineering_section_exists():
    section = paths.section_dir("engineering-workforce")
    assert section.is_dir()
    assert (section / "data").is_dir()


def test_save_and_load_roundtrip_with_meta(tmp_path):
    df = pd.DataFrame({"year": [1500, 2000], "value": [1.0, 2.0]})
    out = qdata.save_processed(
        df,
        tmp_path / "example",
        source="unit test",
        description="roundtrip fixture",
        notes="synthetic",
    )
    assert out.exists()
    loaded = qdata.load_processed(out)
    pd.testing.assert_frame_equal(df, loaded)
    meta = qdata.read_meta(out)
    assert meta["source"] == "unit test"
    assert meta["rows"] == 2
