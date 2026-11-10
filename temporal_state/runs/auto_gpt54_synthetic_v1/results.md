# Temporal state reconstruction results

Status: complete. 960/960 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low_auto | canonical | 192 | 192 | 184 | 184 | 189 | 0/184 | $2.2953 |
| gpt54_low_auto | raw | 192 | 192 | 185 | 185 | 189 | 0/185 | $3.3320 |
| gpt54_low_auto | snapshot | 192 | 192 | 175 | 192 | 175 | 17/192 | $0.9016 |
| gpt54_low_auto | state_canonical | 192 | 192 | 156 | 156 | 161 | 0/156 | $1.6045 |
| gpt54_low_auto | state_raw | 192 | 192 | 185 | 185 | 186 | 0/185 | $2.8713 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| gpt54_low_auto | canonical | joint_exact | 96 | -0.5% | -4.2% to 3.1% |
| gpt54_low_auto | canonical | historical_joint | 96 | -0.5% | -4.2% to 3.1% |
| gpt54_low_auto | canonical | future_joint | 96 | 0.0% | -2.1% to 2.1% |
| gpt54_low_auto | snapshot | joint_exact | 96 | -5.2% | -9.9% to -0.5% |
| gpt54_low_auto | snapshot | historical_joint | 96 | 3.6% | 1.6% to 6.2% |
| gpt54_low_auto | snapshot | future_joint | 96 | -7.3% | -11.5% to -3.1% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
