# Raw data — Engineering Workforce

Immutable, as-downloaded source files live here. **They are not committed**
(they can be large and are reproducible from their sources). Instead, this file
is the **manifest**: record every raw source so any download can be reproduced.

For cleaned, analysis-ready tables, see `../processed/` (those *are* committed,
each with a `.meta.yaml` provenance sidecar).

## Manifest

Add one entry per source as it is downloaded. Template:

```
### <short-id>
- File(s): <filename(s) placed in this dir>
- Source / provider: <name>
- URL / API: <link or endpoint + query>
- Retrieved: <YYYY-MM-DD>
- Coverage: <geography, years, granularity>
- Definition: <exact occupation/degree code or definition used>
- Format & license: <csv/xlsx/api; license>
- Notes / caveats: <...>
```

_(No sources downloaded yet — the data search is in progress; candidate sources
are being catalogued in `../../research/`.)_
