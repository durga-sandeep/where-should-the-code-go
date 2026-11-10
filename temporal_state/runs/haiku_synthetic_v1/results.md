# Temporal state reconstruction results

Status: complete. 1920/1920 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| haiku45 | canonical | 192 | 192 | 152 | 167 | 165 | 15/167 | $2.2666 |
| haiku45 | raw | 192 | 192 | 84 | 92 | 101 | 8/92 | $2.9208 |
| haiku45 | snapshot | 192 | 192 | 178 | 192 | 178 | 14/192 | $0.9656 |
| haiku45 | state_canonical | 192 | 192 | 166 | 166 | 178 | 0/166 | $1.5623 |
| haiku45 | state_raw | 192 | 192 | 85 | 85 | 118 | 0/85 | $2.3416 |
| haiku45_thinking | canonical | 192 | 192 | 182 | 185 | 186 | 3/185 | $5.0507 |
| haiku45_thinking | raw | 192 | 182 | 158 | 160 | 170 | 2/160 | $7.8726 |
| haiku45_thinking | snapshot | 192 | 192 | 190 | 192 | 190 | 2/192 | $1.7841 |
| haiku45_thinking | state_canonical | 192 | 192 | 190 | 190 | 192 | 0/190 | $3.6998 |
| haiku45_thinking | state_raw | 192 | 181 | 163 | 163 | 169 | 0/163 | $6.9251 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| haiku45 | canonical | joint_exact | 96 | 35.4% | 26.6% to 44.8% |
| haiku45 | canonical | historical_joint | 96 | 39.1% | 30.7% to 47.9% |
| haiku45 | canonical | future_joint | 96 | 33.3% | 23.4% to 43.2% |
| haiku45 | snapshot | joint_exact | 96 | 49.0% | 39.6% to 58.3% |
| haiku45 | snapshot | historical_joint | 96 | 52.1% | 43.7% to 60.9% |
| haiku45 | snapshot | future_joint | 96 | 40.1% | 31.2% to 49.0% |
| haiku45_thinking | canonical | joint_exact | 96 | 12.5% | 5.7% to 19.3% |
| haiku45_thinking | canonical | historical_joint | 96 | 13.0% | 7.3% to 19.3% |
| haiku45_thinking | canonical | future_joint | 96 | 8.3% | 3.1% to 14.1% |
| haiku45_thinking | snapshot | joint_exact | 96 | 16.7% | 10.4% to 23.4% |
| haiku45_thinking | snapshot | historical_joint | 96 | 16.7% | 10.9% to 22.9% |
| haiku45_thinking | snapshot | future_joint | 96 | 10.4% | 5.7% to 15.6% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
