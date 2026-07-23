# Data Sources: Engineers as a Share of Population — CHINA (c. 1500 → present)

**Scope of this file.** Best available data for counting *formally trained engineers* (and their historical analogues) in China and dividing by population, across the imperial (Ming/Qing), Republican (1912–1949), and PRC (1949–) eras. Two target definitions:
- **(a) period-contemporary** — whoever counted as a technical expert / "engineer" in that era's own terms;
- **(b) modern-standard** — a person with formal tertiary engineering training (roughly ISCED-F "Engineering, manufacturing & construction," plus architecture/construction).

**Bottom line up front.** China has *excellent* modern data (1998→present) from the Ministry of Education and NBS, *usable* series back to the 1950s from PRC statistical compilations and scholarship, *fragmentary* Republican-era counts from historians and one purpose-built database (CERD), and *no* countable "engineer" category before ~1900 — only proxies (Ministry of Works officials, hydraulic bureaucrats, artisan registers). Population denominators back to 1500 are solid (Maddison; Cao Shuji for Ming–Qing).

> **Retrieval caveat (2026-07-23):** Direct page fetching from this research environment is blocked by an egress-policy proxy for most primary hosts (`stats.gov.cn`, `uis.unesco.org`, `cset.georgetown.edu`, `soc.duke.edu`, `data.worldbank.org`, `dhi.ust.hk`, etc. all returned 403 to the fetcher). URLs below were surfaced and cross-checked via web search but their live contents were **not** individually re-verified by fetch. Treat exact figures as "as reported by the cited source," and re-pull from a normal browser before use. Nothing here is invented; where a number is uncertain it is flagged.

---

## 1. Ranked best-sources table

