"""Load/save processed datasets with lightweight provenance.

We keep raw downloads immutable under ``data/raw`` and write analysis-ready
tables to ``data/processed``. Each processed table is saved as Parquet plus a
sidecar ``.meta.yaml`` recording where it came from, so a reader can always
trace a number back to its source.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def save_processed(
    df: pd.DataFrame,
    path: str | Path,
    *,
    source: str,
    description: str,
    notes: str | None = None,
    **extra: Any,
) -> Path:
    """Write ``df`` to Parquet at ``path`` with a ``.meta.yaml`` provenance sidecar.

    Parameters
    ----------
    df:
        Analysis-ready table.
    path:
        Destination ``.parquet`` path (parents are created).
    source:
        Human-readable citation or URL for where the underlying data came from.
    description:
        One line on what this table contains.
    notes:
        Optional caveats, cleaning decisions, or definitional notes.
    extra:
        Any additional key/values to record in the sidecar (e.g. ``retrieved``).
    """
    path = Path(path)
    if path.suffix != ".parquet":
        path = path.with_suffix(".parquet")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

    meta: dict[str, Any] = {
        "description": description,
        "source": source,
        "rows": int(len(df)),
        "columns": list(map(str, df.columns)),
    }
    if notes:
        meta["notes"] = notes
    meta.update(extra)
    path.with_suffix(".meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False))
    return path


def load_processed(path: str | Path) -> pd.DataFrame:
    """Read a processed Parquet table written by :func:`save_processed`."""
    path = Path(path)
    if path.suffix != ".parquet":
        path = path.with_suffix(".parquet")
    return pd.read_parquet(path)


def read_meta(path: str | Path) -> dict[str, Any]:
    """Read the ``.meta.yaml`` provenance sidecar for a processed table."""
    path = Path(path).with_suffix(".meta.yaml")
    return yaml.safe_load(path.read_text())
