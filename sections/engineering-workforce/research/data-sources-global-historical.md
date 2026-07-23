# Data Sources: Formally Trained Engineers as a Share of Population, Global & Historical (~1500–present)

**Research question:** Long-run trend (back to ~1500) in the number of formally trained engineers as a share of population, globally and by country, under two definitions: (a) period-contemporary formal engineers; (b) people who would qualify as modern engineers.

**Scope of this file:** the GLOBAL picture and the hard pre-1900 / early-modern period (1500–1900). Compiled 2026-07-23.

**Verification note:** URLs below were located via web search; several provider sites (rug.nl, ourworldindata.org grapher pages, nber.org, campop) returned HTTP 403 to the automated fetcher, so their *contents* were confirmed from search-result snippets rather than a full page read. Such items are flagged `[URL not directly fetched]`. No figures or URLs here are invented; anything uncertain is flagged. Always re-verify the exact download link and latest version before use.

---

## 1. TL;DR — the measurement architecture

To build the series you need **numerator ÷ denominator**:

- **Denominator (population):** well-solved back to 1500 (and to 10,000 BCE). Use HYDE 3.3 + Gapminder + UN, most conveniently via the Our World in Data population dataset, or Maddison for a country-economist-standard series. This is the *easy* half.
- **Numerator (engineers):** this is the binding constraint. There is **no continuous global engineer headcount series before ~1950**, and arguably not before UNESCO/ILO data in the late 20th c. Pre-1900 you must assemble it from (i) institution/corps membership rolls, (ii) national occupational censuses (esp. the Cambridge occupational-structure project for Britain and IPUMS for 1850+), and (iii) upper-tail human-capital proxies (patents, Encyclopédie subscribers). Expect a *mosaic of national point-estimates*, not a global time series, before the 20th century.

---

## 2. Ranked "best data sources" table

Rank = usefulness for THIS project (long-run, global, engineer share), weighting coverage depth, authority, and downloadability.

