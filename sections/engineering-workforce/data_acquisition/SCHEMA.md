# Canonical processed-table schemas

The pipeline produces three tidy long tables in `data/processed/`. The
authoritative definition lives in `pipeline/schema.py` (with validators); this
file is the human-readable contract. Prepare tasks must emit these shapes.

## `population_long.parquet` — the denominator

| column | type | notes |
| --- | --- | --- |
| `entity` | str | canonical name (`World`, `United States`, `China`, `United Kingdom`, `Germany`, `France`, `California`) |
| `iso3` | str | `WLD`/`USA`/`CHN`/`GBR`/`DEU`/`FRA`; California = `US-CA` |
| `year` | int | |
| `population` | float | persons |
| `source_id` | str | key into `sources.yaml` |
| `notes` | str | caveats (e.g. border/era) |

## `engineers_long.parquet` — the numerator

| column | type | notes |
| --- | --- | --- |
| `entity`, `iso3`, `year` | | as above |
| `definition` | str | `contemporary` (recognized as an engineer by the era's standard) or `modern` (would qualify by today's standard) |
| `metric` | str | `stock` (engineers active that year) or `annual_flow` (new entrants/graduates that year) |
| `engineers` | float | the count |
| `method` | str | `census`, `membership`, `licensure`, `graduates_stock`, `graduates_flow`, `estimate` |
| `source_id` | str | key into `sources.yaml` |
| `source_definition` | str | **verbatim** definition/occupation code the source used (e.g. "SOC 17-2xxx", "OCC1950 civil engineers", "工程技术人员") |
| `confidence` | str | `primary`, `secondary`, or `literature_unverified` (provisional seed) |
| `notes` | str | |

## `panel.parquet` — the analysis table

`engineers_long` (stock rows only) joined to `population_long` on `(iso3, year)`, plus:

| column | type | notes |
| --- | --- | --- |
| `share_per_100k` | float | `1e5 * engineers / population` |

Carries `definition`, `metric`, `method`, `source_id`, `confidence`, `notes` through.

## Rules the schema enforces

- **Never mix a flow into a stock.** Only `metric == 'stock'` rows get a
  `share_per_100k`; graduate flows must be converted to a stock first
  (task P-STOCK-01) before entering the panel.
- **Definitions travel with the number.** `definition` + `source_definition`
  are mandatory. Two proxies for the same entity-year (e.g. UK ICE membership vs
  Engineering Council register) coexist as separate rows, distinguished by
  `source_id` — they are *not* averaged or silently merged.
- **Provenance travels with the number.** Every row has a `source_id` resolvable
  in `sources.yaml`, and `confidence` flags anything not yet from a primary source.
- **Splices are explicit.** Bridging incompatible definitions across time is a
  documented step (task P-SPLICE-01), shown with overlap years — never a silent join.
