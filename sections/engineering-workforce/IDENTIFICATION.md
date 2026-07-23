# Identification strategy: framing the story and finding the causal direction

The descriptive claims (engineers grew exponentially; they co-move with GDP and
capital; they lead patents) establish **associations**. This document lays out how
to move toward **causation** — which factors drive which, and which way the arrows
point — and the control variables and experiments that isolate them.

## The causal question

Engineers, GDP, physical capital, and IP output all trend up together since ~1800.
Candidate structures:

- **(A) Engineers → output.** A larger trained-engineer stock raises innovative
  capacity → more capital gets built and used productively → higher GDP and more
  patents. (The Maloney–Valencia / upper-tail-human-capital story.)
- **(B) Output → engineers.** Growth and capital accumulation raise the demand for
  and ability to fund engineers (a derived-demand / income-effect story).
- **(C) Common cause.** A latent "development / useful-knowledge" factor drives all
  of them; the pairwise links are partly spurious.

These are not mutually exclusive; the goal is to bound each channel.

## Confounders and control variables

Any engineers↔GDP or engineers↔capital regression should consider controlling for:

- **Population / labour force** (scale) — use the *share* (per 100k) and/or include
  population; both engineers and GDP scale with people.
- **The other input** — GDP and capital are highly collinear; include both to see
  which survives (our `multiple_regression` does this; expect one to absorb the
  other — that collinearity *is* the identification problem, not a nuisance).
- **Overall educational attainment** (Barro–Lee `barro-lee`) — to separate
  *engineers specifically* from human capital in general (the MSV "engineers vs
  lawyers" point).
- **Time / common global trend** — a shared trend can manufacture cointegration;
  cross-country panels with year fixed effects difference it out.
- **Definitional regime** — splices (institution→licensure→census) and the
  post-1985 patent surge are structural; control with regime dummies / breakpoints.

## Methods, weakest → strongest for causal claims

1. **Cointegration + ECM** (`elasticity`, Engle–Granger): establishes a stable
   long-run relationship and short-run error correction; **direction-agnostic**.
2. **Granger causality + lead-lag** (`granger_direction`, `lead_lag`): temporal
   precedence. *Caveat:* for smooth co-trending series Granger is often
   "bidirectional"; the **lead-lag cross-correlation peak** is more robust (it
   cleanly recovered the injected engineers→patents lag in synthetic tests). Lead
   ≠ cause, but a consistent multi-year lead is suggestive and rules out the
   reverse contemporaneous story.
3. **Cross-country panel with fixed effects**: entity + year FE remove
   time-invariant country differences and common global shocks; identify off
   *within-country deviations* from trend.
4. **Instrumental variables**: instrument the engineer stock with something that
   shifts engineer *supply* but not output directly — e.g. the timing of
   engineering-school foundings (land-grant colleges, Technische Hochschulen,
   École Polytechnique expansions), or education-policy shocks — then see the
   effect on GDP/capital/patents.
5. **Natural experiments / event studies** (below): the strongest leverage.

## Natural experiments that shock the ENGINEER stock (supply-side)

Each is a discontinuity in engineer supply, largely for reasons exogenous to
contemporaneous output — ideal for event studies / difference-in-differences.

| Shock | Year(s) | Lever | Design |
| --- | --- | --- | --- |
| Morrill Land-Grant Acts | 1862, 1890 | Big US engineering-education capacity jump | State-level DiD on engineer share vs later output |
| GI Bill | 1944+ | Mass subsidised engineering degrees (US) | Interrupted time series / cohort event study |
| Sputnik → NDEA | 1957–58 | Federal STEM-education surge (US) | ITS around 1958; compare eng vs non-eng fields |
| Soviet industrialization | 1930s–50s | Deliberate engineer mass-production | Cross-country: USSR vs peers |
| China Cultural Revolution | 1966–1976 | Universities **closed** — negative shock | Break + recovery; cohort gap |
| China HE massification | 1999+ | Enrolment quotas multiplied | ITS; engineers vs GDP/patents after |
| Émigré scientists/engineers | 1930s, 1990s | Exogenous inflow (Nazi Europe; post-Soviet) | Receiving-country event study |
| H-1B cap changes | 1990s–2000s | Engineer-supply policy shifts (US) | DiD across visa-dependent sectors |

Symmetrically, **demand-side** shocks (oil shocks → petroleum/chemical
engineering; defense build-downs; the dot-com boom/bust for software engineers)
help identify the reverse channel (output/demand → engineers).

## What to build (analysis tasks)

- **A-IDENT-01** — cross-country panel FE regressions of `log(engineers)` on
  `log(GDP)`, `log(capital)`, attainment, with entity+year FE. *(extends
  `analysis.py` with a panel estimator.)*
- **A-IDENT-02** — IV using engineering-school-founding timing as the instrument.
- **A-IDENT-03** — event-study / DiD templates for the shocks above (each becomes a
  small claim under `claims/`).
- **A-IDENT-04** — ECM (error-correction model) to separate long-run elasticity
  from short-run dynamics and see which variable does the "correcting" (the one
  that adjusts is downstream).

## How the synthetic data supports this now

The synthetic covariates are generated with a **known** structure — GDP and capital
are functions of the engineer stock (so a common-engineer factor, case A-flavored),
and patents are a **lagged** function of engineers. The econometrics recovers the
injected elasticities (0.85, 1.05) and the engineers→patents lead (12 yr), and the
joint GDP+capital regression reproduces the collinearity problem. So every method
above can be coded and validated against ground truth before real data arrives; the
ECM/IV/event-study templates (A-IDENT-*) are the next build.
