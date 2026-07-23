# Claim: the engineer share was flat and negligible, then took off with industrialization

**Status:** Proposed — test wired and validated on synthetic data; **awaiting real
data** before a verdict is recorded. This directory is swap-in ready: when the
real panel exists, `test.py --panel …/panel.parquet` produces the verdict with no
code changes.

## Claim

For a given country, the number of formally trained engineers as a share of
population (`share_per_100k`) was **negligible and approximately flat before the
onset of industrial-era engineering (~1750–1860, country-dependent)**, after
which it **grew super-linearly** — i.e. there is a datable structural break where
the annual growth rate of the share jumps from near-zero to a sustained high
rate. Stated for the **contemporary** definition first; the **modern** definition
is expected to show an earlier, higher-baseline version of the same shape.

## Null hypothesis (H0) and decision rule — *pre-registered*

- **H0:** the log engineer share follows a single growth regime (no structural
  break) over 1700–present; the pre-industrial and industrial growth rates are
  the same.
- **Alternative:** there is ≥1 structural break separating a near-flat regime
  (annual growth < 1.0%/yr) from a sustained high-growth regime (> 3.0%/yr).
- **Test statistic:** BIC-selected number of regimes from piecewise-log-linear
  changepoint detection (`analysis.detect_changepoints`), plus the per-regime
  annualised growth (`analysis.fit_regimes`).
- **Decision rule (fixed before seeing real data):** reject H0 iff BIC selects
  ≥ 2 regimes **and** there exists an adjacent regime pair with
  `pre_growth < 1.0%/yr`, `post_growth > 3.0%/yr`, and the break year in
  `[1700, 2000]`. Thresholds live in `test.py` (`PRE_MAX`, `POST_MIN`, `WINDOW`).

## Data

- Panel: `data/processed/panel.parquet` (real) — currently
  `panel_synth.parquet` (synthetic) for development.
- Definition: `contemporary` (primary), then `modern`.
- **A verdict may only be recorded from `confidence == 'primary'` rows.** The
  cleanest first real series is US (IPUMS/Edwards, tasks G-US-01/04) — dense and
  long. `test.py` prints the data provenance and refuses to dress up a synthetic
  or provisional run as a result.

## Assumptions

- Piecewise-log-linear growth is an adequate description of the share's
  trajectory (reasonable for a quantity that compounds).
- The share is measured consistently within each regime; definition splices
  (task P-SPLICE-01) are handled before the test, not inside it.
- BIC is an acceptable model-order selector here; sensitivity to `max_regimes`
  and `min_size` should be reported alongside the verdict.

## Result

*Pending real data.* On the **synthetic** panel (demonstration only), the test
recovers a takeoff break for the US contemporary series at ~1858, with growth
rising from ~0.1%/yr to ~8%/yr, and reports the claim SUPPORTED — confirming the
machinery works. This is **not** evidence about the world.

To produce the real result:
```bash
uv run python sections/engineering-workforce/claims/engineer-share-takeoff/test.py \
    --panel sections/engineering-workforce/data/processed/panel.parquet \
    --entity "United States" --definition contemporary
```

## Conclusion

*To be written once real data is in.* Record Supported / Refuted / Inconclusive,
the break year(s) and their uncertainty, the pre/post growth rates, robustness to
the model-selection settings, and the definition/splice caveats.
