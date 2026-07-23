# GitHub-hosted mirrors: population / denominator + long-run economic covariates

Discovered via WebSearch, **verified with `curl` against `raw.githubusercontent.com`**
(the only reachable data host in this environment). Every row below returned
**HTTP 200 with real CSV bytes** on 2026-07-23. Landing pages on `rug.nl`,
`ourworldindata.org`, `bankofengland.co.uk`, `dof.ca.gov`, `bls.gov`, etc. remain
egress-blocked (403), so these `raw.githubusercontent.com` URLs are the fetch path.

## Confirmed mirrors

| # | sources.yaml id it fills | Raw URL (HTTP 200) | Coverage (geo × time) | Columns / format | Notes |
|---|---|---|---|---|---|
| 1 | **owid-hyde-population** (population, 1750+) **and maddison-2023** (GDP) | `https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv` | Per-country + **World**, **1750–2024**, annual | `country,year,iso_code,population,gdp,…` (~14.4 MB, ~70 cols) | Single file carries **two** of our blocked sources. `population` = OWID long-run series (HYDE 3.3 + Gapminder + UN); `gdp` (total, 2011 int-$) = **Maddison Project Database 2023**. Verified: World 1750 pop=753,279,296; 1820 pop=1,089,507,052 gdp=1,175,113,811,058; 2020 pop=7,887,001,289. GDP starts ~1820. |
| 1b | (source attribution for #1) | `https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv` | — | `column,title,description,unit,source` | Confirms `gdp` source = "Bolt and van Zanden – Maddison Project Database 2023"; `population` = "various sources (2024)" per https://ourworldindata.org/population-sources. |
| 2 | **pre-1820 WORLD denominator gap** (complements owid-hyde-population before 1750) | `https://raw.githubusercontent.com/datasets/population-global-historical/main/data/population.csv` | **World total only**, **10000 BCE (row -1,000,000) → 1990** | `Year,Average,Deevey,McEvedy and Jones 1978,Durand Low,Durand High,Clark,Biraben,Blaxter,UN,Kremer` (values in **millions**; 55 rows) | Multiple scholarly world-population estimates side by side. Fills the deep-history World denominator (pre-1750). Sparse/benchmark years only. |
| 3 | **California population gap** (US states incl. CA) | `https://raw.githubusercontent.com/JoshData/historical-state-population-csv/main/historical_state_population_by_year.csv` | 50 states + DC, **annual 1900–2025**; **California 1900–2025** | **No header**; rows `state_abbr,year,population` (e.g. `CA,1900,1490000` … `CA,2025,39355309`) (~106 KB) | US Census annual state estimates. Directly gives CA by year 1900→present. Also on `master` branch (same file). **Does not** cover 1850–1899 (see leads). |
| 4 | **pre-1900 per-country long-run population** (complements Maddison benchmarks) | `https://raw.githubusercontent.com/open-numbers/ddf--gapminder--gapminder_world/master/ddf--datapoints--population_total--by--geo--time.csv` | Per country (`geo` = lowercase ISO3), **1800–2015** (decadal pre-1950, then annual) | `geo,population_total,time` (~337 KB) | Gapminder's back-cast country populations from 1800. Fills 1800–1950 per-country denominator where Maddison is only at benchmark years. No single "world" row (regions coded). |
| 5 | denominator cross-check (modern) | `https://raw.githubusercontent.com/open-numbers/ddf--gapminder--population/master/ddf--datapoints--population--by--country--year.csv` | Per country, **1950–2100**, annual | `country,year,population` (~602 KB) | Gapminder v7 / UN-based. Companion world-total file: `.../master/ddf--datapoints--population--by--global--year.csv` (`global,year,population`, World 1950–2100). Both HTTP 200. Modern cross-check only (starts 1950). |
| 6 | **boe-millennium** | `https://raw.githubusercontent.com/datasets/economic-history/main/millennium-macroeconomic-data-uk/data/annual.csv` | United Kingdom, **1086–2016**, annual | Long/tidy: `year,variable_id,variable,section,unit,value` (~2.9 MB) | Bank of England "A Millennium of Macroeconomic Data" (v3.1), A1 annual sheet flattened. Population series present: `variable_id=population-england` and `population-gb-ni` (unit `000s`, 1086→2016). Also `data/quarterly.csv`, `data/monthly.csv`. NB: `unit` field contains commas inside quotes — parse with a real CSV reader. |

### How the confirmed set maps to blocked sources.yaml ids
- **owid-hyde-population** → row 1 (`owid-co2-data.csv`, population 1750+) + row 2 for pre-1750 World totals.
- **maddison-2023** → row 1 (`owid-co2-data.csv`, `gdp` column = Maddison 2023, attribution in row 1b). This is the Maddison 2023 **GDP** series via OWID; the original per-country `mpd2023_web.xlsx` (with `rgdpnapc`/`cgdppc`/`pop`) was **not** found as a plain committed CSV/xlsx on GitHub (see leads).
- **boe-millennium** → row 6.
- **California gap** → row 3 (1900+); row 4 helps for other US context but is country-level.
- **pre-1820 World gap** → row 2 (World totals) + row 4 (per-country from 1800).

## Unconfirmed leads (not verified as raw HTTP 200 CSV)

- **Maddison 2023 full per-country table (`mpd2023_web.xlsx`)** — only on `rug.nl`/DataverseNL (DOI 10.34894/INZBF2, egress-blocked) and Kaggle (`willianoliveiragibin/maddison-project-database-2023`). GitHub R packages `expersso/maddison` and `sbgraves237/MaddisonData` ship the data as binary `.rda` (not curl-able as CSV); `riceissa/maddison-project-data` only holds the **2013** vintage (`mpd_2013-01.csv`, verified present). All guessed `mpd2023*.xlsx/.csv` raw paths returned 404. **Workaround already secured:** the Maddison 2023 GDP series is available via row 1 (`owid-co2-data.csv`).
- **Full HYDE per-country population back to 10000 BCE as one GitHub CSV** — not located. `owid-co2-data.csv` (row 1) starts at 1750; OWID's full 10000 BCE–2100 per-country population is served only from `ourworldindata.org` (blocked). For deep pre-1750 history use row 2 (World totals). `owid/owid-datasets` "Population (Gapminder, HYDE & UN)" folder-name guesses all 404'd; exact path not confirmed.
- **California 1850–1899 state total** — `JoshData` (row 3) starts 1900. Partial GitHub lead: `cestastanford/historical-us-city-populations` (incorporated-city populations from 1850, would need aggregation to a state total; not verified here). Authoritative CA Dept. of Finance decennial table (CA 1850=92,597) is a `dof.ca.gov` PDF (blocked).
- **Fuller World Bank SP.POP.TOTL mirror** — did not improve on the `datasets/population` mirror we already have; `datasets/population-global-historical` (row 2) is scholarly historical estimates, a different (complementary) series, not a WDI superset.

## Reproduce the verification

```bash
curl -sS -L -o /tmp/x -w "HTTP %{http_code}\n" --max-time 40 \
  "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
head -c 300 /tmp/x
```
