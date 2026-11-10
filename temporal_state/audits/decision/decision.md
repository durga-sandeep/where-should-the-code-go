# Post-hoc decision-consequence analysis

- Post hoc: conceived after the original outcomes; all cohorts, configurations, arms and invalid answers retained.
- B is the peak prefix cumulative net demand of the supplied schedule; any future loss occurs iff starting stock < B. Verified exhaustively against independent replay.
- Code decisions are zero-error by definition in the exact and same-side categories and always wrong in the crossing category; the empirical content is the category sizes and the model decisions.
- Responses share histories and repetitions; counts are descriptive, not independent samples.
- Binary decision correctness ignores quantity and timing errors and does not make an answer operationally sufficient.

Exhaustive threshold checks: 10,922

| Cohort | Configuration/arm | valid/N | wrong stock | same side | crossing | model wrong | code wrong | corrected / harmed | exact-stock model wrong |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heldout_v2 | gpt54_low/canonical | 192/192 | 1 | 1 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | gpt54_low/raw | 192/192 | 17 | 13 | 4 | 6 | 4 | 3/1 | 0 |
| heldout_v2 | gpt54_low/snapshot | 192/192 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | mini_low/canonical | 192/192 | 23 | 21 | 2 | 12 | 2 | 10/0 | 5 |
| heldout_v2 | mini_low/raw | 192/192 | 95 | 79 | 16 | 25 | 16 | 15/6 | 3 |
| heldout_v2 | mini_low/snapshot | 192/192 | 0 | 0 | 0 | 4 | 0 | 4/0 | 4 |
| heldout_v2 | sonnet46/canonical | 192/192 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | sonnet46/raw | 192/192 | 1 | 1 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | sonnet46/snapshot | 192/192 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | sonnet46_thinking/canonical | 192/192 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | sonnet46_thinking/raw | 192/192 | 2 | 2 | 0 | 0 | 0 | 0/0 | 0 |
| heldout_v2 | sonnet46_thinking/snapshot | 192/192 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | gpt54_low/canonical | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | gpt54_low/raw | 48/48 | 3 | 3 | 0 | 1 | 0 | 1/0 | 0 |
| hindsight_v2 | gpt54_low/snapshot | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | mini_low/canonical | 48/48 | 9 | 8 | 1 | 3 | 1 | 3/1 | 0 |
| hindsight_v2 | mini_low/raw | 48/48 | 17 | 14 | 3 | 3 | 3 | 2/2 | 0 |
| hindsight_v2 | mini_low/snapshot | 48/48 | 0 | 0 | 0 | 2 | 0 | 2/0 | 2 |
| hindsight_v2 | sonnet46/canonical | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | sonnet46/raw | 48/48 | 3 | 3 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | sonnet46/snapshot | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | sonnet46_thinking/canonical | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | sonnet46_thinking/raw | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| hindsight_v2 | sonnet46_thinking/snapshot | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| display_v2 | gpt54_low/raw | 48/48 | 7 | 7 | 0 | 0 | 0 | 0/0 | 0 |
| display_v2 | mini_low/raw | 48/48 | 25 | 18 | 7 | 10 | 7 | 3/0 | 0 |
| display_v2 | sonnet46/raw | 48/48 | 3 | 3 | 0 | 0 | 0 | 0/0 | 0 |
| display_v2 | sonnet46_thinking/raw | 48/48 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | gpt54_low/canonical | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | gpt54_low/raw | 96/96 | 9 | 8 | 1 | 1 | 1 | 0/0 | 0 |
| profiles_v2 | gpt54_low/snapshot | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | mini_low/canonical | 96/96 | 9 | 7 | 2 | 22 | 2 | 21/1 | 17 |
| profiles_v2 | mini_low/raw | 95/96 | 81 | 59 | 22 | 25 | 22 | 8/5 | 1 |
| profiles_v2 | mini_low/snapshot | 96/96 | 0 | 0 | 0 | 1 | 0 | 1/0 | 1 |
| profiles_v2 | sonnet46/canonical | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | sonnet46/raw | 96/96 | 3 | 3 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | sonnet46/snapshot | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | sonnet46_thinking/canonical | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | sonnet46_thinking/raw | 96/96 | 1 | 1 | 0 | 0 | 0 | 0/0 | 0 |
| profiles_v2 | sonnet46_thinking/snapshot | 96/96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 |
