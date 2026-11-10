# Temporal state reconstruction results

Status: complete. 1152/1152 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_high_auto | canonical | 96 | 95 | 95 | 95 | 95 | 0/95 | $0.0870 |
| dsflash_high_auto | raw | 96 | 93 | 90 | 90 | 91 | 0/90 | $0.2326 |
| dspro_high_auto | canonical | 96 | 96 | 95 | 95 | 96 | 0/95 | $1.1852 |
| dspro_high_auto | raw | 96 | 93 | 92 | 92 | 93 | 0/92 | $2.3156 |
| glmflash_high_auto | canonical | 96 | 96 | 66 | 73 | 81 | 7/73 | $0.0917 |
| glmflash_high_auto | raw | 96 | 96 | 62 | 72 | 68 | 10/72 | $0.2288 |
| oss120b_high_auto | canonical | 96 | 10 | 10 | 10 | 10 | 0/10 | $0.6760 |
| oss120b_high_auto | raw | 96 | 0 | 0 | 0 | 0 | 0/0 | $0.7332 |
| oss20b_high_auto | canonical | 96 | 46 | 45 | 46 | 45 | 1/46 | $0.4371 |
| oss20b_high_auto | raw | 96 | 0 | 0 | 0 | 0 | 0/0 | $0.5047 |
| qwen27b_high_auto | canonical | 96 | 96 | 92 | 94 | 93 | 2/94 | $1.0885 |
| qwen27b_high_auto | raw | 96 | 96 | 93 | 93 | 94 | 0/93 | $2.3184 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_high_auto | canonical | joint_exact | 48 | 46.9% | 37.5% to 56.2% |
| oss20b_high_auto | canonical | historical_joint | 48 | 47.9% | 37.5% to 58.3% |
| oss20b_high_auto | canonical | future_joint | 48 | 46.9% | 37.5% to 56.2% |
| oss120b_high_auto | canonical | joint_exact | 48 | 10.4% | 4.2% to 17.7% |
| oss120b_high_auto | canonical | historical_joint | 48 | 10.4% | 4.2% to 17.7% |
| oss120b_high_auto | canonical | future_joint | 48 | 10.4% | 4.2% to 17.7% |
| qwen27b_high_auto | canonical | joint_exact | 48 | -1.0% | -5.2% to 3.1% |
| qwen27b_high_auto | canonical | historical_joint | 48 | 1.0% | -2.1% to 4.2% |
| qwen27b_high_auto | canonical | future_joint | 48 | -1.0% | -5.2% to 2.1% |
| dsflash_high_auto | canonical | joint_exact | 48 | 5.2% | 0.0% to 11.5% |
| dsflash_high_auto | canonical | historical_joint | 48 | 5.2% | 0.0% to 11.5% |
| dsflash_high_auto | canonical | future_joint | 48 | 4.2% | -1.0% to 10.4% |
| glmflash_high_auto | canonical | joint_exact | 48 | 4.2% | -9.4% to 17.7% |
| glmflash_high_auto | canonical | historical_joint | 48 | 1.0% | -10.4% to 12.5% |
| glmflash_high_auto | canonical | future_joint | 48 | 13.5% | 2.1% to 25.0% |
| dspro_high_auto | canonical | joint_exact | 48 | 3.1% | -1.0% to 8.3% |
| dspro_high_auto | canonical | historical_joint | 48 | 3.1% | -1.0% to 8.3% |
| dspro_high_auto | canonical | future_joint | 48 | 3.1% | 0.0% to 7.3% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
