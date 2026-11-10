# Temporal state reconstruction results

Status: complete. 1152/1152 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 96 | 96 | 88 | 96 | 88 | 8/96 | $1.5392 |
| gpt54_low | raw | 96 | 96 | 85 | 85 | 87 | 0/85 | $2.7278 |
| gpt54_low | snapshot | 96 | 96 | 95 | 96 | 95 | 1/96 | $0.5159 |
| mini_low | canonical | 96 | 96 | 39 | 71 | 45 | 32/71 | $0.4829 |
| mini_low | raw | 96 | 95 | 4 | 4 | 12 | 0/4 | $0.9398 |
| mini_low | snapshot | 96 | 96 | 86 | 96 | 86 | 10/96 | $0.1674 |
| sonnet46 | canonical | 96 | 96 | 94 | 95 | 95 | 1/95 | $4.9453 |
| sonnet46 | raw | 96 | 96 | 88 | 88 | 92 | 0/88 | $10.1339 |
| sonnet46 | snapshot | 96 | 96 | 96 | 96 | 96 | 0/96 | $1.6708 |
| sonnet46_thinking | canonical | 96 | 96 | 96 | 96 | 96 | 0/96 | $7.9251 |
| sonnet46_thinking | raw | 96 | 96 | 93 | 94 | 94 | 1/94 | $14.4301 |
| sonnet46_thinking | snapshot | 96 | 96 | 96 | 96 | 96 | 0/96 | $2.6233 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low | canonical | joint_exact | 48 | 36.5% | 28.1% to 44.8% |
| mini_low | canonical | historical_joint | 48 | 69.8% | 60.4% to 79.2% |
| mini_low | canonical | future_joint | 48 | 34.4% | 24.0% to 44.8% |
| mini_low | snapshot | joint_exact | 48 | 85.4% | 79.2% to 91.7% |
| mini_low | snapshot | historical_joint | 48 | 95.8% | 91.7% to 99.0% |
| mini_low | snapshot | future_joint | 48 | 77.1% | 68.8% to 85.4% |
| gpt54_low | canonical | joint_exact | 48 | 3.1% | -3.1% to 10.4% |
| gpt54_low | canonical | historical_joint | 48 | 11.5% | 6.2% to 17.7% |
| gpt54_low | canonical | future_joint | 48 | 1.0% | -6.2% to 8.3% |
| gpt54_low | snapshot | joint_exact | 48 | 10.4% | 4.2% to 16.7% |
| gpt54_low | snapshot | historical_joint | 48 | 11.5% | 6.2% to 17.7% |
| gpt54_low | snapshot | future_joint | 48 | 8.3% | 3.1% to 14.6% |
| sonnet46 | canonical | joint_exact | 48 | 6.2% | 1.0% to 12.5% |
| sonnet46 | canonical | historical_joint | 48 | 7.3% | 1.0% to 13.5% |
| sonnet46 | canonical | future_joint | 48 | 3.1% | 0.0% to 8.3% |
| sonnet46 | snapshot | joint_exact | 48 | 8.3% | 3.1% to 14.6% |
| sonnet46 | snapshot | historical_joint | 48 | 8.3% | 3.1% to 14.6% |
| sonnet46 | snapshot | future_joint | 48 | 4.2% | 0.0% to 9.4% |
| sonnet46_thinking | canonical | joint_exact | 48 | 3.1% | 0.0% to 8.3% |
| sonnet46_thinking | canonical | historical_joint | 48 | 2.1% | 0.0% to 5.2% |
| sonnet46_thinking | canonical | future_joint | 48 | 2.1% | 0.0% to 6.2% |
| sonnet46_thinking | snapshot | joint_exact | 48 | 3.1% | 0.0% to 8.3% |
| sonnet46_thinking | snapshot | historical_joint | 48 | 2.1% | 0.0% to 5.2% |
| sonnet46_thinking | snapshot | future_joint | 48 | 2.1% | 0.0% to 6.2% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