| # | Source | Provider | Coverage (time / geo) | Engineer definition / unit | Access & format | Lang | Notes / limitations |
|---|--------|----------|------------------------|----------------------------|-----------------|------|---------------------|
| 1 | **Educational Statistics Yearbook of China** (中国教育统计年鉴) + MoE annual "Statistical Report on Educational Development" | Ministry of Education (MoE) | ~1998→present, national + provincial | Graduates/enrollment by discipline; "工学" (Engineering) is a top-level degree category (本科/专科/硕士/博士) | Yearbook = print/CD, China Statistics Press; annual bulletins free at `moe.gov.cn` | ZH (yearbook), ZH+some EN (bulletins) | The authoritative primary source for degree counts. Full yearbook "not permitted to leave China" per Duke study; disciplinary detail often only in Chinese. |
| 2 | **China Statistical Yearbook** (中国统计年鉴) + **National Data portal** (`data.stats.gov.cn`) | National Bureau of Statistics (NBS) | Yearbook annual since 1981; portal has long series | Employed persons; "专业技术人员" (professional & technical personnel), of which "工程技术人员" (engineering-technical personnel) is a defined occupational sub-class | Yearbook HTML at `stats.gov.cn/sj/ndsj/<year>/indexeh.htm` (EN edition exists); portal query/export | ZH + EN | Best for *workforce* (not degrees). Occupational granularity thinner in recent English editions; some series discontinued/redefined over time. |
| 3 | **UNESCO Institute for Statistics (UIS)** — tertiary graduates by ISCED field | UNESCO UIS | China from ~1998/1999; annual | ISCED-F 2013 "Engineering, manufacturing and construction" (+ architecture); graduates & enrolment by level | UIS Data Browser (`data.uis.unesco.org`), bulk downloads (`download.uis.unesco.org`), mirrored in **World Bank Data360** | EN | Internationally comparable; **China's UIS submissions have gaps/lags** and rest on MoE numbers. Best for cross-country normalization. |
| 4 | **OECD** — Education at a Glance / MSTI; "graduates by field" incl. China (partner) | OECD | ~2000→present | ISCED field; S&E doctorates | OECD.Stat / data explorer | EN | China is a non-member "partner"; coverage partial, drawn from MoE + UIS. |
| 5 | **World Bank — Researchers in R&D (per million), SP.POP.SCIE.RD.P6**; WDI | World Bank / UIS | China 1996→2022 | Researchers (FTE), not "engineers" per se | `data.worldbank.org/indicator/SP.POP.SCIE.RD.P6?locations=CN`; API + CSV | EN | Proxy for skilled-technical workforce; researchers ≠ engineers. ~1,849/million (2022, as reported). |
| 6 | **CSET (Georgetown) data briefs & "Country Activity Tracker"** | Center for Security & Emerging Technology | 2000s→projections to ~2025 | STEM (science, engineering, agriculture, medicine per MoE fields); STEM PhDs | Free reports/CSV at `cset.georgetown.edu` | EN | Secondary but rigorous; reconciles MoE + UNESCO + NCES. Projects ~77,000 Chinese STEM PhDs/yr by 2025 vs ~40,000 US (fields incl. non-engineering STEM). |
| 7 | **"Where the Engineers Are" / "Getting the Numbers Right"** — Gereffi, Wadhwa, Rissing, Ong (Duke, 2007–2008) | Duke Univ. / *J. Eng. Education* | ~2004–2006 snapshot | Introduces **4-year "dynamic" vs sub-baccalaureate/3-year "transactional"** distinction | SSRN `abstract_id=1015843`; Wiley 10.1002/j.2168-9830.2008.tb00950.x | EN | **The key definitional source.** Debunks the "China graduates 600,000 engineers" myth by separating true bachelor's from short-cycle/vocational. |
| 8 | **Chinese Engineers Relational Database (CERD)** | HKUST Digital Humanities Initiative | Republican era (early–mid 20th c.) | ~17,600 engineer biographies (prosopography) | `dhi.ust.hk/cerd/` (web DB; not re-verified) | EN/ZH | Best *historical* micro-source for Republican engineers; who/where, not a population-share count. |
| 9 | **Maddison Project Database 2020/2023** | Groningen (GGDC) | China 1→2018/2022, incl. 1500 | Population + GDP/cap denominators | `rug.nl/ggdc/historicaldevelopment/maddison` — Excel/Stata | EN | Standard long-run denominator. |
| 10 | **Cao Shuji, *Population History of China (1368–1953)*** (Brill 2024 EN; orig. 中国人口史) | Brill / Fudan | Ming–Qing–Republican, provincial | Population, incl. 1393 provincial maps + models | Book + supplementary database (Brill) | EN (transl.) | Best scholarly Ming/Qing denominator; supersedes raw dynastic registers. |
| 11 | **PRC population censuses (1953, 1964, 1982, 1990, 2000, 2010, 2020)** | NBS | Decennial | Occupation long-form: professional/technical incl. engineers | Long-form microdata via NBS; guides at Pitt/Princeton/Duke libraries; IPUMS-International (China samples) | ZH + EN | Occupation cross-tabs give workforce counts; long-form access restricted/partial. |

---

## 2. Modern engineering graduates & STEM workforce (detail)

### 2.1 Ministry of Education (primary for *degrees*)
- **Discipline structure:** Chinese higher-ed degrees are grouped into ~12–13 top-level "门类" (categories). **工学 (Engineering / gōngxué)** is one whole category — by far the largest — subdivided into ~30+ first-level disciplines (机械, 电子信息, 土木, 计算机, etc.). This makes "engineering" cleanly identifiable in Chinese data, but the boundary differs from ISCED (Chinese 工学 includes computer science, environmental, some materials that ISCED splits).
- **Annual bulletin:** MoE's "全国教育事业发展统计公报" gives headline enrollment/graduate totals each year (free, `moe.gov.cn`). Reported figures include: **1999** undergraduate engineering enrollment 386,458 (+38% YoY) — the start of the 1999 massification; **2022** ~1.6 million entrants (~36% of all undergraduate entrants) chose engineering; postgraduate engineering degrees ~291,660 (2022) vs 267,399 (2021) *(as reported via MoE-sourced secondary coverage; verify in the yearbook)*.
- **Educational Statistics Yearbook of China (中国教育统计年鉴):** the granular source (graduates by discipline × level × province). **Access limitation flagged by the Duke team:** the detailed yearbooks "generally are not permitted to leave China" and are Chinese-only — a real, recurring obstacle. In practice, obtain via Chinese university libraries, CNKI, or the China Statistics Press CD/print editions.

