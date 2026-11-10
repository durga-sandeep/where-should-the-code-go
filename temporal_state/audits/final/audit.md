# Independent temporal results audit

Passed: True. Episodes: 4224. Mismatches: 0.

| Run | Observed / expected | Mismatches |
| --- | ---: | ---: |
| heldout_v2 | 2304/2304 | 0 |
| hindsight_v2 | 576/576 | 0 |
| display_v2 | 192/192 | 0 |
| profiles_v2 | 1152/1152 | 0 |

All score fields were recomputed from raw provider responses with an independent replay. Source hashes, request bodies, model settings and complete grids were checked. See audit.json for individual issues. External CSV provenance requires a separate check.
