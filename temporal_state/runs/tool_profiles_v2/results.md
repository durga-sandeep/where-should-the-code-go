# Temporal state reconstruction results

Status: complete. 384/384 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | tool_canonical | 96 | 96 | 96 | 96 | 96 | 0/96 | $4.9294 |
| gpt54_low | tool_raw | 96 | 96 | 96 | 96 | 96 | 0/96 | $8.1829 |
| mini_low | tool_canonical | 96 | 96 | 94 | 94 | 96 | 0/94 | $1.4926 |
| mini_low | tool_raw | 96 | 96 | 84 | 84 | 86 | 0/84 | $2.4815 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
