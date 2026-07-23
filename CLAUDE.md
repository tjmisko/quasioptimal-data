# CLAUDE.md

Orientation for working in this repository. Read this first.

## What this repo is

`quasioptimal-data` holds the **data analysis that backs up claims** made in the
quasioptimal project. The unit of work is a *claim*: a specific, falsifiable
statement that we try to **substantiate or refute** with data and formal
statistical tests.

The intended workflow for every claim is:

1. **Explore** — open-ended exploratory analysis in some topic area.
2. **Formulate** — distill a precise, testable claim (with a null hypothesis).
3. **Test** — set up formal statistical test(s) and run them on the data.
4. **Conclude** — record whether the data support, refute, or are inconclusive
   about the claim, with the evidence and its caveats.

We favor being explicit about uncertainty, data provenance, and the exact
definitions behind every number. A claim is only as good as the data and the
definitions under it.

## Repository structure

The repo is organized into **sections** (broad topics), and within each section
into **claims**.

```
quasioptimal-data/
├── CLAUDE.md                 # this file
├── pyproject.toml            # deps + tooling (managed with uv)
├── uv.lock                   # pinned, reproducible environment
├── src/quasioptimal/         # shared, cross-cutting utilities (installable pkg)
│   ├── paths.py              #   locate repo / sections / data dirs by name
│   ├── data.py               #   save/load processed tables + provenance sidecars
│   └── viz.py                #   shared matplotlib style
├── tests/                    # tests for the shared package
└── sections/
    ├── README.md             # index of sections + the section/claim conventions
    └── <section-name>/
        ├── README.md         # what this section is about; index of its claims
        ├── PLAN.md           # exploration + data-search plan for the section
        ├── research/         # literature review + data-source scouting notes
        ├── data/
        │   ├── raw/          # immutable, as-downloaded source files (git-ignored)
        │   └── processed/    # analysis-ready tables (.parquet + .meta.yaml), committed
        ├── notebooks/        # exploratory analysis
        └── claims/
            ├── README.md      # claims register for the section
            └── <claim-slug>/  # one directory per claim (created as claims form)
```

A **claim directory** (created when a claim has been formulated) should contain
its own `README.md` stating the claim, the null hypothesis, the test(s) used,
and the conclusion — plus the code/notebook that produces the result.

## Toolchain

Standard modern Python data stack, managed with **uv**.

```bash
uv sync --extra notebooks      # create/refresh the environment
uv run pytest                  # run tests
uv run ruff check .            # lint
uv run ruff format .           # format
uv run jupyter lab             # exploratory notebooks
uv run python path/to/script.py
```

- **uv** — environment + dependency management (`uv.lock` is committed).
- **pandas / numpy / scipy / statsmodels** — data wrangling + statistics.
- **matplotlib / seaborn** — figures (use `quasioptimal.viz.set_style()`).
- **pyarrow** — Parquet I/O for processed tables.
- **ruff** — lint + format. **pytest** — tests.

Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>` for tooling).

## Conventions

- **Data provenance is mandatory.** Raw files go in `data/raw/` untouched and
  are *not* committed (they can be large); instead record where each came from
  in that section's data-sources notes so downloads are reproducible. Cleaned,
  analysis-ready tables go in `data/processed/` as Parquet written via
  `quasioptimal.data.save_processed(...)`, which also writes a `.meta.yaml`
  sidecar with the source, description, and caveats. These small processed
  tables *are* committed.
- **Definitions first.** Especially here, a number is meaningless without its
  definition (e.g. what counts as an "engineer" in a given source/era). State
  the definition next to the number.
- **Separate exploration from confirmation.** Exploratory notebooks can be
  messy; the formal test backing a claim should be clean, reproducible, and
  state its hypotheses and assumptions up front.
- **Reference paths by section name**, not fragile relative paths — use
  `quasioptimal.paths` (e.g. `raw_dir("engineering-workforce")`).
- Keep new code consistent with the surrounding style; run ruff before committing.

## Git

The maintainer works directly on `main` and keeps `origin` up to date. Commit in
logical units with clear messages.

## Sections

See `sections/README.md` for the current index. The first section is
`engineering-workforce` (long-run trends in the number of formally trained
engineers as a share of population).
