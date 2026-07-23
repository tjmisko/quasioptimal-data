# quasioptimal-data

Data analysis backing quasioptimal claims. The repo is organized into
**sections** (broad topics) and, within each, **claims** — falsifiable
statements we try to substantiate or refute with data and formal statistical
tests.

## Quickstart

```bash
uv sync --extra notebooks   # set up the environment
uv run pytest               # run tests
uv run ruff check .         # lint
uv run jupyter lab          # exploratory analysis
```

## Layout

- `src/quasioptimal/` — shared utilities (paths, provenance-aware data I/O, plot style).
- `sections/` — one directory per topic; see `sections/README.md`.
- `CLAUDE.md` — full orientation and conventions. **Start there.**

## Sections

| Section | Topic |
| --- | --- |
| [`engineering-workforce`](sections/engineering-workforce/) | Long-run trends in formally trained engineers as a share of population (global + by country), back to ~1500. |
