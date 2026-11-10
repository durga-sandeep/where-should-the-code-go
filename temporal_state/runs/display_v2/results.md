# Temporal state reconstruction results

Status: complete. 192/192 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | raw | 48 | 48 | 39 | 39 | 41 | 0/39 | $0.9659 |
| mini_low | raw | 48 | 48 | 20 | 20 | 23 | 0/20 | $0.2785 |
| sonnet46 | raw | 48 | 48 | 43 | 43 | 45 | 0/43 | $3.2085 |
| sonnet46_thinking | raw | 48 | 48 | 47 | 47 | 48 | 0/47 | $4.7323 |

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
