# Claim: <one-line statement>

> Copy this directory to `claims/<claim-slug>/` when formulating a claim, fill it
> in, and add a row to `claims/README.md`. Write H0 and the decision rule
> *before* running the test.

## Claim

A precise, falsifiable statement. Include the **definition** of "engineer" used
(`contemporary` or `modern`), the entity, and the period.

## Null hypothesis (H0) and decision rule

- **H0:** …
- **Alternative:** …
- **Test / statistic:** … (e.g. Bai–Perron structural break; log-linear trend slope)
- **Decision rule:** reject H0 if … (significance level, and any robustness bar).
  *Fixed before seeing the test result.*

## Data

- Processed tables + columns used (e.g. `panel.parquet`, `definition == 'contemporary'`).
- `source_id`s involved and their `confidence`. **A claim may not rest on
  `literature_unverified` rows** — list the primary sources backing it.
- Any splices (link the P-SPLICE step) and the denominator vintage.

## Assumptions

Model assumptions and their plausibility; how violations would change the result.

## Result

The numbers, the test output, and a figure. State the effect size and its
uncertainty, not just significance.

## Conclusion

**Supported / Refuted / Inconclusive**, with the key caveats and what would
change the verdict.
