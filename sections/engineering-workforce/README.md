# Section: Engineering Workforce

**Question.** What is the long-run trend — going back to roughly **1500** — in the
number of **formally trained engineers as a share of population**, both globally
and for specific places (United States, and California in particular; China; the
United Kingdom; Germany; and other comparators such as France)?

We track the trend under **two definitions of "engineer"**:

1. **Contemporary/period definition** — whoever counted as a formally trained or
   professionally recognized engineer *at the time* (e.g. members of a corps of
   military/civil engineers, licensed/chartered engineers, holders of an
   engineering degree by the standards of the era).
2. **Modern-standard definition** — people who would qualify as an engineer by
   *today's* standards (roughly, a person with tertiary engineering training
   working in an engineering role), applied as consistently as the historical
   record allows.

The two series should diverge sharply before ~1900: definition (1) captures a
tiny, formally organized professional class, while definition (2) is largely a
counterfactual/estimation exercise in eras before modern engineering education
existed.

## Why this matters

The size of the engineering/technical workforce is a candidate driver of
innovation and economic growth (the "upper-tail human capital" and
"engineers vs. rent-seeking professions" literatures). Establishing the long-run
levels and inflection points — and how they differ across countries — is the
empirical groundwork for claims about engineering capacity and development. See
`research/literature-review.md`.

## Geographies in scope

- **Global** (aggregate share of world population)
- **United States** — national, plus **California** specifically
- **China**
- **United Kingdom**
- **Germany**
- **France** and other comparators as data allow

## Structure

- [`PLAN.md`](PLAN.md) — the exploration and data-search plan, definitions, and
  the intended path from exploration to formal tests.
- [`research/`](research/) — literature review and data-source scouting notes.
- [`data_acquisition/`](data_acquisition/) — the data-gathering framework:
  `sources.yaml` (source registry), `TASKS.md` (handoff-ready Gather/Prepare/
  Analyze cards), `SCHEMA.md` (canonical table shapes), and the provisional seed.
- [`pipeline/`](pipeline/) — runnable ETL: `fetch` → `prepare_*` → `build_panel`,
  plus the schema/validators and the `sources.yaml` loader.
- [`data/`](data/) — `raw/` source downloads (not committed; manifest in
  `raw/README.md`) and `processed/` analysis-ready tables (committed).
- [`notebooks/`](notebooks/) — exploratory analysis (`00_explore_panel.py`).
- [`claims/`](claims/) — claims formulated in this section (register in
  `claims/README.md`; template in `claims/_TEMPLATE/`).

## Status

**Exploring — analysis stack complete and swap-in ready.** Literature review and
data search are done (`research/`); a GitHub-mirror hunt (`data_acquisition/
mirrors-*.md`) closed the denominator gaps.

- **Denominator is real and rich:** World from 10000 BCE, countries annually from
  1750 (OWID/Maddison/World Bank mirrors), **California 1900+** — see
  `data/processed/population_long.parquet`.
- **Numerators:** one real point (US engineers 2021 from a BLS mirror) plus a
  small **provisional literature seed**; the rest are egress-blocked `G-*` tasks.
  So `panel.parquet` is still a preliminary read, not a result.
- **Ready to go:** the full analysis + output stack runs now on **dense synthetic
  data** and switches to real data by changing one path — `pipeline/synthetic.py`,
  `pipeline/analysis.py` (changepoint / growth regimes / cross-country /
  counterfactual), `pipeline/report.py` (figures + report), and the first claim
  `claims/engineer-share-takeoff/` (formal test wired and validated).

No claim verdicts recorded yet — those wait on real numerator data.
