# Temporal state reconstruction results

Status: complete. 2304/2304 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 192 | 192 | 182 | 184 | 189 | 2/184 | $2.3042 |
| gpt54_low | raw | 192 | 192 | 161 | 166 | 169 | 5/166 | $3.3404 |
| gpt54_low | snapshot | 192 | 192 | 190 | 192 | 190 | 2/192 | $0.9181 |
| mini_low | canonical | 192 | 192 | 118 | 133 | 146 | 15/133 | $0.7748 |
| mini_low | raw | 192 | 192 | 63 | 83 | 72 | 20/83 | $1.0708 |
| mini_low | snapshot | 192 | 192 | 172 | 192 | 172 | 20/192 | $0.3014 |
| sonnet46 | canonical | 192 | 192 | 190 | 191 | 191 | 1/191 | $7.0429 |
| sonnet46 | raw | 192 | 192 | 188 | 189 | 190 | 1/189 | $11.2709 |
| sonnet46 | snapshot | 192 | 192 | 192 | 192 | 192 | 0/192 | $2.6998 |
| sonnet46_thinking | canonical | 192 | 192 | 192 | 192 | 192 | 0/192 | $11.8074 |
| sonnet46_thinking | raw | 192 | 192 | 186 | 188 | 188 | 2/188 | $17.4317 |
| sonnet46_thinking | snapshot | 192 | 192 | 192 | 192 | 192 | 0/192 | $4.2186 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low | canonical | joint_exact | 96 | 28.6% | 18.8% to 38.5% |
| mini_low | canonical | historical_joint | 96 | 26.0% | 16.7% to 35.4% |
| mini_low | canonical | future_joint | 96 | 38.5% | 28.6% to 47.9% |
| mini_low | snapshot | joint_exact | 96 | 56.8% | 49.0% to 64.6% |
| mini_low | snapshot | historical_joint | 96 | 56.8% | 48.4% to 65.1% |
| mini_low | snapshot | future_joint | 96 | 52.1% | 43.8% to 60.4% |
| gpt54_low | canonical | joint_exact | 96 | 10.9% | 4.7% to 17.7% |
| gpt54_low | canonical | historical_joint | 96 | 9.4% | 3.1% to 16.1% |
| gpt54_low | canonical | future_joint | 96 | 10.4% | 5.7% to 15.6% |
| gpt54_low | snapshot | joint_exact | 96 | 15.1% | 9.4% to 21.4% |
| gpt54_low | snapshot | historical_joint | 96 | 13.5% | 7.8% to 19.8% |
| gpt54_low | snapshot | future_joint | 96 | 10.9% | 6.2% to 16.7% |
| sonnet46 | canonical | joint_exact | 96 | 1.0% | -1.6% to 3.6% |
| sonnet46 | canonical | historical_joint | 96 | 1.0% | -1.0% to 3.1% |
| sonnet46 | canonical | future_joint | 96 | 0.5% | -1.0% to 2.6% |
| sonnet46 | snapshot | joint_exact | 96 | 2.1% | 0.5% to 4.2% |
| sonnet46 | snapshot | historical_joint | 96 | 1.6% | 0.0% to 3.6% |
| sonnet46 | snapshot | future_joint | 96 | 1.0% | 0.0% to 2.6% |
| sonnet46_thinking | canonical | joint_exact | 96 | 3.1% | 1.0% to 5.7% |
| sonnet46_thinking | canonical | historical_joint | 96 | 2.1% | 0.5% to 4.2% |
| sonnet46_thinking | canonical | future_joint | 96 | 2.1% | 0.5% to 4.2% |
| sonnet46_thinking | snapshot | joint_exact | 96 | 3.1% | 1.0% to 5.7% |
| sonnet46_thinking | snapshot | historical_joint | 96 | 2.1% | 0.5% to 4.2% |
| sonnet46_thinking | snapshot | future_joint | 96 | 2.1% | 0.5% to 4.2% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
