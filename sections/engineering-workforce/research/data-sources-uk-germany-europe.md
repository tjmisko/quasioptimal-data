# Data Sources: Formally-Trained Engineers as a Share of Population — UK, Germany, France & Europe-wide

**Task scope:** Best available data on counts of engineers / engineering-trained people over time (ideally back to ~1500) plus population denominators, for the **United Kingdom** and **Germany**, with **France** and **Europe-wide** modern series as efficient add-ons.

**Two engineer definitions this feeds:**
- **(a) Period-contemporary** — whatever counted as an "engineer" in that era: membership of professional engineering institutions (ICE, IMechE, IET, VDI), state engineering corps, graduates of technical schools / Technische Hochschulen / grandes écoles, chartered/registered engineers.
- **(b) Modern-standard** — a fixed modern definition applied retrospectively: ISCO "Science and engineering professionals" (occupation) and ISCED-F field 07 "Engineering, manufacturing and construction" tertiary graduates.

> **Key caveat used throughout:** Professional-institution membership is a period-appropriate but **partial** proxy — it undercounts engineers who never joined and (for global institutions today) overcounts the domestic workforce because membership is international. Before ~1850 no "engineer" occupational category exists in most sources; counts must be built from institution rolls, state-corps records, and school matriculation registers. Deep back to ~1500 is only feasible as isolated institutional headcounts (e.g. French corps/écoles from the 18th c.), not as continuous series.

> **Research-environment note:** In this session `WebFetch` and direct `curl` were blocked by egress policy for many hosts (Wikipedia, engc.org.uk, Eurostat databrowser, etc. returned HTTP 403 at the gateway). Numeric figures below are drawn from **search-result snippets** and should be treated as **provisional / to-be-verified** against the primary source before use. URLs are real (returned by search) but were not all individually fetched. Items flagged **[VERIFY]** need a direct read of the source.

---

## Ranked best-sources table

