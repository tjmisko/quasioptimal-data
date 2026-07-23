# Data Sources: Engineers as a Share of Population — United States & California

**Task:** Locate the best available data on formally trained engineers / engineering-trained
people over time in the United States overall and California in particular, plus population
denominators. Two engineer definitions in play: (a) *period-contemporary* (whatever the census
of a given era called an "engineer") and (b) *modern-standard* (SOC-defined engineering
occupations, CIP-14 engineering degrees, PE licensure).

**Compiled:** 2026-07-23. Author: research assistant (Claude).

> **Access note / caveat.** During compilation, direct HTTPS fetches (WebFetch and curl) to
> several primary government hosts — `bls.gov`, `usa.ipums.org`, `developer.ipums.org`,
> `ncees.org` PDFs — were **blocked by this environment's egress policy** (403 at the proxy
> CONNECT stage), so page bodies could not be retrieved and parsed directly. All URLs below are
> real and were surfaced via web search, but specific counts flagged with ⚠ were read from
> search snippets or secondary sources and **must be re-verified against the primary document**
> before use. URL path patterns for data downloads should also be confirmed against the live
> site. No numbers here were invented; uncertain ones are flagged.

---

## Ranked best-sources table

| # | Source | Provider | What it gives | Geo granularity | Temporal | Engineer definition | Format / access | Rank rationale |
|---|--------|----------|---------------|-----------------|----------|---------------------|-----------------|----------------|
| 1 | **IPUMS USA** (decennial + ACS microdata) | Univ. of Minnesota / IPUMS | Individual-level occupation counts; build engineer counts by year & state | National, **state (STATEFIP)**, PUMA/metro | **1850–present** (decennial samples; ACS 2000–) | Both: `OCC1950` (harmonized, engineers separable) + period `OCC` codes | Custom extract (web UI or API); CSV/DAT/Stata/SAS/SPSS; free w/ registration | The single best long-run, geographically resolved source; only one reaching ~1850 with a California cut |
| 2 | **BLS OEWS / OES** | US Bureau of Labor Statistics | Engineer *employment* counts + wages by detailed SOC occupation | National, **state (CA)**, ~530 metro areas | 1997/1999–present (annual; series comparability breaks ~2000, 2010, 2018 SOC revisions) | SOC 17-2xxx detailed engineering occupations | XLSX/TXT downloads + BLS Public Data API v2 | Best *modern* occupational headcount; authoritative, metro-level, CA available |
| 3 | **NCES IPEDS Completions** | US Dept. of Education / NCES | Engineering **degrees conferred** by level, institution, state | National, **state**, institution | 1980–81 to present (annual); some series to 1966 via NSF | CIP code **14 = Engineering** (+ 15 Eng. Tech.) | CSV via Data Center; Trend Generator UI; API | Best education-pipeline series; long, granular, downloadable |
| 4 | **NSF NCSES** (WMPD data tables, WebCASPAR, SED, NSCG) | National Science Foundation | Degrees earned (S&E), *stock* of engineering-degree holders in workforce | National (some state) | Degrees 1966– (WebCASPAR); doctorates 1958– (SED); NSCG stock | Field-of-degree "engineering"; occupation "engineers" | Interactive tables, XLSX/CSV, WebCASPAR query tool | Best for "engineering-trained *people*" (stock), not just annual flow |
| 5 | **NCEES "Squared" + state boards (CA BPELSG)** | NCEES; CA Board (BPELSG) | Count of **licensed PEs** nationally and by state | National, **state (CA)** | Modern (annual reports; recent years); CA board data | Legally licensed Professional Engineer (PE) | PDF reports; CA license lookup / public records | Best licensure proxy; narrower than "trained" (only ~1/5 of engineers hold a PE) |
| 6 | **US Census pop. + CA Dept. of Finance** | US Census Bureau; CA DOF | **Denominators**: total population, US & CA | National, **state**, county | US 1790–; CA 1850– | n/a (population) | XLSX/CSV/PDF | Required denominator; authoritative and long |
| 7 | **Historical Statistics of the US (HSUS), Millennial Edition** | Cambridge U. Press (orig. Census) | Pre-digested occupation series incl. engineers by discipline | National | Colonial–1990s; engineers **1850–1990** | Census occupational categories (period + reconciled) | Online DB (subscription) + free 1970 print edn (Internet Archive) | Best ready-made long national engineer series; secondary but curated |

---

## 1. Census occupational microdata — IPUMS USA (rank 1)

