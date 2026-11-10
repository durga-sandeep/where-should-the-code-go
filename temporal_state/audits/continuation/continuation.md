# Post-hoc executable continuation

- Added after final study outcomes; all configurations, arms, cohorts and invalid contracts retained.
- Original model answer versus exact future replay from its emitted stock; no new prompts, repairs or provider calls.
- The full original five-field validity gate applies to both endpoints, even when the stock alone is usable.
- Correct code-continuation future triple is equivalent to correct stock by conservation; this is not independent evidence of temporal reasoning.
- Repetitions averaged within base; descriptive percentile intervals are not multiplicity adjusted.
- Code continuation may discard accidentally correct future answers paired with wrong stock; regressions are explicitly counted.
- Full-code historical replay plus future rollout is the exact practical baseline, not a model competitor to outperform.

| Cohort | Configuration | Arm | N | Model correct | Code correct | Corrected / regressed | Difference [95% CI], pp |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| heldout_v2 | gpt54_low | canonical | 192 | 189 | 191 | 2 / 0 | +1.0 [+0.0, +2.6] |
| heldout_v2 | gpt54_low | raw | 192 | 169 | 175 | 6 / 0 | +3.1 [+1.0, +5.7] |
| heldout_v2 | gpt54_low | snapshot | 192 | 190 | 192 | 2 / 0 | +1.0 [+0.0, +2.6] |
| heldout_v2 | mini_low | canonical | 192 | 146 | 169 | 23 / 0 | +12.0 [+6.8, +17.7] |
| heldout_v2 | mini_low | raw | 192 | 72 | 97 | 25 / 0 | +13.0 [+7.8, +18.2] |
| heldout_v2 | mini_low | snapshot | 192 | 172 | 192 | 20 / 0 | +10.4 [+6.2, +15.1] |
| heldout_v2 | sonnet46 | canonical | 192 | 191 | 192 | 1 / 0 | +0.5 [+0.0, +1.6] |
| heldout_v2 | sonnet46 | raw | 192 | 190 | 191 | 1 / 0 | +0.5 [+0.0, +1.6] |
| heldout_v2 | sonnet46 | snapshot | 192 | 192 | 192 | 0 / 0 | +0.0 [+0.0, +0.0] |
| heldout_v2 | sonnet46_thinking | canonical | 192 | 192 | 192 | 0 / 0 | +0.0 [+0.0, +0.0] |
| heldout_v2 | sonnet46_thinking | raw | 192 | 188 | 190 | 2 / 0 | +1.0 [+0.0, +2.6] |
| heldout_v2 | sonnet46_thinking | snapshot | 192 | 192 | 192 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | gpt54_low | canonical | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | gpt54_low | raw | 48 | 44 | 45 | 1 / 0 | +2.1 [+0.0, +6.2] |
| hindsight_v2 | gpt54_low | snapshot | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | mini_low | canonical | 48 | 31 | 39 | 8 / 0 | +16.7 [+4.2, +29.2] |
| hindsight_v2 | mini_low | raw | 48 | 27 | 31 | 4 / 0 | +8.3 [+2.1, +16.7] |
| hindsight_v2 | mini_low | snapshot | 48 | 44 | 48 | 4 / 0 | +8.3 [+2.1, +16.7] |
| hindsight_v2 | sonnet46 | canonical | 48 | 47 | 48 | 1 / 0 | +2.1 [+0.0, +6.2] |
| hindsight_v2 | sonnet46 | raw | 48 | 44 | 45 | 1 / 0 | +2.1 [+0.0, +6.2] |
| hindsight_v2 | sonnet46 | snapshot | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | sonnet46_thinking | canonical | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | sonnet46_thinking | raw | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| hindsight_v2 | sonnet46_thinking | snapshot | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| display_v2 | gpt54_low | raw | 48 | 41 | 41 | 0 / 0 | +0.0 [+0.0, +0.0] |
| display_v2 | mini_low | raw | 48 | 23 | 23 | 0 / 0 | +0.0 [+0.0, +0.0] |
| display_v2 | sonnet46 | raw | 48 | 45 | 45 | 0 / 0 | +0.0 [+0.0, +0.0] |
| display_v2 | sonnet46_thinking | raw | 48 | 48 | 48 | 0 / 0 | +0.0 [+0.0, +0.0] |
| profiles_v2 | gpt54_low | canonical | 96 | 88 | 96 | 8 / 0 | +8.3 [+3.1, +13.5] |
| profiles_v2 | gpt54_low | raw | 96 | 87 | 87 | 0 / 0 | +0.0 [+0.0, +0.0] |
| profiles_v2 | gpt54_low | snapshot | 96 | 95 | 96 | 1 / 0 | +1.0 [+0.0, +3.1] |
| profiles_v2 | mini_low | canonical | 96 | 45 | 87 | 42 / 0 | +43.8 [+34.4, +53.1] |
| profiles_v2 | mini_low | raw | 96 | 12 | 14 | 3 / 1 | +2.1 [-2.1, +6.2] |
| profiles_v2 | mini_low | snapshot | 96 | 86 | 96 | 10 / 0 | +10.4 [+5.2, +16.7] |
| profiles_v2 | sonnet46 | canonical | 96 | 95 | 96 | 1 / 0 | +1.0 [+0.0, +3.1] |
| profiles_v2 | sonnet46 | raw | 96 | 92 | 93 | 1 / 0 | +1.0 [+0.0, +3.1] |
| profiles_v2 | sonnet46 | snapshot | 96 | 96 | 96 | 0 / 0 | +0.0 [+0.0, +0.0] |
| profiles_v2 | sonnet46_thinking | canonical | 96 | 96 | 96 | 0 / 0 | +0.0 [+0.0, +0.0] |
| profiles_v2 | sonnet46_thinking | raw | 96 | 94 | 95 | 1 / 0 | +1.0 [+0.0, +3.1] |
| profiles_v2 | sonnet46_thinking | snapshot | 96 | 96 | 96 | 0 / 0 | +0.0 [+0.0, +0.0] |

