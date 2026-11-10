# Temporal state reconstruction results

Status: complete. 768/768 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_high | canonical | 192 | 192 | 181 | 188 | 182 | 7/188 | $3.2562 |
| gpt54_high | raw | 192 | 192 | 181 | 185 | 181 | 4/185 | $5.9080 |
| gpt54_medium | canonical | 192 | 192 | 180 | 183 | 184 | 3/183 | $2.7564 |
| gpt54_medium | raw | 192 | 192 | 183 | 189 | 183 | 6/189 | $4.6327 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| gpt54_medium | canonical | joint_exact | 96 | -1.6% | -6.8% to 3.1% |
| gpt54_medium | canonical | historical_joint | 96 | -3.1% | -7.3% to 0.5% |
| gpt54_medium | canonical | future_joint | 96 | 0.5% | -3.6% to 4.2% |
| gpt54_high | canonical | joint_exact | 96 | 0.0% | -4.7% to 4.7% |
| gpt54_high | canonical | historical_joint | 96 | 1.6% | -1.6% to 4.7% |
| gpt54_high | canonical | future_joint | 96 | 0.5% | -4.2% to 5.2% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
