# Data tasks — Engineering Workforce

Handoff-ready task cards for **gathering** data, **preparing** series, and
**analyzing** them. Each card is self-contained: an agent or a person should be
able to pick one up and know exactly what "done" means. Task IDs match the
`task:` field in `sources.yaml`.

## How to use this board

- **Owner type** — `agent` (a web-capable research/ETL agent), `human`
  (needs an account, a login, a library book, or a scan), or `either`.
- **Status** — `todo` → `in_progress` → `blocked` → `done`. Mirror the source's
  `status` in `sources.yaml` when you change it.
- **Definition of done** is the acceptance criteria on each card. A gather task
  is done when the raw file is in `data/raw/` **and** logged in the manifest
  (`data/raw/README.md`) with URL, retrieval date, coverage, and the exact
  occupation/degree code used. A prepare task is done when a `prepare_*` step
  emits a schema-valid processed table. An analyze task is done when its output
  (figure/claim/test) is committed.
- **Environment note.** As of 2026-07-23 the session egress policy 403-blocks
  every host below except `raw.githubusercontent.com`. Tasks marked
  ⛔ need either a different network, a logged-in human, or an offline source.
  `raw.githubusercontent.com`-reachable tasks are marked ✅.

Pipeline entry points these tasks feed:
`pipeline/fetch.py` → `data/raw/` → `pipeline/prepare_*.py` → `data/processed/*.parquet`
→ `pipeline/build_panel.py` → `notebooks/00_explore_panel.py`.

---

## Track G — Gather (raw acquisition)

### G-POP-01 ✅ — Long-run population denominators (Maddison + WB)  · owner: agent · **done**
- **Sources:** `maddison-2020`, `worldbank-population`.
- **Do:** already fetched via `pipeline/fetch.py` from the OWID/datahub GitHub mirrors.
- **Done when:** raw CSVs present + logged (they are); `population_long.parquet` builds.

### G-POP-02 ⛔ — Pre-1820 world + newer/UK denominators  · owner: agent (needs egress) / human
- **Sources:** `owid-hyde-population` (world pop pre-1820 + smoother series),
  `maddison-2023` (newer than 2020), `boe-millennium` (UK 1086–2016).
- **Do:** download OWID population long-run CSV; Maddison 2023 xlsx from rug.nl;
  BoE "Millennium of Macroeconomic Data" xlsx.
- **Acceptance:** world population back to ≥1500 in `population_long`; UK series
  extended pre-1820. Update `prepare_population.py` to prefer 2023 over 2020.
- **Blocked by:** egress 403 on ourworldindata.org, rug.nl, bankofengland.co.uk.

### G-US-01 ⛔ — IPUMS USA census microdata (engineer stock, US + CA)  · owner: human · **priority 1**
- **Source:** `ipums-usa`. **Needs a free IPUMS account + extract builder.**
- **Do:** build an extract, samples = every decennial 1850–2010 + ACS; variables
  `YEAR, STATEFIP, PERWT, OCC1950` (add `OCC`/`OCCSOC` for post-1950 detail).
- **Two definitions:**
  - *contemporary* — `PERWT`-weighted count where `OCC1950` ∈ engineer codes
    valid that year (civil, mechanical, electrical, mining, chemical, "engineers (n.e.c.)").
  - *modern* — restrict to degreed/professional engineering occupations; **exclude
    the stationary-/locomotive-engine operator sense** of "engineer."
  - California = `STATEFIP == 6`.
- **Acceptance:** `data/raw/ipums-usa-extract.csv.gz` + a codebook note listing
  the exact OCC1950 codes used per year; implement `prepare_ipums_usa()` (P-US-01).

### G-US-02 ⛔ — BLS OEWS engineer employment (US + CA), 1997+  · owner: agent (needs egress)
- **Source:** `bls-oews`. **Do:** pull OEWS national + state (CA) + metro for SOC
  17-2xxx (all detailed engineer codes) for each available year.
- **Acceptance:** tidy `data/raw/bls-oews-eng.csv` (year, area, soc, employment);
  implement `prepare_bls_oews()` (P-US-02).

