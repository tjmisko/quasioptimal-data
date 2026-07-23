"""quasioptimal: shared utilities for section/claim-organized data analysis.

The repository is organized into *sections* (broad topics) and, within each
section, *claims* that we try to substantiate or refute with data. This package
holds cross-cutting helpers so that per-claim analysis code stays thin and
consistent: locating the repo and data directories, loading/saving processed
datasets with provenance, and a shared plotting style.
"""

from quasioptimal.paths import (
    data_dir,
    processed_dir,
    raw_dir,
    repo_root,
    section_dir,
)

__all__ = [
    "repo_root",
    "section_dir",
    "data_dir",
    "raw_dir",
    "processed_dir",
]

__version__ = "0.1.0"
