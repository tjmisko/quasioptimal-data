# Data acquisition — Engineering Workforce

The framework for turning the scouted sources (in `../research/`) into
analysis-ready series. Designed so work can be handed to agents or people.

## Pieces

| File | Role |
| --- | --- |
| `sources.yaml` | **Registry** — every dataset we want, with access method, reachability, target path, and owning task. Single source of truth (read by the pipeline). |
| `TASKS.md` | **Task board** — handoff-ready Gather / Prepare / Analyze cards, each with a definition of done. IDs match `sources.yaml`. |
| `SCHEMA.md` | **Contract** — the canonical processed-table shapes prepare tasks must emit. |
| `seed/engineers_anchors.csv` | **Provisional** literature-transcribed anchor points (`confidence = literature_unverified`), used only until primary numerators land. Not data. |
| `fetch_log.csv` | Written by `fetch.py`: URL, bytes, sha256 of each raw pull (reproducibility; raw files themselves are git-ignored). |

## Pipeline (in `../pipeline/`)

```
fetch.py            # download reachable sources -> data/raw/ ; report blocked ones
  --status          # print the source status table
prepare_population.py  # Maddison(+WB) -> processed/population_long.parquet
prepare_engineers.py   # primary transforms (+ provisional seed) -> engineers_long.parquet
  --no-seed            #   primary sources only, exclude the provisional anchors
build_panel.py         # join -> processed/panel.parquet (share_per_100k)
schema.py / registry.py  # canonical schema + validators; sources.yaml loader
```

Run the whole thing:

```bash
uv run python sections/engineering-workforce/pipeline/fetch.py
uv run python sections/engineering-workforce/pipeline/prepare_population.py
uv run python sections/engineering-workforce/pipeline/prepare_engineers.py
uv run python sections/engineering-workforce/pipeline/build_panel.py
uv run python sections/engineering-workforce/notebooks/00_explore_panel.py
```

## Current state (2026-07-23)

- **Reachable & fetched:** the population denominator (Maddison 2020 + World Bank),
  via `raw.githubusercontent.com` — the only host the session egress policy allows.
- **Blocked (26 sources):** every primary numerator host (IPUMS, BLS, Census, NCES,
  NSF, UNESCO, ILO, Eurostat, OECD, China MOE/NBS, Nomis, Engineering Council,
  Destatis, rug.nl, Bank of England, ...) returns HTTP 403 at the egress gateway.
  These are captured as G-* task cards for a web-capable environment or a
  logged-in human. Per proxy policy we do not retry policy denials.
- **Numerator today** = the provisional seed only, so the panel is a **methods
  demonstration and preliminary read, not a result.** Every seed row must be
  replaced by a primary pull (its G-*/P-* task) before backing any claim.

## Adding a source

Append an entry to `sources.yaml` (copy the field template at its top), add a
matching card to `TASKS.md`, and — for a numerator — a `prepare_<source>()` in
`pipeline/prepare_engineers.py` that emits the `SCHEMA.md` shape.