**What & why.** IPUMS USA harmonizes the U.S. decennial census public-use microdata (1850
onward) plus the American Community Survey (ACS, 2000–present). It is the *only* source that
lets you count "engineers" at the individual level, by census year and **by state (including
California)**, all the way back to the 19th century. You can produce both engineer definitions:
period-contemporary (each census's own `OCC` scheme) and a consistent modern-style series
(`OCC1950` harmonized codes).

**Occupation coding schemes.**
- **`OCC1950`** — the 1950 Census Bureau occupational classification applied to *all* years
  (1850–present), the workhorse for cross-time comparability. Pre-1940 samples were coded from
  enumerators' written occupation strings directly into the 1950 scheme. Engineers are broken
  out by discipline (civil, mechanical, electrical, chemical, mining, etc.); "civil engineer"
  appears as an explicit category. **Get the exact numeric codes** from the OCC1950 codes page
  (see URLs); confirm the specific 3-digit codes for each engineering discipline there.
- **`OCC1990`**, **`OCC2010`** — later harmonized schemes (better for the modern period).
- **`OCC`** — the *original, year-specific* codes as the census recorded them (use these for the
  period-contemporary definition). Separate documented schemes exist for 1850–1930, 1940, 1950,
  1960, 1970, 1980/1990, and ACS 2000–2017 / 2018+.

**Key URLs (verify live; several blocked from direct fetch here):**
- Occupation & industry codes hub: `https://usa.ipums.org/usa/volii/occ_ind.shtml`
- OCC1950 variable description: `https://usa.ipums.org/usa-action/variables/OCC1950`
- Integrated occ/ind codes chapter: `https://usa.ipums.org/usa/chapter4/chapter4.shtml`
- ACS OCC codes 2000–2017: `https://usa.ipums.org/usa/volii/occ_acs.shtml`
- 1880 / 1900(1950-basis) / 1960 code pages under `.../usa/volii/`

**How to get engineer counts by year and by California:**
1. Register (free) at `https://usa.ipums.org`.
2. Create an extract selecting **samples** = the decennial 1% (or larger) samples for each year
   you need (1850, 1860, … 2000) plus ACS 1-yr/5-yr for recent years.
3. Add **variables**: `OCC1950` (and/or year-specific `OCC`), `STATEFIP` (state; California =
   FIPS 06), `PERWT` (person weight — essential; counts must be weighted), plus `AGE`, `SEX`,
   `EDUC`/`EDUCD` if you want to condition on training.
4. Submit; download the fixed-width/CSV data + DDI codebook.
5. Tabulate: engineer count = Σ `PERWT` over records whose `OCC1950` ∈ {engineering codes};
   filter `STATEFIP==6` for California. Divide by weighted total population for the share.

**API / programmatic access.** IPUMS Microdata Extract API (base `https://api.ipums.org/`).
Requires an API key (register, then request access). Clients:
- R: `ipumsr` — `define_extract_micro("usa", ...)`, `submit_extract()`, `download_extract()`.
  Docs: `https://tech.popdata.org/ipumsr/articles/ipums-api.html`
- Python: `ipumspy` — `MicrodataExtract("usa", samples=[...], variables=["OCC1950","STATEFIP","PERWT"])`.
  Docs: `https://ipumspy.readthedocs.io/en/latest/ipums_api/index.html`
- Developer portal: `https://developer.ipums.org/docs/v1/workflows/create_extracts/usa/`

**Coverage / granularity:** national, state, and PUMA/metro (later years). 1850 California
present but incomplete (San Francisco/Contra Costa/Santa Clara 1850 schedules were lost/burned).
**Licensing:** free for research; redistribution restricted; cite IPUMS. **Limitations:**
samples are fractions (weight up); occupational meaning of "engineer" drifts across eras
(esp. 19th c. "engineer" often = *stationary/locomotive engine operator*, not a degreed
engineer — critical for the period-contemporary vs modern distinction); small-cell noise for CA
in early years; "engineering-trained" ≠ "working as engineer."

---

## 2. Modern labor statistics — BLS (rank 2)

### 2a. OEWS / OES — Occupational Employment and Wage Statistics
- **What:** employment counts + wages for ~830 detailed occupations, cross-industry, from an
  establishment survey (~200k+ establishments semi-annually). Engineers appear as SOC major
  group **17-2xxx**.
- **Engineering SOC codes (2018 SOC):** 17-2011 Aerospace; 17-2021 Agricultural; 17-2031
  Bioengineers & Biomedical; 17-2041 Chemical; 17-2051 Civil; 17-2061 Computer Hardware; 17-2071
  Electrical; 17-2072 Electronics (exc. computer); 17-2081 Environmental; 17-2111 Health & Safety;
  17-2112 Industrial; 17-2121 Marine Engineers & Naval Architects; 17-2131 Materials; 17-2141
  Mechanical; 17-2151 Mining & Geological; 17-2161 Nuclear; 17-2171 Petroleum; 17-2199 Engineers,
  all other. (17-3xxx = drafters/technicians — usually *exclude* for "engineers".)
  Reference: `https://www.bls.gov/soc/2018/major_groups.htm`; STEM attachment
  `https://www.bls.gov/soc/attachment_c_stem_2018.pdf`
- **Geography:** national; **state incl. California**; ~530 metro/nonmetro areas (e.g., San
  Jose–Sunnyvale–Santa Clara, San Francisco). Coverage ~1997/1999–present, annual (May reference).
  ⚠ **Comparability breaks** at SOC revisions (2000, 2010, 2018) and OES→OEWS renaming; do not
  treat as a clean continuous series across those boundaries.
- **Download:** `https://www.bls.gov/oes/tables.htm` — per-year XLSX & TXT for national, state,
  metro, and national industry files. Occupation profile example (Civil):
  `https://www.bls.gov/oes/current/oes172051.htm`; all-occupation structure
  `https://www.bls.gov/oes/current/oes_stru.htm`. Overview: `https://www.bls.gov/oes/`.
- **California-specific:** CA EDD Labor Market Info OEWS dashboard
  `https://labormarketinfo.edd.ca.gov/data/oews-dashboard.html`; CA open-data mirror (OEWS
  2009–2025) `https://data.ca.gov/dataset/oews`.
- **API:** BLS Public Data API v2 (`https://api.bls.gov/publicAPI/v2/`; register for key —
  500 req/day, 50 series/req). OEWS series IDs encode area+occupation+industry+measure; series-ID
  construction is fiddly — community tutorial: `https://github.com/govex/bls-oews-api-tutorial`.
- **Definition:** employment = jobs (not people; excludes self-employed). ⚠ Civil engineers
  national employment ≈ **310,850** (recent May estimate, per secondary source — verify against
  the current `oes172051` file). **Limitations:** short history (no pre-1997), jobs-not-persons,
  excludes self-employed, SOC breaks.

### 2b. Current Population Survey (CPS)
- **What:** monthly household labor-force survey (Census + BLS); annual occupation employment,
  demographics, earnings for engineers; includes self-employed; longer modern history than OEWS
  and lets you compute *labor-force* shares.
- **Access:** published tables `https://www.bls.gov/cps/data.htm`,
  `https://www.bls.gov/cps/lfcharacteristics.htm`; **microdata** via Census
  (`https://www.census.gov/programs-surveys/cps.html`) and the analysis-friendly
  **NBER CPS** mirror `https://www.nber.org/research/data/current-population-survey-cps-data-nber`
  and **IPUMS-CPS** `https://cps.ipums.org` (harmonized, 1962–present).
- **Definition:** self-reported occupation (Census occ codes, which map to SOC). **Limitations:**
  smaller sample → noisy at state level (CA is large enough for annual estimates but detailed
  engineering disciplines are thin); occ code revisions.

---

## 3. Engineering education — degrees conferred (ranks 3 & 4)

### 3a. NCES IPEDS Completions (primary flow series)
- **What:** number of awards conferred by all Title-IV postsecondary institutions, by field
  (**CIP**), award level (certificate → doctorate), and institution → aggregable to **state**.
- **Engineering field:** **CIP 2-digit series 14 = "Engineering"** (add **15 = Engineering/
  Engineering-Related Technologies** if you want technicians). CIP explorer:
  `https://nces.ed.gov/ipeds/cipcode/`
- **Coverage:** complete data files from **1980–81** to present, annual. (Pre-1980 engineering
  degree counts exist via NSF/HEGIS back to the 1940s–60s — see NSF below.)
- **Download / access:**
  - Complete Data Files (CSV, ≤250 vars, 7,000+ institutions): `https://nces.ed.gov/ipeds/use-the-data`
  - Trend Generator (quick time series UI): `https://nces.ed.gov/ipeds/trendgenerator`
    (Degrees & Certificates: `.../trendgenerator/app/answer/4/24`)
  - Per-year Completions survey files: `https://nces.ed.gov/ipeds/use-the-data/download-survey-material/2023/completions`
  - IPEDS also exposes a data API / the Urban Institute `educationdata` API mirrors IPEDS.
- **Definition:** completions = degrees/awards (a person with a double major can be counted
  twice under some fields — check first/second major flags). **Limitations:** US institutions
  only; flow (annual awards) not stock; state = institution location, not student origin.

### 3b. NSF NCSES (best for degree history + *stock* of engineering-trained people)
- **WMPD / "Diversity and STEM" data tables** — detailed S&E degrees by field, sex, race,
  level, with long trend tables. Landing: `https://ncses.nsf.gov/wmpd/` ; 2021 edition data
  tables `https://ncses.nsf.gov/pubs/nsf21321/data-tables`.
- **WebCASPAR** `https://webcaspar.nsf.gov/` — integrated query tool over IPEDS/HEGIS/SED;
  **engineering degrees by year back to ~1966** (HEGIS), custom cross-tabs, downloadable.
- **Survey of Earned Doctorates (SED)** — engineering PhDs; interactive tables **1958–present**.
  `https://ncses.nsf.gov/surveys/earned-doctorates/` (e.g., 2024 edition).
- **National Survey of College Graduates (NSCG) / SESTAT** — the *stock* of people **holding an
  engineering degree** and whether they work as engineers (directly answers "engineering-trained
  as a share of population"). `https://ncses.nsf.gov/surveys/national-survey-college-graduates/`
- **Definition:** field-of-degree "engineering"; occupation "engineers." **Limitations:** mostly
  national (limited state detail); NSCG is a modern periodic survey (1993–), not long-run.

---

## 4. Licensure — PE counts (rank 5)

- **NCEES "Squared"** (annual "year in numbers"): official U.S. engineering + surveying
  licensure statistics — number of U.S. licensees, exam volumes, pass rates, examinee age.
  Publications hub: `https://ncees.org/about/publications/`. Direct PDFs:
  - Squared 2024 (FY Oct 2023–Sep 2024): `https://ncees.org/wp-content/uploads/2025/02/Squared-2024_pages.pdf`
  - Squared 2025: `https://ncees.org/wp-content/uploads/2026/02/Squared-2025.pdf`
  - Squared 2023: `https://ncees.org/wp-content/uploads/2024/06/Squared-2023_spreads.pdf`
  - NCEES Annual Report 2024: `https://ncees.org/wp-content/uploads/2025/02/Annual-report-2024_pages5.pdf`
  - ⚠ Secondary source figure: as of ~2022 there were **~931,640 PE licenses** across states +
    DC, representing **~494,542 resident (unique) licensees** (many engineers hold PEs in
    multiple states). **Verify** against the primary Squared PDF; get the current-year number and
    any state breakdown there.
- **California — Board for Professional Engineers, Land Surveyors & Geologists (BPELSG):**
  - Site: `https://www.bpelsg.ca.gov/` ; license verification/lookup:
    `https://www.bpelsg.ca.gov/licensees/verification.shtml`
  - Applying for PE (context on CA classes incl. the CA-specific Civil/Structural titles):
    `https://www.bpelsg.ca.gov/applicants/applying_for_pe.shtml`
  - ⚠ Secondary source: **~89,000+** licensed PEs + architects + land surveyors in California
    (combined; disaggregate via BPELSG statistics/annual reports — verify).
  - CA also uniquely licenses **Structural Engineers** and title-authority acts (Civil,
    Electrical, Mechanical) — relevant for a CA deep-dive.
- **Definition:** legally licensed PE (a *subset* of practicing/trained engineers — roughly
  one-fifth of engineers hold a PE; heavily skewed toward civil). Good as a licensure proxy and
  because state boards give long administrative series, but **not** a substitute for occupation
  or degree counts. **Limitations:** cross-state double counting; PE ≠ "engineer"; historical
  licensure only exists after Wyoming's first act (1907) → all 48 states by 1950.

---

## 5. Population denominators (rank 6)

- **United States (Census Bureau):**
  - Decennial resident population **1790–2020**: `https://www.census.gov/programs-surveys/decennial-census/decade.2020.html`
    and historical population-change tables `https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html`
  - Population Estimates Program (intercensal/postcensal, annual):
    `https://www.census.gov/programs-surveys/popest.html`
  - Formats: XLSX/CSV/PDF.
- **California (Dept. of Finance, Demographic Research Unit — the authoritative CA source):**
  - Demographics hub: `https://dof.ca.gov/forecasting/demographics/`
  - Historical: CA total resident population by decennial census **1850–2020** (1850 ≈ 92,597;
    2020 = 39,538,223). "California Apportionment 1860–2020" PDF:
    `https://dof.ca.gov/media/docs/forecasting/Demographics/2020-census-demographics/California-Apportionment-1860-2020.pdf`
  - Historical census populations of CA state/counties/places 1850–2000 (DOF compilation):
    `https://nrm.dfg.ca.gov/FileHandler.ashx?DocumentID=8648`
  - Annual state/county estimates (E-series tables): `https://dof.ca.gov/forecasting/demographics/estimates/`
- **Note on consistency:** when computing "engineers per capita" from IPUMS, prefer the *same
  IPUMS weighted totals* as denominator to keep numerator/denominator internally consistent; use
  Census/DOF totals as an external cross-check.

---

## 6. California-specific long history (rank 7 context)

- **Historical Statistics of the United States, Millennial Edition** (Cambridge) —
  `https://hsus.cambridge.org/` — curated national occupation series with **engineers by
  discipline (aeronautical, chemical, civil, electrical, industrial, mechanical, metallurgical,
  mining, …) 1850–1990**. Best ready-made long national engineer series; subscription (via most
  research libraries). Free predecessor: *Historical Statistics of the US: Colonial Times to
  1970* on Internet Archive (`https://archive.org/details/HistoricalStatisticsOfTheUnitedStatesColonialTimesTo1970`).
- **Gold Rush / mining-engineer era:** the profession's early CA footprint is dominated by
  **mining engineers** (post-1849). Quantify via IPUMS `OCC1950` mining-engineer code filtered
  to `STATEFIP==6`, 1860–1910 samples. Institutional context: American Institute of Mining
  Engineers founded 1871; UC Berkeley College of Mining (later Engineering) 1860s–1870s.
- **20th-century professionalization / Silicon Valley:** IPUMS ACS + BLS OEWS (San Jose &
  San Francisco metros, SOC 17-2061/17-2071/17-2072 computer-hardware/electrical/electronics
  engineers, plus software developers 15-1252 if you count them) capture the postwar and
  Silicon-Valley surge. IPEDS/WebCASPAR capture the CA engineering-degree pipeline (Berkeley,
  Stanford, Caltech, the CSU/UC system).
- **Secondary framing sources (context, not primary counts):** NSPE/Abt "Overview of the
  Profession" report; note the finding that the U.S. engineering workforce grew ~6× between 1900
  and 1930 and >2× between 1950 and 1970 — useful as sanity checks on any constructed series.

---

## Concrete "starter" retrieval recipe (long-run US + CA engineer share)

1. **Numerator, long run (1850–2000):** IPUMS USA extract — all decennial samples + ACS;
   variables `OCC1950`, `STATEFIP`, `PERWT`, `EDUCD`. Tabulate weighted engineer counts,
   national and `STATEFIP==6`. (Decide upfront how to treat 19th-c. "engineer" = engine
   operator: use `OCC1950` discipline detail to isolate professional engineering categories for
   the modern-standard definition; keep the raw period category for the period-contemporary one.)
2. **Numerator, modern detail (1997–):** BLS OEWS state+metro XLSX (or API) for SOC 17-2xxx,
   national and California — cross-check IPUMS/ACS.
3. **Education pipeline:** IPEDS Completions (CIP 14) via Data Center/Trend Generator, national +
   CA; extend pre-1980 with NSF WebCASPAR (to ~1966) and SED (PhDs to 1958).
4. **Licensure overlay:** NCEES Squared (national PE counts) + BPELSG (California PE counts).
5. **Denominator:** Census decennial (US) and CA DOF (California), 1850–present; or IPUMS
   weighted totals for internal consistency.
6. **Compute share** = engineers ÷ population, per year, US and CA, for both engineer
   definitions.

---

## Key gaps & cautions

- **No single downloadable long CA-specific engineer time series exists** — it must be
  *constructed* from IPUMS microdata (the only source combining pre-1900 coverage + state cut).
- **"Engineer" definitional drift** is the central hazard: 19th-century census "engineers" are
  largely engine/locomotive operators, not degreed engineers. `OCC1950` discipline detail is the
  tool to separate them, but early-year California cell sizes are small and noisy.
- **Series breaks:** OES/OEWS is discontinuous at SOC revisions (2000/2010/2018) and has no
  pre-1997 data; IPEDS starts 1980 (NSF extends to ~1966); PE licensure only exists post-1907.
- **Flow vs stock vs jobs:** degrees = annual flow; OEWS = jobs (not persons, excludes
  self-employed); NSCG = stock of degree-holders; PE = licensed subset. These answer different
  versions of "engineering-trained share" — keep them distinct.
- **Verification still required (⚠ items):** exact NCEES national/CA PE counts, the current
  OEWS civil-engineer employment figure, and several `bls.gov`/`ipums.org`/`ncees.org` URLs and
  file-path patterns could **not be directly fetched** in this environment (egress-policy 403).
  Re-open them from an unrestricted network before citing exact numbers.
