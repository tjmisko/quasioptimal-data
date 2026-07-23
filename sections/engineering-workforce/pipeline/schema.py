"""Canonical schemas for the engineering-workforce processed tables.

Three tidy long tables flow through the pipeline:

- ``population_long``  — the denominator: persons by entity-year.
- ``engineers_long``  — the numerator(s): engineer counts by entity-year, under
  each *definition* and *metric*, tagged with the source and the source's own
  definition string.
- ``panel``           — the analysis table: engineers joined to population with
  ``share_per_100k`` computed, one row per (entity, year, definition).

Keeping the numerator explicit about ``definition`` (contemporary vs. modern),
``metric`` (a stock of engineers vs. an annual flow of graduates), and
``method`` (how it was counted) is the whole point: "engineer" is not one thing
across eras and countries, and we refuse to silently splice incompatible series.
"""

from __future__ import annotations

import pandas as pd

# --- controlled vocabularies -------------------------------------------------

DEFINITIONS = ("contemporary", "modern")
"""How 'engineer' is scoped. ``contemporary`` = recognized as an engineer by the
standards of the era (corps/institution member, licensed/chartered, degree-holder
by then-current norms). ``modern`` = would qualify as an engineer by today's
standard (tertiary engineering training + engineering work), applied
retrospectively (a modeled counterfactual before ~1900)."""

METRICS = ("stock", "annual_flow")
"""``stock`` = number of engineers alive/active in that year. ``annual_flow`` =
new entrants that year (e.g. graduates). A flow is NOT a stock; converting flows
to a stock requires an accumulation/attrition model — never sum them naively."""

METHODS = (
    "census",  # population census / labour-force survey occupation code
    "membership",  # professional-institution rolls (ICE, VDI, ASCE, ...)
    "licensure",  # licensed / chartered engineers (PE, CEng)
    "graduates_stock",  # cumulative living holders of an engineering degree
    "graduates_flow",  # engineering degrees conferred per year
    "estimate",  # modeled / literature-derived estimate (document assumptions)
)

CANONICAL_ENTITIES = {
    # entity -> iso3 (regions get a pseudo-code)
    "World": "WLD",
    "United States": "USA",
    "California": "US-CA",
    "China": "CHN",
    "United Kingdom": "GBR",
    "Germany": "DEU",
    "France": "FRA",
}

# --- column specs ------------------------------------------------------------

POPULATION_COLUMNS = ["entity", "iso3", "year", "population", "source_id", "notes"]

ENGINEERS_COLUMNS = [
    "entity",
    "iso3",
    "year",
    "definition",  # one of DEFINITIONS
    "metric",  # one of METRICS
    "engineers",  # float count
    "method",  # one of METHODS
    "source_id",  # key into sources.yaml
    "source_definition",  # the source's own definition / occupation code, verbatim
    "confidence",  # 'primary' | 'secondary' | 'literature_unverified'
    "notes",
]

PANEL_COLUMNS = [
    "entity",
    "iso3",
    "year",
    "definition",
    "engineers",
    "population",
    "share_per_100k",
    "metric",
    "method",
    "source_id",
    "confidence",
    "notes",
]

# Covariates for the causal story: relate the engineer stock to macro quantities.
COVARIATE_VARIABLES = (
    "gdp_real",  # real GDP (constant int$)
    "capital_stock",  # real net capital stock / plant (constant int$)
    "investment",  # gross fixed capital formation (constant int$/yr)
    "patents_flow",  # patent applications or grants per year
    "patents_stock",  # accumulated (depreciated) patent stock
)

COVARIATES_COLUMNS = [
    "entity",
    "iso3",
    "year",
    "variable",  # one of COVARIATE_VARIABLES
    "value",
    "unit",
    "source_id",
    "confidence",
    "notes",
]


class SchemaError(ValueError):
    """Raised when a dataframe does not satisfy a canonical schema."""


def _require_columns(df: pd.DataFrame, columns: list[str], kind: str) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SchemaError(f"{kind}: missing columns {missing}. Have {list(df.columns)}")


def validate_population(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, POPULATION_COLUMNS, "population_long")
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["population"] = out["population"].astype(float)
    if (out["population"] < 0).any():
        raise SchemaError("population_long: negative population values")
    return out[POPULATION_COLUMNS]


def validate_engineers(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, ENGINEERS_COLUMNS, "engineers_long")
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["engineers"] = out["engineers"].astype(float)
    bad_def = set(out["definition"]) - set(DEFINITIONS)
    if bad_def:
        raise SchemaError(f"engineers_long: bad definition {bad_def}; allowed {DEFINITIONS}")
    bad_metric = set(out["metric"]) - set(METRICS)
    if bad_metric:
        raise SchemaError(f"engineers_long: bad metric {bad_metric}; allowed {METRICS}")
    bad_method = set(out["method"]) - set(METHODS)
    if bad_method:
        raise SchemaError(f"engineers_long: bad method {bad_method}; allowed {METHODS}")
    return out[ENGINEERS_COLUMNS]


def validate_covariates(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, COVARIATES_COLUMNS, "covariates_long")
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["value"] = out["value"].astype(float)
    bad = set(out["variable"]) - set(COVARIATE_VARIABLES)
    if bad:
        raise SchemaError(f"covariates_long: bad variable {bad}; allowed {COVARIATE_VARIABLES}")
    return out[COVARIATES_COLUMNS]


def build_panel(engineers: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Join a *stock* of engineers to population and compute per-100k share.

    Only ``metric == 'stock'`` rows produce a share (a share of a flow is
    meaningless). Flow rows are dropped from the panel with the expectation that
    a separate stock-reconstruction step turns them into stocks first.
    """
    eng = validate_engineers(engineers)
    pop = validate_population(population)
    eng_stock = eng[eng["metric"] == "stock"].copy()
    merged = eng_stock.merge(
        pop[["iso3", "year", "population"]],
        on=["iso3", "year"],
        how="left",
    )
    merged["share_per_100k"] = 1e5 * merged["engineers"] / merged["population"]
    for col in PANEL_COLUMNS:
        if col not in merged.columns:
            merged[col] = pd.NA
    return merged[PANEL_COLUMNS]
