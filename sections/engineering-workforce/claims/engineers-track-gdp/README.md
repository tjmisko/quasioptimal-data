# Claim (H2): the engineer stock tracks real GDP

**Status:** Proposed — test wired and validated on synthetic data; **verdict awaits
real engineer + GDP data.**

## Claim

The number of engineers and real GDP move together over the long run: they are
**cointegrated**, with a **positive elasticity** of engineers with respect to GDP.

## Null hypothesis (H0) and decision rule — *pre-registered*

- **H0:** engineers and GDP are **not** cointegrated (any level correlation is
  spurious co-trending), and/or the elasticity is not positive.
- **Test:** log-log OLS elasticity `d log(engineers) / d log(GDP)` with an
  Engle–Granger cointegration check (ADF on residuals); plus a multiple regression
  controlling for capital, and a lead-lag diagnostic (`analysis.elasticity`,
  `multiple_regression`, `lead_lag`).
- **Decision rule (fixed):** SUPPORTED iff residuals are stationary
  (`coint_adf_pvalue < 0.05`) **and** the 95% CI for the elasticity is strictly
  positive.

## Data

`panel.parquet` (engineers) + `covariates_long.parquet` (`gdp_real`) merged by
`analysis.entity_frame`. GDP: Maddison/PWT (see `sources.yaml`). Verdict only from
real (`confidence = primary`) data.

## Identification note

Cointegration + a positive elasticity establishes a **long-run relationship**, not
its **direction**. Direction and confounding are handled in `../../IDENTIFICATION.md`
(controls, GDP↔capital collinearity, Granger/lead-lag, instruments, natural
experiments). Report the elasticity as an association until an identification
strategy licenses a causal reading.

## Result

*Pending real data.* On synthetic data: elasticity ≈ 0.85 (GDP on engineers),
cointegrated — machinery confirmed. Run with `--real`.

## Conclusion

*To be written from real data.*