| # | Source | Provider | Role | Coverage (geo / time) | Granularity | Format / access | License | Key limitation |
|---|--------|----------|------|------------------------|-------------|-----------------|---------|----------------|
| 1 | **Our World in Data – Population** | OWID (compiles HYDE, Gapminder, UN) | Denominator (headline) | Global + countries/regions; **10,000 BCE–2023** (+proj. to 2100) | Country-year (annual from 1800; decadal 1500–1800 via HYDE) | CSV/ZIP download button on grapher; also API | CC BY (OWID) / upstream terms | Pre-1800 country detail is interpolated/modelled |
| 2 | **HYDE 3.3** | PBL Netherlands Env. Assessment Agency + Utrecht Univ. | Denominator (primary pre-1800) | Global gridded + national; **10,000 BCE–2023** | 5-arc-min grid; national totals; decadal pre-1950 | ESRI ASCII grids + tables; DataHub/Kaggle mirrors | Research use (cite PBL) | Deep-past numbers are model reconstructions; sparse pre-1950 time resolution |
| 3 | **Maddison Project Database 2023** | Groningen Growth & Dev. Centre (GGDC), Univ. of Groningen | Denominator + GDP context | 169 countries/regions; **1 AD–2022** (sparse early, denser post-1500) | Country-year | Excel + Stata on Dataverse (DOI 10.34894/INZBF2) | Academic, cite | Population is secondary to GDP focus; early years thin |
| 4 | **UIS Data (UNESCO Institute for Statistics)** | UNESCO | Numerator (modern): tertiary graduates in Engineering | ~200 countries; **~1970–present** (patchy early) | Country-year, by ISCED-F field 07 (Engineering, Manufacturing & Construction) | Data Browser + Data API + Bulk Download Service (BDDS, flat files) | CC BY-SA 3.0 IGO (typical UIS) | Field 07 bundles manufacturing & construction with engineering; pre-1998 sparse; graduates ≠ stock of engineers |
| 5 | **ILOSTAT – Employment by occupation (ISCO)** | ILO | Numerator (modern): stock of working "Engineering professionals" | ~180 countries; **~1990s–present** (some back to ~1969) | Country-year, ISCO-08 sub-major **21** (Science & engineering professionals) / minor **214** (Engineering professionals, excl. electrotech.) | Bulk CSV (gz), API, Rilostat R pkg | CC BY 4.0 | Occupational-code comparability breaks at ISCO revisions; short history |
| 6 | **Cambridge "Occupational Structure of Britain c.1379–1911"** | Cambridge Group (Shaw-Taylor, Wrigley) / economiespast.org | Numerator (pre-1900, best national case) | England & Wales (some Britain); **c.1710–1911** (+ medieval fragments) | Parish/county; PST occupational codes | Working papers (PDF) + data via economiespast.org / UK Data Service | Academic, cite | PST "engineer" category emerges late & is small; England-only; definitional churn |
| 7 | **IPUMS International** | Univ. of Minnesota | Numerator (national censuses): harmonized OCC incl. engineers | 100+ countries; **1960 forward** (a few 1850s+ via IPUMS-USA/NAPP) | Individual microdata, harmonized OCC/OCCISCO | Free download after registration; extract system | Free, registration + citation | Starts ~1960 for most; earliest samples only US/Europe/Canada |
| 8 | **Squicciarini & Voigtländer (2015), Encyclopédie subscribers** | QJE / NBER WP 20219 | Pre-1900 upper-tail human-capital **proxy** | France (city-level), mid-18th c. | City | Replication data (QJE/authors) | Academic | Proxy for "knowledge elite," not an engineer count |
| 9 | **Hanlon (2022) "The Rise of the Engineer"** | NBER WP 29751 (W. Walker Hanlon) | Pre-1900 numerator method + patents/DNB | Britain; ~1700s–1860s | Individual (439 pre-1850 engineers in DNB) + patents | Working paper PDF; replication data | Academic | Britain-only; elite biographical sample, not full stock |
| 10 | **Clio-Infra** | IISH (Amsterdam) | Long-run human-capital context (not engineers directly) | Global; **1500–2010** | Country-decade | Per-indicator XLSX download | Academic | No engineer indicator; use for education/numeracy denominators of "human capital" |
| 11 | **Institution rolls: ICE, École des Ponts, Corps des Ponts, Bergakademie** | Individual institutions / historians | Pre/early-modern period-contemporary counts | France, Britain, Saxony, etc.; ~1650–1900 | Institution-level point estimates | Secondary literature, institutional archives | Varies | Point estimates only; not a continuous series; membership ≠ practising engineers |

---

## 3. POPULATION DENOMINATORS (detailed)

### 3.1 Our World in Data — Population (recommended headline denominator)
- **URL:** https://ourworldindata.org/grapher/population `[URL not directly fetched; content from search]`
- **Sources methodology page:** https://ourworldindata.org/population-sources
- **Composition (per OWID):** **HYDE v3.3 (2023)** for 10,000 BCE–1799; **Gapminder v7 (2022)** for 1800–1949; **UN World Population Prospects (2024)** for 1950–2100. Gapminder Systema Globalis (2023) fills former states (USSR, Yugoslavia).
- **Download:** "Download" button on the grapher page → ZIP with CSV + JSON metadata + README. Country-year, annual from 1800.
- **Best for:** the ready-made spliced long-run series; annual granularity 1800+; consistent country coding.
- **Limitation:** pre-1800 country-level figures are decadal (from HYDE) and modelled.

