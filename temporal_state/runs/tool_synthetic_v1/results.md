# Temporal state reconstruction results

Status: complete. 768/768 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | tool_canonical | 192 | 192 | 186 | 188 | 187 | 2/188 | $7.1840 |
| gpt54_low | tool_raw | 192 | 192 | 192 | 192 | 192 | 0/192 | $9.9754 |
| mini_low | tool_canonical | 192 | 192 | 182 | 184 | 188 | 2/184 | $1.8090 |
| mini_low | tool_raw | 192 | 192 | 173 | 175 | 176 | 2/175 | $2.6801 |

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
