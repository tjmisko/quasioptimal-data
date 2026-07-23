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
| `mirrors-*.md` | GitHub-mirror hunt results (curl-verified reachable mirrors of blocked sources). |
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
synthetic.py           # dense SYNTHETIC panel (*_synth.parquet) for developing the stack
analysis.py            # changepoint / growth-regime / cross-country / counterfactual (panel-agnostic)
report.py              # publication figures + markdown report from any panel (watermarked)
```

The analysis stack (`synthetic`, `analysis`, `report`, and `../claims/*/test.py`)
is **swap-in ready**: it runs on the synthetic panel today and on the real panel
(same commands, `--panel …/panel.parquet`) once numerators land.

Run the whole thing:

```bash
uv run python sections/engineering-workforce/pipeline/fetch.py
uv run python sections/engineering-workforce/pipeline/prepare_population.py
uv run python sections/engineering-workforce/pipeline/prepare_engineers.py
uv run python sections/engineering-workforce/pipeline/build_panel.py
uv run python sections/engineering-workforce/notebooks/00_explore_panel.py
```

## GitHub-mirror hunt (2026-07-23)

Because only `raw.githubusercontent.com` is reachable, a fan-out searched GitHub
for mirrors of the blocked sources. Findings (curl-verified HTTP 200) are in
`mirrors-population.md`, `mirrors-numerators-modern.md`, `mirrors-historical.md`.
Confirmed mirrors were folded into `sources.yaml` (`reachable: here`).

## Current state (2026-07-23)

- **Reachable & fetched (7):** a now-rich **denominator** — `owid-co2-population`
  (annual World+country pop 1750-2024 + Maddison-2023 GDP), `maddison-2020`
  (pre-1750 country benchmarks), `world-historical-population` (World back to
  10000 BCE), `california-population` (CA 1900+, closing the state gap),
  `worldbank-population`; a partial **numerator** `bls-oews` (US engineers 2021,
  national, real/primary); and `barro-lee` educational attainment (A-02 covariate).
- **Still blocked (25):** most primary numerators (IPUMS, Census, NCES/NSF,
  UNESCO counts, ILO ISCO-214, OECD, China MOE/NBS, Nomis, Engineering Council,
  Destatis, historical scans/books) have no GitHub mirror and return HTTP 403.
  Captured as `G-*` cards for a web-capable environment or a logged-in human.
- **Numerators today** = one real point (US 2021, BLS) + the provisional seed, so
  the panel remains a **preliminary read, not a result.** Seed rows must be
  replaced by primary pulls before backing any claim.
- **Development stack is complete and swap-in ready** — see `../pipeline/`
  (`synthetic.py`, `analysis.py`, `report.py`) and `../claims/`: the analysis,
  figures, report, and first claim's formal test all run now on dense synthetic
  data and switch to real data by changing the input path.

## Adding a source

Append an entry to `sources.yaml` (copy the field template at its top), add a
matching card to `TASKS.md`, and — for a numerator — a `prepare_<source>()` in
`pipeline/prepare_engineers.py` that emits the `SCHEMA.md` shape.
