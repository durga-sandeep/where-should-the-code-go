# Temporal state reconstruction results

Status: complete. 960/960 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| haiku45 | canonical | 96 | 96 | 69 | 74 | 86 | 5/74 | $1.5558 |
| haiku45 | raw | 96 | 96 | 1 | 1 | 6 | 0/1 | $2.3138 |
| haiku45 | snapshot | 96 | 96 | 89 | 96 | 89 | 7/96 | $0.5430 |
| haiku45 | state_canonical | 96 | 96 | 75 | 75 | 91 | 0/75 | $1.1299 |
| haiku45 | state_raw | 96 | 96 | 1 | 1 | 6 | 0/1 | $2.0196 |
| haiku45_thinking | canonical | 96 | 96 | 84 | 90 | 88 | 6/90 | $3.1765 |
| haiku45_thinking | raw | 96 | 59 | 32 | 33 | 39 | 1/33 | $7.3990 |
| haiku45_thinking | snapshot | 96 | 96 | 93 | 96 | 93 | 3/96 | $1.0754 |
| haiku45_thinking | state_canonical | 96 | 96 | 91 | 91 | 95 | 0/91 | $2.5963 |
| haiku45_thinking | state_raw | 96 | 74 | 45 | 45 | 57 | 0/45 | $6.8860 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| haiku45 | canonical | joint_exact | 48 | 70.8% | 60.4% to 81.2% |
| haiku45 | canonical | historical_joint | 48 | 76.0% | 65.6% to 86.5% |
| haiku45 | canonical | future_joint | 48 | 83.3% | 74.0% to 91.7% |
| haiku45 | snapshot | joint_exact | 48 | 91.7% | 86.5% to 96.9% |
| haiku45 | snapshot | historical_joint | 48 | 99.0% | 96.9% to 100.0% |
| haiku45 | snapshot | future_joint | 48 | 86.5% | 79.2% to 92.7% |
| haiku45_thinking | canonical | joint_exact | 48 | 54.2% | 41.7% to 65.6% |
| haiku45_thinking | canonical | historical_joint | 48 | 59.4% | 50.0% to 68.8% |
| haiku45_thinking | canonical | future_joint | 48 | 51.0% | 39.6% to 62.5% |
| haiku45_thinking | snapshot | joint_exact | 48 | 63.5% | 55.2% to 71.9% |
| haiku45_thinking | snapshot | historical_joint | 48 | 65.6% | 57.3% to 74.0% |
| haiku45_thinking | snapshot | future_joint | 48 | 56.2% | 46.9% to 65.6% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
