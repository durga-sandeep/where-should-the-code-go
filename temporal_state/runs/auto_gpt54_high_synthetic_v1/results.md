# Temporal state reconstruction results

Status: complete. 384/384 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_high_auto | canonical | 192 | 192 | 191 | 191 | 192 | 0/191 | $3.0800 |
| gpt54_high_auto | raw | 192 | 192 | 190 | 191 | 190 | 1/191 | $5.7713 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| gpt54_high_auto | canonical | joint_exact | 96 | 0.5% | -1.0% to 2.6% |
| gpt54_high_auto | canonical | historical_joint | 96 | 0.0% | -1.6% to 1.6% |
| gpt54_high_auto | canonical | future_joint | 96 | 1.0% | 0.0% to 2.6% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
