# Temporal state reconstruction results

Status: complete. 384/384 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_high_auto | canonical | 96 | 96 | 96 | 96 | 96 | 0/96 | $1.9580 |
| gpt54_high_auto | raw | 96 | 96 | 96 | 96 | 96 | 0/96 | $5.0033 |
| mini_high_auto | canonical | 96 | 95 | 90 | 92 | 91 | 2/92 | $0.9616 |
| mini_high_auto | raw | 96 | 95 | 34 | 34 | 47 | 0/34 | $3.2547 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_high_auto | canonical | joint_exact | 48 | 58.3% | 47.9% to 68.8% |
| mini_high_auto | canonical | historical_joint | 48 | 60.4% | 50.0% to 69.8% |
| mini_high_auto | canonical | future_joint | 48 | 45.8% | 35.4% to 56.2% |
| gpt54_high_auto | canonical | joint_exact | 48 | 0.0% | 0.0% to 0.0% |
| gpt54_high_auto | canonical | historical_joint | 48 | 0.0% | 0.0% to 0.0% |
| gpt54_high_auto | canonical | future_joint | 48 | 0.0% | 0.0% to 0.0% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
