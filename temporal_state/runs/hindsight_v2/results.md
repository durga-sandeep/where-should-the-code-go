# Temporal state reconstruction results

Status: complete. 576/576 expected episodes.

| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 48 | 48 | 45 | 45 | 48 | 0/45 | $0.6361 |
| gpt54_low | raw | 48 | 48 | 44 | 45 | 44 | 1/45 | $0.8828 |
| gpt54_low | snapshot | 48 | 48 | 48 | 48 | 48 | 0/48 | $0.2307 |
| mini_low | canonical | 48 | 48 | 27 | 32 | 31 | 5/32 | $0.2173 |
| mini_low | raw | 48 | 48 | 21 | 25 | 27 | 4/25 | $0.2643 |
| mini_low | snapshot | 48 | 48 | 44 | 48 | 44 | 4/48 | $0.0757 |
| sonnet46 | canonical | 48 | 48 | 46 | 47 | 47 | 1/47 | $1.9851 |
| sonnet46 | raw | 48 | 48 | 44 | 45 | 44 | 1/45 | $2.8688 |
| sonnet46 | snapshot | 48 | 48 | 48 | 48 | 48 | 0/48 | $0.6867 |
| sonnet46_thinking | canonical | 48 | 48 | 48 | 48 | 48 | 0/48 | $3.3182 |
| sonnet46_thinking | raw | 48 | 48 | 48 | 48 | 48 | 0/48 | $4.0205 |
| sonnet46_thinking | snapshot | 48 | 48 | 48 | 48 | 48 | 0/48 | $1.0850 |

All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.

## Paired differences (right minus raw)

| Configuration | Right arm | Metric | Bases | Difference | 95% interval |
| --- | --- | --- | ---: | ---: | --- |
| mini_low | canonical | joint_exact | 24 | 12.5% | -4.2% to 27.1% |
| mini_low | canonical | historical_joint | 24 | 14.6% | -4.2% to 33.3% |
| mini_low | canonical | future_joint | 24 | 8.3% | -6.2% to 25.0% |
| mini_low | snapshot | joint_exact | 24 | 47.9% | 31.2% to 64.6% |
| mini_low | snapshot | historical_joint | 24 | 47.9% | 29.2% to 66.7% |
| mini_low | snapshot | future_joint | 24 | 35.4% | 18.8% to 52.1% |
| gpt54_low | canonical | joint_exact | 24 | 2.1% | -12.5% to 16.7% |
| gpt54_low | canonical | historical_joint | 24 | 0.0% | -12.5% to 12.5% |
| gpt54_low | canonical | future_joint | 24 | 8.3% | 0.0% to 18.8% |
| gpt54_low | snapshot | joint_exact | 24 | 8.3% | 0.0% to 18.8% |
| gpt54_low | snapshot | historical_joint | 24 | 6.2% | 0.0% to 16.7% |
| gpt54_low | snapshot | future_joint | 24 | 8.3% | 0.0% to 18.8% |
| sonnet46 | canonical | joint_exact | 24 | 4.2% | -6.2% to 16.7% |
| sonnet46 | canonical | historical_joint | 24 | 4.2% | -4.2% to 14.6% |
| sonnet46 | canonical | future_joint | 24 | 6.2% | -2.1% to 16.7% |
| sonnet46 | snapshot | joint_exact | 24 | 8.3% | 0.0% to 18.8% |
| sonnet46 | snapshot | historical_joint | 24 | 6.2% | 0.0% to 16.7% |
| sonnet46 | snapshot | future_joint | 24 | 8.3% | 0.0% to 18.8% |
| sonnet46_thinking | canonical | joint_exact | 24 | 0.0% | 0.0% to 0.0% |
| sonnet46_thinking | canonical | historical_joint | 24 | 0.0% | 0.0% to 0.0% |
| sonnet46_thinking | canonical | future_joint | 24 | 0.0% | 0.0% to 0.0% |
| sonnet46_thinking | snapshot | joint_exact | 24 | 0.0% | 0.0% to 0.0% |
| sonnet46_thinking | snapshot | historical_joint | 24 | 0.0% | 0.0% to 0.0% |
| sonnet46_thinking | snapshot | future_joint | 24 | 0.0% | 0.0% to 0.0% |

Differences and intervals are percentage-point differences, not relative percentage changes.

- Stored scorer output analyzed; not independent replay validation.
- Primary accuracies require a valid full output contract.
- Paired differences average matched repetitions within independent base, then bootstrap bases.
- Intervals are descriptive, percentile, and not multiplicity adjusted.
- Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.
- Factor strata are descriptive; no independent-episode significance claims.
