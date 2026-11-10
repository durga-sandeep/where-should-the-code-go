# Temporal state reconstruction results

Status: complete. 576/576 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mini_low | canonical | 192 | 192 | 111 | 133 | 129 | 22/133 | $0.7607 |
| mini_low | raw | 192 | 192 | 60 | 75 | 69 | 15/75 | $1.0016 |
| mini_low | snapshot | 192 | 192 | 171 | 192 | 171 | 21/192 | $0.2983 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low | canonical | joint_exact | 96 | 26.6% | 18.2% to 34.9% |
| mini_low | canonical | historical_joint | 96 | 30.2% | 20.8% to 39.6% |
| mini_low | canonical | future_joint | 96 | 31.2% | 22.9% to 39.6% |
| mini_low | snapshot | joint_exact | 96 | 57.8% | 48.4% to 67.2% |
| mini_low | snapshot | historical_joint | 96 | 60.9% | 52.1% to 69.8% |
| mini_low | snapshot | future_joint | 96 | 53.1% | 43.8% to 62.5% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
