# GitHub mirrors: macro / capital-stock datasets (country-year)

Purpose: national-accounts and **physical capital-stock** series by country-year,
to relate to engineer counts. This environment blocks the usual data hosts
(rug.nl, imf.org, worldbank, oecd, ggdc), but `raw.githubusercontent.com` is
reachable — so we mirror-hunt on GitHub.

**Verification protocol.** Every URL in the "Confirmed" table below was fetched
with `curl -sS -L` from this environment and returned **HTTP 200** with real
data; columns/coverage were parsed directly from the downloaded file. Candidates
that only 404'd or that resolve to blocked hosts are in "Unconfirmed leads".
Date verified: 2026-07-23.

## Confirmed mirrors (HTTP 200, data inspected)

| # | Dataset / vintage | Quantity provided | Raw URL (200) | Format | Columns (key) | Coverage | Units |
|---|---|---|---|---|---|---|---|
| 1 | **Penn World Table 10.01** (`pwt101`) | **Capital stock** + real GDP + employment + labour share | `https://raw.githubusercontent.com/jivizcaino/PWT10.1/main/pwt101.csv` | CSV, ~4.0 MB, 12,810 rows, UTF-8-BOM | `countrycode,country,year,` `rgdpe,rgdpo,pop,emp,avh,hc,` `cgdpe,cgdpo,`**`cn,ck,`**`rgdpna,`**`rnna,rkna,`**`rtfpna,labsh,delta,...` (52 cols) | **183 countries, 1950–2019** | `rnna` = capital stock at constant 2017 national prices (mil. 2017 US$); `cn` = capital stock at current PPPs (mil. 2017 US$); `rgdpna` = real GDP at constant 2017 national prices; `emp` = persons engaged (millions); `labsh` = labour share (0–1) |
| 2 | **Jordà–Schularick–Taylor Macrohistory, Release 3** (`JSTdatasetR3`) | Long-run **real GDP** + **investment ratio** (+ credit, money, rates, crises) | `https://raw.githubusercontent.com/bank-of-england/MachineLearningCrisisPrediction/master/data/JSTdatasetR3.xlsx` | XLSX, ~635 KB (data in sheet **"Data"**; sheet 1 is the CC licence) | `year,country,iso,ifs,pop,` `rgdpmad,rgdppc,rconpc,gdp,`**`iy,`**`cpi,ca,imports,exports,narrowm,money,stir,ltrate,stocks,debtgdp,revenue,expenditure,xrusd,crisisJST,tloans,tmort,thh,tbus,hpnom` (29 cols) | **17 advanced economies, 1870–2016** (AUS,BEL,CAN,DNK,FIN,FRA,DEU,ITA,JPN,NLD,NOR,PRT,ESP,SWE,CHE,UK,USA) | `iy` = investment-to-GDP ratio (**investment/plant proxy**; no capital-stock level); `rgdpmad` = real GDP (Maddison, geary-khamis $); `rgdppc` = real GDP per capita; `gdp` = nominal GDP (local) |
| 3 | **Maddison Project 2023** (via `expersso/maddison` R pkg) | **Real GDP per capita** + population (per-country levels) | `https://raw.githubusercontent.com/expersso/maddison/master/data/maddison.rda` | RData (bzip2), ~185 KB, 131,144 rows — load with `pyreadr.read_r()` (object `maddison`) | `countrycode,country,region,year,gdppc,pop,iso2c,iso3c,continent` | ~169 countries, **year 1 – 2022** (annual from ~1820) | `gdppc` = real GDP per capita (2011 int\$, multiple-benchmark); `pop` = population (000s). Richer variant (has region/continent labels) |
| 4 | **Maddison Project 2023** (via `sbgraves237/MaddisonData` R pkg, updated 2026-01) | Real GDP per capita + population | `https://raw.githubusercontent.com/sbgraves237/MaddisonData/master/data/MaddisonData.rda` | RData (bzip2), ~185 KB, 23,280 rows — load with `pyreadr.read_r()` (object `MaddisonData`) | `ISO,year,gdppc,pop` | ~169 countries, **year 1 – 2022** | Same as #3 but minimal columns (ISO3, year, gdppc, pop). Simpler tidy shape |
| 5 | **Maddison Project 2013** (`mpd_2013-01`, via `riceissa`) | Real GDP per capita only (superseded vintage) | `https://raw.githubusercontent.com/riceissa/maddison-project-data/master/mpd_2013-01.csv` | CSV, ~139 KB, **wide** (year × country) | `Year,` then one column per country (`Austria, Belgium, ... England/GB/UK, USA ...`) | ~AD1–2010, wide by country | GDP per capita (1990 int. GK$). Old vintage — use #3/#4 instead unless the 2013 GK benchmark is specifically wanted |

