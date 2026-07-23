"""Filesystem helpers for locating the repo, sections, and their data dirs.

These functions let analysis code (scripts and notebooks) reference data by
*section name* rather than by fragile relative paths, so a notebook works the
same regardless of the directory it is launched from.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def repo_root() -> Path:
    """Return the repository root (the directory containing ``pyproject.toml``).

    Walks upward from this file, then from the current working directory, so it
    resolves correctly whether imported from an installed package or a notebook.
    """
    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / "pyproject.toml").is_file() and (candidate / "sections").is_dir():
                return candidate
    raise FileNotFoundError(
        "Could not locate the repository root (a directory with pyproject.toml and sections/)."
    )


def sections_root() -> Path:
    """Return the top-level ``sections/`` directory."""
    return repo_root() / "sections"


def section_dir(section: str) -> Path:
    """Return the directory for a named section, erroring if it does not exist."""
    path = sections_root() / section
    if not path.is_dir():
        available = sorted(p.name for p in sections_root().iterdir() if p.is_dir())
        raise FileNotFoundError(f"No section {section!r}. Available: {available}")
    return path


def data_dir(section: str) -> Path:
    """Return ``sections/<section>/data``."""
    return section_dir(section) / "data"


def raw_dir(section: str) -> Path:
    """Return the raw (immutable, as-downloaded) data dir for a section."""
    path = data_dir(section) / "raw"
    path.mkdir(parents=True, exist_ok=True)
    return path


def processed_dir(section: str) -> Path:
    """Return the processed (analysis-ready) data dir for a section."""
    path = data_dir(section) / "processed"
    path.mkdir(parents=True, exist_ok=True)
    return path
