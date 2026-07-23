# GitHub-hosted mirrors — historical engineer / education & human-capital data

Cluster: **historical engineer/education data + academic replication packages**
(supporting the long-run "engineers as a share of population" project).

**Why this file exists.** This session's egress policy 403-blocks almost every
data host (journals, `nber.org`, `census.gov`, `cambridge.org`, `oup.com`,
`rug.nl`, Dataverse, openICPSR, university sites). Only
`raw.githubusercontent.com` is reachable. So we hunt for datasets **mirrored in
public GitHub repos** and pull them via `raw.githubusercontent.com`.

**Verification protocol.** Candidates were *discovered* with WebSearch + the
GitHub code/repo search API, then every reported URL was *verified* by an actual
`curl` in this session:
`curl -sS -L -o /tmp/x -w "%{http_code}" --max-time 40 "<raw-url>"`.
Only rows that returned **HTTP 200 with real tabular data** are in the confirmed
table. Verified 2026-07-23.

**Headline finding.** None of the *engineer-specific* targets
(`maloney-valencia`, `edwards-1943`, `uk-institutions`, `de-gispen-lundgreen`,
`fr-corps-ecoles`, `fox-guagnini-1993`) is mirrored on GitHub — those live on
openICPSR / journal sites / Dataverse / in books (all blocked or offline); see
**Unconfirmed leads**. What *is* confirmed on GitHub is the long-run
**human-capital / education** layer that feeds the **A-02 modern-standard
counterfactual** (mapping schooling / skill shares to a "would-qualify-as-modern-
engineer" band) and serves as covariates / cross-checks.

---

## Confirmed mirrors (HTTP 200 verified in-session)

| # | Dataset (raw URL) | HTTP | Coverage | Key columns | Format | Supports |
|---|---|---|---|---|---|---|
| 1 | Barro–Lee long-run attainment, both sexes 15–64 — `https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/OUP/OUP_long_MF1564_v1.csv` | 200 | 1870–2010, 5-yr, ~146 countries (2 581 rows) | `country,year,sex,agefrom,ageto,lu,lp,lpc,ls,lsc,lh,lhc,yr_sch,yr_sch_pri,yr_sch_sec,yr_sch_ter,pop` | CSV | **A-02** (human-capital band); covariate |
| 2 | Barro–Lee school-enrollment ratios — `https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/OUP/OUP_enrol_MF_v1.csv` | 200 | **1820**–2010, 5-yr (3 471 rows) | `BLcode,WBcode,region_code,country,year,sex,priad,secad,ter` | CSV | **A-02**; earliest long-run education series on GitHub |
| 3 | Barro–Lee v3 attainment, 25–64 — `https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL_v3_MF2564.csv` | 200 | 1950–2010, 5-yr (2 044 rows) | same schema as #1 (+ `pop` in 000s) | CSV | **A-02**; covariate |
| 4 | OWID cross-country literacy rates — `https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Cross-country%20literacy%20rates%20-%20World%20Bank,%20CIA%20World%20Factbook,%20and%20other%20sources/Cross-country%20literacy%20rates%20-%20World%20Bank,%20CIA%20World%20Factbook,%20and%20other%20sources.csv` | 200 | long-run literacy, many countries (1 423 rows) | `Entity,Year,Literacy rates (...)` | CSV | **A-02**; covariate |
| 5 | OWID education quality — Altinok, Angrist & Patrinos (2018) — `https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Global%20Data%20Set%20on%20Education%20Quality%20(1965-2015)%20-%20Altinok,%20Angrist,%20and%20Patrinos%20(2018)/Global%20Data%20Set%20on%20Education%20Quality%20(1965-2015)%20-%20Altinok,%20Angrist,%20and%20Patrinos%20(2018).csv` | 200 | 1965–2015, many countries | `Entity,Year,Average harmonised learning outcome score,...` | CSV | covariate (quality, modern) |
| 6 | OWID Life Expectancy at Birth — Clio Infra (Zijdeman) — `https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Life%20Expectancy%20at%20Birth%20(both%20genders)%20%E2%80%93%20Clio%20Infra/Life%20Expectancy%20at%20Birth%20(both%20genders)%20%E2%80%93%20Clio%20Infra.csv` | 200 | Clio-Infra long-run | `Entity,Year,Life Expectancy at Birth (both genders) (Clio Infra)` | CSV | covariate; a **live Clio-Infra mirror on GitHub** (proves the pattern) |
| 7 | OWID Metal production — Clio Infra & USGS — `https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Metal%20production%20-%20Clio%20Infra%20&%20USGS/Metal%20production%20-%20Clio%20Infra%20&%20USGS.csv` | 200 | 1850–2011 | `Entity,Year,Nickel/Tungsten/Zinc/... Production (Clio-Infra & USGS)` | CSV | covariate (industrialization proxy) |

**Notes on the confirmed set**

- **Barro–Lee** (`barrolee/BarroLeeDataSet`, default branch `master`, GitHub Pages
  site `barrolee.github.io/BarroLeeDataSet`) is the single most useful confirmed
  mirror for us. Column glossary: `lu` = % no schooling; `lp`/`lpc` = % primary
  attained / completed; `ls`/`lsc` = secondary; **`lh`/`lhc` = % tertiary attained
  / completed** (the closest long-run, cross-country upper-tail human-capital
  proxy on GitHub — a natural input/ceiling for the A-02 "modern engineer" band);
  `yr_sch*` = average years of schooling; `pop` in thousands.
  The repo holds the full matrix of `OUP_{long,proj,enrol}_{M,F,MF}{1524,1564,2564}`
  (1820/1870–2040) and `BLData/BL_v3_*` + `BL2013_*` (1950–2010). Swap the filename
  in URL #1/#3 for any age×sex cut — all live under the same two folders and were
  spot-checked 200.
- **OWID** (`owid/owid-datasets`, branch `master`) is our confirmed conduit for
  **Clio-Infra**-derived series (the Clio-Infra portal `clio-infra.eu` itself and
  its Dataverse are blocked). URL convention:
  `.../master/datasets/<Folder>/<Folder>.csv` (URL-encode spaces `%20`, `&`,
  and the en-dash `%E2%80%93`). The already-registered `maddison-2020` source uses
  the same repo, so this host is battle-tested here.
- These are **education / human-capital / industrialization covariates, not
  engineer counts.** They do not replace any numerator source; they feed A-02 and
  the covariate layer. Add them to `sources.yaml` as new covariate ids (suggested:
  `barro-lee-attainment`, `owid-clio-*`) with `method: github_raw`,
  `reachable: here`.

---

## Dead ends checked (so nobody re-walks them)

- **Clio-Infra "mirror" repos are scaffolding, not data.** `4tikhonov/clioinfra.js`
  and `CLARIAH/wp4-clioinfra` contain website code + tiny demo CSVs (`bdata.csv`,
  `oecdregions.csv`) — the real 85 indicators sit on the (blocked) Clio-Infra
  Dataverse. `basm92/clio` is an R package that *scrapes* `clio-infra.eu` at
  runtime (blocked here), not a committed data mirror.
- **api.github.com is proxied/blocked** for arbitrary repos (403 "not enabled for
  this session"); the git-trees API can't be used to enumerate directories. Use
  the GitHub **code-search** API (works server-side) to discover exact paths, then
  `curl` the raw URL.
- The GitHub MCP `get_file_contents` is restricted to `tjmisko/quasioptimal-data`;
  it can't read third-party repos. Discovery must go through search + raw curl.

---

## Unconfirmed leads (blocked hosts — a human / different network can fetch)

None of these is on GitHub; recorded with stable handles for later retrieval.

| Target id / task | Source | Handle / DOI | Where it actually lives |
|---|---|---|---|
| `maloney-valencia` / G-ANCHOR-01, A-06 | Maloney & Valencia Caicedo, "Engineering Growth", JEEA 2022 (cross-country engineer densities c.1870–1914) | DOI **10.1093/jeea/jvac014**; SSRN 3674932; CESifo WP 6339 | JEEA "Data & code" tab / openICPSR (search authors); World Bank (Maloney) & UBC (Valencia Caicedo) pages |
| A-02 (skill→engineer mapping) | de Pleijt, Nuvolari & Weisdorf, "Human Capital Formation During the First Industrial Revolution: Evidence from the Use of Steam Engines", JEEA 2020 (county steam engines × HISCLASS skill shares) | DOI **10.1093/jeea/jvz006**; SSRN 3198139; CAGE WP (Warwick, 2016) | JEEA replication files; CAGE working-paper page (Warwick) |
| A-02 / upper-tail proxy | Squicciarini & Voigtländer, "Human Capital and Industrialization: Evidence from the Age of Enlightenment", QJE 2015 (Encyclopédie subscribers by city) | QJE 130(4):1825–1883; NBER w20219; SSRN 2450919 | QJE Dataverse / supplementary; NBER |
| A-02 / upper-tail proxy | Kelly, Mokyr & Ó Gráda, "The Mechanics of the Industrial Revolution", JPE 2023 | DOI **10.1086/720890**; SSRN 3628205; CEPR DP14884; UCD WP 2020-16 | JPE replication (uchicago) / author sites |
| `edwards-1943` / G-US-04 | Edwards, *Comparative Occupation Statistics 1870–1940* (US Census, 1943) | census.gov 1943 Dec publication | census.gov (blocked); needs offline scan → digitize |
| `edwards-1943` / G-US-04 | Blank & Stigler, *Demand & Supply of Scientific Personnel*, App. B (1957) | NBER book | nber.org (blocked); offline scan |
| `uk-institutions` / G-UK-03 | ICE / IMechE / IEE membership series | Grace's Guide (`gracesguide.co.uk`) | blocked; scrape/scan when reachable |
| `de-gispen-lundgreen` / G-DE-02 | German TH enrollments/graduates (Gispen 1989; Lundgreen; *Statistik des Deutschen Reichs*) | Cambridge UP book; ISBN | book / library; not digitized on GitHub |
| `fr-corps-ecoles` / G-FR-01 | Ponts et Chaussées / Polytechnique cohort registers | polytechnique.edu archives | blocked; archival |
| `fox-guagnini-1993` / G-EU-02 | Fox & Guagnini (eds.), *Education, Technology & Industrial Performance* (CUP 1993) | Cambridge UP book | book; transcribe tables |
| covariate (patents, pre-1900 upper-tail proxy) | HistPat — Petralia, Balland & Rigby, "Unveiling the geography of historical patents… 1836–1975", *Scientific Data* 2016 (5M US patents) | DOI **10.1038/sdata.2016.74** | Nature Sci-Data / MIT Media Lab / uu.nl (blocked); **not** found as a raw-CSV GitHub mirror despite searching |
| covariate | Lee & Lee educational-attainment underlying tables (same family as confirmed Barro–Lee) | barrolee.github.io | *(already confirmed above via `barrolee/BarroLeeDataSet`)* |

**Retrieval tip for the human:** the four econ replication packages above are the
highest-value grabs. JEEA (OUP) now requires deposited replication packages, so
the Maloney–Valencia and de Pleijt et al. data are almost certainly downloadable
from the article's "Data & code" tab or openICPSR once on an unblocked network —
grab the country/county-level CSVs and drop them in `data/raw/`, then they become
`method: github_raw`-independent primary sources.
