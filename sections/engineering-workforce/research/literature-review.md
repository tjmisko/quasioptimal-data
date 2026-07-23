# Literature Review: Measuring the Engineering Profession/Workforce Over the Long Run

**Prepared:** 2026-07-23
**Research question (project):** What is the long-run trend (back to ~1500) in the number of formally trained engineers as a share of population, globally and for specific countries? Two working definitions of "engineer": (a) whatever counted as a formally trained/recognized engineer *at the time*; (b) people who would qualify as an engineer *by modern standards*.
**Scope of this document:** A scholarly literature review of how academics and analysts have approached measuring the size of the engineering profession over time — *why* they care, *what* data they use, and *what* they find. It is a map of the literature and its datasets, not an original estimate.

> **Methodological note on sourcing.** All citations below were located via live web search. Bibliographic details (authors, titles, journals, years, DOIs/URLs) are drawn from publisher/repository pages (Oxford Academic, NBER, CEPR, IDEAS/RePEc, Cambridge Core, university sites) and are reliable. Direct full-text retrieval of several PDFs (World Bank, CESifo, SSRN, arXiv, publisher paywalls) was **blocked in this environment** (403/egress policy), so specific *quantitative figures* attributed to a paper come from the authors' own summaries (VoxDev/VoxEU/World Bank blogs, university press releases, journal abstracts) rather than from my reading of the primary tables. Points where a figure comes from a **secondary or non-authoritative source** and should be re-verified against the primary source are flagged **[VERIFY]**. Nothing here is fabricated; where I could not confirm something I say so explicitly.

---

## 1. Why economists care: engineers, "upper-tail" human capital, and growth

The modern economics interest in *counting engineers specifically* (rather than years of schooling or literacy) rests on a distinction between **average human capital** (literacy, primary schooling, mean years of education) and **upper-tail human capital** (a thin elite of technically skilled, knowledge-producing individuals — engineers, mechanics, inventors, "knowledge elites"). The claim in this literature is that the upper tail, not the average, is what drove the transition to modern growth and continues to explain cross-country income gaps.

### 1.1 The "engineers vs. lawyers" allocation-of-talent thesis

- **Murphy, Kevin M., Andrei Shleifer, and Robert W. Vishny (1991). "The Allocation of Talent: Implications for Growth." *Quarterly Journal of Economics* 106(2): 503–530.** NBER WP 3530.
  - URL (abstract): https://academic.oup.com/qje/article-abstract/106/2/503/1905462 ; NBER: https://www.nber.org/papers/w3530 ; Shleifer copy: https://scholar.harvard.edu/shleifer/publications/allocation-talent-implications-growth
  - **Argument/finding:** When talented people become entrepreneurs/innovators they raise growth; when they become rent-seekers (e.g., lawyers) they merely redistribute. Cross-country evidence: **a higher share of college students majoring in engineering is associated with faster growth; a higher share concentrating in law with slower growth.**
  - **Data/definition:** College-major *enrollment shares* by field (engineering vs. law) across countries, correlated with growth. This is the foundational cite for treating "engineer density" as a growth-relevant quantity — but it measures *students choosing a major*, not the stock of practicing engineers.
  - **Caveat:** Cross-sectional correlation; small country sample; "engineering major share" is a proxy, and reverse causality/omitted variables are acknowledged concerns in the subsequent literature.

### 1.2 The central paper for this project: Maloney & Valencia Caicedo

This is the single most directly relevant body of work — it explicitly constructs long-run **engineer-density** data and links it to development.