| Cohort | Configuration | Arm | Model false / negatives | Code false / negatives | Model missed / positives | Code missed / positives |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| heldout_v2 | gpt54_low | canonical | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | gpt54_low | raw | 3/70 | 4/70 | 3/122 | 0/122 |
| heldout_v2 | gpt54_low | snapshot | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | mini_low | canonical | 5/70 | 1/70 | 7/122 | 1/122 |
| heldout_v2 | mini_low | raw | 14/70 | 12/70 | 11/122 | 4/122 |
| heldout_v2 | mini_low | snapshot | 2/70 | 0/70 | 2/122 | 0/122 |
| heldout_v2 | sonnet46 | canonical | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | sonnet46 | raw | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | sonnet46 | snapshot | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | sonnet46_thinking | canonical | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | sonnet46_thinking | raw | 0/70 | 0/70 | 0/122 | 0/122 |
| heldout_v2 | sonnet46_thinking | snapshot | 0/70 | 0/70 | 0/122 | 0/122 |
| hindsight_v2 | gpt54_low | canonical | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | gpt54_low | raw | 0/20 | 0/20 | 1/28 | 0/28 |
| hindsight_v2 | gpt54_low | snapshot | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | mini_low | canonical | 1/20 | 1/20 | 2/28 | 0/28 |
| hindsight_v2 | mini_low | raw | 2/20 | 3/20 | 1/28 | 0/28 |
| hindsight_v2 | mini_low | snapshot | 1/20 | 0/20 | 1/28 | 0/28 |
| hindsight_v2 | sonnet46 | canonical | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | sonnet46 | raw | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | sonnet46 | snapshot | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | sonnet46_thinking | canonical | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | sonnet46_thinking | raw | 0/20 | 0/20 | 0/28 | 0/28 |
| hindsight_v2 | sonnet46_thinking | snapshot | 0/20 | 0/20 | 0/28 | 0/28 |
| display_v2 | gpt54_low | raw | 0/20 | 0/20 | 0/28 | 0/28 |
| display_v2 | mini_low | raw | 5/20 | 5/20 | 5/28 | 2/28 |
| display_v2 | sonnet46 | raw | 0/20 | 0/20 | 0/28 | 0/28 |
| display_v2 | sonnet46_thinking | raw | 0/20 | 0/20 | 0/28 | 0/28 |
| profiles_v2 | gpt54_low | canonical | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | gpt54_low | raw | 1/46 | 1/46 | 0/50 | 0/50 |
| profiles_v2 | gpt54_low | snapshot | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | mini_low | canonical | 15/46 | 1/46 | 7/50 | 1/50 |
| profiles_v2 | mini_low | raw | 15/46 | 19/46 | 10/49 | 3/49 |
| profiles_v2 | mini_low | snapshot | 0/46 | 0/46 | 1/50 | 0/50 |
| profiles_v2 | sonnet46 | canonical | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | sonnet46 | raw | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | sonnet46 | snapshot | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | sonnet46_thinking | canonical | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | sonnet46_thinking | raw | 0/46 | 0/46 | 0/50 | 0/50 |
| profiles_v2 | sonnet46_thinking | snapshot | 0/46 | 0/46 | 0/50 | 0/50 |