| Rank | Source | Provider | Geography | Time coverage | What it measures | Definition / code | Access & format | Notes / limitations |
|---|---|---|---|---|---|---|---|---|
| 1 | **Engineering Council — Registration Statistics** | Engineering Council (UK) | UK | ~1980s→present (annual) | Registered CEng, IEng, EngTech, ICTTech; new registrations; stock | UK-SPEC titles (period-contemporary UK "professional engineer") | engc.org.uk, annual PDF reports + summary web tables | Register ≈228–229k stock; membership-gated (undercounts non-registered engineers) [VERIFY exact series] |
| 2 | **I-CeM (Integrated Census Microdata) 1851–1911** | UK Data Service / Cambridge (Campop) | GB (E&W 1851–61,1881–1911; Scot 1851–1901) | 1851–1911 | Individual occupation strings → HISCO/coded engineer occupations | Census self-reported occupation | UK Data Service SN 7481 (free, registration; safeguarded). Names/addresses SN 7856 (Special Licence) | Best long-run micro source for pre-1911 UK engineer counts; occupation coding is the analytic work; 1871 E&W & some Scot years missing |
| 3 | **HESA Higher Education Student Statistics** | HESA / Jisc | UK | 1994/95→present | Enrolments & qualifiers in Engineering & Technology (CAH/JACS subject) | ISCED-comparable subject area | hesa.ac.uk open tables + custom/paid data | Flow (graduates/yr), not stock; ~70–86k E&T entrants/yr recent [VERIFY] |
| 4 | **Nomis (APS / Census / LFS by occupation)** | ONS | UK (+ regions/LAs) | Census 1981→; APS 2004→ | Employment by SOC occupation, incl. SOC 212 Engineering professionals | SOC 2020 (maps to ISCO) | nomisweb.co.uk, free API + bulk CSV | Modern-standard occupation stock; SOC revisions break series (2020 rebase) |
| 5 | **VDI membership series** | Verein Deutscher Ingenieure | Germany (intl.) | 1856→present | VDI members | Period-contemporary German engineer proxy | VDI publications; Gispen & VDI histories for pre-1914 | ~130k members (2025); intl. membership; not = German engineer stock [VERIFY historical series] |
| 6 | **Destatis Hochschulstatistik + Mikrozensus** | Statistisches Bundesamt (Destatis) | Germany | Students/grads 1950s→ (online ~1993→); Mikrozensus 1957→ | Engineering students & graduates; employed persons with engineering degree | Fächergruppe Ingenieurwissenschaften; ISCED-F 07 | GENESIS-Online DB + API (free); tables via destatis.de | ~128k engineering exams (2023); ~1.9M employed w/ engineering degree (2019) [VERIFY] |
| 7 | **Eurostat — occupation (LFS) & graduates (UOE)** | Eurostat | EU/EEA + UK (to 2020) | LFS occ. ~1998→; grads ~1998→ | Employed "Science & engineering professionals" (ISCO OC21); tertiary graduates ISCED-F field 07 | ISCO-88→ISCO-08 (2011); ISCED-F 2013 | databrowser + bulk download + JSON/SDMX API (free, open) | Best harmonised modern cross-country panel; starts ~1998–2000 only |
| 8 | **Maddison Project Database 2023** (denominator) | Groningen GGDC | Global incl. UK/DE/FR | 1 AD–2022 | Population + GDP p.c. | — | rug.nl/ggdc; DOI 10.34894/INZBF2; Excel/Stata | Primary long-run population denominator (annual for modern era; benchmarks earlier) |
| 9 | **Bank of England "Millennium of Macroeconomic Data"** (denominator) | Bank of England | UK / England / GB | 1086–2016 | Population (England/GB) + 130 macro vars | — | bankofengland.co.uk/statistics/research-datasets; Excel (also datahub.io, Kaggle) | Best UK-specific long-run population back to Domesday |
| 10 | **Gispen, *New Profession, Old Order* (1989)** | Cambridge Univ. Press | Germany (Prussia) | 1815–1914 | TH students, Diplom-Ingenieure, engineer associations | Period-contemporary | Book; charts, tables, appendix | Authoritative secondary synthesis with statistical appendix for pre-1914 Germany |
| 11 | **ICE / IMechE / IET membership histories** | Institutions | UK (intl.) | 1818/1847/1871→ | Institution membership by grade | Period-contemporary | Institution "about/history" pages; Grace's Guide; institution archives | ICE ~95k (2022)→~100k (2025); IMechE ~110–115k; series must be stitched from histories [VERIFY] |
| 12 | **EngineeringUK workforce reports** | EngineeringUK | UK | 2010s→ (updated ~annually) | Engineering & tech workforce totals by SOC | Modern occupation aggregate | engineeringuk.com PDF reports | Secondary aggregator of ONS/Nomis; ~6.4M E&T workforce (2026) [VERIFY]; good for definitions/breakdowns |
| 13 | **CDEFI / Conférence des Grandes Écoles** | CDEFI; CGE | France | recent (annual) | Engineering graduates/yr; school panorama | Diplôme d'ingénieur (period-contemporary FR) | cdefi.fr; cge.asso.fr PDFs | ~46,500 engineering graduates 2022 [VERIFY]; historical headcounts need Grelon/Picon literature |
| 14 | **French écoles/corps heritage records** | ENPC, École Polytechnique | France | 1716/1747/1794→ | Corps & school student headcounts | Period-contemporary (state engineers) | heritage.ecoledesponts.fr; polytechnique.edu/history | Earliest usable engineer counts anywhere (~18th c.); tiny annual cohorts; proxy only |

---

## 1. United Kingdom

### 1a. Professional engineering institutions (period-contemporary proxy)

