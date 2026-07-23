# GitHub mirrors — modern numerators (engineer counts & graduates)

**Cluster:** MODERN NUMERATORS (counts/graduates of engineers).
**Why this file exists:** almost every primary data host (bls.gov, census.gov,
nces.ed.gov, ncses.nsf.gov, uis.unesco.org, ilostat.ilo.org, ec.europa.eu,
oecd.org, stats.gov.cn, nomisweb.co.uk, engc.org.uk, destatis.de) returns HTTP
403 from this environment. `raw.githubusercontent.com` **is** reachable, so we
hunt for the datasets mirrored in public GitHub repos.

**Verification protocol (all rows below):** candidate discovered via WebSearch /
GitHub code search, then the raw URL fetched with
`curl -sS -L -w "%{http_code}"` and the first lines + columns inspected. Only
HTTP 200 responses with real, on-topic CSV/TSV are listed as CONFIRMED.
Probed 2026-07-23.

---

## CONFIRMED mirrors

| sources.yaml id | Raw URL (verified, HTTP 200) | Format / size | Key columns | Coverage | What it actually contains (checked) |
|---|---|---|---|---|---|
| `bls-oews` | `https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/national_May2021_dl.csv` | CSV, 309 KB | `OCC_CODE, OCC_TITLE, O_GROUP, TOT_EMP, A_MEAN, …` | US national, **May 2021 only** | Full BLS OEWS national file. Verified engineer rows: `17-2000 Engineers` (minor) `TOT_EMP = 1,631,080`; `17-2051 Civil Engineers = 304,310`; `17-2141 Mechanical Engineers`, etc. All SOC 17-2xxx present. Employment **stock** by detailed occupation. Single year, national only (no state/CA, no time series). |
| `eurostat-educ-grad02` | `https://raw.githubusercontent.com/jsollari/EUhackathon2017/master/data/educ_uoe_grad02.tsv` | Eurostat TSV, 3.8 MB | dim key `unit,isced11,iscedf13,sex,geo\time` + year cols `2015 2014 2013` | EU/EFTA countries; **years 2013–2015 only** | Tertiary **graduate counts** by ISCED-F 2013 field. Field code `F07` = *Engineering, manufacturing and construction* (verified rows, e.g. `NR,ED35,F07,F,AT = 3281`). `unit=NR` → number of graduates. By ISCED level (ED35, …) and sex. Snapshot from a 2017 hackathon, so only 3 years. |
| `unesco-uis` / WDI #6 (researchers proxy) | `https://raw.githubusercontent.com/open-numbers/ddf--open_numbers--world_development_indicators/master/datapoints/ddf--datapoints--sp_pop_scie_rd_p6--by--geo--time.csv` | CSV (tidy long), 38 KB | `geo, time, sp_pop_scie_rd_p6` | Many countries, **through 2024** (USA→2022, CHN→2023) | World Bank WDI **Researchers in R&D (per million people)**, `SP.POP.SCIE.RD.P6`. Tidy long format, cleanest/most current researchers mirror found. A **covariate/proxy** for engineer stock — NOT an engineer count. Verified: `usa,2022,4937.49`; `chn,2023,2107.27`. |
| WDI #6 (researchers proxy, alt) | `https://raw.githubusercontent.com/berkanteber/data-science-project/master/data/wb_researchers_in_rd.csv` | CSV (wide), 92 KB | `Country Name, Country Code, Indicator Code, 1960…~2019` | Many countries, 1960–~2019 | Same `SP.POP.SCIE.RD.P6` indicator, standard World Bank wide download format. Redundant with the open-numbers file but keeps original WB layout. |
| WDI #6 (researchers proxy, alt) | `https://raw.githubusercontent.com/ronnywang/worldbank/master/WDI_bundle/parsed/SP.POP.SCIE.RD.P6_WDI.csv` | CSV (wide), 44 KB | `Country Name, Country Code, Indicator Code, 1960…2013` | Many countries, **only through 2013** | Same indicator, older WDI vintage. Use open-numbers file above instead unless you need this specific vintage. |
| `nces-ipeds` / `nsf-ncses` (weak US proxy) | `https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/all-ages.csv` | CSV, 18 KB | `Major_code, Major, Major_category, Total, Employed, Median` | US, single ACS cross-section (~2012) | ACS-derived **stock of degree holders** by major. `Major_category = "Engineering"` groups ~15 engineering majors (e.g. `GENERAL ENGINEERING Total = 503,080`). **Not** IPEDS completions and **not** a time series — a one-shot ACS count. Companion file `college-majors/recent-grads.csv` (200 OK) has the same for recent grads (age <28). Treat as a rough US numerator cross-check only. |

### Notes on the confirmed rows
- **BLS OEWS:** the `openai/GPTs-are-GPTs` repo carries only the May 2021 national
  extract. For a state (California) or multi-year OEWS series there is no verified
  GitHub mirror — that remains a gap (see leads).
