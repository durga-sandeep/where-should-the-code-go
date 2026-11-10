# Temporal state reconstruction results

Status: complete. 1728/1728 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_low_auto | canonical | 96 | 95 | 92 | 93 | 93 | 1/93 | $0.0704 |
| dsflash_low_auto | raw | 96 | 94 | 88 | 88 | 91 | 0/88 | $0.1823 |
| dsflash_low_auto | snapshot | 96 | 96 | 95 | 96 | 95 | 1/96 | $0.0245 |
| dspro_low_auto | canonical | 96 | 96 | 95 | 95 | 96 | 0/95 | $0.8973 |
| dspro_low_auto | raw | 96 | 96 | 91 | 93 | 92 | 2/93 | $1.7618 |
| dspro_low_auto | snapshot | 96 | 96 | 92 | 96 | 92 | 4/96 | $0.1851 |
| glmflash_low_auto | canonical | 96 | 96 | 42 | 64 | 56 | 22/64 | $0.0722 |
| glmflash_low_auto | raw | 96 | 96 | 11 | 21 | 25 | 10/21 | $0.1324 |
| glmflash_low_auto | snapshot | 96 | 96 | 37 | 96 | 37 | 59/96 | $0.0211 |
| oss120b_low_auto | canonical | 96 | 95 | 68 | 76 | 70 | 8/76 | $0.1771 |
| oss120b_low_auto | raw | 96 | 49 | 2 | 2 | 5 | 0/2 | $0.1932 |
| oss120b_low_auto | snapshot | 96 | 95 | 83 | 94 | 83 | 11/94 | $0.0549 |
| oss20b_low_auto | canonical | 96 | 38 | 14 | 16 | 17 | 2/16 | $0.0323 |
| oss20b_low_auto | raw | 96 | 27 | 0 | 0 | 0 | 0/0 | $0.0477 |
| oss20b_low_auto | snapshot | 96 | 95 | 74 | 94 | 74 | 20/94 | $0.0168 |
| qwen27b_low_auto | canonical | 96 | 96 | 95 | 96 | 95 | 1/96 | $1.3018 |
| qwen27b_low_auto | raw | 96 | 96 | 90 | 90 | 93 | 0/90 | $2.3851 |
| qwen27b_low_auto | snapshot | 96 | 96 | 96 | 96 | 96 | 0/96 | $0.3345 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_low_auto | canonical | joint_exact | 48 | 14.6% | 8.3% to 21.9% |
| oss20b_low_auto | canonical | historical_joint | 48 | 16.7% | 9.4% to 24.0% |
| oss20b_low_auto | canonical | future_joint | 48 | 17.7% | 10.4% to 25.0% |
| oss20b_low_auto | snapshot | joint_exact | 48 | 77.1% | 68.8% to 85.4% |
| oss20b_low_auto | snapshot | historical_joint | 48 | 97.9% | 94.8% to 100.0% |
| oss20b_low_auto | snapshot | future_joint | 48 | 77.1% | 68.8% to 85.4% |
| oss120b_low_auto | canonical | joint_exact | 48 | 68.8% | 59.4% to 77.1% |
| oss120b_low_auto | canonical | historical_joint | 48 | 77.1% | 67.7% to 85.4% |
| oss120b_low_auto | canonical | future_joint | 48 | 67.7% | 58.3% to 77.1% |
| oss120b_low_auto | snapshot | joint_exact | 48 | 84.4% | 77.1% to 91.7% |
| oss120b_low_auto | snapshot | historical_joint | 48 | 95.8% | 91.7% to 99.0% |
| oss120b_low_auto | snapshot | future_joint | 48 | 81.2% | 72.9% to 89.6% |
| qwen27b_low_auto | canonical | joint_exact | 48 | 5.2% | 0.0% to 10.4% |
| qwen27b_low_auto | canonical | historical_joint | 48 | 6.2% | 2.1% to 11.5% |
| qwen27b_low_auto | canonical | future_joint | 48 | 2.1% | -2.1% to 6.2% |
| qwen27b_low_auto | snapshot | joint_exact | 48 | 6.2% | 2.1% to 11.5% |
| qwen27b_low_auto | snapshot | historical_joint | 48 | 6.2% | 2.1% to 11.5% |
| qwen27b_low_auto | snapshot | future_joint | 48 | 3.1% | 0.0% to 7.3% |
| dsflash_low_auto | canonical | joint_exact | 48 | 4.2% | -3.1% to 11.5% |
| dsflash_low_auto | canonical | historical_joint | 48 | 5.2% | -1.0% to 12.5% |
| dsflash_low_auto | canonical | future_joint | 48 | 2.1% | -4.2% to 8.3% |
| dsflash_low_auto | snapshot | joint_exact | 48 | 7.3% | 2.1% to 13.5% |
| dsflash_low_auto | snapshot | historical_joint | 48 | 8.3% | 3.1% to 14.6% |
| dsflash_low_auto | snapshot | future_joint | 48 | 4.2% | 0.0% to 9.4% |
| glmflash_low_auto | canonical | joint_exact | 48 | 32.3% | 20.8% to 43.8% |
| glmflash_low_auto | canonical | historical_joint | 48 | 44.8% | 33.3% to 56.2% |
| glmflash_low_auto | canonical | future_joint | 48 | 32.3% | 18.8% to 45.8% |
| glmflash_low_auto | snapshot | joint_exact | 48 | 27.1% | 15.6% to 38.5% |
| glmflash_low_auto | snapshot | historical_joint | 48 | 78.1% | 68.8% to 86.5% |
| glmflash_low_auto | snapshot | future_joint | 48 | 12.5% | -2.1% to 27.1% |
| dspro_low_auto | canonical | joint_exact | 48 | 4.2% | 0.0% to 9.4% |
| dspro_low_auto | canonical | historical_joint | 48 | 2.1% | -2.1% to 6.2% |
| dspro_low_auto | canonical | future_joint | 48 | 4.2% | 1.0% to 8.3% |
| dspro_low_auto | snapshot | joint_exact | 48 | 1.0% | -5.2% to 7.3% |
| dspro_low_auto | snapshot | historical_joint | 48 | 3.1% | 0.0% to 7.3% |
| dspro_low_auto | snapshot | future_joint | 48 | 0.0% | -6.2% to 6.2% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
