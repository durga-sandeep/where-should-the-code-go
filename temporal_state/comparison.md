# Paired temporal controls

## hindsight

24 shared bases; 17 have changed oracle answers.

| Configuration | Arm | Paired episodes | Original joint | Control joint | Both correct | Valid answer invariant |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 48 | 46 | 45 | 93.8% | 29.2% |
| gpt54_low | raw | 48 | 39 | 44 | 79.2% | 27.1% |
| gpt54_low | snapshot | 48 | 46 | 48 | 95.8% | 29.2% |
| mini_low | canonical | 48 | 28 | 27 | 37.5% | 16.7% |
| mini_low | raw | 48 | 15 | 21 | 20.8% | 16.7% |
| mini_low | snapshot | 48 | 45 | 44 | 85.4% | 22.9% |
| sonnet46 | canonical | 48 | 48 | 46 | 95.8% | 29.2% |
| sonnet46 | raw | 48 | 47 | 44 | 89.6% | 27.1% |
| sonnet46 | snapshot | 48 | 48 | 48 | 100.0% | 29.2% |
| sonnet46_thinking | canonical | 48 | 48 | 48 | 100.0% | 29.2% |
| sonnet46_thinking | raw | 48 | 46 | 48 | 95.8% | 27.1% |
| sonnet46_thinking | snapshot | 48 | 48 | 48 | 100.0% | 29.2% |

Exact joint columns are counts. Diagnostic rates average repetitions within bases. Full conditional denominators, paired differences and bootstrap intervals are in `comparison.json`.

- Request bodies verified against task/arm; all remaining provider settings match within pairs.
- Task equality checked except intended cutoff or harmless report permutation.
- Repetitions and views remain clustered within latent base. Intervals are descriptive and unadjusted.
- Answer-change diagnostics require both valid; invalid pairs count as failures, with both-valid rate reported.
- Change when required does not establish correct sensitivity; both-correct-when-required is also reported.
- Display cross-view disagreement includes ordinary request stochasticity; within-view r0/r1 baselines are post-hoc and do not isolate causal order effects.
- Historical K130 view is retrospective reconstruction followed by a hypothetical scenario, not a T100 forecast.

## display

24 shared bases; 0 have changed oracle answers.

| Configuration | Arm | Paired episodes | Original joint | Control joint | Both correct | Valid answer invariant |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | raw | 48 | 39 | 39 | 68.8% | 68.8% |
| mini_low | raw | 48 | 15 | 20 | 25.0% | 27.1% |
| sonnet46 | raw | 48 | 47 | 43 | 89.6% | 89.6% |
| sonnet46_thinking | raw | 48 | 46 | 47 | 93.8% | 93.8% |

### Within-view repetition baselines (post-hoc)

Existing r0/r1 requests on the same control bases; one pair per base. These are descriptive stochasticity checks, not prespecified endpoints or isolated causal effects of display order.

| Configuration | View | r0/r1 base pairs | Valid identical answers | Both correct |
| --- | --- | ---: | ---: | ---: |
| gpt54_low | original | 24 | 70.8% | 70.8% |
| gpt54_low | display | 24 | 70.8% | 70.8% |
| mini_low | original | 24 | 25.0% | 20.8% |
| mini_low | display | 24 | 33.3% | 33.3% |
| sonnet46 | original | 24 | 95.8% | 95.8% |
| sonnet46 | display | 24 | 83.3% | 83.3% |
| sonnet46_thinking | original | 24 | 91.7% | 91.7% |
| sonnet46_thinking | display | 24 | 95.8% | 95.8% |

Exact joint columns are counts. Diagnostic rates average repetitions within bases. Full conditional denominators, paired differences and bootstrap intervals are in `comparison.json`.

- Request bodies verified against task/arm; all remaining provider settings match within pairs.
- Task equality checked except intended cutoff or harmless report permutation.
- Repetitions and views remain clustered within latent base. Intervals are descriptive and unadjusted.
- Answer-change diagnostics require both valid; invalid pairs count as failures, with both-valid rate reported.
- Change when required does not establish correct sensitivity; both-correct-when-required is also reported.
- Display cross-view disagreement includes ordinary request stochasticity; within-view r0/r1 baselines are post-hoc and do not isolate causal order effects.
- Historical K130 view is retrospective reconstruction followed by a hypothetical scenario, not a T100 forecast.
