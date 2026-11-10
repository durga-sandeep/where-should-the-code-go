# Temporal state reconstruction results

Status: complete. 4608/4608 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_high | canonical | 192 | 174 | 2 | 2 | 2 | 0/2 | $0.0529 |
| dsflash_high | raw | 192 | 180 | 3 | 3 | 3 | 0/3 | $0.0500 |
| dsflash_low | canonical | 192 | 182 | 4 | 5 | 4 | 1/5 | $0.0342 |
| dsflash_low | raw | 192 | 184 | 4 | 4 | 4 | 0/4 | $0.0461 |
| dspro_high | canonical | 192 | 160 | 154 | 156 | 158 | 2/156 | $1.6515 |
| dspro_high | raw | 192 | 176 | 176 | 176 | 176 | 0/176 | $2.3038 |
| dspro_low | canonical | 192 | 190 | 187 | 188 | 189 | 1/188 | $1.1779 |
| dspro_low | raw | 192 | 186 | 181 | 181 | 185 | 0/181 | $1.6776 |
| glmflash_high | canonical | 192 | 192 | 143 | 160 | 158 | 17/160 | $0.1229 |
| glmflash_high | raw | 192 | 192 | 120 | 143 | 143 | 23/143 | $0.2150 |
| glmflash_low | canonical | 192 | 192 | 103 | 134 | 120 | 31/134 | $0.1115 |
| glmflash_low | raw | 192 | 192 | 73 | 111 | 101 | 38/111 | $0.1473 |
| oss120b_high | canonical | 192 | 127 | 127 | 127 | 127 | 0/127 | $0.9919 |
| oss120b_high | raw | 192 | 103 | 103 | 103 | 103 | 0/103 | $1.1069 |
| oss120b_low | canonical | 192 | 192 | 119 | 132 | 133 | 13/132 | $0.2369 |
| oss120b_low | raw | 192 | 192 | 82 | 89 | 88 | 7/89 | $0.3043 |
| oss20b_high | canonical | 192 | 127 | 127 | 127 | 127 | 0/127 | $0.5992 |
| oss20b_high | raw | 192 | 86 | 81 | 81 | 81 | 0/81 | $0.6420 |
| oss20b_low | canonical | 192 | 133 | 97 | 105 | 100 | 8/105 | $0.0590 |
| oss20b_low | raw | 192 | 107 | 39 | 51 | 45 | 12/51 | $0.0642 |
| qwen27b_high | canonical | 192 | 182 | 174 | 179 | 176 | 5/179 | $1.2039 |
| qwen27b_high | raw | 192 | 164 | 148 | 150 | 154 | 2/150 | $1.9020 |
| qwen27b_low | canonical | 192 | 176 | 176 | 176 | 176 | 0/176 | $1.5000 |
| qwen27b_low | raw | 192 | 151 | 145 | 146 | 147 | 1/146 | $2.0375 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_low | canonical | joint_exact | 96 | 30.2% | 21.9% to 38.5% |
| oss20b_low | canonical | historical_joint | 96 | 28.1% | 20.3% to 35.9% |
| oss20b_low | canonical | future_joint | 96 | 28.6% | 20.3% to 37.0% |
| oss20b_high | canonical | joint_exact | 96 | 24.0% | 16.1% to 32.3% |
| oss20b_high | canonical | historical_joint | 96 | 24.0% | 16.1% to 32.3% |
| oss20b_high | canonical | future_joint | 96 | 24.0% | 16.1% to 32.3% |
| oss120b_low | canonical | joint_exact | 96 | 19.3% | 11.5% to 27.6% |
| oss120b_low | canonical | historical_joint | 96 | 22.4% | 15.1% to 30.2% |
| oss120b_low | canonical | future_joint | 96 | 23.4% | 15.6% to 31.8% |
| oss120b_high | canonical | joint_exact | 96 | 12.5% | 4.7% to 20.3% |
| oss120b_high | canonical | historical_joint | 96 | 12.5% | 4.7% to 20.3% |
| oss120b_high | canonical | future_joint | 96 | 12.5% | 4.7% to 20.3% |
| qwen27b_low | canonical | joint_exact | 96 | 16.1% | 9.4% to 23.4% |
| qwen27b_low | canonical | historical_joint | 96 | 15.6% | 8.9% to 22.9% |
| qwen27b_low | canonical | future_joint | 96 | 15.1% | 8.3% to 21.9% |
| qwen27b_high | canonical | joint_exact | 96 | 13.5% | 6.8% to 20.8% |
| qwen27b_high | canonical | historical_joint | 96 | 15.1% | 8.3% to 21.9% |
| qwen27b_high | canonical | future_joint | 96 | 11.5% | 4.7% to 18.2% |
| dsflash_low | canonical | joint_exact | 96 | 0.0% | -2.6% to 3.1% |
| dsflash_low | canonical | historical_joint | 96 | 0.5% | -2.6% to 3.6% |
| dsflash_low | canonical | future_joint | 96 | 0.0% | -2.6% to 3.1% |
| dsflash_high | canonical | joint_exact | 96 | -0.5% | -2.6% to 1.6% |
| dsflash_high | canonical | historical_joint | 96 | -0.5% | -2.6% to 1.6% |
| dsflash_high | canonical | future_joint | 96 | -0.5% | -2.6% to 1.6% |
| glmflash_low | canonical | joint_exact | 96 | 15.6% | 6.2% to 25.0% |
| glmflash_low | canonical | historical_joint | 96 | 12.0% | 3.1% to 20.8% |
| glmflash_low | canonical | future_joint | 96 | 9.9% | -0.5% to 20.3% |
| glmflash_high | canonical | joint_exact | 96 | 12.0% | 4.2% to 20.3% |
| glmflash_high | canonical | historical_joint | 96 | 8.9% | 2.1% to 15.6% |
| glmflash_high | canonical | future_joint | 96 | 7.8% | 0.5% to 15.6% |
| dspro_low | canonical | joint_exact | 96 | 3.1% | -0.5% to 6.8% |
| dspro_low | canonical | historical_joint | 96 | 3.6% | 0.0% to 7.3% |
| dspro_low | canonical | future_joint | 96 | 2.1% | -1.0% to 5.2% |
| dspro_high | canonical | joint_exact | 96 | -11.5% | -17.2% to -5.7% |
| dspro_high | canonical | historical_joint | 96 | -10.4% | -16.1% to -4.7% |
| dspro_high | canonical | future_joint | 96 | -9.4% | -15.6% to -3.1% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
