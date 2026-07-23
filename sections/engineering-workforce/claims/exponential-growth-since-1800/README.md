# Claim (H1): quasi-exponential growth in the number of engineers since ~1800

**Status:** Proposed — test wired and validated on synthetic data; **verdict awaits
real numerator data.**

## Claim

The **number** of formally trained engineers in a country has grown
**quasi-exponentially since ~1800** — i.e. `log(engineers)` is approximately
linear in year, with a high and roughly constant proportional growth rate.

## Null hypothesis (H0) and decision rule — *pre-registered*

- **H0:** engineer counts do **not** grow exponentially — `log(engineers)` is not
  well described by a constant-slope line since 1800 (low fit, or growth rate not
  distinguishable from zero).
- **Test:** OLS of `log(engineers)` on year since 1800 (`analysis.test_exponential_growth`);
  report R², implied CAGR, and a curvature check (quadratic term).
- **Decision rule (fixed):** SUPPORTED iff `R² ≥ 0.95` **and** `CAGR ≥ 2%/yr`.
  Report separately whether growth is *constant* (quadratic term insignificant =
  clean exponential) vs *accelerating/decelerating* (still "quasi-exponential" if
  R² high but curvature present).

## Data

`panel.parquet`, engineer **count** (`engineers`), `definition = contemporary`
(then `modern`). Verdict only from `confidence = primary` rows.

## Result

*Pending real data.* On synthetic data the test recovers R²≈0.97, CAGR≈6.5%/yr
with detectable curvature (the baked-in regime breaks) — machinery confirmed.

```bash
uv run python sections/engineering-workforce/claims/exponential-growth-since-1800/test.py \
    --real --entity "United States"
```

## Conclusion

*To be written from real data:* the growth rate, its constancy, and how the
break/regime structure (claim `engineer-share-takeoff`) qualifies "exponential."
