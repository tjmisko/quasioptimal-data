# Claim (H3): the engineer stock tracks the physical capital stock (plant)

**Status:** Proposed — test wired and validated on synthetic data; **verdict awaits
real engineer + capital-stock data.**

## Claim

The number of engineers and the real physical capital stock (plant & equipment)
move together over the long run: they are **cointegrated**, with a **positive
elasticity** of engineers with respect to capital.

## Null hypothesis (H0) and decision rule — *pre-registered*

- **H0:** engineers and capital stock are **not** cointegrated, and/or the
  elasticity is not positive.
- **Test:** log-log elasticity + Engle–Granger cointegration; multiple regression
  controlling for GDP; lead-lag.
- **Decision rule (fixed):** SUPPORTED iff `coint_adf_pvalue < 0.05` **and** the
  95% CI for the elasticity is strictly positive.

## Data

`panel.parquet` (engineers) + `covariates_long.parquet` (`capital_stock`) via
`analysis.entity_frame`. Capital: PWT `rnna` / Jordà–Schularick–Taylor / IMF ICSD
(see `sources.yaml`). Verdict only from real (`confidence = primary`) data.

## Identification note

Capital and GDP are highly collinear, so H2 and H3 cannot both be read causally
from level regressions alone — the multiple regression here will typically show
one absorbing the other. This is the central identification problem framed in
`../../IDENTIFICATION.md` (is capital-deepening pulling engineers, or are
engineers enabling capital accumulation?). Treat the elasticity as association
pending an identification strategy.

## Result

*Pending real data.* On synthetic data: elasticity ≈ 1.05 (capital on engineers),
cointegrated; in a joint regression GDP and capital compete (collinear) — the
identification lesson is visible. Run with `--real`.

## Conclusion

*To be written from real data.*
