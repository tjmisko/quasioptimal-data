# Claim: engineers drive the accumulation of patents / intellectual property

**Status:** Proposed — test wired and validated on synthetic data; **verdict awaits
real engineer + patent data.**

A distinct claim from the GDP/capital ones: here the question is **directional** —
does the engineering workforce *lead* intellectual-property output?

## Claim

Growth in the engineer stock **leads** growth in patent output (applications /
grants), i.e. engineers are an upstream driver of IP accumulation, with a
positive lead of a few years to a decade.

## Null hypothesis (H0) and decision rule — *pre-registered*

- **H0:** engineers do not lead patents — the peak growth-rate cross-correlation
  is at lag ≤ 0 (contemporaneous or patents-lead), and Granger tests do not favor
  the engineers→patents direction.
- **Test:** cross-correlation lead-lag of growth rates (`analysis.lead_lag`),
  Granger causality both ways (`analysis.granger_direction`), and the patents-on-
  engineers elasticity.
- **Decision rule (fixed):** SUPPORTED iff `lead_lag.best_lag > 0` (engineers
  lead) **and** the engineers→patents Granger p-value is smaller than the reverse.

## Data

`panel.parquet` (engineers) + `covariates_long.parquet` (`patents_flow`,
`patents_stock`). Patents: World Bank `IP.PAT.RESD` + `IP.PAT.NRES` (1960+, see
`sources.yaml` / `mirrors-patents.md`); pre-1960 US backbone needs HistPat/USPTO
(blocked). Build a **patent stock** by cumulating the flow with depreciation.

## Definitional caveats (must be stated with any result)

Applications vs grants; counted by **office** vs by **inventor origin**; total
filings vs first-filings/families; and the huge **post-1985 surge** (China's 1985
law; US/JP/KR) — normalize per-capita or per-engineer. A patent is a noisy,
regime-dependent proxy for "IP output."

## Result

*Pending real data.* On synthetic data (patents generated as a lagged function of
engineers): lead-lag recovers engineers→patents with the injected lag; Granger
favors the same direction — machinery confirmed. This may graduate into its own
section (`innovation-output`) if it grows.

## Conclusion

*To be written from real data.*
