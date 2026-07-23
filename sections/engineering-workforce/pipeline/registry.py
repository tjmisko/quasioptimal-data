"""Load and query the data-source registry (``data_acquisition/sources.yaml``)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

SECTION = "engineering-workforce"


def _section_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def sources_yaml_path() -> Path:
    return _section_dir() / "data_acquisition" / "sources.yaml"


def raw_path(raw_name: str) -> Path:
    return _section_dir() / "data" / "raw" / raw_name


@dataclass
class Source:
    id: str
    name: str
    role: str
    reachable: str
    method: str
    status: str
    url: str = ""
    raw: str | None = None
    metric: str = "n/a"
    definition: str = "n/a"
    priority: int = 3
    task: str = ""
    geography: list | None = None
    years: str = ""
    provider: str = ""
    notes: str = ""

    @property
    def raw_file(self) -> Path | None:
        return raw_path(self.raw) if self.raw else None


def load_sources() -> list[Source]:
    data = yaml.safe_load(sources_yaml_path().read_text())
    out = []
    for entry in data["sources"]:
        known = {f: entry.get(f) for f in Source.__dataclass_fields__ if f in entry}
        out.append(Source(**known))
    return out


def get_source(source_id: str) -> Source:
    for s in load_sources():
        if s.id == source_id:
            return s
    raise KeyError(f"No source {source_id!r} in {sources_yaml_path()}")


def by_reachability(reachable: str) -> list[Source]:
    return [s for s in load_sources() if s.reachable == reachable]