### 2.2 NBS (primary for *workforce/occupation*)
- **China Statistical Yearbook** chapters relevant here: Population; Employment & Wages; Education; Science & Technology. NBS's own occupation definition explicitly lists **"engineering professionals"** first within "professional personnel (专业技术人员)" — followed by agricultural, scientific-research, health, teaching, etc. (per NBS "Employment and Wages — Definitions" page).
- **National Data portal (`data.stats.gov.cn`):** query builder + export (Excel/CSV) for national and provincial series; also the **English NBS yearbook** at `stats.gov.cn/sj/ndsj/<year>/indexeh.htm`.
- **Workforce magnitudes (as reported, verify):** Chinese S&E labor force ~1.2 million (1982) → ~3.2 million scientists & engineers by 2010, of which ~2.4 million engineers (figures surfaced via S&T-history literature, e.g. PNAS 2014 "China's rise…"). Treat as order-of-magnitude.

### 2.3 UNESCO UIS & World Bank Data360 (for cross-country comparability)
- **UIS "Distribution of tertiary graduates by field of study"** (legacy query id 3830) → ISCED-F "Engineering, manufacturing and construction." China included from ~1998/99. Bulk downloads at `download.uis.unesco.org/bdds/`. Mirrored/queryable at **`data360.worldbank.org`** (dataset `UNESCO_UIS`).
- Use UIS/World Bank when you need a **denominator-consistent, ISCED-harmonized** engineering-graduate series to place China alongside other countries; use MoE when you need China's own maximal detail.

### 2.4 The "China graduates X million engineers per year" claim — trace & caveats
- **Origin of the myth:** mid-2000s policy panic (e.g. widely-cited "China 600,000 / India 350,000 / US 70,000 engineers per year"). The **Duke "Where the Engineers Are" (2007)** and **Gereffi et al., "Getting the Numbers Right," *J. Eng. Education* (2008)** showed these numbers **conflated three-year short-cycle/vocational graduates ("大专"/associate) and even motor-mechanics with four-year bachelor's engineers**, and mixed CS/IT in. Their **"dynamic vs. transactional"** distinction is the analytic core: China/India lead on *volume* (including many "transactional" short-cycle grads) while the gap in *four-year "dynamic" engineers* is far smaller; China does clearly lead on **master's and doctoral** engineering output.
- **Definitional to-watch list when counting Chinese engineers:**
  1. **本科 (4-yr bachelor) vs 专科 (3-yr associate/junior college):** always separate them; the inflated claims lump them.
  2. **工学 ≠ ISCED engineering** (Chinese 工学 includes CS, some fields ISCED classifies elsewhere).
  3. **Graduates (flow) vs stock of practising engineers (workforce):** MoE = flow; NBS occupation = stock.
  4. **STEM ≠ engineering:** CSET's "77,000 PhDs" covers science+engineering+agriculture+medicine.
  5. **Enrollment vs graduation** (drop the confusion; use graduates).

---

## 3. Historical 20th century

### 3.1 Republican era (1912–1949)
- **Professionalization:** engineering societies emerged 1912–1949 (e.g. Chinese Society of Electrical Engineers, Shanghai 1934, founded by ~67 engineers); the diaspora **Chinese Institute of Engineers (CIE), founded 1917 in the US**. First Chinese-led major project: Zhan Tianyou's Beijing–Zhangjiakou railway, 1905.
- **Counts (fragmentary, as reported):** ~**4,000** Chinese had studied engineering abroad by ~1930; a Republican engineer prosopography analyzes **~17,600** professional biographies.
- **1949 baseline (widely cited):** 205 higher-ed institutions, of which **28 engineering colleges**, **30,414 engineering students (~26% of enrollment)** — a small elite base at Liberation.
- **Best sources:**
  - **CERD — Chinese Engineers Relational Database**, HKUST (`dhi.ust.hk/cerd/`): purpose-built prosopographic DB (~17,600 engineers).
  - Journal articles: "Engineering Societies in China: Spaces of Professionalization…, 1912–1949" (*East Asian Science, Technology and Society* / T&F, 2025, doi 10.1080/18752160.2025.2546742); "The Emergence of the Modern Civil Engineer in China, 1900–1940"; "Engineers on the Move: Elite Geographic Mobility in Republican China" (Project MUSE).

