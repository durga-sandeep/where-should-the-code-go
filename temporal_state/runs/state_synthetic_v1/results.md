# Temporal state reconstruction results

Status: complete. 1920/1920 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | state_canonical | 192 | 192 | 186 | 186 | 189 | 0/186 | $1.7168 |
| gpt54_low | state_raw | 192 | 192 | 170 | 170 | 176 | 0/170 | $2.8592 |
| mini_high | state_canonical | 192 | 191 | 124 | 124 | 137 | 0/124 | $0.7349 |
| mini_high | state_raw | 192 | 192 | 87 | 87 | 104 | 0/87 | $1.4621 |
| mini_low | state_canonical | 192 | 192 | 141 | 141 | 180 | 0/141 | $0.5785 |
| mini_low | state_raw | 192 | 192 | 83 | 83 | 106 | 0/83 | $0.8811 |
| sonnet46 | state_canonical | 192 | 192 | 190 | 190 | 192 | 0/190 | $5.6027 |
| sonnet46 | state_raw | 192 | 192 | 191 | 191 | 192 | 0/191 | $8.8383 |
| sonnet46_thinking | state_canonical | 192 | 192 | 191 | 191 | 192 | 0/191 | $9.7436 |
| sonnet46_thinking | state_raw | 192 | 192 | 190 | 190 | 192 | 0/190 | $15.4314 |

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
