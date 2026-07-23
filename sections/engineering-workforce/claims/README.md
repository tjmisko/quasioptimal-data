# Claims register — Engineering Workforce

Claims formulated in this section. Each row links to a claim directory
containing the precise statement, null hypothesis, test, and conclusion.

| Claim | Status | Statement (short) | Test |
| --- | --- | --- | --- |
| _(none yet)_ | — | Claims will be added after exploratory analysis. | — |

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
