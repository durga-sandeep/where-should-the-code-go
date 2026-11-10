# Temporal state reconstruction results

Status: complete. 576/576 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mini_high | canonical | 96 | 96 | 26 | 27 | 28 | 1/27 | $0.5714 |
| mini_high | raw | 96 | 95 | 13 | 13 | 20 | 0/13 | $1.3666 |
| mini_high | snapshot | 96 | 96 | 90 | 96 | 90 | 6/96 | $0.2384 |
| mini_medium | canonical | 96 | 96 | 35 | 40 | 37 | 5/40 | $0.5256 |
| mini_medium | raw | 96 | 96 | 11 | 11 | 16 | 0/11 | $1.0111 |
| mini_medium | snapshot | 96 | 96 | 91 | 96 | 91 | 5/96 | $0.2056 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_medium | canonical | joint_exact | 48 | 25.0% | 13.5% to 36.5% |
| mini_medium | canonical | historical_joint | 48 | 30.2% | 19.8% to 40.6% |
| mini_medium | canonical | future_joint | 48 | 21.9% | 9.4% to 34.4% |
| mini_medium | snapshot | joint_exact | 48 | 83.3% | 72.9% to 92.7% |
| mini_medium | snapshot | historical_joint | 48 | 88.5% | 81.2% to 94.8% |
| mini_medium | snapshot | future_joint | 48 | 78.1% | 67.7% to 87.5% |
| mini_high | canonical | joint_exact | 48 | 13.5% | 2.1% to 25.0% |
| mini_high | canonical | historical_joint | 48 | 14.6% | 3.1% to 26.0% |
| mini_high | canonical | future_joint | 48 | 8.3% | -3.1% to 19.8% |
| mini_high | snapshot | joint_exact | 48 | 80.2% | 71.9% to 88.5% |
| mini_high | snapshot | historical_joint | 48 | 86.5% | 79.2% to 92.7% |
| mini_high | snapshot | future_joint | 48 | 72.9% | 63.5% to 82.3% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