### 3.2 PRC industrialization & Soviet model (1950s)
- **1952 college reorganization (院系调整):** universities restructured on the Soviet polytechnic model; Tsinghua converted from comprehensive to polytechnic (65 Soviet advisers 1952–1960). Engineering education mass-expanded around the **1st Five-Year Plan (1953–57)** with heavy Soviet technical assistance (>10,000 Soviet experts sent; several thousand engineers/technicians).
- **Sources:** "The formation of higher engineering education system in new China…" (*Engineering Education Review*, HKSMP); "The Transformation of Engineering Disciplines at Tsinghua… Soviet Influence (1952–1960)" (*CAHST*, doi 10.3724/SP.J.1461.2023.01108); Springer "The Soviet Model and China's Initial Endeavor… Higher Education"; IHNS "Technology Transfer from the USSR to the PRC."

### 3.3 Cultural Revolution disruption (1966–1976)
- Universities effectively **closed 1966–1970/71**; entrance exams abolished **1966–1971** (restored 1977); "worker-peasant-soldier students" admitted by recommendation from ~1970–73 with politicized curricula; ~16 million youth "sent down." This creates a **cohort gap** — a decade with almost no formally trained engineers — that any long-run series must show as a trough.
- **Sources:** IZA DP 10460 "The Long Shadow of the Chinese Cultural Revolution"; CUHK "Scarring Effects of Deprived College Education…"; NBER digest Aug 2020 "Disruptions in Education Stunt Innovation."

### 3.4 Post-1978 reform & post-1999 massification
- Deng-era rebuilding, then the **1999 enrollment-expansion ("扩招")**: undergraduate engineering enrollment 386,458 (1999) → 798,106 (2006); >6 million total college graduates/yr since ~2003; engineering the single largest field.
- **Sources:** Wu Zhengyang, "The Giant Leap in the Development of Higher Engineering Education in China" (*ECNU Review of Education* / SAGE, 2025, doi 10.1177/20965311241265731); Xu, "From massification towards post-massification" (SAGE 2021); "Expansion of Chinese Higher Education Since 1998" (ERIC EJ752324).

---

## 4. Imperial / pre-modern China (Ming/Qing → toward 1500): the measurement problem

**Honest assessment: there is no countable "engineer" population before ~1900, and any pre-modern share is a proxy estimate, not a measurement.** Reasons:

1. **No engineering profession or credential existed.** The **imperial examination (科举)** tested only the Confucian Four Books and Five Classics — *no* technical/engineering track. Advancement and status flowed through literary examination, not technical certification. Confucian hierarchy ranked scholar-officials (士) above artisans (工) and merchants (商) — the maxim "君子不器" ("a cultured man is not a tool") captures the low prestige of technical/vocational skill (see T&F, "'A cultured man is not a tool': Confucian legacies and vocational education," 2021).
2. **Technical expertise was embedded in the bureaucracy and the crafts, not a separate profession.** Candidate proxies one *could* attempt to count:
   - **Ministry of Works (工部)** officials, and specialized directorates (e.g. Directorate of Architecture/Engineering of the imperial palaces); occasionally artisans rose into it (Ming: woodworkers Kuai Xiang, Cai Xin, Xu Gao — the last reaching Minister of Works).
   - **Hydraulic / water-control officials** (river conservancy, Yellow River & Grand Canal administration) — the largest sustained "engineering" bureaucracy, reflecting the social centrality of water control.
   - **Artisan/craftsman registers (匠籍):** the Ming hereditary artisan-household registration system in principle enumerates skilled craftsmen (carpenters, metal-casters, shipwrights) — the closest thing to a headcount of technical labor, but it counts *craft households*, not "engineers," and the category dissolves in the Qing.
3. **Scholarship, not statistics, is the resource.** **Joseph Needham, *Science and Civilisation in China*** — esp. **Vol. 4 Pt 2 (Mechanical Engineering)** and **Vol. 4 Pt 3 (Civil Engineering and Nautics)** — documents the technology and its organization but does not provide population counts of practitioners. Use it to justify *which offices/roles* proxy for "period-contemporary engineers," not to derive a number.

**Recommended handling in the dataset:** For pre-1900 China, record engineers as **"no direct count; proxy-only"** with a documented proxy (e.g. Ministry of Works + hydraulic bureaucracy establishment size, or artisan-household counts where extant), an explicit large uncertainty band, and a note that the *modern-standard* definition yields effectively zero. Do **not** manufacture a share.

