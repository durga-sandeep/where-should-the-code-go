# Temporal state reconstruction results

Status: complete. 2304/2304 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dsflash_high_auto | canonical | 192 | 192 | 185 | 186 | 187 | 1/186 | $0.1330 |
| dsflash_high_auto | raw | 192 | 190 | 177 | 179 | 179 | 2/179 | $0.2270 |
| dspro_high_auto | canonical | 192 | 190 | 185 | 185 | 187 | 0/185 | $1.6862 |
| dspro_high_auto | raw | 192 | 180 | 178 | 179 | 179 | 1/179 | $2.3544 |
| glmflash_high_auto | canonical | 192 | 192 | 143 | 160 | 162 | 17/160 | $0.1408 |
| glmflash_high_auto | raw | 192 | 191 | 128 | 152 | 147 | 24/152 | $0.2427 |
| oss120b_high_auto | canonical | 192 | 132 | 132 | 132 | 132 | 0/132 | $1.0009 |
| oss120b_high_auto | raw | 192 | 94 | 94 | 94 | 94 | 0/94 | $1.1267 |
| oss20b_high_auto | canonical | 192 | 117 | 114 | 116 | 114 | 2/116 | $0.6685 |
| oss20b_high_auto | raw | 192 | 80 | 75 | 78 | 75 | 3/78 | $0.7687 |
| qwen27b_high_auto | canonical | 192 | 184 | 175 | 181 | 178 | 6/181 | $1.5154 |
| qwen27b_high_auto | raw | 192 | 173 | 165 | 165 | 170 | 0/165 | $2.5070 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| oss20b_high_auto | canonical | joint_exact | 96 | 20.3% | 12.5% to 28.1% |
| oss20b_high_auto | canonical | historical_joint | 96 | 19.8% | 12.0% to 27.6% |
| oss20b_high_auto | canonical | future_joint | 96 | 20.3% | 12.5% to 28.1% |
| oss120b_high_auto | canonical | joint_exact | 96 | 19.8% | 12.0% to 28.1% |
| oss120b_high_auto | canonical | historical_joint | 96 | 19.8% | 12.0% to 28.1% |
| oss120b_high_auto | canonical | future_joint | 96 | 19.8% | 12.0% to 28.1% |
| qwen27b_high_auto | canonical | joint_exact | 96 | 5.2% | -1.6% to 12.0% |
| qwen27b_high_auto | canonical | historical_joint | 96 | 8.3% | 2.1% to 15.1% |
| qwen27b_high_auto | canonical | future_joint | 96 | 4.2% | -2.1% to 10.9% |
| dsflash_high_auto | canonical | joint_exact | 96 | 4.2% | 0.0% to 8.3% |
| dsflash_high_auto | canonical | historical_joint | 96 | 3.6% | -0.5% to 7.8% |
| dsflash_high_auto | canonical | future_joint | 96 | 4.2% | 0.5% to 8.3% |
| glmflash_high_auto | canonical | joint_exact | 96 | 7.8% | -0.5% to 16.7% |
| glmflash_high_auto | canonical | historical_joint | 96 | 4.2% | -2.6% to 10.9% |
| glmflash_high_auto | canonical | future_joint | 96 | 7.8% | 0.5% to 15.6% |
| dspro_high_auto | canonical | joint_exact | 96 | 3.6% | -0.5% to 8.3% |
| dspro_high_auto | canonical | historical_joint | 96 | 3.1% | -1.0% to 7.8% |
| dspro_high_auto | canonical | future_joint | 96 | 4.2% | 0.5% to 8.9% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
