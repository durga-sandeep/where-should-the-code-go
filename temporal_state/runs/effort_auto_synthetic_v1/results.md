# Temporal state reconstruction results

Status: complete. 768/768 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mini_high_auto | canonical | 192 | 192 | 171 | 178 | 179 | 7/178 | $1.5608 |
| mini_high_auto | raw | 192 | 191 | 139 | 145 | 152 | 6/145 | $3.0270 |
| mini_low_auto | canonical | 192 | 192 | 139 | 147 | 166 | 8/147 | $0.8175 |
| mini_low_auto | raw | 192 | 191 | 89 | 92 | 109 | 3/92 | $1.2310 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low_auto | canonical | joint_exact | 96 | 26.0% | 16.7% to 35.4% |
| mini_low_auto | canonical | historical_joint | 96 | 28.6% | 19.3% to 37.5% |
| mini_low_auto | canonical | future_joint | 96 | 29.7% | 20.3% to 38.5% |
| mini_high_auto | canonical | joint_exact | 96 | 16.7% | 9.4% to 24.0% |
| mini_high_auto | canonical | historical_joint | 96 | 17.2% | 10.4% to 24.5% |
| mini_high_auto | canonical | future_joint | 96 | 14.1% | 7.8% to 20.8% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
