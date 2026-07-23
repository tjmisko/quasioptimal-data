"""Tests for the engineering-workforce pipeline schema and panel join."""

from __future__ import annotations

import sys

import pandas as pd
import pytest

from quasioptimal.paths import section_dir

PIPELINE = section_dir("engineering-workforce") / "pipeline"
sys.path.insert(0, str(PIPELINE))

import schema  # noqa: E402


def _eng_row(**kw):
    base = {
        "entity": "United States",
        "iso3": "USA",
        "year": 1920,
        "definition": "contemporary",
        "metric": "stock",
        "engineers": 136000.0,
        "method": "census",
        "source_id": "edwards-1943",
        "source_definition": "US census engineers",
        "confidence": "literature_unverified",
        "notes": "",
    }
    base.update(kw)
    return base


def test_validate_engineers_rejects_bad_metric():
    df = pd.DataFrame([_eng_row(metric="membership")])
    with pytest.raises(schema.SchemaError):
        schema.validate_engineers(df)


def test_validate_engineers_rejects_bad_definition():
    df = pd.DataFrame([_eng_row(definition="futuristic")])
    with pytest.raises(schema.SchemaError):
        schema.validate_engineers(df)


def test_build_panel_computes_share_and_drops_flows():
    eng = pd.DataFrame(
        [
            _eng_row(engineers=136000.0, metric="stock"),
            _eng_row(engineers=50000.0, metric="annual_flow"),  # should be dropped
        ]
    )
    pop = pd.DataFrame(
        [
            {
                "entity": "United States",
                "iso3": "USA",
                "year": 1920,
                "population": 106_881_000.0,
                "source_id": "maddison-2020",
                "notes": "",
            }
        ]
    )
    panel = schema.build_panel(eng, pop)
    assert len(panel) == 1  # flow row dropped
    share = panel.iloc[0]["share_per_100k"]
    assert share == pytest.approx(1e5 * 136000 / 106_881_000, rel=1e-9)


def test_canonical_entities_have_iso3():
    assert schema.CANONICAL_ENTITIES["World"] == "WLD"
    assert schema.CANONICAL_ENTITIES["California"] == "US-CA"
