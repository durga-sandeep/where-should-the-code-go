# Temporal state reconstruction results

Status: complete. 384/384 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_high | canonical | 96 | 96 | 85 | 87 | 85 | 2/87 | $2.0048 |
| gpt54_high | raw | 96 | 96 | 95 | 95 | 95 | 0/95 | $5.1770 |
| gpt54_medium | canonical | 96 | 96 | 91 | 95 | 91 | 4/95 | $1.7914 |
| gpt54_medium | raw | 96 | 96 | 92 | 92 | 92 | 0/92 | $3.8017 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| gpt54_medium | canonical | joint_exact | 48 | -1.0% | -7.3% to 5.2% |
| gpt54_medium | canonical | historical_joint | 48 | 3.1% | -1.0% to 7.3% |
| gpt54_medium | canonical | future_joint | 48 | -1.0% | -7.3% to 5.2% |
| gpt54_high | canonical | joint_exact | 48 | -10.4% | -16.7% to -4.2% |
| gpt54_high | canonical | historical_joint | 48 | -8.3% | -14.6% to -2.1% |
| gpt54_high | canonical | future_joint | 48 | -10.4% | -16.7% to -4.2% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