---

## 5. Population denominators (the easy part)

| Source | Coverage | Access | Use |
|--------|----------|--------|-----|
| **Maddison Project Database 2020 (and 2023 update, Bolt & van Zanden)** | China population + GDP/cap, benchmark years incl. **1500**, 1600, 1700, then denser to 2018/2022 | `rug.nl/ggdc/historicaldevelopment/maddison/releases` — Excel/Stata, free | Primary long-run denominator; consistent across countries for the global comparison. |
| **Cao Shuji, *The Population History of China (1368–1953)*** (Brill 2024, transl. of 中国人口史) | Ming–Qing–Republican, provincial; 1393 provincial maps; model-based reconstructions + database/metadata | Brill (book + supplementary data) `brill.com/display/title/69014` | Best Ming/Qing denominator; corrects raw dynastic *ding*/household registers. |
| **NBS annual population series + censuses (1953–2020)** | 1949→present | `data.stats.gov.cn`; census guides at Pitt/Princeton/Duke libguides; IPUMS-International China samples | Modern denominator + occupation cross-tabs for the workforce numerator. |
| **Ge Jianxiong (ed.), 中国人口史 (6 vols)** | Antiquity→1953 | Chinese academic presses | Deeper dynastic detail if 1500-era precision needed. |

*Note:* Ming/Qing official registers (丁 counts / household 户) are **tax/corvée units, not headcounts** — never use them raw; rely on Cao/Ge reconstructions.

---

## 6. Concrete retrieval steps

1. **MoE engineering degrees (flow):** `moe.gov.cn` → 教育统计数据 → "全国教育事业发展统计公报" for headline yearly totals (free). For discipline × level detail, obtain *Educational Statistics Yearbook of China* via CNKI / a Chinese university library / China Statistics Press (print/CD). Expect Chinese-only and in-China access.
2. **NBS workforce (stock):** `stats.gov.cn/sj/ndsj/2024/indexeh.htm` (English yearbook, browse Employment/Education/S&T chapters) or `data.stats.gov.cn` query→export. Occupation code of interest: **工程技术人员 (engineering-technical personnel)** within **专业技术人员**.
3. **UIS harmonized series:** `data.uis.unesco.org` → Education → graduates by ISCED field → "Engineering, manufacturing and construction," filter China; or bulk CSV from `download.uis.unesco.org/bdds/`; or `data360.worldbank.org` dataset `UNESCO_UIS`.
4. **World Bank researcher density:** API `https://api.worldbank.org/v2/country/CN/indicator/SP.POP.SCIE.RD.P6?format=json` (open license CC-BY-4.0).
5. **Historical micro:** CERD at `dhi.ust.hk/cerd/`; Duke study SSRN `abstract_id=1015843`.
6. **Denominators:** download Maddison 2020 Excel from GGDC; Cao Shuji via Brill.

---

## 7. Gaps, risks & honest flags

- **Egress-blocked verification:** live contents of `stats.gov.cn`, `uis.unesco.org`, `cset.georgetown.edu`, `soc.duke.edu`, `dhi.ust.hk`, `data.worldbank.org` were **not** fetchable from this environment (policy 403). All figures are "as reported by search-surfaced sources"; re-pull before publication.
- **In-China-only detail:** the granular *Educational Statistics Yearbook* is the single biggest access obstacle for degree-level detail; Chinese-language, restricted export.
- **Definitional murk (the central hazard):** 工学 vs ISCED; 本科 vs 专科; STEM vs engineering; graduates vs practising stock. The "millions of engineers/yr" headline is **not usable without disaggregation** — anchor on Duke/Gereffi.
- **Series breaks:** occupation categories, discipline catalogs (专业目录 revised repeatedly, e.g. 1998, 2012, 2020), and even what counts as "higher education" changed across eras — long-run splicing needs documented adjustments.
- **Cultural Revolution trough** must be shown, not smoothed.
- **Pre-1900 = no count.** Any imperial-era "engineer share" is a labeled proxy with wide uncertainty; the modern-standard definition is ~0 before the 1900s.
- **Political sensitivity:** headline STEM/engineer counts are used in US–China competition framing; some official detail is unpublished or lagged. Prefer triangulating MoE ↔ UIS ↔ CSET.