### G-US-03 ⛔ — US engineering degrees (IPEDS CIP 14 + NSF NCSES)  · owner: human/agent
- **Sources:** `nces-ipeds`, `nsf-ncses`. Degrees conferred = **annual_flow**.
- **Acceptance:** degrees by year (and level) for CIP 14 / NSF engineering;
  note this is a flow, not a stock (needs P-STOCK-01 to convert).

### G-US-04 ⛔ — Historical US engineer stock (Edwards 1943 + Blank–Stigler)  · owner: human · **priority 1**
- **Sources:** `edwards-1943`, `nber-blank-stigler`. **Offline scans / PDFs.**
- **Do:** transcribe engineer counts by decade 1870–1940 (Edwards) and 1890–1950
  (Blank–Stigler App. B) into CSV, replacing the provisional US seed anchors.
- **Acceptance:** `data/raw/edwards-1943-engineers.csv` with the verbatim source
  definition per row; flip those seed rows from `literature_unverified` → `primary`.

### G-US-05 ⛔ — PE licensure (NCEES + CA BPELSG)  · owner: human · priority 3
- **Source:** `ncees-pe`. Narrow contemporary definition (many engineers unlicensed).

### G-US-06 ⛔ — California population denominator  · owner: agent (needs egress) / human · **priority 1**
- **Gap:** Maddison/WB have no California. **Do:** pull CA population time series
  (US Census historical + CA Dept. of Finance E-series; colonial/1850+ from
  Census historical statistics). **Acceptance:** add California rows to
  `population_long` (extend `prepare_population.py`) so CA shares can be computed.

### G-INT-01 ⛔ — Global graduates & occupation stock (UNESCO, ILO, OECD)  · owner: agent (needs egress) · **priority 1**
- **Sources:** `unesco-uis` (ISCED-F 07 graduate flow), `ilostat` (ISCO-08 214
  occupation stock), `oecd-eag` (cross-check). **Acceptance:** per-country-year
  tidy CSVs for World + all targets; note ISCO OC21 vs 214 scope differences.

### G-EU-01 ⛔ — Eurostat employment + graduates (UK/DE/FR)  · owner: agent (needs egress)
- **Sources:** `eurostat-lfsa-egai2d` (ISCO OC21 stock), `eurostat-educ-grad02`
  (ISCED-F 07 flow). **Acceptance:** note the OC21 scientist+engineer over-count;
  flag the ISCO-88→08 (2011) and ISCED-1997→2011 (2014) breaks.

### G-EU-02 ⛔ — Historical European graduates (Fox & Guagnini 1993)  · owner: human · book
- **Source:** `fox-guagnini-1993`. Transcribe national engineering-graduate tables 1850–1939.

### G-CN-01 ⛔ — China engineers (MOE graduates + NBS technical personnel)  · owner: agent (needs egress) / human · **priority 1**
- **Sources:** `china-moe` (工学 graduate flow), `china-nbs` (工程技术人员 stock).
- **Watch:** definitional breadth of "engineering graduate" in Chinese stats
  (the Duke/Gereffi caution); language = Chinese. **Acceptance:** year series for
  both, with the Chinese category label recorded verbatim.

### G-UK-01 ⛔ — I-CeM UK census microdata 1851–1911  · owner: human · registration · **priority 1**
- **Source:** `uk-icem` (UK Data Service SN 7481, safeguarded — needs registration).
- **Watch:** 1871 E&W missing; disambiguate "engineer" vs "engine-driver" pre-1881.

### G-UK-02 ⛔ — UK modern stock (Nomis SOC 212 + Engineering Council register)  · owner: agent (needs egress)
- **Sources:** `uk-nomis`, `uk-engineering-council`. Register back-series needs the
  Annual Registration Statistics PDFs. Replaces the provisional UK seed anchors.

