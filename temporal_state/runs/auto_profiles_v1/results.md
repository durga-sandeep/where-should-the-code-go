# Temporal state reconstruction results

Status: complete. 960/960 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low_auto | canonical | 96 | 96 | 96 | 96 | 96 | 0/96 | $1.5395 |
| gpt54_low_auto | raw | 96 | 96 | 92 | 92 | 94 | 0/92 | $2.7531 |
| gpt54_low_auto | snapshot | 96 | 96 | 86 | 96 | 86 | 10/96 | $0.5079 |
| gpt54_low_auto | state_canonical | 96 | 96 | 88 | 88 | 88 | 0/88 | $1.1542 |
| gpt54_low_auto | state_raw | 96 | 96 | 90 | 90 | 92 | 0/90 | $2.5298 |
| mini_low_auto | canonical | 96 | 95 | 69 | 76 | 79 | 7/76 | $0.5126 |
| mini_low_auto | raw | 96 | 96 | 4 | 5 | 14 | 1/5 | $1.1431 |
| mini_low_auto | snapshot | 96 | 96 | 86 | 96 | 86 | 10/96 | $0.1650 |
| mini_low_auto | state_canonical | 96 | 94 | 81 | 81 | 91 | 0/81 | $0.3938 |
| mini_low_auto | state_raw | 96 | 95 | 4 | 4 | 19 | 0/4 | $1.0621 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low_auto | canonical | joint_exact | 48 | 67.7% | 58.3% to 76.0% |
| mini_low_auto | canonical | historical_joint | 48 | 74.0% | 65.6% to 82.3% |
| mini_low_auto | canonical | future_joint | 48 | 67.7% | 56.2% to 78.1% |
| mini_low_auto | snapshot | joint_exact | 48 | 85.4% | 77.1% to 92.7% |
| mini_low_auto | snapshot | historical_joint | 48 | 94.8% | 90.6% to 99.0% |
| mini_low_auto | snapshot | future_joint | 48 | 75.0% | 63.5% to 84.4% |
| gpt54_low_auto | canonical | joint_exact | 48 | 4.2% | 1.0% to 8.3% |
| gpt54_low_auto | canonical | historical_joint | 48 | 4.2% | 1.0% to 8.3% |
| gpt54_low_auto | canonical | future_joint | 48 | 2.1% | 0.0% to 5.2% |
| gpt54_low_auto | snapshot | joint_exact | 48 | -6.2% | -13.5% to 1.0% |
| gpt54_low_auto | snapshot | historical_joint | 48 | 4.2% | 1.0% to 8.3% |
| gpt54_low_auto | snapshot | future_joint | 48 | -8.3% | -15.6% to -1.0% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
