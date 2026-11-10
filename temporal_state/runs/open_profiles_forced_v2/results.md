# Temporal state reconstruction results

Status: complete. 1920/1920 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_high | canonical | 96 | 95 | 0 | 0 | 1 | 0/0 | $0.0262 |
| dsflash_high | raw | 96 | 85 | 0 | 2 | 1 | 2/2 | $0.0403 |
| dsflash_low | canonical | 96 | 89 | 0 | 0 | 1 | 0/0 | $0.0252 |
| dsflash_low | raw | 96 | 96 | 0 | 1 | 0 | 1/1 | $0.0356 |
| dspro_high | canonical | 96 | 76 | 75 | 75 | 75 | 0/75 | $1.1597 |
| dspro_high | raw | 96 | 77 | 76 | 76 | 76 | 0/76 | $2.3216 |
| dspro_low | canonical | 96 | 94 | 92 | 93 | 93 | 1/93 | $0.9448 |
| dspro_low | raw | 96 | 89 | 87 | 87 | 88 | 0/87 | $1.8214 |
| glmflash_high | canonical | 96 | 96 | 64 | 72 | 80 | 8/72 | $0.0851 |
| glmflash_high | raw | 96 | 96 | 57 | 69 | 68 | 12/69 | $0.2166 |
| glmflash_low | canonical | 96 | 96 | 47 | 65 | 62 | 18/65 | $0.0725 |
| glmflash_low | raw | 96 | 96 | 22 | 27 | 30 | 5/27 | $0.1365 |
| oss120b_high | canonical | 96 | 11 | 11 | 11 | 11 | 0/11 | $0.6770 |
| oss120b_high | raw | 96 | 0 | 0 | 0 | 0 | 0/0 | $0.7332 |
| oss120b_low | canonical | 96 | 96 | 67 | 75 | 73 | 8/75 | $0.1896 |
| oss120b_low | raw | 96 | 96 | 1 | 3 | 7 | 2/3 | $0.2062 |
| oss20b_high | canonical | 96 | 47 | 44 | 44 | 46 | 0/44 | $0.3915 |
| oss20b_high | raw | 96 | 0 | 0 | 0 | 0 | 0/0 | $0.3679 |
| oss20b_low | canonical | 96 | 43 | 7 | 9 | 11 | 2/9 | $0.0309 |
| oss20b_low | raw | 96 | 23 | 0 | 0 | 1 | 0/0 | $0.0411 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_low | canonical | joint_exact | 48 | 7.3% | 3.1% to 12.5% |
| oss20b_low | canonical | historical_joint | 48 | 9.4% | 4.2% to 14.6% |
| oss20b_low | canonical | future_joint | 48 | 10.4% | 4.2% to 16.7% |
| oss20b_high | canonical | joint_exact | 48 | 45.8% | 36.5% to 55.2% |
| oss20b_high | canonical | historical_joint | 48 | 45.8% | 36.5% to 55.2% |
| oss20b_high | canonical | future_joint | 48 | 47.9% | 39.6% to 57.3% |
| oss120b_low | canonical | joint_exact | 48 | 68.8% | 59.4% to 78.1% |
| oss120b_low | canonical | historical_joint | 48 | 75.0% | 65.6% to 83.3% |
| oss120b_low | canonical | future_joint | 48 | 68.8% | 57.3% to 79.2% |
| oss120b_high | canonical | joint_exact | 48 | 11.5% | 5.2% to 18.8% |
| oss120b_high | canonical | historical_joint | 48 | 11.5% | 5.2% to 18.8% |
| oss120b_high | canonical | future_joint | 48 | 11.5% | 5.2% to 18.8% |
| dsflash_low | canonical | joint_exact | 48 | 0.0% | 0.0% to 0.0% |
| dsflash_low | canonical | historical_joint | 48 | -1.0% | -3.1% to 0.0% |
| dsflash_low | canonical | future_joint | 48 | 1.0% | 0.0% to 3.1% |
| dsflash_high | canonical | joint_exact | 48 | 0.0% | 0.0% to 0.0% |
| dsflash_high | canonical | historical_joint | 48 | -2.1% | -6.2% to 0.0% |
| dsflash_high | canonical | future_joint | 48 | 0.0% | -3.1% to 3.1% |
| glmflash_low | canonical | joint_exact | 48 | 26.0% | 13.5% to 37.5% |
| glmflash_low | canonical | historical_joint | 48 | 39.6% | 28.1% to 51.0% |
| glmflash_low | canonical | future_joint | 48 | 33.3% | 18.8% to 47.9% |
| glmflash_high | canonical | joint_exact | 48 | 7.3% | -5.2% to 19.8% |
| glmflash_high | canonical | historical_joint | 48 | 3.1% | -9.4% to 14.6% |
| glmflash_high | canonical | future_joint | 48 | 12.5% | 0.0% to 25.0% |
| dspro_low | canonical | joint_exact | 48 | 5.2% | -1.0% to 11.5% |
| dspro_low | canonical | historical_joint | 48 | 6.2% | 0.0% to 12.5% |
| dspro_low | canonical | future_joint | 48 | 5.2% | -1.0% to 11.5% |
| dspro_high | canonical | joint_exact | 48 | -1.0% | -10.4% to 8.3% |
| dspro_high | canonical | historical_joint | 48 | -1.0% | -10.4% to 8.3% |
| dspro_high | canonical | future_joint | 48 | -1.0% | -10.4% to 8.3% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