### G-UK-03 ⛔ — UK institution membership series (ICE/IMechE/IET)  · owner: human · scans
- **Source:** `uk-institutions` (Grace's Guide + archives). Splice ICE(1818)/
  IMechE(1847)/IEE(1871), avoid double-counting, then bridge to the EngC register.

### G-DE-01 / G-DE-02 ⛔ — Germany (Destatis + Gispen/Lundgreen)  · owner: agent/human
- Modern engineering students/graduates & employed engineers (GENESIS API);
  historical TH enrollments from Gispen (1989) + *Statistik des Deutschen Reichs*.

### G-FR-01 ⛔ — France corps/école registers  · owner: human · archives
- Ponts et Chaussées (1716) / Polytechnique (1794) cohort sizes; CDEFI for modern.

### G-ANCHOR-01 ⛔ — Maloney & Valencia "Engineering Growth" replication data  · owner: human
- Download the JEEA 2022 replication package; use its c.1870–1914 engineer
  densities to **validate** our own reconstructed series (analysis cross-check).

---

## Track P — Prepare (raw → canonical processed tables)

Each prepare task maps one raw source into the schema in `SCHEMA.md`
(`engineers_long` or `population_long`), tagging `definition`, `metric`,
`method`, `source_id`, and a verbatim `source_definition`. Implement as a
`prepare_<source>()` in `pipeline/prepare_engineers.py` (or extend
`prepare_population.py`).

- **P-POP-02** — fold HYDE/Maddison-2023/BoE and **California** into `population_long`.
- **P-US-01** — `prepare_ipums_usa()` (stub exists): OCC1950 → US & CA stock, both defs.
- **P-US-02** — `prepare_bls_oews()` (stub exists): SOC 17-2xxx → US & CA modern stock.
- **P-STOCK-01** — **flow→stock model.** Convert graduate flows (IPEDS/UIS/Eurostat/
  MOE) into an engineer *stock* via a cohort accumulation + attrition (retirement/
  mortality/attrition) model. Document assumptions; this is what makes graduate
  data comparable to census/occupation stocks. Needed before flows enter the panel.
- **P-INT-01 / P-EU-01 / P-CN-01 / P-UK-01 / P-DE-01 / P-FR-01** — one per gathered
  source; each replaces the corresponding provisional seed anchors and sets
  `confidence = 'primary'`.
- **P-SPLICE-01** — **definition splices.** Where a country's series crosses
  incompatible definitions (e.g. UK institution membership → EngC register →
  census SOC), document each splice, show overlap years, and never silently join.

## Track A — Analyze (exploration → claims → formal tests)

- **A-01 — assemble & sanity-check** the full panel once primary series land;
  extend `notebooks/00_explore_panel.py`. Done: skeleton runs on provisional data.
- **A-02 — modern-standard counterfactual (pre-1900).** Build the definition-(2)
  estimate as **explicit bounded scenarios** (not a point estimate): map technical/
  mechanical trade shares + education attainment to a "would-qualify-as-modern-
  engineer" count, with sensitivity over assumptions. Output a scenario band.
- **A-03 — formal structural-break / changepoint test** on the dense share series
  (Bai–Perron and/or Bayesian changepoint) to date inflections (onset of formal
  engineering education; post-WWII expansion; China post-1999 massification).
  Pre-register H0 + decision rule in the claim dir first. *Needs primary data.*
- **A-04 — trend & growth estimation** with autocorrelation-aware models on
  log-share; report growth-rate regimes per country/definition.
- **A-05 — cross-country comparison** of levels/timing, with uncertainty carried
  from the A-02 scenarios and the definition splices (A-SPLICE-01).
- **A-06 — validate** reconstructed c.1870–1914 densities against the
  Maloney–Valencia replication data (G-ANCHOR-01).

Each formal test that backs a claim gets a `claims/<slug>/` directory (see the
`claims/_TEMPLATE/`), with H0, method, assumptions, result, and conclusion.

---

## Priority path (recommended order)

1. **G-POP-02 + G-US-06** — complete the denominator (world pre-1820 + California).
2. **G-US-01, G-US-04** — the cleanest, longest numerator (US census + historical),
   which alone supports a first claim end-to-end.
3. **G-INT-01, G-CN-01** — global + China modern series.
4. **G-UK-01/02/03, G-DE-*, G-EU-*, G-FR-01** — the European long-run detail.
5. **P-STOCK-01** — unlock the graduate-flow sources.
6. **A-03/A-04/A-05** — formal tests once ≥1 country has a dense series.
