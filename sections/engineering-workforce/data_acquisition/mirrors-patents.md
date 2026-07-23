# GitHub-hosted mirrors — patents / intellectual-property counts by country-year

Cluster: **patent / IP flow data** (to build patent **stocks** and relate patent
accumulation to the engineering workforce).

**Why this file exists.** This session's egress policy 403-blocks essentially
every primary IP-data host — `wipo.int`, `uspto.gov`, `oecd.org`, `epo.org`,
`ourworldindata.org`, `data.worldbank.org`, Harvard Dataverse. Only
`raw.githubusercontent.com` is reachable. So we hunt for the same datasets
**mirrored in public GitHub repos** and pull them via `raw.githubusercontent.com`.

**Verification protocol.** Candidates were *discovered* with WebSearch + the
GitHub code-search API, then every reported URL was *verified* by an actual
`curl` in this session:
`curl -sS -L -o /tmp/x -w "%{http_code}" --max-time 45 "<raw-url>"`.
Only rows that returned **HTTP 200 with real tabular data** are in the confirmed
table. Verified 2026-07-23.

**Headline finding.** The **World Bank WDI patent indicators**
(`IP.PAT.RESD` = applications by residents, `IP.PAT.NRES` = by non-residents)
*are* mirrored on GitHub in several student/replication repos and pull cleanly.
Together they give broad country-year **patent-application flows, 1960–2024**.
What is **not** on GitHub: the long-run 19th-century series (HistPat 1836–1975;
USPTO 1790-present; OWID's US-since-1790 grapher) — those live on blocked hosts
(see **Unconfirmed leads**). OWID's "annual patent applications" grapher is also
blocked, but it *is* the same WIPO-via-World-Bank data as the WDI mirrors below,
so the WDI mirrors substitute for it directly.

---

## Confirmed mirrors (HTTP 200 verified in-session)

| # | Dataset (raw URL) | HTTP | What is counted | Coverage | Columns / format |
|---|---|---|---|---|---|
| 1 | **WDI IP.PAT.RESD — residents** (clean wide) `https://raw.githubusercontent.com/ronnywang/worldbank/master/WDI_bundle/parsed/IP.PAT.RESD_WDI.csv` | 200 | Patent applications filed **at each country's own patent office by residents** of that jurisdiction (WIPO via World Bank) | **1960–2013**, 248 economies + WB regional aggregates (252 data rows) | `Country Name,Country Code,Indicator Name,Indicator Code,1960,…,2013` — CSV, one row per economy, values wide by year |
| 2 | **WDI IP.PAT.NRES — non-residents** (clean wide) `https://raw.githubusercontent.com/ronnywang/worldbank/master/WDI_bundle/parsed/IP.PAT.NRES_WDI.csv` | 200 | Applications filed **at each country's office by non-residents** (foreign applicants) | **1960–2013**, 248 economies + aggregates (252 rows) | same schema as #1 |
| 3 | **WDI IP.PAT.RESD — residents** (official WB API dump, most current) `https://raw.githubusercontent.com/Wei-Seng/group30_week4teamassignment/main/TASK1.4/API_IP.PAT.RESD_DS2_en_csv_v2_226.csv` | 200 | Same definition as #1 | **1960–2024** (WB "Last Updated 2026-01-28") — most current RESD found | Official WB format: 4 preamble lines, then `"Country Name","Country Code","Indicator Name","Indicator Code","1960",…,"2024"`; quoted CSV |
| 4 | **WDI IP.PAT.RESD — residents** (official WB API dump) `https://raw.githubusercontent.com/syro13/DAV_CA/main/unclean_data/API_IP.PAT.RESD_DS2_en_csv_v2_19391.csv` | 200 | Same definition as #1 | **1960–2024** (WB "Last Updated 2025-04-15") | same official WB format as #3 |
| 5 | **WDI IP.PAT.RESD — residents** (tidy, ISO3) `https://raw.githubusercontent.com/njf0/frankenstein/main/resources/wdi/IP.PAT.RESD.csv` | 200 | Same definition as #1 | **2003–2021**, 150 economies | `country_code,2003,…,2021` — ISO3 only (no names/aggregates), wide CSV |
| 6 | **WDI IP.PAT.NRES — non-residents** (tidy, ISO3) `https://raw.githubusercontent.com/njf0/frankenstein/main/resources/wdi/IP.PAT.NRES.csv` | 200 | Same definition as #2 | **2003–2021**, 150 economies | `country_code,2003,…,2021` — wide CSV |
| 7 | **OECD triadic patent families** `https://raw.githubusercontent.com/erkgd/novatech/main/novatech/pipeline/data/rnd_investment/triadic_patent_families.csv` | 200 | **Triadic patent families** (patents filed at EPO + JPO + USPTO for the same invention), count and % of world, by inventor country | **single year 2021 only**, 49 OECD/partner countries | OECD SDMX flat CSV: `REF_AREA_code,REF_AREA_label,…,MEASURE_label,…,TIME_PERIOD_code,value` |
| 8 | *(bonus, IP-input proxy)* **WDI researchers in R&D** `SP.POP.SCIE.RD.P6` `https://raw.githubusercontent.com/ronnywang/worldbank/master/WDI_bundle/parsed/SP.POP.SCIE.RD.P6_WDI.csv` | 200 | Researchers in R&D per million people | 1960–2013, ~248 economies | same clean wide schema as #1 |
| 9 | *(bonus, IP-input proxy)* **WDI R&D expenditure %GDP** `GB.XPD.RSDV.GD.ZS` `https://raw.githubusercontent.com/ronnywang/worldbank/master/WDI_bundle/parsed/GB.XPD.RSDV.GD.ZS_WDI.csv` | 200 | R&D expenditure as % of GDP | 1960–2013, ~248 economies | same clean wide schema as #1 |

**Spot-check values (confirm real data, not stubs):**
US residents `IP.PAT.RESD` 1960 = 63 090; Japan 1963 = 53 876; China first appears
1985 = 4 065. US non-residents `IP.PAT.NRES` 1960 = 16 631; Germany 1963 = 24 923.

### Notes on the confirmed set

- **`ronnywang/worldbank`** (branch `master`, folder `WDI_bundle/parsed/`) is the
  single most useful mirror: it holds **both** RESD and NRES in a clean,
  name+ISO3 wide layout, plus the two IP-input proxies (researchers, R&D/GDP) —
  all under one predictable path `.../parsed/<INDICATOR_CODE>_WDI.csv`. Swap the
  code in the URL for any other WDI indicator. **Caveat: it stops at 2013**, so it
  misses the biggest part of the post-1985 surge's tail.
- **`Wei-Seng/...` (#3)** is the **most current** patent file found (through 2024,
  WB-refreshed Jan 2026) but the repo only mirrors **RESD** — no NRES companion.
  `syro13/...` (#4) is the same series one refresh older (through 2024, Apr 2025).
  Use one of these for residents to 2024 and fall back to `ronnywang` NRES (to
  2013) or `njf0` NRES (to 2021) for the non-resident leg.
- **To reconstruct a country's total office intake** = `IP.PAT.RESD` + `IP.PAT.NRES`
  for that country-year. This total is what OWID's "annual patent applications"
  grapher plots. To build a **stock**, cumulate the flow (optionally with a
  depreciation/expiry rate — patents lapse ~20 yr).

### Definitional caveats (must state next to any number)

- **Applications, not grants.** All WDI IP.PAT.* series count **applications
  filed**, not patents granted. Grant series (e.g. USPTO issued counts) are a
  different, smaller number and are **not** among these mirrors.
- **By office (with residence split), not by global inventor origin.**
  `IP.PAT.RESD`/`NRES` are counted **at each country's patent office**, split by
  whether the applicant resides in that office's jurisdiction. A country's
  residents also file abroad; those foreign filings are *not* in that country's
  RESD. So RESD ≈ "home-office filings by locals," a lower bound on a country's
  total inventive output. For inventor-origin totals you need WIPO "by origin"
  tables (blocked; see leads).
- **Total, not first-filings.** WIPO counts include duplicate filings of the same
  invention across offices; it is not a first-filing / patent-family count.
  Triadic families (#7) *are* de-duplicated by invention but cover only 3 offices
  and few countries.
- **The post-1985 surge.** Global counts explode after ~1985 (China's patent law
  1985; pro-patent policy; software/biotech). Any long-run stock will be
  dominated by post-1985 flows and by China/US/Japan/Korea — interpret levels
  cautiously and consider per-capita or per-engineer normalization.
- These are **flows of IP output**, not engineer counts. They feed the
  patents-per-engineer / IP-accumulation claim as the numerator's *output* side.

---

## Dead ends checked (so nobody re-walks them)

- **`owid/owid-datasets` has no patent folder.** Code search for `patent` in that
  repo returns 0; OWID's patent graphers are served only from the blocked
  `ourworldindata.org/grapher/*.csv` API and (for newer data) `owid/etl`, which
  does not commit a plain patent CSV that code-search can find.
- **Full `WDIData.csv` / `WDICSV.csv` mirrors don't surface** in GitHub code
  search — those files exceed the code-search indexing size limit, so a repo can
  hold the whole WDI dump yet be invisible to search. The per-indicator files
  above are the reliable way in.
- **`georgetown-cset/1790-ai-patent-data`** — the "1790" is the tool name, not a
  1790 start year; it is a modern AI-patent tagging project, not a long-run count.
- **`PetraMoser/Pirates_and_Patents`** exists but exposes no code-search-visible
  patent-count CSV (data likely `.dta`/large); could not confirm a raw 200 CSV.
- **api.github.com raw directory enumeration is blocked**; discovery must go
  through GitHub code-search then a `curl` of the exact raw path.

---

## Unconfirmed leads (blocked hosts — a human / different network can fetch)

The long-run (pre-1960 / 19th-century) patent series we most want are **not** on
GitHub as raw CSVs. Recorded here with stable handles.

| Target | Source | Handle / DOI | Where it lives (blocked here) |
|---|---|---|---|
| Long-run **US patents 1790–present** (applications + grants, annual) | USPTO "U.S. Patent Activity, CY 1790 to Present" (`h_counts`) | uspto.gov `/web/offices/ac/ido/oeip/taf/data/h_counts.htm` | uspto.gov (403) — small HTML table, easy to transcribe offline |
| **US patents since 1790**, invention/utility, annual | OWID grapher `annual-patents-invention-united-states-1790` | ourworldindata.org/grapher/annual-patents-invention-united-states-1790 | ourworldindata.org (403); underlying = US Census *Historical Statistics of the US* series W-96 + USPTO |
| **HistPat** — geolocated US historical patents 1790/1836–1975 (~2.8 M docs, county level) | Petralia, Balland & Rigby, *Scientific Data* 2016 | DOI **10.1038/sdata.2016.74**; Harvard Dataverse `doi:10.7910/DVN/QT4OJS` (HistPat International) | Harvard Dataverse + MIT Media Lab (blocked); **not** a raw GitHub CSV |
| **USPTO Historical Patent Data Files** (HPDF) — patents 1790–2014, applications/grants/in-force by NBER subcategory | USPTO Office of the Chief Economist, WP 2015-01 (Marco et al.) | uspto.gov `/ip-policy/economic-research/research-datasets/historical-patent-data-files` | uspto.gov (403) |
| **OWID "annual patent applications"** (WIPO via World Bank, world + by country) | OWID grapher `annual-patent-applications` | ourworldindata.org/grapher/annual-patent-applications | ourworldindata.org (403) — but **equals RESD+NRES**, already covered by confirmed mirrors #1–6 |
| **WIPO IP Statistics** — applications & grants **by office and by origin**, 1883– for some offices | WIPO IP Statistics Data Center | wipo.int/ipstats | wipo.int (403) — the authoritative by-origin split the WDI series lack |
| **OECD patent statistics** — triadic families, PCT, patents by technology, full time series 1985– | OECD.Stat / OECD Patents database | oecd.org / stats.oecd.org | oecd.org (403); GitHub mirror #7 is only a single-year (2021) slice |
| **Long-run cross-country patents** (Great Britain 1617–, France, US) | Nuvolari–Tartari; British Patent Office; Lindgren | various econ-history datasets | journal/replication sites (blocked) |

**Retrieval tips for the human.** (1) The **USPTO `h_counts` table** (1790-present,
US applications and grants) is a tiny HTML table — grab it on any unblocked
network and drop it in `data/raw/` as the backbone of the long-run US flow, then
cumulate to a US patent **stock**. (2) **HistPat** (Harvard Dataverse) gives the
geographic/county detail for 1836–1975 if the claim needs sub-national or
inventor-location resolution. (3) For **by-inventor-origin** international
comparisons (rather than by-office), the **WIPO IP Statistics Data Center**
bulk download is the authoritative source the WDI RESD/NRES mirrors cannot
replace.
