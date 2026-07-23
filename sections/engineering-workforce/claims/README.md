# Claims register — Engineering Workforce

Claims formulated in this section. Each row links to a claim directory
containing the precise statement, null hypothesis, test, and conclusion.

All tests below are **wired and validated on synthetic data** (swap-in ready);
verdicts await real numerator/covariate data. See `../IDENTIFICATION.md` for the
causal strategy that turns these associations into directional claims.

| Claim | Status | Statement (short) | Test |
| --- | --- | --- | --- |
| [`engineer-share-takeoff`](engineer-share-takeoff/) | Proposed | Engineer share ~flat pre-industrial, then structural-break takeoff. | changepoint (BIC) + growth regimes |
| [`exponential-growth-since-1800`](exponential-growth-since-1800/) | Proposed | Engineer **count** grew quasi-exponentially since ~1800. | log-linear fit + curvature (H1) |
| [`engineers-track-gdp`](engineers-track-gdp/) | Proposed | Engineers cointegrated with real GDP, positive elasticity. | elasticity + Engle–Granger (H2) |
| [`engineers-track-capital`](engineers-track-capital/) | Proposed | Engineers cointegrated with physical capital stock. | elasticity + Engle–Granger (H3) |
| [`patent-accumulation`](patent-accumulation/) | Proposed | Engineers **lead** patent/IP accumulation (directional). | lead-lag + Granger |

_`_TEMPLATE/` is the blank claim skeleton; `_common.py` is shared test-loading._

## How to add a claim

1. Create `claims/<claim-slug>/` with a `README.md` that states:
   - **Claim** — the precise, falsifiable statement.
   - **Null hypothesis (H0)** and decision rule — written *before* running the test.
   - **Data** — which processed tables and definitions it uses.
   - **Test** — the statistical method and its assumptions.
   - **Result & conclusion** — supported / refuted / inconclusive, with caveats.
2. Put the analysis code/notebook in that directory.
3. Add a row to the table above.

Statuses: `Proposed` → `Testing` → `Supported` / `Refuted` / `Inconclusive`.