- **Institution of Civil Engineers (ICE), founded 1818.** Reported membership series (from snippets, **[VERIFY]** against ICE history / *Grace's Guide* / Porter): 220 (1830); 2,000 (1850); 797 (1856) / 1,339 (1866) / 2,884 (1876); 3,500 (1870); 5,100 (1886). Modern: Dec 2022 ≈ 5,191 Fellows + 39,507 Members + **95,460 all grades**; approaching **100,000** (June 2025).
  - History: https://www.ice.org.uk/about-us/our-organisation/history  ; About: https://www.ice.org.uk/about-us
  - 19th-c. figures: https://victorianweb.org/technology/porter4.html (G.R. Porter data) — *blocked in-session, fetch directly*
  - Recent: https://www.newcivilengineer.com/latest/ice-membership-approaches-100000-after-decade-of-continuous-growth-03-06-2025/
  - Also cross-check **Grace's Guide to British Industrial History** (gracesguide.co.uk) for year-by-year institution figures and lists.
- **Institution of Mechanical Engineers (IMechE), founded 1847** (Royal Charter 1930). ~**110,000–115,000** members in ~140 countries today. Historical **membership application forms 1847–1938 digitised** (searchable via Ancestry) — a route to counts and biographical data.
  - Archives: https://archives.imeche.org/archive/institution-history
  - Archive blog: https://imechearchive.wordpress.com/2020/10/26/a-history-of-the-institutions-membership-forms/
- **IET / IEE.** Lineage: Society of Telegraph Engineers (1871) → Institution of Electrical Engineers (IEE, 1888) → **Institution of Engineering and Technology (IET, 2006** merger with IIE). ~150,000+ members today. **[VERIFY numbers and historical series]** via theiet.org and IET Archives.
- **Engineering Council (UK register).** Holds national registers of **CEng, IEng, EngTech, ICTTech**; stock **≈228,000–229,000** (+ ~10,000 interim). Q1 2023 new registrations: 1,792 (971 CEng, 262 IEng, 517 EngTech, 42 ICTTech). Publishes **Annual Registration Statistics Report**.
  - Stats landing: https://www.engc.org.uk/professional-registration/registration-statistics/
  - Summary report page: https://www.engc.org.uk/resources-and-guidance/reports-and-publications/registration-statistics-summary-2023
  - *engc.org.uk returned 403 in-session; fetch directly / download the PDF for the full CEng/IEng/EngTech time series (registration began 1965 as CEI; Engineering Council from 1981).* **[VERIFY back-series]**

**Retrieval:** For a long-run "professional engineer" series, stitch ICE(1818)+IMechE(1847)+IEE/IET(1871)+ other chartered institutions, then splice into Engineering Council register (1965/1981→) to avoid double counting (Engineering Council register aggregates across licensed institutions). Grace's Guide is the most convenient single stop for scattered 19th–20th c. institution figures.

### 1b. Census / occupational data

- **I-CeM (Integrated Census Microdata), 1851–1911** — the primary source for pre-1911 UK engineer counts. 180M+ individual records; standardised occupation coding (with original strings preserved) mapped to HISCO. Coverage: E&W 1851, 1861, 1881, 1891, 1901, 1911 (1871 E&W missing); Scotland 1851–1901.
  - UK Data Service main study **SN 7481** (anonymised, free w/ registration, "safeguarded"): https://datacatalogue.ukdataservice.ac.uk/studies/study/7481
  - Names & addresses **SN 7856** — Special Licence (application required): see CESSDA / Harmony listings.
  - Project background: https://www.campop.geog.cam.ac.uk/research/projects/icem/
  - *Retrieval:* register with UK Data Service → accept safeguarded licence → download; extract records where coded occupation = civil/mechanical/mining/electrical engineer, etc. Note pre-1881 "engineer" often meant engine-driver/operator — occupation-string disambiguation required.
- **Modern occupational stock (SOC / ISCO):**
  - **Nomis** (ONS): free API + bulk CSV; Census (1981→) and Annual Population Survey (2004→) employment by occupation. Engineering = **SOC major-group 212 "Engineering professionals"** (subgroups: civil, mechanical, electrical, electronics, design/development, production/process, n.e.c.). https://www.nomisweb.co.uk (e.g. dataset aps168).
  - **ONS Census 2021** occupation variable & **EMP04** (employment by occupation): https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/employmentbyoccupationemp04 ; census dictionary: https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/labourmarketvariablescensus2021/occupationcurrent
  - **Caution:** SOC was rebased in **2020**; series before/after are not directly comparable. Published historical census occupational abstracts (1841–1931) exist in ONS/Vision of Britain scans for pre-I-CeM/inter-census bridging.

### 1c. Graduates (education flow)

- **HESA** Higher Education Student Statistics — enrolments and qualifiers in **Engineering & Technology** (CAH/JACS subject). 1994/95→present. Open summary tables free; unit-record/custom data via HESA (paid/licensed). Recent: ~70,845 "other engineering & tech" + ~85,875 computing entrants (2023/24) **[VERIFY]**.
  - https://www.hesa.ac.uk (see SB271 2023/24 subjects; SB269 2022/23).
- **EngineeringUK** — secondary aggregator, useful for definitions and workforce totals: engineering & technology workforce ≈ **6.3M (2024) → 6.4M (2026)** (~4M "core" + ~2.3M "related"), ≈19% of UK workforce **[VERIFY]**.
  - Workforce report: https://www.engineeringuk.com/media/pa4mjmli/the-engineering-and-technology-workforce-update-engineeringuk-april-2026.pdf
  - Higher-education report: https://www.engineeringuk.com/media/mxxjczpv/engineering-in-higher-education_report_engineeringuk_march-23.pdf
  - Data-source notes: https://www.engineeringuk.com/research-and-insights/infographic-references/

---

## 2. Germany

### 2a. VDI and the profession

- **Verein Deutscher Ingenieure (VDI)**, founded **12 May 1856** (now Düsseldorf); largest engineering association in Western Europe. Membership ≈ **130,679 (2025)**; ~150,000+ (early 2010s) **[VERIFY; series]**. Includes engineers, natural scientists, IT. Historical membership growth (1856→1914) is documented in VDI's own jubilee histories and in Gispen (below).
  - Wikipedia (blocked in-session, fetch directly): https://en.wikipedia.org/wiki/Verein_Deutscher_Ingenieure
- **Protected title "Ingenieur":** protected by **Ingenieurgesetze since 1970**, now **16 state (Länder) laws**; requires ≥3-year technical/natural-science degree. Before 1970 the title was unregulated → pre-1970 "engineer" counts must come from education (Diplom-Ingenieur) or occupation statistics, not title.
  - Overview: https://www.ingenieur.de/karriere/arbeitsrecht/ingenieurgesetze-wann-ist-ein-ingenieur-ein-ingenieur/
- **Bundesingenieurkammer — Ingenieurstatistik:** annual engineer statistics built on Destatis Umsatzsteuerstatistik and Mikrozensus. https://bingk.de/ingenieurstatistik/  (also chamber report PDFs, e.g. bak.de).

### 2b. Destatis (official statistics)

- **Hochschulstatistik** (higher-education statistics): engineering students & graduates (*Fächergruppe Ingenieurwissenschaften*). ~500k+ engineering students/yr enrolled 2013–2022; **128,164 engineering exams passed (2023)** **[VERIFY]**. Online series roughly 1990s→ ; earlier print volumes (Fachserie 11) go back further.
  - Landing: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bildung-Forschung-Kultur/Hochschulen/_inhalt.html
  - **GENESIS-Online** database + REST/SOAP **API** (free account) for machine download: https://www-genesis.destatis.de
- **Erwerbstätige / Mikrozensus** (employed persons by qualification/occupation): ~**1.9M employed persons with an engineering university degree (2019)**, +~20% since 2010 **[VERIFY]**. Uses **Klassifikation der Berufe (KldB)**, mappable to ISCO.
  - https://www.destatis.de/DE/Themen/Arbeit/Arbeitsmarkt/Erwerbstaetigkeit/_inhalt.html
- **Bundesagentur für Arbeit** (statistik.arbeitsagentur.de) — Akademiker/Berufsgruppen reports for employed engineers by KldB group.

### 2c. Historical (pre-1914) Germany / Prussia

- **Kees Gispen, *New Profession, Old Order: Engineers and German Society, 1815–1914*** (Cambridge UP, 1989) — authoritative synthesis with **charts, tables, statistical appendix** on TH students, Diplom-Ingenieure vs. non-academic engineers, and associations. The single best secondary starting point for period-contemporary German engineer counts. https://www.cambridge.org/core (book page)
- **Peter Lundgreen** — foundational quantitative research on the German engineering profession and technical education (engineer numbers, TH enrollments); search "Lundgreen Ingenieure Deutschland" for his statistical papers/chapters (a key primary-quantification author to add). **[ADD/VERIFY]**
- **Technische Hochschulen enrollment (illustrative):** Karlsruhe ≈1,360 students (winter 1900/01); TH Aachen founded 1870; Prussian THs granted the right to award doctorates in 1899. Comprehensive year-by-year multi-institution enrollment must be assembled from **Statistik des Deutschen Reichs** / Prussian statistical yearbooks and from Lundgreen/Gispen tables. **[VERIFY]**

---

## 3. France (efficient add)

- **State engineering corps & grandes écoles** give the earliest usable engineer headcounts anywhere:
  - **Corps des ponts et chaussées (1716)**; **École (nationale) des ponts et chaussées (1747)** — 18th c. had a single official student category (élèves du Corps), i.e. tens per year. Heritage records & history: https://heritage.ecoledesponts.fr/enpc/en/content/histoire-de-lecole-des-eleves-et-des-ingenieurs-en ; https://ecoledesponts.fr/en/school/welcome-school/school-history
  - **École Polytechnique (1794, renamed 1795)** — feeder to state corps (Ponts, Mines, artillery/génie). History with periodised figures: https://www.polytechnique.edu/en/school/history
  - **École des Mines**, later **écoles d'arts et métiers**, **École Centrale (1829)**.
  - Use school matriculation/graduation registers as **period-contemporary proxies**; annual cohorts small (tens→hundreds) through the 19th c.
- **Modern graduates:** **CDEFI** (Conférence des directeurs des écoles françaises d'ingénieurs) — ~**46,500 engineering graduates in 2022** **[VERIFY]**; **Conférence des Grandes Écoles (CGE, 1973)** annual insertion survey (~139 engineering schools). cdefi.fr ; https://www.cge.asso.fr
- **Workforce / historical demography:** **INSEE** (recensement, enquête emploi) for engineer occupation stock; historical engineer-profession quantification in the work of **André Grelon** and **Antoine Picon** (history of French engineers/education) — add as secondary. **[ADD/VERIFY]**

---

## 4. Europe-wide modern harmonised series

**Eurostat** (free, open licence; databrowser + bulk download + JSON/SDMX **API**):
- **Occupation (EU-LFS):**
  - `lfsa_egai2d` — Employed persons by detailed occupation, **ISCO-08 2-digit**; engineers = **OC21 "Science and engineering professionals"** (associate professionals = OC31). https://ec.europa.eu/eurostat/databrowser/view/lfsa_egai2d/default/table
  - Related: `lfsa_egised`, `lfsa_egais`.
- **Graduates (UOE):**
  - `educ_uoe_grad02` — Graduates by education level, orientation, sex, **field of education (ISCED-F 2013)**; engineering = **field 07 "Engineering, manufacturing and construction"**. https://ec.europa.eu/eurostat/databrowser/view/educ_uoe_grad02/default/table
  - `educ_uoe_grad04` — tertiary STEM graduates **per 1,000 population aged 20–29** (already a rate).
- **Human resources in S&T:** `hrst_*` series (stock of people educated/employed in S&T).
- **Classification breaks:** occupation ISCO-88 (to 2010) → **ISCO-08 (from 2011)**; education **ISCED-1997 (to 2013) → ISCED-2011/ISCED-F 2013 (from 2014)**. Coverage EU + EFTA (+ UK through 2020), typically **~1998/2000 onward** only.
- Statistics Explained context: "Human resources in science and technology"; "Tertiary education statistics" (ec.europa.eu/eurostat/statistics-explained).

**OECD** (complement / broader country set): **Education at a Glance** and **OECD.Stat / data-explorer** — graduates by field of education (incl. engineering) and labour-force by occupation; STAN. Coverage OECD members, ~1990s→. (data.oecd.org / stats.oecd.org). **[ADD exact dataset IDs when fetching]**

**UNESCO UIS** — tertiary graduates by ISCED field for non-OECD countries (global coverage for the modern denominator of "engineering graduates").

---

## 5. Population denominators (long run)

| Source | Geography | Coverage | Access |
|---|---|---|---|
| **Maddison Project Database 2023** | Global (UK, DE, FR incl.) | 1 AD–2022, population + GDP p.c. | rug.nl/ggdc; DOI 10.34894/INZBF2; Excel/Stata download. Annual for modern era, benchmark years earlier. https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023 |
| **Bank of England, "A Millennium of Macroeconomic Data"** | UK / England / GB | 1086–2016; population + 130 macro vars | Excel: https://www.bankofengland.co.uk/statistics/research-datasets ; mirrors datahub.io, Kaggle. Best UK-specific long-run population. |
| **ONS population estimates & historical censuses** | UK | Mid-year 1838→; censuses 1801→ | ons.gov.uk; A Vision of Britain (visionofbritain.org.uk) & GB Historical GIS for parish/county historic figures. |
| **Destatis population** | Germany | 1950→ online; historical via Statistisches Reichsamt / *Statistik des Deutschen Reichs* | destatis.de GENESIS; historical German states via B.R. Mitchell. |
| **INSEE population** | France | 1946→ online; historical via INED / Toutain reconstructions | insee.fr; INED historical demography. |
| **B.R. Mitchell, *International Historical Statistics — Europe*** | Europe | ~1750–present | Standard reference volume (print/library) for pre-1900 national populations across states. |
| **Our World in Data / Clio Infra / HYDE** | Global | very long run (to 1500 and earlier) | Convenient harmonised long-run population for the ~1500 anchor; ultimately draws on Maddison/HYDE. ourworldindata.org; clio-infra.eu |

**Recommendation:** Use **Maddison 2023** as the master denominator (consistent cross-country, back to 1 AD), cross-checked with **Bank of England millennium** for the UK, **B.R. Mitchell / Destatis / INSEE** for Germany & France pre-1900.

---

## Definition-mapping cheatsheet

- **(a) Period-contemporary numerator sources:** ICE/IMechE/IET/VDI membership rolls; Engineering Council register (UK, 1965/1981→); Corps + grandes écoles registers (FR, 1716/1747/1794→); Diplom-Ingenieur graduates & TH enrollments (DE, ~1870→); census "engineer" occupation (with era-appropriate meaning).
- **(b) Modern-standard numerator sources:** ISCO **OC21 "Science & engineering professionals"** (Eurostat `lfsa_egai2d`, Nomis SOC 212, Destatis KldB→ISCO); ISCED-F **field 07** engineering graduates (Eurostat `educ_uoe_grad02`, HESA, Destatis Hochschulstatistik, OECD/UIS). Applied retrospectively via I-CeM occupation coding for the UK pre-1911.

## Priority gaps to close (need direct fetch / library)
1. **Exact Engineering Council back-series** (CEng/IEng/EngTech by year) — download annual PDFs (engc.org.uk was 403 in-session).
2. **Continuous ICE/IMechE/IET year-by-year membership** — assemble from Grace's Guide + institution archives; reconcile with Engineering Council to avoid double counting.
3. **VDI historical membership series 1856–1945** — VDI jubilee histories + Gispen/Lundgreen tables.
4. **German pre-1914 engineer & TH-student counts** — Gispen appendix + **Peter Lundgreen** quantitative studies + *Statistik des Deutschen Reichs*.
5. **French historical engineer counts** — ENPC/Polytechnique registers + **Grelon / Picon** literature; INSEE for modern stock.
6. **Occupation-code disambiguation in I-CeM** (engineer vs. engine-driver pre-1881) — methodological task, not a new source.
7. Confirm Eurostat/OECD **exact dataset IDs & earliest years**, and pull bulk downloads via API.