### 3.2 HYDE 3.3 (History Database of the Global Environment)
- **Provider:** PBL Netherlands Environmental Assessment Agency + Utrecht University.
- **Coverage:** 10,000 BCE–2023; 5-arc-minute gridded population + land use; also national/regional totals.
- **Access:** primary distribution via PBL/ftp; mirrors on DataHub (https://datahub.io/climate-and-environment/hyde-history-database-of-the-global-environment) and Kaggle (https://www.kaggle.com/datasets/ilyenkov/hyde-3-3). Grids in ESRI ASCII.
- **Best for:** the pre-1500 and 1500–1800 denominator, and any sub-national/gridded work.
- **Limitation:** deep-past values are reconstructions; only decadal for 1800–1950.

### 3.3 Maddison Project Database 2023
- **Provider:** GGDC, University of Groningen.
- **Landing:** https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023 `[returns 403 to fetcher]`
- **Data (authoritative):** DataverseNL, **DOI 10.34894/INZBF2** → https://doi.org/10.34894/INZBF2 . Files in **Excel and Stata** (CSV not confirmed as an official export; convert from Excel).
- **Coverage:** 169 countries/regions, 1 AD–2022; GDP per capita **and** population.
- **Citation:** Bolt, J. & van Zanden, J.L. (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update," *Journal of Economic Surveys*, DOI 10.1111/joes.12618.
- **Best for:** economist-standard denominators + GDP-per-capita covariate; harmonized long-run country panel.

### 3.4 UN World Population Prospects (2024)
- **Provider:** UN DESA Population Division. **URL:** https://population.un.org/wpp/ `[not directly fetched]`
- **Coverage:** 1950–2100, all countries; CSV/Excel + API. The modern-era gold standard denominator (already embedded in OWID from 1950).

### 3.5 Gapminder
- **Provider:** Gapminder Foundation. GitHub: https://github.com/open-numbers/ddf--gapminder--population and `ddf--gapminder--systema_globalis`.
- **Coverage:** 1800–present (annual), country. Underlies OWID's 1800–1949 segment.

**Denominator recommendation:** use OWID's spliced series as the working denominator; keep Maddison as a cross-check and for the GDP covariate; go to HYDE directly only if you need gridded/sub-national or pre-1500 detail.

---

## 4. MODERN-ERA ENGINEER NUMERATORS (20th c.–present)

### 4.1 UNESCO UIS — tertiary graduates in Engineering (flow)
- **Data Browser:** https://databrowser.uis.unesco.org/
- **API:** https://api.uis.unesco.org/api/public/documentation/ (100,000-record/request cap).
- **Bulk Data Download Service (BDDS):** aggregated datasets as flat files (linked from the Data Browser "Resources" page https://databrowser.uis.unesco.org/resources).
- **Also via:** UNdata series **G_56_F500_DCOUNT** "Tertiary graduates from Engineering, Manufacturing and Construction programmes" (http://data.un.org/Data.aspx?d=UNESCO&f=series%3AG_56_F500_DCOUNT); and World Bank Data360 dataset "UNESCO_UIS" (https://data360.worldbank.org/en/dataset/UNESCO_UIS).
- **Definition:** ISCED-F 2013 **broad field 07 = Engineering, Manufacturing and Construction** (note: broader than engineering alone). Detailed field descriptions PDF: https://www.uis.unesco.org/sites/default/files/medias/fichiers/2025/04/international-standard-classification-of-education-fields-of-education-and-training-2013-detailed-field-descriptions-2015-en.pdf
- **Coverage:** ~1970s onward, thin before ~1998; ~200 countries.
- **Limitation:** measures **annual graduates (flow)**, not stock; field 07 mixes construction/manufacturing; no pre-1970 data.

### 4.2 ILOSTAT — Employment by occupation (stock of working engineers)
- **Bulk download:** https://ilostat.ilo.org/data/bulk/ (zipped CSV `.gz` + CSV dictionaries).
- **Data tools:** https://ilostat.ilo.org/data/
- **Relevant indicator codes:** `EMP_TEMP_SEX_OCU_NB` (employment by sex & occupation) and modelled `EMP_2EMP_SEX_OCU_NB`; disaggregate by ISCO.
- **Occupation definition:** ISCO-08 sub-major group **21 "Science and Engineering Professionals"**; minor group **214 "Engineering professionals"** (excludes 215 electrotechnology engineers and 216 architects/planners — decide whether to include). ISCO methodology: https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/
- **Coverage:** mostly 1990s–present; some series to ~1969; ~180 countries.
- **Limitation:** breaks across ISCO-68/88/08 revisions; "engineering professionals" excludes technicians (ISCO 31) — a definitional choice that matters for "modern engineer."

### 4.3 OECD & Eurostat (rich-country depth)
- **OECD.Stat / Education at a Glance:** graduates by field (engineering), tertiary; https://stats.oecd.org / https://gpseducation.oecd.org
- **Eurostat:** `LFSA_EGAI2D` employed persons by ISCO-08 2-digit (occupation stock); `hrst_*` HRST/graduate series. https://ec.europa.eu/eurostat/databrowser/
- **Best for:** long, consistent post-1970 OECD panels to benchmark UIS/ILO.

### 4.4 National statistical offices (deep national series)
- US: NSF NCSES "Science & Engineering Indicators"; Census/ACS occupation. UK: ONS + professional-body membership. India/China: national education ministries. Use where a specific country needs pre-1970 modern-era depth.

---

## 5. PRE-1900 / EARLY-MODERN NUMERATOR (the hard core)

There is **no global engineer count before the 20th century.** Build a mosaic from three strands.

### 5.1 Institutional & corps membership (period-contemporary "formal engineers")
Concrete, citable anchor points (all from secondary literature / institutional histories — treat as point estimates, verify each before use):

- **France – Corps des ingénieurs des Ponts et Chaussées:** created by royal order **1716**; small body of state civil engineers. History: https://ecoledesponts.fr/en/school/welcome-school/school-history ; Picon, "Le Corps des Ponts et Chaussées" (Harvard GSD PDF: https://www.gsd.harvard.edu/wp-content/uploads/2016/06/picon-corpsdespontsetchausseese.pdf).
- **France – École des Ponts et Chaussées:** founded **1747**; ~50 students at outset; **~700 students total 1750–1789**, fewer than half admitted to the Corps. Heritage site: https://heritage.ecoledesponts.fr/enpc/en/content/histoire-de-lecole-des-eleves-et-des-ingenieurs-en
- **France – École Polytechnique:** **1794/95** (as École centrale des travaux publics). https://www.polytechnique.edu/bibliotheque/patrimoine/portail-patrimoine/histoire-de-lecole
- **France – military engineers ("ingénieurs du roi" → Génie militaire 1743 → Corps du Génie ~1750s):** Vauban-era corps, 17th c. Reference: https://sites-vauban.org/en/resources/bibliographic-references/vauban-et-le-corps-des-ingenieurs-militaires (exact headcounts require specialist archival sources — **flagged uncertain**).
- **Britain – Institution of Civil Engineers (ICE):** founded **1818** (8 founders); Royal Charter 1828. Membership (ICE + IMechE combined per one secondary source): **~220 (1830) → ~2,000 (1850) → ~3,500 (1870)**. Wikipedia: https://en.wikipedia.org/wiki/Institution_of_Civil_Engineers ; ICE history: https://www.ice.org.uk/about-us/our-organisation/history — **verify the 220/2,000/3,500 figures against a primary ICE source before citing.**
- **Britain – Institution of Mechanical Engineers:** founded **1847**.
- **Saxony – Bergakademie Freiberg (mining/metallurgy + surveying):** founded **1765**, oldest surviving mining academy; spawned St. Petersburg (1773), Almadén (1777), Mexico (1792) academies. https://en.wikipedia.org/wiki/Freiberg_University_of_Mining_and_Technology
- **Mining engineering lineage:** Agricola's *De re metallica* (1556) marks the codified body of mining/metallurgical knowledge that these academies later formalized — useful for the "definition" narrative, not a headcount.

**How to use:** these give sparse, country-specific level estimates (tens → hundreds → low thousands) that, divided by contemporaneous population (from §3), yield engineer-share *point estimates* for France and Britain across the 18th–19th c. They will not knit into a smooth global series.

### 5.2 Occupational censuses (best systematic pre-1900 counts)
- **Cambridge "Occupational Structure of Britain c.1379–1911"** (Shaw-Taylor & Wrigley, Cambridge Group). Project hub: https://www.campop.geog.cam.ac.uk/research/projects/occupations/britain19c/ ; visualization/data portal: https://www.economiespast.org/ . Papers (PDF): https://www.campop.geog.cam.ac.uk/research/projects/occupations/britain19c/papers/paper2.pdf and `/paper3.pdf`. Data coded to **PST (Primary/Secondary/Tertiary)** system; England & Wales adult-male structure reconstructed c.1710, 1817, and decennial censuses 1851–1911. `[campop pages 403 to fetcher — confirm data-download route via economiespast.org and the UK Data Service]`
  - *Value:* the single best route to a **quantitative English "engineer" occupational count** back to the early 19th c. (censuses started recording "engineer"/"civil engineer"/"engine maker" as occupational titles from 1841/1851).
  - *Caveat:* the occupational label "engineer" in Victorian censuses often meant engine-drivers/mechanics, not degreed professionals — a definitional landmine (see §6).
- **IPUMS International:** https://international.ipums.org/ — harmonized census microdata, 100+ countries, **1960 forward** (occupation vars OCC, OCCISCO). For pre-1900 census microdata use **IPUMS-USA** (1850+) and **NAPP** (North Atlantic Population Project: US, Canada, Britain, Scandinavia, 19th c.). Free, registration required.
- **National census reports (published tables):** many European censuses 1850–1900 published occupation tables listing "engineers/surveyors" — primary but non-harmonized.

### 5.3 Upper-tail human-capital proxies (when no count exists)
- **Squicciarini & Voigtländer (2015), "Human Capital and Industrialization: Evidence from the Age of Enlightenment," QJE 130(4):1825–1883** (NBER WP 20219: https://www.nber.org/papers/w20219 ; author PDF: https://www.anderson.ucla.edu/faculty/nico.v/Research/Encyclopedie_forthcoming.pdf). City-level **Encyclopédie subscriber density** as a proxy for the knowledge elite; links to British patents + 1840s French firm survey.
- **Hanlon (2022), "The Rise of the Engineer," NBER WP 29751** (https://www.nber.org/papers/w29751 ; PDF https://www.nber.org/system/files/working_papers/w29751/w29751.pdf). Uses **all 439 engineers born before 1850 in the Oxford Dictionary of National Biography** + patent data; documents the rising share of patents attributable to engineers (10% in 1800s → 3× by 1860s). Method template for a Britain numerator; replication data likely available.
- **Patent records** (as engineer-activity proxy): British patents (via Hanlon; and Bottomley, *The British Patent System during the Industrial Revolution*); Google Patents historical; USPTO historical. Proxy for engineering activity, not headcount.
- **Clio-Infra** (https://clio-infra.eu/): 1500–2010 human-capital indicators (average years of education, numeracy, book titles per capita). **No engineer indicator**, but useful to contextualize the human-capital denominator and to sanity-check where formal technical education could even exist.

### 5.4 Additional cross-country historical human-capital datasets
- **Barro-Lee Educational Attainment** (http://www.barrolee.com/) — 1950–2010, tertiary attainment by country (not field-specific; modern only).
- **Lee-Lee (2016)** long-run schooling, 1870–2010.
- **de la Croix et al., academic/university data** and **RETE/university foundation datasets** — counts of universities/technical schools over time as an *institutional-capacity* proxy for where engineers could be trained.

---

## 6. The conceptual problem: applying a "modern engineer" definition retroactively

This is a genuine measurement hazard, not just a caveat. Key points, with supporting scholarship:

1. **"Engineer" barely existed as a distinct civilian profession before ~1750.** Pre-industrial engineers were essentially only **military (fortification/siege) and, later, civil** practitioners; the profession did not clearly "professionalize" until the 18th–19th c. (Institution of Civil Engineers 1818, IMechE 1847). See the *tandfonline* survey "Becoming an engineer in eighteenth-century Europe" (https://www.tandfonline.com/doi/full/10.1080/19378629.2011.631271) and Encyclopedia.com "Engineers."
2. **The word's meaning drifts.** In 19th-c. British censuses "engineer" frequently denoted engine-operators/mechanics, inflating naive counts; conversely, many people doing *modern-engineer work* (millwrights, instrument makers, surveyors, master masons, mining Steiger, architects) were never labelled "engineer." Any period-contemporary count and any "would-qualify-as-modern" count will therefore **diverge sharply**, and the gap itself is the interesting object.
3. **Two-definition strategy (matches the project's a/b split):**
   - **(a) Period-contemporary:** count only those the era itself called engineers / admitted to a corps or institution (§5.1, §5.2 titles). Cleaner provenance, but tiny and institution-gated pre-1850.
   - **(b) Modern-equivalent:** back-cast a modern occupational definition (ISCO-08 "engineering professionals" ≈ tertiary-trained applied-science practitioners) onto historical occupation lists — pulling in surveyors, mining/fortification experts, machine designers. This requires an explicit crosswalk from PST/historical occupational titles to a modern engineer class; **document the crosswalk as a first-class deliverable**, because results are highly sensitive to it.
4. **Bounding it:** Hanlon (2022) and the *Rise of the Engineer / Inventing the Professional Inventor* literature effectively bound the British numerator two ways — a narrow elite (439 DNB engineers) and a broad activity proxy (share of patents by engineers) — giving a lower/upper envelope. Replicate that "narrow institutional count vs. broad functional proxy" bracketing per country to express definitional uncertainty as an explicit range rather than a false-precision point.
5. **Survivorship/elite bias:** DNB, institution rolls, and subscriber lists over-represent the famous/elite; census/PST data are more representative but start late (England ~1841). Use them as complementary bounds.

---

## 7. Concrete download recipes

- **Population (headline):** OWID grapher → https://ourworldindata.org/grapher/population → "Download" → full-history CSV. (Programmatic: OWID grapher CSV endpoint pattern `.../grapher/population.csv?csvType=full`.)
- **Population (deep-past / gridded):** HYDE 3.3 via DataHub mirror https://datahub.io/climate-and-environment/hyde-history-database-of-the-global-environment (or PBL FTP for authoritative grids).
- **Maddison:** https://doi.org/10.34894/INZBF2 → download the MPD 2023 Excel (`mpd2023_web.xlsx`) — contains `gdppc`, `pop`, country, year.
- **Engineering graduates (modern):** UIS Data Browser → filter indicator = graduates, ISCED field 07 → export; or BDDS flat file; or UNdata series `G_56_F500_DCOUNT`.
- **Engineering workforce stock (modern):** ILOSTAT bulk https://ilostat.ilo.org/data/bulk/ → `EMP_TEMP_SEX_OCU_NB` (or use Rilostat: `get_ilostat("EMP_TEMP_SEX_OCU_NB")`) → filter ISCO-08 code 21/214.
- **Census microdata (engineers by occupation, 1850+/1960+):** register at https://international.ipums.org/ (global 1960+) or https://www.nappdata.org/ / IPUMS-USA (19th c. Atlantic) → build extract with OCC/OCCISCO → keep engineer codes.
- **Britain pre-1900 occupational counts:** economiespast.org + campop working papers; underlying data via UK Data Service (search "Occupational Structure of England and Wales").
- **Proxies:** Squicciarini-Voigtländer replication files (QJE 2015 / author page); Hanlon NBER WP 29751 PDF + replication.

---

## 8. Biggest data gaps (explicit)

1. **No pre-1970 global engineer series exists** — the numerator must be assembled country-by-country from heterogeneous sources; a truly *global* pre-20th-c. figure will be an educated aggregation, not a measured series.
2. **Pre-1850 counts are institution-gated** (corps/school rolls) and therefore capture *formally credentialed* engineers only — missing the far larger body of functionally-engineering practitioners.
3. **Definitional discontinuity** across "engineer" meanings (engine-driver vs. professional) corrupts naive census counts; needs a documented crosswalk.
4. **Non-Western coverage is nearly absent before the 20th c.** (China, India, Ottoman, Japan pre-Meiji) — early data is overwhelmingly French/British/German. Global shares before ~1900 will be dominated by a few European denominators.
5. **Flow vs. stock mismatch:** UIS gives graduate *flows*; ILO gives employment *stock*; institution rolls give *membership*. Reconciling these into one "number of engineers" requires assumptions (career length, attrition).
6. **Field-boundary noise in modern data:** UIS field 07 bundles manufacturing/construction; ISCO 214 excludes electro/ICT engineers (215) and technicians (31) — the modern number swings 2–3× depending on boundaries chosen.
7. **Unverified secondary figures:** several early headcounts here (ICE 220/2,000/3,500; French corps sizes) come from tertiary sources and need primary confirmation before publication.

---

## 9. Priority next steps

1. Lock the denominator: pull OWID population CSV + Maddison MPD 2023; splice-check.
2. Build the modern numerator: UIS (graduates, field 07) + ILOSTAT (stock, ISCO 214), 1970–present, and reconcile.
3. Britain deep-dive as the pre-1900 pilot: extract engineer occupational counts from the Cambridge/economiespast PST data (1841–1911) + ICE rolls + Hanlon's DNB/patent envelope → produce a two-definition English engineer-share series 1750–1911.
4. France pilot: Ponts et Chaussées + Polytechnique + Génie rolls → point estimates.
5. Write the historical→modern occupational crosswalk (PST / historical titles → ISCO-08 "engineering professionals") and treat it as a versioned artifact.
6. Document every early figure's provenance and confidence; express definitional uncertainty as ranges.

---

### Source list (primary/authoritative)
- OWID Population & sources: https://ourworldindata.org/grapher/population ; https://ourworldindata.org/population-sources
- HYDE 3.3: https://datahub.io/climate-and-environment/hyde-history-database-of-the-global-environment
- Maddison 2023: https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023 ; data DOI https://doi.org/10.34894/INZBF2
- UN WPP: https://population.un.org/wpp/
- UIS: https://databrowser.uis.unesco.org/ ; API https://api.uis.unesco.org/api/public/documentation/ ; UNdata G_56_F500_DCOUNT http://data.un.org/Data.aspx?d=UNESCO&f=series%3AG_56_F500_DCOUNT
- ILOSTAT: https://ilostat.ilo.org/data/bulk/ ; ISCO methods https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/
- IPUMS International: https://international.ipums.org/ ; NAPP: https://www.nappdata.org/
- Cambridge Occupational Structure: https://www.campop.geog.cam.ac.uk/research/projects/occupations/britain19c/ ; https://www.economiespast.org/
- Clio-Infra: https://clio-infra.eu/
- Squicciarini & Voigtländer 2015: https://www.nber.org/papers/w20219
- Hanlon 2022 "Rise of the Engineer": https://www.nber.org/papers/w29751
- ICE history: https://www.ice.org.uk/about-us/our-organisation/history ; École des Ponts history: https://ecoledesponts.fr/en/school/welcome-school/school-history ; Bergakademie Freiberg: https://en.wikipedia.org/wiki/Freiberg_University_of_Mining_and_Technology
