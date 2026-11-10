# Temporal state reconstruction results

Status: complete. 960/960 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | state_canonical | 96 | 96 | 95 | 95 | 95 | 0/95 | $1.1797 |
| gpt54_low | state_raw | 96 | 96 | 82 | 82 | 87 | 0/82 | $2.4366 |
| mini_high | state_canonical | 96 | 96 | 25 | 25 | 33 | 0/25 | $0.4720 |
| mini_high | state_raw | 96 | 96 | 21 | 21 | 33 | 0/21 | $1.6535 |
| mini_low | state_canonical | 96 | 96 | 86 | 86 | 95 | 0/86 | $0.3814 |
| mini_low | state_raw | 96 | 96 | 3 | 3 | 17 | 0/3 | $0.9706 |
| sonnet46 | state_canonical | 96 | 96 | 95 | 95 | 96 | 0/95 | $4.0556 |
| sonnet46 | state_raw | 96 | 96 | 89 | 89 | 92 | 0/89 | $8.6456 |
| sonnet46_thinking | state_canonical | 96 | 96 | 96 | 96 | 96 | 0/96 | $6.9869 |
| sonnet46_thinking | state_raw | 96 | 96 | 93 | 93 | 96 | 0/93 | $14.6158 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