- **Maloney, William F., and Felipe Valencia Caicedo (2022). "Engineering Growth: Innovative Capacity and Development in the Americas." *Journal of the European Economic Association* 20(4): 1554–1594.** (August 2022.)
  - URL (abstract): https://academic.oup.com/jeea/article-abstract/20/4/1554/6550029
  - Predecessor working papers (same project, evolving titles):
    - **"Engineers, Innovative Capacity and Development in the Americas."** World Bank Policy Research Working Paper **6814** (2014). IDEAS: https://ideas.repec.org/p/wbk/wbrwps/6814.html ; SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2451275
    - **"Engineering Growth: Innovative Capacity and Development in the Americas."** CESifo Working Paper **6339** (2017). https://ideas.repec.org/p/ces/ceswps/_6339.html ; SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2932756
  - **Definition of "engineer":** Members of the engineering labor force / engineering graduates. Density is expressed as **engineers (or engineering graduates) per 100,000 (male) workers**. Series are built by "aggregating graduates from local engineering programmes, augmented with information from censuses and professional societies." **[VERIFY exact construction against the JEEA appendix.]**
  - **Data / geography / time span:** A newly constructed database of the **share of engineers in the labor force during the Second Industrial Revolution (c. 1870–1914)**, at the **county level for the United States** and the **state and national levels across the Americas** (incl. Argentina, Chile, Mexico, and comparators such as the Nordic countries).
  - **Key quantitative findings:**
    - A one-standard-deviation increase in engineering density in **1880** is associated with roughly **10% higher US county income today**; patenting capacity adds another ~10%. National differences in engineering density explain **~a quarter of the income divergence within the Americas**. **[VERIFY — early press releases stated "16%"; the published JEEA version reports ~10% for the county-income channel.]**
    - Illustrative 1900 densities (engineers per 100,000 workers): **Nordic countries ~100; the US South ~60; Chile, Argentina and the rest of Latin America <20** — despite similar income levels c. 1900, i.e., a roughly *tenfold* gap in engineers among similarly-rich places, which then diverged. **[VERIFY figures against paper; sourced from authors' VoxEU/UBC summaries.]**
  - **Why it matters for us:** This is essentially the only peer-reviewed source that has *systematically assembled engineer-per-worker series across many countries for a pre-1914 benchmark.* Its underlying database (US county + Americas state/national) is the most important dataset lead for the project.
  - **Caveats (authors' and reviewers'):** Engineer counts before national licensing are noisy; "engineer" is defined heterogeneously across countries and censuses; graduate-based counts miss self-taught/"shop-trained" engineers; persistence regressions face standard omitted-variable/institutions concerns.
  - Accessible summaries: World Bank blog https://blogs.worldbank.org/en/psd/engineering-growth-innovative-capacity-and-development ; VoxDev https://voxdev.org/topic/technology-innovation/engineering-growth-innovative-capacity-and-development ; VoxEU https://voxeu.org/article/engineering-growth-innovative-capacity-and-development ; UBC news https://economics.ubc.ca/news/todays-prosperous-economies-owe-wealth-to-engineers-of-the-past/

### 1.3 Upper-tail human capital and the Industrial Revolution

- **Squicciarini, Mara P., and Nico Voigtländer (2015). "Human Capital and Industrialization: Evidence from the Age of Enlightenment." *Quarterly Journal of Economics* 130(4): 1825–1883.** NBER WP 20219 (2014).
  - URL: https://academic.oup.com/qje/article-abstract/130/4/1825/1914932 ; NBER PDF: https://www.nber.org/system/files/working_papers/w20219/w20219.pdf
  - **Definition/proxy:** "Knowledge elites" proxied by **city-level subscriptions to Diderot's *Encyclopédie*** in mid-18th-century France (a proxy for upper-tail knowledge, distinct from literacy).
  - **Finding:** Subscriber density strongly predicts **city growth after the onset of French industrialization**; literacy predicts cross-sectional development but **not growth.** Mechanism (via British patents + 1840s French firm survey): upper-tail knowledge raised productivity specifically in innovative industrial technologies.
  - **Relevance/caveat:** Establishes the *average vs. upper-tail* distinction empirically. The proxy is encyclopédie subscribers, not engineers per se, but the paper is the canonical "upper-tail human capital" reference invoked by the engineering-density literature.

- **Kelly, Morgan, Joel Mokyr, and Cormac Ó Gráda (2023). "The Mechanics of the Industrial Revolution." *Journal of Political Economy* 131(1): 59–94.** CEPR DP 14884; SSRN 3628205.
  - URL: https://cepr.org/publications/dp14884 ; SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3628205
  - **Finding:** Across 41 English counties (1760s–1830s), industrialization (textile growth) is explained by **low wages + high mechanical/artisanal skills**; literacy, capital access, and coal proximity have *no* predictive power. Emphasizes Britain's abundant supply of **artisan skills in metalworking** (watchmakers, iron founders, instrument makers) as the effective "upper tail."
  - **Relevance/caveat:** Reframes the relevant upper tail as *skilled artisans/mechanics* — a definitional expansion of "engineer" toward practitioners without formal credentials. Their skill measure is occupational, not credential-based. See also the related debate piece: Kelly, Mokyr & Ó Gráda, "Could Artisans Have Caused the Industrial Revolution?" (Rivisteweb/*Scienza & Politica*).

- **Mokyr, Joel (2002). *The Gifts of Athena: Historical Origins of the Knowledge Economy.* Princeton University Press.**
  - URL: https://press.princeton.edu/books/paperback/9780691120133/the-gifts-of-athena
  - **Contribution:** The "**Industrial Enlightenment**" framework distinguishing **propositional knowledge** ("what") from **prescriptive knowledge** ("how"), and the role of a small elite of intellectuals and skilled craftsmen ("upper-tail human capital") plus institutions (societies, publishers, engineering schools) that lowered *access costs* to useful knowledge. Conceptual backbone for why counting the technical elite (engineers) is economically meaningful.
  - **Caveat:** Conceptual/historical; supplies no time-series count of engineers.

### 1.4 Human capital and regional development (modern cross-section)

- **Gennaioli, N., R. La Porta, F. Lopez-de-Silanes, and A. Shleifer (2013). "Human Capital and Regional Development." *Quarterly Journal of Economics* 128(1): 105–164.** NBER WP 17158.
  - URL: https://academic.oup.com/qje/article-abstract/128/1/105/1840182 ; Harvard copy: https://shleifer.scholars.harvard.edu/sites/g/files/omnuum10626/files/shleifer/files/human_capital_qje_final.pdf
  - **Data:** 1,569 subnational regions in 110 countries. **Finding:** human capital (education) is the paramount correlate of regional development; entrepreneurial human capital matters. Uses education generally, not engineers specifically, but is a key anchor for the "human capital → development" chain.

### 1.5 The "human capital and the Industrial Revolution" debate

The engineering-density literature sits inside a long debate over whether *formal* human capital mattered for early industrialization.

- **Skeptical/"deskilling" side:** David Mitch (1999), "The Role of Education and Skill in the British Industrial Revolution" (in Mokyr, ed., *The British Industrial Revolution: An Economic Perspective*), argues formal education/literacy contributed little to early British growth. Robert C. Allen, *The British Industrial Revolution in Global Perspective* (2009), stresses cheap energy + expensive labor over schooling.
- **Revisionist/skills side:**
  - **de Pleijt, Alexandra, Alessandro Nuvolari, and Jacob Weisdorf (2020). "Human Capital Formation During the First Industrial Revolution: Evidence from the Use of Steam Engines." *Journal of the European Economic Association* 18(2): 829–889.** CEPR DP 12987. https://academic.oup.com/jeea/article-abstract/18/2/829/5398135 ; https://cepr.org/publications/dp12987
    - Classifies 2.6M English male workers (HISCO) into unskilled/lower/medium/high skill; finds steam-engine adoption **causally raised the share of (mechanical) skilled workers** at the county level, but had a **negative** effect on primary schooling/literacy — i.e., the IR demanded *artisanal* upper-tail skills, not mass literacy. (Also: de Pleijt & Weisdorf, "Human capital formation from occupations: the 'deskilling hypothesis' revisited," *Cliometrica*.)
  - de Pleijt & van Zanden and others on long-run "average years of schooling in England 1300–1900" (*Cliometrica* 2016) provide long-run human-capital series but not engineer counts.
  - **Relevance:** These papers show the field increasingly separates *credentialed* engineers from *skilled mechanics/artisans* — directly relevant to the project's two definitions.

---

## 2. History of the engineering profession and its professionalization

This literature is qualitative/institutional but supplies the definitional scaffolding (what counted as an "engineer," and when the category stabilized) and some head-counts of society memberships and graduates.

### 2.1 United States

- **Layton, Edwin T., Jr. (1971/1986). *The Revolt of the Engineers: Social Responsibility and the American Engineering Profession.* (Case Western Reserve UP 1971; Johns Hopkins UP 1986.)**
  - Reviews/essays: Project MUSE https://muse.jhu.edu/article/255448 ; ERIC ED275555 https://eric.ed.gov/?id=ED275555
  - **Focus:** professionalization, ethics, and the divided loyalty of the salaried engineer (employer vs. profession) in the early 20th century; a study of a "failed" professional-reform movement. Foundational to "engineering studies." Not primarily quantitative.
- **Reynolds, Terry S., ed. (1991). *The Engineer in America: A Historical Anthology from Technology and Culture.* University of Chicago Press.** ISBN 9780226710327. https://archive.org/details/engineerinameric0000unse
  - Anthology on the rise of the US engineering profession; includes Reynolds's own essays (e.g., "The Engineer in 19th-Century America" and "Engineers and Engineering History: Problems and Perspectives," ResearchGate: https://www.researchgate.net/publication/249027020 ). Good qualitative source on the shift from shop-trained to school-trained engineers and the founding of the branch societies.
- **Meiksins, Peter F. (1988). "The 'Revolt of the Engineers' Reconsidered." *Technology and Culture* 29(2).** https://muse.jhu.edu/article/889248/summary . Also Meiksins & Chris Smith, *Engineering Labour: Technical Workers in Comparative Perspective* (Verso, 1996) — comparative sociology of engineers (US, UK, France, Germany, etc.); explains why US engineers did not unionize. Sociological, comparative, not a count.
- **Founding of US engineering societies (chronology, from Encyclopedia.com "Engineering Societies" and Reynolds):** Boston Society of Civil Engineers (1848); American Society of Civil Engineers **ASCE (1852)**; American Institute of Mining Engineers (1871); American Society of Mechanical Engineers **ASME (1880)**; American Institute of Electrical Engineers **AIEE (1884)**. Society membership rolls are an underused proxy for the size of the professionalized workforce.

### 2.2 Germany

- **Gispen, Kees (1989). *New Profession, Old Order: Engineers and German Society, 1815–1914.* Cambridge University Press.** ISBN 9780521371988. https://www.cambridge.org/core/journals/history-of-education-quarterly/article/abs/... (review) ; Google Books: https://books.google.com/books/about/New_Profession_Old_Order.html?id=FfNVztgZ4bgC
  - **Contribution:** Social/educational history of German engineers; the split between academically trained **Diplom-Ingenieure** (Technische Hochschulen) and practical "shop engineers," and an **"overproduction of engineers"** employment crisis pre-1914 — an early instance of *supply* running ahead of professional absorption. Contains **charts, tables, and an appendix** (per publisher description) — a lead for German engineer/graduate counts. **[VERIFY tables.]**
- Wolfgang König's work on German technical education (see Fox & Guagnini, §3) complements Gispen.

### 2.3 Britain and the emergence of "civil" engineering as a distinct profession

- **Smeatonian Society of Civil Engineers (founded 1771)** — the world's oldest engineering society; John Smeaton coined "**civil engineer**" to distinguish civilian public-works engineers from **military** engineers. https://en.wikipedia.org/wiki/Smeatonian_Society_of_Civil_Engineers
- **Institution of Civil Engineers (ICE), founded 1818** (Thomas Telford first president, 1820) — "earliest of the modern professional engineering societies," with membership restricted to practicing engineers. https://en.wikipedia.org/wiki/Institution_of_Civil_Engineers . Later branch bodies: Institution of Mechanical Engineers (1847), etc.
- **Relevance:** Marks the ~1770–1820 crystallization of "engineer" as a self-conscious civilian profession in Britain. Society membership series (ICE, IMechE) are candidate quantitative proxies back to the early 19th century.

### 2.4 Early-modern / Renaissance roots (1500–1700) — the pre-professional era

- Etymology: Latin *ingenium* → *ingeniator* (a deviser of clever contrivances); Old French *engigneor* (c. 14th c.) = maker of **military engines**. The **civil/public-works sense is recorded from ~1600 but does not become the dominant meaning until the 19th century** (etymonline: https://www.etymonline.com/word/engineer ).
- In the Renaissance, "engineers" were largely **military engineers / architect-engineers** (Francesco di Giorgio, the Sangallo family, Sanmicheli, Peruzzi) working on fortifications, plus court "ingegneri." See e.g. *The Medieval Military Engineer* (Boydell & Brewer, 2018) and *Shadow Agents of Renaissance War* (Cambridge). Diderot's *Encyclopédie* still divides engineers into **war, naval, and civil** types.
- **Implication for the project:** For 1500–~1750 there is **no professional category "engineer" with membership rolls or graduate counts** — the population of "engineers" is tiny, court/military-based, and definitionally slippery. Any pre-1750 "share of population" number would rest on prosopography (naming individuals), not aggregate statistics. This is a hard definitional boundary for definition (a).

---

## 3. History of engineering *education* (the main pre-census data source for counts)

Because pre-20th-century censuses rarely isolate "engineer," **graduation counts from engineering schools** are the workhorse source for early quantification.

- **École (nationale) des Ponts et Chaussées — founded 1747** (from the Corps des Ponts et Chaussées, est. 1716; first director Jean-Rodolphe Perronet). Widely called the **oldest civil-engineering school in the world.** https://www.asce.org/about-civil-engineering/history-and-heritage/historic-landmarks/ecole-nationale-des-ponts-et-chaussees ; https://www.britannica.com/place/Ecole-Nationale-des-Ponts-et-Chaussees . Trained a small, state-directed corps of civil engineers.
- **École Polytechnique — founded 1794** (as École Centrale des Travaux Publics; renamed 1795; militarized by Napoleon 1804). Founded explicitly to remedy a "**dearth of engineers**." Early scale: ~400 students initially, **~120 admitted per year.** https://www.polytechnique.edu/en/school/history/1794-1804-revolution-and-napoleonic-period . The French *grandes écoles* model (see MacTutor: https://mathshistory.st-andrews.ac.uk/Projects/Ayel/chapter-3/ ).
- **Technische Hochschulen (German-speaking Europe, 19th c.):** polytechnic schools (Karlsruhe 1825, Dresden, Darmstadt, Munich, Zürich ETH 1855, Vienna) that gained university status as *Technische Hochschulen* later in the century; TH Darmstadt founded the world's first electrical-engineering chair/department. https://en.wikipedia.org/wiki/Technische_Hochschule ; Karlsruhe case study: https://www.researchgate.net/publication/263487949 . Enrollment figures exist school-by-school (e.g., Dresden had 281 students, >60% in engineering, at one 19th-c. point **[VERIFY/date]**).
- **US land-grant colleges — Morrill Act (1862), Second Morrill Act (1890):** created "colleges of agriculture and the mechanic arts," driving explosive growth in engineering degrees.
  - Widely cited figures **[VERIFY against primary source — these come from a secondary explainer, engineeringsauthority.com, echoing older histories]:** ~**300 engineers** graduated by ~6 universities four years after the Act; by 1870 ~21 universities graduating ~3× that; by 1890 **"almost 3,000 engineers"** in the US annually, said to surpass Germany. Undergraduate engineering degrees rose **~7× between 1866 and 1880** and another **~15× by 1911.** Today land-grant institutions award ~70% of US engineering degrees. https://en.wikipedia.org/wiki/Morrill_Land-Grant_Acts
- **Fox, Robert, and Anna Guagnini, eds. (1993). *Education, Technology and Industrial Performance in Europe, 1850–1939.* Cambridge University Press.** ISBN 9780521381536. https://www.cambridge.org/us/academic/subjects/history/european-history-after-1450/education-technology-and-industrial-performance-europe-18501939
  - **The single best comparative-history volume** on engineering training and careers: country chapters on England (Guagnini, mechanical engineers 1850–1914), France (André Grelon, 1880–1939), Germany (Wolfgang König), Belgium (Baudet), plus Sweden, Spain, Italy, and the USA. Contains institution-level student/graduate data and career-structure analysis — a rich mine for national engineer-education series c. 1850–1939.
- **Goldin, Claudia, and Lawrence F. Katz (2008). *The Race Between Education and Technology.* Harvard University Press.** NBER WP 12984. https://www.nber.org/system/files/working_papers/w12984/w12984.pdf ; "Extending the Race…" NBER WP 26705. Provides the 20th-century US framework for college attainment / field composition and skill demand; useful for placing engineering-degree growth within total higher-education expansion.

---

## 4. International & organizational measurement efforts (definitions and modern series)

### 4.1 UNESCO Engineering Reports

- **UNESCO (2010). *Engineering: Issues, Challenges and Opportunities for Development.*** UNESCO Publishing. https://unesdoc.unesco.org/ark:/48223/pf0000214229 (full text) ; overview https://www.unesco.org/en/basic-sciences-engineering/report
  - First UNESCO global engineering report; frames engineering shortages as a development problem. Reported per-capita disparity (widely cited): **developing countries average ~5 engineers per 10,000 population (under 1 in some African countries); developed countries ~20–50 per 10,000.** https://www.universityworldnews.com/post.php?story=20101105221936787
- **UNESCO (2021). *Engineering for Sustainable Development: Delivering on the Sustainable Development Goals.*** Executive summary: https://unesdoc.unesco.org/ark:/48223/pf0000375634 ; overview https://www.unesco.org/en/articles/engineering-sustainable-development-delivering-sustainable-development-goals
  - Ties engineering capacity to the SDGs; e.g., ~2.5M additional engineers needed in Sub-Saharan Africa for water/sanitation alone. UN News: https://news.un.org/en/story/2021/03/1086262
  - **Caveat:** UNESCO's per-capita numbers are illustrative and drawn from heterogeneous national reporting; definitions of "engineer" vary by country.

### 4.2 NSF / NCSES — *Science and Engineering Indicators*

- **National Science Board / NSF NCSES, *Science and Engineering Indicators* (biennial).** Portal: https://ncses.nsf.gov/indicators ; S&E Labor Force chapter (2022): https://ncses.nsf.gov/pubs/nsb20212/assets/nsb20212.pdf ; S&E Workforce interest area: https://ncses.nsf.gov/interest-areas/science-engineering-workforce
  - **Definitions:** distinguishes S&E *occupations* (ISCO/SOC-based) from holders of S&E *degrees*. Recent scale: ~**7 million** in S&E occupations; ~**25 million** hold ≥ bachelor's in S&E; STEM workforce ~¼ of US employment (2023).
  - **Longitudinal reach:** Consistent occupational series generally traceable to **1960 Census** onward (and ACS thereafter); earlier requires the historical census monographs (see §5).
  - **Historical predecessor dataset (strong lead):** **NBER, "Appendix B: Census Data on Number of Engineers and Chemists, 1890–1950,"** in *The Demand and Supply of Scientific Personnel* (Blank & Stigler, 1957). https://www.nber.org/books-and-chapters/demand-and-supply-scientific-personnel/appendix-b-census-data-number-engineers-and-chemists-1890-1950 — an explicit engineer time series 1890–1950.

### 4.3 OECD / ILO — classification and comparability

- **ISCO (International Standard Classification of Occupations, ILO), ISCO-88 / ISCO-08.** Engineers fall under major group 2, "Science and engineering professionals" (sub-major 21). https://en.wikipedia.org/wiki/International_Standard_Classification_of_Occupations
  - OECD: share of "science and engineering professionals" reached **3.7% of the OECD workforce in 2024** (STEM occupation measures from labor-force/census data classified by ISCO). https://eaccny.com/news/oecd-the-research-and-innovation-workforce-continues-to-expand-across-the-oecd/
  - **Definitional caveat:** Cross-country comparability is imperfect even with ISCO; "engineer" spans technicians vs. professionals, and national practice/licensing differs. (See also the **OECD Frascati Manual** definition of "researchers," which overlaps but is not identical to "engineers.")

### 4.4 Counting engineers: the methodological cautionary tale (Duke/Gereffi–Wadhwa)

- **Wadhwa, Vivek, Gary Gereffi, et al. (2005/2007). "Framing the Engineering Outsourcing Debate" and "Getting the Numbers Right: International Engineering Education in the United States, China and India."** Duke Global Engineering & Entrepreneurship. https://www.soc.duke.edu/GlobalEngineering/papers_outsourcing.php ; https://www.soc.duke.edu/GlobalEngineering/papers_gettingthenumbers.php ; SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1015831
  - **The key methodology lesson for this project.** Popular claims (US ~70,000 vs China ~600,000 vs India ~350,000 engineering grads in 2004) were **not like-for-like**: Chinese/Indian totals mixed 4-year degrees with 3-year/diploma/sub-baccalaureate programs, and definitions of "engineer" differed. On a **per-capita** basis, the US graduated **~750 engineers per million population**, vs. India ~200 and China ~500 per million (Duke, 2005). **[VERIFY exact figures.]**
  - **Takeaway:** Any long-run engineer count is hostage to (i) the credential threshold used, (ii) inclusion of technicians/diploma-holders, and (iii) national reporting practices. This is the definitional problem the project's dual definitions (a)/(b) are designed to confront.

### 4.5 World Bank

- Beyond the Maloney–Valencia project (§1.2), World Bank regional studies use engineer density as a development indicator (e.g., LAC studies on innovation and human capital). The Bank does not maintain a dedicated long-run global engineer series; its contribution is the Maloney–Valencia dataset and country/regional STEM-workforce diagnostics.

---

## 5. Quantitative estimates of engineers as a share of population/labor force over time

What actually exists as **numbers**, by period:

**Pre-1750 (definition (a) essentially unmeasurable):** No aggregate counts; engineers = a handful of military/court engineers and architect-engineers. Estimation would be prosopographic. **Literature gap.**

**~1750–1870 (school-graduate era):** Counts derive from **engineering-school enrollment/graduation** (Ponts et Chaussées from 1747; Polytechnique from 1794 at ~120/yr; German polytechnics from 1820s–50s; US land-grant surge post-1862) and **society membership** (Smeatonian 1771, ICE 1818→). No standardized national "share of population" series; must be built school-by-school. Fox & Guagnini (1993) is the best comparative base for 1850+.

**~1870–1914 (first systematic cross-country densities):** **Maloney & Valencia Caicedo** provide engineer-per-100,000-worker series for the Americas + comparators. Illustrative 1900 densities: Nordic ~100, US South ~60, Latin America <20 per 100,000 workers. **[VERIFY]**

**US census occupational series (the best single-country long series):**
- Authoritative primary sources: **Alba M. Edwards, *Comparative Occupation Statistics for the United States, 1870 to 1940*** (US Census, 1943) — the standard back-cast of occupations incl. "technical engineers"; PDF of the 1870–1930 comparative volume: https://www2.census.gov/library/publications/decennial/1940/population-occupation/00312147ch2.pdf ; and *Historical Statistics of the United States* (Census), chapter D (labor force): https://www2.census.gov/library/publications/1949/compendia/hist_stats_1789-1945/hist_stats_1789-1945-chD.pdf . Plus NBER Appendix B (engineers 1890–1950, §4.2).
- Widely repeated growth figures **[VERIFY against Edwards 1943 / Historical Statistics — the round numbers below came from a secondary web explainer and should be checked]:** US engineers rose from on the order of **~7,000 in 1880** to **~136,000 by 1920** (technical/professional engineers). These orders of magnitude are consistent with the census occupational record but the exact counts and category boundaries must be pinned to Edwards (1943).

**Modern per-capita snapshots (definition (b), roughly comparable):**
- UNESCO: developing ~5 vs developed ~20–50 engineers per 10,000 population (2010).
- OECD: science & engineering professionals ~3.7% of the workforce (2024).
- Duke/Gereffi: US ~750 engineering graduates per million population/yr (mid-2000s) vs India ~200, China ~500 — but definitionally fraught.

---

## 6. Bibliography (verified citations with URLs)

**Economics / growth / human capital**
1. Murphy, K. M., A. Shleifer, R. W. Vishny (1991). "The Allocation of Talent: Implications for Growth." *QJE* 106(2): 503–530. NBER WP 3530. https://academic.oup.com/qje/article-abstract/106/2/503/1905462 · https://www.nber.org/papers/w3530
2. Maloney, W. F., F. Valencia Caicedo (2022). "Engineering Growth: Innovative Capacity and Development in the Americas." *JEEA* 20(4): 1554–1594. https://academic.oup.com/jeea/article-abstract/20/4/1554/6550029 (WP versions: World Bank PRWP 6814, 2014, https://ideas.repec.org/p/wbk/wbrwps/6814.html ; CESifo 6339, 2017, https://ideas.repec.org/p/ces/ceswps/_6339.html ; SSRN 2451275 & 2932756)
3. Squicciarini, M. P., N. Voigtländer (2015). "Human Capital and Industrialization: Evidence from the Age of Enlightenment." *QJE* 130(4): 1825–1883. NBER WP 20219. https://academic.oup.com/qje/article-abstract/130/4/1825/1914932 · https://www.nber.org/papers/w20219
4. Kelly, M., J. Mokyr, C. Ó Gráda (2023). "The Mechanics of the Industrial Revolution." *Journal of Political Economy* 131(1): 59–94. CEPR DP 14884. https://cepr.org/publications/dp14884 · https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3628205
5. Mokyr, J. (2002). *The Gifts of Athena: Historical Origins of the Knowledge Economy.* Princeton UP. https://press.princeton.edu/books/paperback/9780691120133/the-gifts-of-athena
6. Gennaioli, N., R. La Porta, F. Lopez-de-Silanes, A. Shleifer (2013). "Human Capital and Regional Development." *QJE* 128(1): 105–164. NBER WP 17158. https://academic.oup.com/qje/article-abstract/128/1/105/1840182
7. de Pleijt, A., A. Nuvolari, J. Weisdorf (2020). "Human Capital Formation During the First Industrial Revolution: Evidence from the Use of Steam Engines." *JEEA* 18(2): 829–889. CEPR DP 12987. https://academic.oup.com/jeea/article-abstract/18/2/829/5398135
8. Goldin, C., L. F. Katz (2008). *The Race Between Education and Technology.* Harvard UP. NBER WP 12984. https://www.nber.org/system/files/working_papers/w12984/w12984.pdf
9. (Debate context) Mitch, D. (1999), in J. Mokyr (ed.), *The British Industrial Revolution: An Economic Perspective*; Allen, R. C. (2009), *The British Industrial Revolution in Global Perspective*, Cambridge UP.

**History of the profession**
10. Layton, E. T., Jr. (1971/1986). *The Revolt of the Engineers: Social Responsibility and the American Engineering Profession.* Johns Hopkins UP. https://muse.jhu.edu/article/255448
11. Reynolds, T. S., ed. (1991). *The Engineer in America: A Historical Anthology from Technology and Culture.* Univ. of Chicago Press. https://archive.org/details/engineerinameric0000unse
12. Meiksins, P. F. (1988). "The 'Revolt of the Engineers' Reconsidered." *Technology and Culture* 29(2). https://muse.jhu.edu/article/889248/summary · Meiksins, P. & C. Smith (1996), *Engineering Labour*, Verso.
13. Gispen, K. (1989). *New Profession, Old Order: Engineers and German Society, 1815–1914.* Cambridge UP. https://books.google.com/books/about/New_Profession_Old_Order.html?id=FfNVztgZ4bgC
14. Smeatonian Society (1771) / Institution of Civil Engineers (1818): https://en.wikipedia.org/wiki/Smeatonian_Society_of_Civil_Engineers · https://en.wikipedia.org/wiki/Institution_of_Civil_Engineers

**History of engineering education**
15. Fox, R., A. Guagnini, eds. (1993). *Education, Technology and Industrial Performance in Europe, 1850–1939.* Cambridge UP. https://www.cambridge.org/us/academic/subjects/history/european-history-after-1450/education-technology-and-industrial-performance-europe-18501939
16. École des Ponts et Chaussées (1747): https://www.asce.org/about-civil-engineering/history-and-heritage/historic-landmarks/ecole-nationale-des-ponts-et-chaussees
17. École Polytechnique (1794): https://www.polytechnique.edu/en/school/history/1794-1804-revolution-and-napoleonic-period
18. Technische Hochschule (system history): https://en.wikipedia.org/wiki/Technische_Hochschule
19. Morrill Land-Grant Acts (1862, 1890): https://en.wikipedia.org/wiki/Morrill_Land-Grant_Acts

**Measurement / organizations / data**
20. UNESCO (2010). *Engineering: Issues, Challenges and Opportunities for Development.* https://unesdoc.unesco.org/ark:/48223/pf0000214229
21. UNESCO (2021). *Engineering for Sustainable Development.* https://unesdoc.unesco.org/ark:/48223/pf0000375634
22. NSF/NCSES, *Science and Engineering Indicators* (biennial). https://ncses.nsf.gov/indicators · S&E Labor Force 2022: https://ncses.nsf.gov/pubs/nsb20212/assets/nsb20212.pdf
23. Blank, D. M., G. J. Stigler (1957), *The Demand and Supply of Scientific Personnel*, NBER — "Appendix B: Census Data on Number of Engineers and Chemists, 1890–1950." https://www.nber.org/books-and-chapters/demand-and-supply-scientific-personnel/appendix-b-census-data-number-engineers-and-chemists-1890-1950
24. Edwards, A. M. (1943). *Comparative Occupation Statistics for the United States, 1870 to 1940* (US Census). https://www2.census.gov/library/publications/decennial/1940/population-occupation/00312147ch2.pdf
25. ISCO (ILO): https://en.wikipedia.org/wiki/International_Standard_Classification_of_Occupations · OECD S&E professionals: https://eaccny.com/news/oecd-the-research-and-innovation-workforce-continues-to-expand-across-the-oecd/
26. Wadhwa, V., G. Gereffi, et al. (2005–2007). "Framing the Engineering Outsourcing Debate" / "Getting the Numbers Right." Duke. https://www.soc.duke.edu/GlobalEngineering/papers_outsourcing.php · https://www.soc.duke.edu/GlobalEngineering/papers_gettingthenumbers.php

---

## 7. Gaps in the literature and implications for our study

**Where the literature is strong (build on it):**
- **A single peer-reviewed, cross-country engineer-density dataset exists for c. 1870–1914** (Maloney & Valencia Caicedo, JEEA 2022) — US county + Americas state/national engineers per 100,000 workers. This is the natural spine for any pre-WWI global benchmark and its construction method (school graduates + censuses + society rolls) is the template to extend to Europe/Asia.
- **The US has the deepest national time series** via census occupational data, back-cast by Alba Edwards (1943) and extended by NBER (engineers 1890–1950) and NSF/NCSES (1960→). A continuous US "engineers as % of labor force" series from ~1850 to today is feasible from published sources.
- **The conceptual case for counting engineers specifically** (vs. average schooling) is well established: Murphy–Shleifer–Vishny (engineers vs. lawyers), Squicciarini–Voigtländer, Kelly–Mokyr–Ó Gráda, Mokyr. Use these to motivate the project.

**Where the literature is thin or conflicting (our contribution space):**
1. **No long-run *global* engineer series, and essentially nothing systematic before ~1870.** Pre-1870 counts must be assembled bottom-up from engineering-school graduation records (Ponts et Chaussées 1747→, Polytechnique 1794→, German TH 1820s→, US land-grant 1862→) and professional-society rolls (Smeatonian 1771, ICE 1818→). No one has stitched these into a population-share series. This is the clearest open niche.
2. **Definition instability is the central measurement problem.** "Engineer" shifts from *military/architect-engineer* (1500–1700), to *state civil-engineering corps graduate* (1750–1850), to *credentialed professional-society member / degree-holder* (1850–1950), to *ISCO occupational category* (modern). The project's dual definitions (a) "recognized at the time" and (b) "modern standard" directly address this — but every historical number must be tagged with which definition and threshold it uses. The Duke/Gereffi episode shows how much cross-country counts swing on the credential threshold (4-year vs diploma/technician).
3. **Shop-trained vs school-trained.** Much 19th-century engineering capacity (esp. US/UK mechanical, and the artisan "upper tail" in Kelly–Mokyr–Ó Gráda / de Pleijt) was *not* credentialed. Definition (a) will undercount it via graduation data; definition (b) requires occupational/skill measures. Expect the two definitions to diverge most sharply in 1750–1900 Britain and the US.
4. **Pre-1750 is a hard floor.** For 1500–1750 only prosopographic/individual-level identification is possible; a meaningful "share of population" is not recoverable from aggregate statistics. Frame this period qualitatively (etymology, military/court engineers, first schools) rather than numerically.
5. **Comparability of modern per-capita figures is weak** (UNESCO, OECD, national ministries use different ISCO cuts and include/exclude technicians). Any modern global share needs an explicit reconciliation to a common threshold.

**Concrete data leads to pursue next:**
- Obtain the **Maloney–Valencia (JEEA 2022) replication dataset/appendix** (World Bank / JEEA / authors' pages) — the engineer-per-100,000 series and its country coverage.
- Pull **Alba Edwards (1943)** and **NBER Blank–Stigler Appendix B** for the authoritative US engineer series 1870/1890–1950, then splice to **NSF/NCSES** for 1960→.
- Mine **Fox & Guagnini (1993)** country chapters for institution-level engineering-graduate counts across Europe + US, 1850–1939.
- Extract **school-level graduation series** (Ponts et Chaussées, Polytechnique, ETH Zürich, German TH, US land-grants) and **society membership rolls** (ICE, ASCE, ASME, VDI) as the pre-census backbone, 1747–1900.
- Reconcile modern counts to a **common ISCO-08 "engineering professionals"** definition for the contemporary global-share endpoint.

**Verification to-dos (figures I could not confirm against primary text in this environment):** the exact Maloney–Valencia county-income coefficient (10% vs 16%) and 1900 density table; the US "7,000 (1880) → 136,000 (1920)" engineer counts (check Edwards 1943); the land-grant "300 → ~3,000 engineers" figures; the Duke per-million engineer figures; and Gispen's German engineer/graduate tables. Full-text PDFs (World Bank, CESifo, SSRN, publisher pages) were not retrievable here and should be read directly for the project's quantitative core.
