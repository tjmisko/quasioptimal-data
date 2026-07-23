# Plan: Long-run trends in the engineering workforce

This is the working plan for the `engineering-workforce` section. It defines the
question precisely, the two engineer definitions, the data-search strategy, the
measurement challenges, and the path from exploration to formal statistical
tests. It will be revised as the literature review and data search land.

## 1. Research question, stated precisely

> Let `E_d(c, t)` = the number of engineers under definition `d` in place `c` at
> time `t`, and `P(c, t)` = population. We want the series
> `share_d(c, t) = E_d(c, t) / P(c, t)` for `t` from ~1500 to present, for
> `c ∈ {World, USA, California, China, UK, Germany, France, ...}`, and
> `d ∈ {contemporary, modern-standard}`.

Primary outputs:
- Long-run time series of the engineer share for each place and definition.
- Identification of inflection points (e.g. onset of formal engineering
  education; industrialization; post-WWII expansion; recent massification).
- Cross-country comparison of levels, timing, and growth rates.

## 2. The two definitions (and how to operationalize them)

**(1) Contemporary / period definition.** Count those who, by the standards of
the era, were formally recognized engineers. Operational proxies, in rough order
of availability going back in time:
- Modern era: census/labor-force occupation "engineer"; engineering degree
  holders; licensed (PE) / chartered (CEng) engineers.
- 19th–early 20th c.: membership of professional institutions (ICE 1818, IMechE
  1847, VDI 1856, ASCE 1852, ...); enrollment/graduates of polytechnics and
  technical colleges.
- 18th c. and earlier: members of state engineering corps (e.g. French *Corps
  des ponts et chaussées*, 1716; *École des ponts*, 1747; *École Polytechnique*,
  1794) and military/fortification engineer corps; surveyors; mining engineers.
- Pre-1700: essentially no organized profession — expect near-zero counts and
  heavy reliance on named-individual/institutional records. Treat as a lower
  bound with wide uncertainty.

**(2) Modern-standard definition.** Estimate how many people would qualify as
engineers by *today's* criteria (tertiary engineering training + engineering
work). For the modern era this is close to definition (1) via degrees/occupation
codes. For pre-modern eras this is a **counterfactual estimate** and must be
presented as such — likely built from (a) education-attainment reconstructions,
(b) shares of the workforce in technical/mechanical trades that map to modern
engineering, and (c) explicit assumptions. We will bound it with scenarios
rather than pretend to a point estimate.

**Definitional hygiene.** Every series carries metadata: the exact source
definition, occupation/degree code, and era. We never silently splice
incompatible definitions; splices are documented and, where possible, shown with
overlap periods.

## 3. Data-search strategy (exhaustive)

Running as a fan-out of research agents; findings land in `research/`:
- `literature-review.md` — how scholars have measured this and what they find.
- `data-sources-global-historical.md` — global + the hard pre-1900 period;
  population denominators (Maddison, HYDE, OWID); UNESCO/OECD/World Bank/ILO
  modern series; early engineering institutions.
- `data-sources-us-california.md` — IPUMS USA census microdata, BLS OEWS, NSF
  NCSES + NCES IPEDS degrees, NCEES/CA PE licensure, Census population.
- `data-sources-china.md` — MOE / NBS yearbooks, UNESCO/World Bank, historical
  (Republican, PRC, imperial) scholarship.
- `data-sources-uk-germany-europe.md` — Engineering Council/ICE/IMechE, VDI &
  Technische Hochschulen, ONS/Destatis/Eurostat, historical censuses (I-CeM).

Selection criteria for "best" data: authoritative/primary; downloadable;
documented definitions; long temporal coverage; consistent geography; open
licensing. Each source recorded in a manifest with URL, coverage, definition,
format, and limitations so downloads are reproducible.

## 4. Denominators

Population series to compute shares:
- **Global & country, long run:** Maddison Project Database; HYDE; Our World in
  Data / Gapminder; UN WPP for recent decades.
- **US & California:** Census Bureau + historical statistics.
- Match denominator vintage/geography to the engineer numerator carefully
  (e.g. borders change; "Germany" pre-1871 ≠ modern Germany).

## 5. Measurement challenges to confront explicitly

- **The word "engineer" is unstable** across time, language, and country
  (title protection in Germany; "engineer" as machine-operator in some usages;
  technicians vs. professional engineers).
- **Professional-body membership undercounts** trained engineers (not all join)
  and its meaning shifts as licensure regimes appear.
- **Pre-1900 is sparse**; the modern-standard series there is a modeled estimate,
  not a measurement.
- **Border and denominator changes** over centuries.
- **Survivorship / selection** in historical records.
- **Chinese statistics**: definitional breadth of "engineering graduates" and
  comparability issues.

## 6. From exploration to formal tests

Once data are in hand:
1. **Exploratory** (`notebooks/`): assemble and plot each series; sanity-check
   levels and splices; visualize shares and growth rates by place/definition.
2. **Formulate claims** (`claims/<slug>/`) — candidates likely to emerge:
   - The engineer share was negligible (~0) and roughly flat before ~1750, then
     grew super-linearly after the onset of formal engineering education.
   - Cross-country: identify structural breaks (e.g. China's post-1999 higher-ed
     massification; US post-WWII expansion) and test their timing/magnitude.
   - Relative levels: e.g. Germany's engineer share led early industrializers in
     a given window.
3. **Formal tests** — chosen to fit each claim, e.g.:
   - **Structural-break / changepoint** tests (Chow, Bai–Perron, Bayesian
     changepoint) for inflection dates.
   - **Trend/growth-rate** estimation with appropriate models for count/share
     data and autocorrelated time series.
   - **Cross-country comparisons** with explicit uncertainty from the
     definitional scenarios (sensitivity analysis over the modern-standard
     assumptions).
   - Pre-register the null hypothesis and the decision rule in each claim's
     README before running the test.

## 7. Deliverables for this section

- A tidy, provenance-tracked panel: `place × year × definition → engineer count,
  population, share` in `data/processed/`.
- Exploratory notebooks with the assembled long-run series.
- One or more formulated, tested claims in `claims/`.

## 8. Open decisions

- How aggressively to attempt the pre-1900 **modern-standard** counterfactual vs.
  presenting it only as bounded scenarios. *(Lean: scenarios with explicit
  assumptions; no false precision.)*
- Whether "engineer" should include or exclude technicians, architects, and
  computer/software engineers — decide per series and document.
