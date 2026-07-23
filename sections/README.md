# Sections

Each section is a broad topic. Within a section we develop **claims** —
falsifiable statements we try to substantiate or refute with data.

## Index

| Section | Status | Topic |
| --- | --- | --- |
| [`engineering-workforce`](engineering-workforce/) | Exploring | Long-run trends in formally trained engineers as a share of population. |

## Anatomy of a section

```
<section-name>/
├── README.md      # what the section is about + index of its claims
├── PLAN.md        # exploration + data-search plan
├── research/      # literature review and data-source scouting notes
├── data/
│   ├── raw/       # immutable source downloads (not committed; see data-sources notes)
│   └── processed/ # analysis-ready tables (.parquet + .meta.yaml), committed
├── notebooks/     # exploratory analysis
└── claims/
    ├── README.md      # claims register
    └── <claim-slug>/  # one dir per formulated claim
```

## Lifecycle of a claim

1. **Explore** the topic (notebooks, data scouting).
2. **Formulate** a precise, testable claim + null hypothesis. Create
   `claims/<claim-slug>/` and register it in `claims/README.md`.
3. **Test** it with an appropriate formal statistical test.
4. **Conclude**: supported / refuted / inconclusive, with evidence and caveats,
   recorded in the claim's `README.md`.

## Adding a new section

Create `sections/<name>/` mirroring the structure above (a `README.md`,
`PLAN.md`, `research/`, `data/{raw,processed}/`, `notebooks/`, `claims/`), and
add a row to the index table here.