### Notes on the priority item (physical capital stock)
- **PWT 10.01 (`pwt101.csv`) is the capital-stock source.** It carries two
  capital-stock levels — `rnna` (constant 2017 national prices, the series to use
  for within-country real capital growth) and `cn` (current PPPs, for
  cross-country level comparison) — plus `ck` (capital services), `rkna`, `delta`
  (depreciation), `emp`, `avh`, `hc` (human capital), and `labsh`. This single
  file covers capital + labour + output for 183 countries 1950–2019 and is the
  best per-country capital mirror found.
- **JST gives the long 1870+ span but only an investment *ratio* (`iy`), not a
  capital-stock level.** Good as a plant/investment proxy and for pre-1950 real
  GDP on the 17 advanced economies; pair with PWT for post-1950 capital levels.
  (This is Release 3 / 2017; latest is R6 — see leads below.)

## Unconfirmed leads (for a human — hosts blocked here, or no committed data file)

| Target | Where it lives | Identifier / URL | Why unconfirmed |
|---|---|---|---|
| **IMF Investment & Capital Stock Dataset (ICSD)** — general govt / private / PPP capital stock, ~170 countries 1960–2019 | IMF PIMA knowledge hub | `https://infrastructuregovern.imf.org/content/dam/PIMA/Knowledge-Hub/dataset/IMFInvestmentandCapitalStockDataset2021.xlsx` | No GitHub CSV mirror found. `github.com/mingjerli/IMFData` is an **API wrapper**, not a committed mirror. IMF host is blocked here. **This is the main gap: no public-govt capital-stock mirror on GitHub.** |
| **Global Macro Database (GMD)** — 46 vars incl. investment, GDP, 239 countries, yr 1086–2030; consolidates PWT/JST/Maddison/IMF | `github.com/KMueller-Lab/Global-Macro-Database` (+ `-R`, `-Python` pkgs) | Final data via `https://www.globalmacrodata.com/data.html` (CSV/XLSX/DTA) | Repo holds replication code + a cloud pipeline; the **assembled panel is not committed** as a raw CSV (no `GMD.csv` at obvious paths). Website host not tested/likely blocked. Worth a manual download — single tidy file covering GDP + investment for the whole panel. |
| **Maddison Project 2023 — official full data** (per-country GDP levels + pop, `mpd2023`) | GGDC / Dataverse | DOI **10.34894/INZBF2**; also Kaggle `willianoliveiragibin/maddison-project-database-2023` | Official `.xlsx` on rug.nl is blocked here. The two `.rda` mirrors above (#3/#4) already deliver the 2023 gdppc+pop; grab the Dataverse `.xlsx`/`.dta` if the full multi-column ("Full data" / "Regional data") sheet is needed. |
| **PWT 10.0 (`pwt100`)** packaged in `spring-haru/pwtdata` (Python) | `github.com/spring-haru/pwtdata` | pkg installs via pip; data bundled inside module (exact committed data-file path not located; only `setup.py`/`README` were 200) | Superseded by the confirmed PWT 10.01 CSV (#1) anyway. |
| **PWT 11.0** (latest, 1950–2023, adds 2020–2023) | official GGDC / FRED release 285 | rug.nl `pwt110.xlsx` | No GitHub CSV mirror located; rug.nl blocked. #1 (PWT 10.01) is the working substitute (ends 2019). |
| **JST Release 6** (latest, 18 countries to ~2020) | macrohistory.net | `https://www.macrohistory.net/app/download/.../JSTdatasetR6.dta` | Only R3 (#2) found committed on GitHub. macrohistory.net not tested/likely blocked. R3 differs from R6 mainly in later years + a few series; fine for long-run structure. |
| **Long-run net capital stock, single countries** (BEA Fixed Assets US; UK/DE/FR/CN historical national accounts) | BEA / national stats | — | No dedicated GitHub CSV mirror found in this pass. PWT `rnna` (#1) is the cross-country substitute for 1950+; JST (#2) covers pre-1950 GDP/investment only. |

## How to load the confirmed files (Python)

```python
import pandas as pd, pyreadr

# 1. PWT 10.01 capital stock + output (note UTF-8 BOM)
pwt = pd.read_csv(
    "https://raw.githubusercontent.com/jivizcaino/PWT10.1/main/pwt101.csv",
    encoding="utf-8-sig",
)
pwt[["countrycode", "year", "rnna", "cn", "rgdpna", "emp", "labsh"]]

# 2. JST R3 — data is in the "Data" sheet (sheet 0 is the licence)
jst = pd.read_excel(
    "https://raw.githubusercontent.com/bank-of-england/"
    "MachineLearningCrisisPrediction/master/data/JSTdatasetR3.xlsx",
    sheet_name="Data",
)

# 3/4. Maddison 2023 (RData) — pyreadr returns an ordered dict of DataFrames
mad = pyreadr.read_r("maddison.rda")["maddison"]  # after downloading the .rda
```
