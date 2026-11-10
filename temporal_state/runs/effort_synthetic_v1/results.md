# Temporal state reconstruction results

Status: complete. 1152/1152 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mini_high | canonical | 192 | 191 | 65 | 100 | 67 | 35/100 | $0.9411 |
| mini_high | raw | 192 | 192 | 43 | 66 | 48 | 23/66 | $1.4371 |
| mini_high | snapshot | 192 | 192 | 187 | 192 | 187 | 5/192 | $0.4406 |
| mini_medium | canonical | 192 | 191 | 83 | 112 | 90 | 29/112 | $0.8615 |
| mini_medium | raw | 192 | 190 | 45 | 68 | 51 | 23/68 | $1.2054 |
| mini_medium | snapshot | 192 | 192 | 188 | 192 | 188 | 4/192 | $0.3724 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_medium | canonical | joint_exact | 96 | 19.8% | 10.9% to 28.6% |
| mini_medium | canonical | historical_joint | 96 | 22.9% | 14.1% to 31.8% |
| mini_medium | canonical | future_joint | 96 | 20.3% | 12.0% to 28.6% |
| mini_medium | snapshot | joint_exact | 96 | 74.5% | 67.2% to 81.2% |
| mini_medium | snapshot | historical_joint | 96 | 64.6% | 56.8% to 72.4% |
| mini_medium | snapshot | future_joint | 96 | 71.4% | 63.5% to 78.6% |
| mini_high | canonical | joint_exact | 96 | 11.5% | 2.6% to 20.3% |
| mini_high | canonical | historical_joint | 96 | 17.7% | 8.3% to 27.1% |
| mini_high | canonical | future_joint | 96 | 9.9% | 1.0% to 18.8% |
| mini_high | snapshot | joint_exact | 96 | 75.0% | 67.2% to 82.3% |
| mini_high | snapshot | historical_joint | 96 | 65.6% | 57.8% to 73.4% |
| mini_high | snapshot | future_joint | 96 | 72.4% | 64.6% to 79.7% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
