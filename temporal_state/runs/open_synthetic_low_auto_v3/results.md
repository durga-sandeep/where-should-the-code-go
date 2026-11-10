# Temporal state reconstruction results

Status: complete. 5760/5760 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_low_auto | canonical | 192 | 192 | 188 | 188 | 190 | 0/188 | $0.1029 |
| dsflash_low_auto | raw | 192 | 192 | 181 | 181 | 189 | 0/181 | $0.1775 |
| dsflash_low_auto | snapshot | 192 | 192 | 190 | 192 | 190 | 2/192 | $0.0453 |
| dsflash_low_auto | state_canonical | 192 | 191 | 187 | 187 | 190 | 0/187 | $0.0750 |
| dsflash_low_auto | state_raw | 192 | 192 | 182 | 182 | 191 | 0/182 | $0.1547 |
| dspro_low_auto | canonical | 192 | 192 | 187 | 189 | 190 | 2/189 | $1.1582 |
| dspro_low_auto | raw | 192 | 192 | 189 | 189 | 190 | 0/189 | $1.7914 |
| dspro_low_auto | snapshot | 192 | 192 | 190 | 192 | 190 | 2/192 | $0.3358 |
| dspro_low_auto | state_canonical | 192 | 192 | 186 | 186 | 190 | 0/186 | $0.8149 |
| dspro_low_auto | state_raw | 192 | 190 | 188 | 188 | 189 | 0/188 | $1.5402 |
| glmflash_low_auto | canonical | 192 | 190 | 97 | 130 | 123 | 33/130 | $0.1278 |
| glmflash_low_auto | raw | 192 | 192 | 84 | 114 | 107 | 30/114 | $0.1469 |
| glmflash_low_auto | snapshot | 192 | 192 | 113 | 192 | 113 | 79/192 | $0.0387 |
| glmflash_low_auto | state_canonical | 192 | 192 | 133 | 133 | 167 | 0/133 | $0.0787 |
| glmflash_low_auto | state_raw | 192 | 192 | 101 | 101 | 149 | 0/101 | $0.1182 |
| oss120b_low_auto | canonical | 192 | 180 | 130 | 134 | 141 | 4/134 | $0.2437 |
| oss120b_low_auto | raw | 192 | 151 | 90 | 97 | 95 | 7/97 | $0.3153 |
| oss120b_low_auto | snapshot | 192 | 191 | 182 | 190 | 182 | 8/190 | $0.0999 |
| oss120b_low_auto | state_canonical | 192 | 188 | 131 | 131 | 146 | 0/131 | $0.1804 |
| oss120b_low_auto | state_raw | 192 | 176 | 93 | 93 | 111 | 0/93 | $0.3010 |
| oss20b_low_auto | canonical | 192 | 141 | 89 | 100 | 98 | 11/100 | $0.0673 |
| oss20b_low_auto | raw | 192 | 104 | 40 | 49 | 46 | 9/49 | $0.0673 |
| oss20b_low_auto | snapshot | 192 | 192 | 159 | 192 | 159 | 33/192 | $0.0317 |
| oss20b_low_auto | state_canonical | 192 | 160 | 111 | 111 | 137 | 0/111 | $0.0518 |
| oss20b_low_auto | state_raw | 192 | 139 | 57 | 57 | 72 | 0/57 | $0.0879 |
| qwen27b_low_auto | canonical | 192 | 192 | 189 | 189 | 191 | 0/189 | $1.8563 |
| qwen27b_low_auto | raw | 192 | 189 | 177 | 177 | 183 | 0/177 | $2.7389 |
| qwen27b_low_auto | snapshot | 192 | 192 | 192 | 192 | 192 | 0/192 | $0.5973 |
| qwen27b_low_auto | state_canonical | 192 | 192 | 191 | 191 | 192 | 0/191 | $1.3173 |
| qwen27b_low_auto | state_raw | 192 | 189 | 184 | 184 | 186 | 0/184 | $2.5017 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_low_auto | canonical | joint_exact | 96 | 25.5% | 18.2% to 32.8% |
| oss20b_low_auto | canonical | historical_joint | 96 | 26.6% | 19.3% to 33.9% |
| oss20b_low_auto | canonical | future_joint | 96 | 27.1% | 19.8% to 34.4% |
| oss20b_low_auto | snapshot | joint_exact | 96 | 62.0% | 52.6% to 71.4% |
| oss20b_low_auto | snapshot | historical_joint | 96 | 74.5% | 67.7% to 81.2% |
| oss20b_low_auto | snapshot | future_joint | 96 | 58.9% | 49.5% to 68.2% |
| oss120b_low_auto | canonical | joint_exact | 96 | 20.8% | 13.0% to 29.2% |
| oss120b_low_auto | canonical | historical_joint | 96 | 19.3% | 11.5% to 27.1% |
| oss120b_low_auto | canonical | future_joint | 96 | 24.0% | 16.1% to 31.8% |
| oss120b_low_auto | snapshot | joint_exact | 96 | 47.9% | 38.5% to 56.8% |
| oss120b_low_auto | snapshot | historical_joint | 96 | 48.4% | 39.6% to 57.3% |
| oss120b_low_auto | snapshot | future_joint | 96 | 45.3% | 36.5% to 54.2% |
| qwen27b_low_auto | canonical | joint_exact | 96 | 6.2% | 2.1% to 10.9% |
| qwen27b_low_auto | canonical | historical_joint | 96 | 6.2% | 2.1% to 10.9% |
| qwen27b_low_auto | canonical | future_joint | 96 | 4.2% | 1.0% to 7.8% |
| qwen27b_low_auto | snapshot | joint_exact | 96 | 7.8% | 4.2% to 12.5% |
| qwen27b_low_auto | snapshot | historical_joint | 96 | 7.8% | 4.2% to 12.5% |
| qwen27b_low_auto | snapshot | future_joint | 96 | 4.7% | 1.6% to 8.3% |
| dsflash_low_auto | canonical | joint_exact | 96 | 3.6% | 0.0% to 7.8% |
| dsflash_low_auto | canonical | historical_joint | 96 | 3.6% | 0.0% to 7.8% |
| dsflash_low_auto | canonical | future_joint | 96 | 0.5% | -1.6% to 2.6% |
| dsflash_low_auto | snapshot | joint_exact | 96 | 4.7% | 1.0% to 8.3% |
| dsflash_low_auto | snapshot | historical_joint | 96 | 5.7% | 2.6% to 8.9% |
| dsflash_low_auto | snapshot | future_joint | 96 | 0.5% | -1.6% to 2.6% |
| glmflash_low_auto | canonical | joint_exact | 96 | 6.8% | -2.6% to 15.6% |
| glmflash_low_auto | canonical | historical_joint | 96 | 8.3% | -0.5% to 17.2% |
| glmflash_low_auto | canonical | future_joint | 96 | 8.3% | 0.0% to 16.7% |
| glmflash_low_auto | snapshot | joint_exact | 96 | 15.1% | 4.7% to 25.5% |
| glmflash_low_auto | snapshot | historical_joint | 96 | 40.6% | 32.8% to 49.0% |
| glmflash_low_auto | snapshot | future_joint | 96 | 3.1% | -6.8% to 13.0% |
| dspro_low_auto | canonical | joint_exact | 96 | -1.0% | -4.2% to 1.6% |
| dspro_low_auto | canonical | historical_joint | 96 | 0.0% | -2.1% to 2.1% |
| dspro_low_auto | canonical | future_joint | 96 | 0.0% | -2.1% to 2.1% |
| dspro_low_auto | snapshot | joint_exact | 96 | 0.5% | -1.6% to 3.1% |
| dspro_low_auto | snapshot | historical_joint | 96 | 1.6% | 0.0% to 3.6% |
| dspro_low_auto | snapshot | future_joint | 96 | 0.0% | -2.1% to 2.1% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
