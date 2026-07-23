# Raw data — Engineering Workforce

Immutable, as-downloaded source files live here. **They are not committed**
(they can be large and are reproducible from their sources). Instead, this file
is the **manifest**: record every raw source so any download can be reproduced.

For cleaned, analysis-ready tables, see `../processed/` (those *are* committed,
each with a `.meta.yaml` provenance sidecar).

## Manifest

Add one entry per source as it is downloaded. Template:

```
### <short-id>
- File(s): <filename(s) placed in this dir>
- Source / provider: <name>
- URL / API: <link or endpoint + query>
- Retrieved: <YYYY-MM-DD>
- Coverage: <geography, years, granularity>
- Definition: <exact occupation/degree code or definition used>
- Format & license: <csv/xlsx/api; license>
- Notes / caveats: <...>
```

Machine-readable pull log (URL, bytes, sha256) is at
`../../data_acquisition/fetch_log.csv`, written by `pipeline/fetch.py`. The full
source registry with reachability/status is `../../data_acquisition/sources.yaml`.

### maddison-2020
- File(s): `maddison-2020.csv`
- Source / provider: Maddison Project Database 2020 (Bolt & van Zanden), via the
  `owid/owid-datasets` GitHub mirror.
- URL: https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020))/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020)).csv
- Retrieved: 2026-07-23
- Coverage: World (from 1820) + countries (1500/1700/1820 then denser) to 2018.
- Definition: `Population` (persons), `GDP`, `GDP per capita`.
- Format & license: CSV; underlying MPD terms (academic use, cite Bolt & van Zanden 2020).
- Notes: Primary long-run denominator. Pre-1820 world total absent (see G-POP-02).

### worldbank-population
- File(s): `worldbank-population.csv`
- Source / provider: World Bank WDI `SP.POP.TOTL`, via the `datasets/population` mirror.
- URL: https://raw.githubusercontent.com/datasets/population/main/data/population.csv
- Retrieved: 2026-07-23
- Coverage: countries + aggregates, 1960–present.
- Definition: total resident population.
- Format & license: CSV; World Bank open data (CC-BY-4.0).
- Notes: Modern fill for post-2018 years in `population_long`.

_All other catalogued sources are egress-blocked (HTTP 403); see the G-* task
cards in `../../data_acquisition/TASKS.md`._