- **Eurostat grad02:** exactly the `educ_uoe_grad02` product named in `sources.yaml`,
  and it is engineer **graduate counts** — the single most on-target find for a
  harmonised EU engineering-graduate flow — but only 2013–2015. A fuller/newer
  pull still needs Eurostat egress.
- **Researchers-in-R&D** files fill the *proxy* leg of target #6, not a direct
  engineer count. Good for China (`chn`) and cross-country density checks, but it
  counts all R&D researchers, not engineers.

---

## Unconfirmed leads (repos exist; raw CSV not yet path-verified or wrong granularity)

| sources.yaml id | Lead | Status / why not confirmed |
|---|---|---|
| `ilostat` | `open-numbers/ddf--ilo--ilostat` — full ILOSTAT mirror as tidy DDF CSV. Employment-by-occupation file **is reachable & HTTP 200**: `…/master/datapoints/ddf--datapoints--emp_temp_sex_ocu_nb--by--ref_area--sex--classif1--time.csv` (5.3 MB, `ref_area,sex,classif1,time,value`, 178 countries, →2025). | **Too coarse to use as-is.** Occupation dimension in the fetched datapoints is only **1-digit ISCO-08** (major groups 0–9); group `ocu_isco08_2` = *all Professionals* (US 2024 ≈ 37.6 M), which cannot isolate ISCO **214** engineering professionals or even 2-digit **21**. The `oc2_isco08_21` code appears in `ddf--entities--classif1.csv` but no verified datapoint exposes it. Reachable infrastructure, but does **not** cleanly fill `ilostat`. Worth deeper spelunking (other `emp_*` indicators) before relying on it. |
| `unesco-uis` | World Bank/UIS field-of-study share `SE.TER.GRAD.EN.ZS` (*graduates in engineering, manufacturing & construction, % of total*). | Only ever found in **metadata/index files** (`csarven/lsd-sense`, `albertmeronyo/SemanticCorrelation`, `*/knowledge-engineering*` `index.csv`), never as a populated data file. It is also a **percentage, not a count**, and the broad EMC field. No clean UIS engineering-**graduate-count** mirror located. **Real gap.** |
| `nces-ipeds` | IPEDS Completions mirrors: `rearc-data/ipeds-…-datasets`, `paulgp/ipeds-database`, `RVA-ALT-Lab/ipeds`, `ajhaller/IPEDS`, `UrbanInstitute/ipeds-scraper`, `scienceforamerica/scipeds`, `wbuchanan/ipeds`. | Repos confirmed to exist, but the raw `cXXXX_a.csv` completion files (cols `UNITID,CIPCODE,MAJORNUM,AWLEVEL,CTOTALT`) were **not** retrievable by path guessing — likely git-LFS, `.zip`, or external S3, not plain committed CSV. `wbuchanan/ipeds/ipedsdb.csv` (200 OK) is only a **file manifest**, not data. Needs directory browsing to confirm a CIP-14 raw CSV. |
| `oecd-eag` | OECD Education at a Glance graduates-by-field. | No GitHub raw CSV mirror found. |
| `eurostat-lfsa-egai2d` | Eurostat employment of science & engineering professionals (ISCO OC21). | Not present in `jsollari/EUhackathon2017`; no other GitHub TSV/CSV mirror found. |
| `china-moe` / `china-nbs` | China MOE 工学 (engineering) graduates; NBS engineering-technical personnel. | Best source is `chinadata.live` (JSON/CSV API, 1949–2025) — **not** GitHub/raw. No engineering-specific China education mirror found on GitHub. The researchers-per-million files above cover `chn` as a partial NBS-personnel proxy. **Gap for a true 工学 graduate series.** |
| `uk-nomis` / `uk-engineering-council` | ONS/Nomis SOC 212 engineering professionals; Engineering Council register counts. | No GitHub mirror found. |
| `destatis-genesis` | Destatis engineering students/graduates. | No GitHub mirror found. |

### Discovery references (not data files)
- BLS OEWS discovery came via code search hitting `openai/GPTs-are-GPTs`,
  `HSV-AI/presentations`, Hortonworks/Cloudera `sample_07/08.csv` (older OES
  vintages, tab-separated — usable but undated).
- Eurostat lead surfaced from `jsollari/EUhackathon2017` (INE Portugal, 2017 EU
  Big Data Hackathon).
- ILOSTAT lead: `open-numbers/ddf--ilo--ilostat` (Gapminder Open Numbers DDF).

---

## Bottom line
- **Strong, on-target confirms:** BLS OEWS engineer stock (`bls-oews`, 2021 national)
  and Eurostat engineering-graduate counts (`eurostat-educ-grad02`, 2013–2015).
- **Proxy confirms:** researchers-in-R&D per million (tidy, →2024) for target #6 /
  loose `china-nbs` proxy.
- **Notable gaps still needing egress or deeper browsing:** UNESCO UIS engineering
  graduate **counts**, ILOSTAT ISCO-214 (coarse mirror only), OECD EAG, Eurostat
  `lfsa_egai2d`, China 工学 graduates, UK Nomis/EngC, Destatis, and a raw IPEDS
  CIP-14 completions CSV.
