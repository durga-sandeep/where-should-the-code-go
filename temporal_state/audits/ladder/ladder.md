# Amendment 4: independent analysis

- Every response reparsed; truth recomputed with the independent auditor replay; hybrid answers rebuilt with a separate scenario simulator.
- Open-weight models are served through OpenRouter with one pinned upstream per model; the served provider is recorded per call.
- Requested effort is a family-specific provider setting; observed reasoning tokens are reported next to every effort comparison.
- Interaction = (auto high - auto low) - (forced high - forced low), paired by history; positive means the forced call penalizes extra effort.
- All configurations, arms, invalid answers, refusals and truncations are retained; transport retries never re-sample a model output.

Audit passed: True; runs present: ['auto_gpt54_high_synthetic_v1', 'auto_gpt54_synthetic_v1', 'auto_high_profiles_v1', 'auto_mini_high_synthetic_v2', 'auto_mini_synthetic_v2', 'auto_profiles_v1', 'haiku_profiles_v1', 'haiku_synthetic_v1', 'open_profiles_forced_v2', 'open_profiles_high_auto_v1', 'open_profiles_low_auto_v1', 'open_synthetic_forced_v1', 'open_synthetic_high_auto_v2', 'open_synthetic_low_auto_v3']; absent: []

| Cohort | Configuration | Arm | N | Missing | Truncated | Future joint | Stock exact | Mean reasoning tok. | Cost USD |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heldout_v2 | dsflash_high | canonical | 192 | 15 | 0 | 1.0 | 3.6 | 24 | 0.05 |
| heldout_v2 | dsflash_high | raw | 192 | 10 | 0 | 1.6 | 6.8 | 78 | 0.05 |
| heldout_v2 | dsflash_high_auto | canonical | 192 | 0 | 0 | 97.4 | 97.9 | 2451 | 0.13 |
| heldout_v2 | dsflash_high_auto | raw | 192 | 2 | 2 | 93.2 | 94.3 | 4756 | 0.23 |
| heldout_v2 | dsflash_low | canonical | 192 | 6 | 0 | 2.1 | 7.8 | 32 | 0.03 |
| heldout_v2 | dsflash_low | raw | 192 | 4 | 0 | 2.1 | 6.2 | 103 | 0.05 |
| heldout_v2 | dsflash_low_auto | canonical | 192 | 0 | 0 | 99.0 | 99.0 | 1695 | 0.10 |
| heldout_v2 | dsflash_low_auto | raw | 192 | 0 | 0 | 98.4 | 98.4 | 3443 | 0.18 |
| heldout_v2 | dsflash_low_auto | snapshot | 192 | 0 | 0 | 99.0 | 100.0 | 612 | 0.05 |
| heldout_v2 | dsflash_low_auto | state_canonical | 192 | 0 | 0 | 99.0 | 99.0 | 1201 | 0.07 |
| heldout_v2 | dsflash_low_auto | state_raw | 192 | 0 | 0 | 99.5 | 99.5 | 3074 | 0.15 |
| heldout_v2 | dspro_high | canonical | 192 | 32 | 1 | 82.3 | 83.3 | 3191 | 1.65 |
| heldout_v2 | dspro_high | raw | 192 | 16 | 9 | 91.7 | 91.7 | 5211 | 2.30 |
| heldout_v2 | dspro_high_auto | canonical | 192 | 2 | 2 | 97.4 | 97.4 | 3971 | 1.69 |
| heldout_v2 | dspro_high_auto | raw | 192 | 12 | 11 | 93.2 | 93.8 | 5768 | 2.35 |
| heldout_v2 | dspro_low | canonical | 192 | 2 | 0 | 98.4 | 99.0 | 2523 | 1.18 |
| heldout_v2 | dspro_low | raw | 192 | 6 | 0 | 96.4 | 95.8 | 3662 | 1.68 |
| heldout_v2 | dspro_low_auto | canonical | 192 | 0 | 0 | 99.0 | 100.0 | 2461 | 1.16 |
| heldout_v2 | dspro_low_auto | raw | 192 | 0 | 0 | 99.0 | 99.0 | 4142 | 1.79 |
| heldout_v2 | dspro_low_auto | snapshot | 192 | 0 | 0 | 99.0 | 100.0 | 517 | 0.34 |
| heldout_v2 | dspro_low_auto | state_canonical | 192 | 0 | 0 | 99.0 | 99.0 | 1653 | 0.81 |
| heldout_v2 | dspro_low_auto | state_raw | 192 | 2 | 1 | 98.4 | 98.4 | 3615 | 1.54 |
| heldout_v2 | glmflash_high | canonical | 192 | 0 | 0 | 82.3 | 93.8 | 415 | 0.12 |
| heldout_v2 | glmflash_high | raw | 192 | 0 | 0 | 74.5 | 91.1 | 823 | 0.22 |
| heldout_v2 | glmflash_high_auto | canonical | 192 | 0 | 0 | 84.4 | 95.8 | 503 | 0.14 |
| heldout_v2 | glmflash_high_auto | raw | 192 | 1 | 0 | 76.6 | 92.2 | 991 | 0.24 |
| heldout_v2 | glmflash_low | canonical | 192 | 0 | 0 | 62.5 | 84.4 | 316 | 0.11 |
| heldout_v2 | glmflash_low | raw | 192 | 0 | 0 | 52.6 | 78.1 | 444 | 0.15 |
| heldout_v2 | glmflash_low_auto | canonical | 192 | 2 | 1 | 64.1 | 85.9 | 441 | 0.13 |
| heldout_v2 | glmflash_low_auto | raw | 192 | 0 | 0 | 55.7 | 76.0 | 441 | 0.15 |
| heldout_v2 | glmflash_low_auto | snapshot | 192 | 0 | 0 | 58.9 | 100.0 | 65 | 0.04 |
| heldout_v2 | glmflash_low_auto | state_canonical | 192 | 0 | 0 | 87.0 | 87.0 | 148 | 0.08 |
| heldout_v2 | glmflash_low_auto | state_raw | 192 | 0 | 0 | 77.6 | 77.6 | 313 | 0.12 |
| heldout_v2 | gpt54_high | canonical | 192 | 0 | 0 | 94.8 | 98.4 | 749 | 3.26 |
| heldout_v2 | gpt54_high | raw | 192 | 0 | 0 | 94.3 | 96.9 | 1602 | 5.91 |
| heldout_v2 | gpt54_high_auto | canonical | 192 | 0 | 0 | 100.0 | 100.0 | 688 | 3.08 |
| heldout_v2 | gpt54_high_auto | raw | 192 | 0 | 0 | 99.0 | 99.5 | 1554 | 5.77 |
| heldout_v2 | gpt54_low | canonical | 192 | 0 | 0 | 98.4 | 99.5 | 419 | 2.30 |
| heldout_v2 | gpt54_low | raw | 192 | 0 | 0 | 88.0 | 91.1 | 710 | 3.34 |
| heldout_v2 | gpt54_low | snapshot | 192 | 0 | 0 | 99.0 | 100.0 | 142 | 0.92 |
| heldout_v2 | gpt54_low | state_canonical | 192 | 0 | 0 | 98.4 | 98.4 | 290 | 1.72 |
| heldout_v2 | gpt54_low | state_raw | 192 | 0 | 0 | 91.7 | 91.7 | 618 | 2.86 |
| heldout_v2 | gpt54_low | tool_canonical | 192 | 0 | 0 | 97.4 | 98.4 | 1590 | 7.18 |
| heldout_v2 | gpt54_low | tool_raw | 192 | 0 | 0 | 100.0 | 100.0 | 2248 | 9.98 |
| heldout_v2 | gpt54_low_auto | canonical | 192 | 0 | 0 | 98.4 | 98.4 | 415 | 2.30 |
| heldout_v2 | gpt54_low_auto | raw | 192 | 0 | 0 | 98.4 | 98.4 | 707 | 3.33 |
| heldout_v2 | gpt54_low_auto | snapshot | 192 | 0 | 0 | 91.1 | 100.0 | 136 | 0.90 |
| heldout_v2 | gpt54_low_auto | state_canonical | 192 | 0 | 0 | 83.9 | 83.9 | 248 | 1.60 |
| heldout_v2 | gpt54_low_auto | state_raw | 192 | 0 | 0 | 96.9 | 96.9 | 622 | 2.87 |
| heldout_v2 | gpt54_medium | canonical | 192 | 0 | 0 | 95.8 | 97.9 | 576 | 2.76 |
| heldout_v2 | gpt54_medium | raw | 192 | 0 | 0 | 95.3 | 98.4 | 1159 | 4.63 |
| heldout_v2 | haiku45 | canonical | 192 | 0 | 0 | 85.9 | 96.9 | n/a | 2.27 |
| heldout_v2 | haiku45 | raw | 192 | 0 | 0 | 52.6 | 59.4 | n/a | 2.92 |
| heldout_v2 | haiku45 | snapshot | 192 | 0 | 0 | 92.7 | 100.0 | n/a | 0.97 |
| heldout_v2 | haiku45 | state_canonical | 192 | 0 | 0 | 92.7 | 92.7 | n/a | 1.56 |
| heldout_v2 | haiku45 | state_raw | 192 | 0 | 0 | 61.5 | 61.5 | n/a | 2.34 |
| heldout_v2 | haiku45_thinking | canonical | 192 | 0 | 0 | 96.9 | 100.0 | n/a | 5.05 |
| heldout_v2 | haiku45_thinking | raw | 192 | 10 | 10 | 88.5 | 90.1 | n/a | 7.87 |
| heldout_v2 | haiku45_thinking | snapshot | 192 | 0 | 0 | 99.0 | 100.0 | n/a | 1.78 |
| heldout_v2 | haiku45_thinking | state_canonical | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 3.70 |
| heldout_v2 | haiku45_thinking | state_raw | 192 | 11 | 11 | 88.0 | 88.0 | n/a | 6.93 |
| heldout_v2 | mini_high | canonical | 192 | 0 | 0 | 34.9 | 56.2 | 708 | 0.94 |
| heldout_v2 | mini_high | raw | 192 | 0 | 0 | 25.0 | 41.7 | 1214 | 1.44 |
| heldout_v2 | mini_high | snapshot | 192 | 0 | 0 | 97.4 | 100.0 | 333 | 0.44 |
| heldout_v2 | mini_high | state_canonical | 192 | 0 | 0 | 71.4 | 71.4 | 544 | 0.73 |
| heldout_v2 | mini_high | state_raw | 192 | 0 | 0 | 54.2 | 54.2 | 1317 | 1.46 |
| heldout_v2 | mini_high_auto | canonical | 192 | 0 | 0 | 93.2 | 96.9 | 1425 | 1.56 |
| heldout_v2 | mini_high_auto | raw | 192 | 1 | 1 | 79.2 | 82.3 | 3054 | 3.03 |
| heldout_v2 | mini_high_auto | snapshot | 192 | 0 | 0 | 98.4 | 100.0 | 332 | 0.44 |
| heldout_v2 | mini_low | canonical | 192 | 0 | 0 | 76.0 | 88.0 | 515 | 0.77 |
| heldout_v2 | mini_low | raw | 192 | 0 | 0 | 37.5 | 50.5 | 790 | 1.07 |
| heldout_v2 | mini_low | snapshot | 192 | 0 | 0 | 89.6 | 100.0 | 172 | 0.30 |
| heldout_v2 | mini_low | state_canonical | 192 | 0 | 0 | 93.8 | 93.8 | 363 | 0.58 |
| heldout_v2 | mini_low | state_raw | 192 | 0 | 0 | 55.2 | 55.2 | 645 | 0.88 |
| heldout_v2 | mini_low | tool_canonical | 192 | 0 | 0 | 97.9 | 99.5 | 1265 | 1.81 |
| heldout_v2 | mini_low | tool_raw | 192 | 0 | 0 | 91.7 | 94.8 | 2044 | 2.68 |
| heldout_v2 | mini_low_auto | canonical | 192 | 0 | 0 | 86.5 | 91.7 | 565 | 0.82 |
| heldout_v2 | mini_low_auto | raw | 192 | 1 | 0 | 56.8 | 58.9 | 975 | 1.23 |
| heldout_v2 | mini_low_auto | snapshot | 192 | 0 | 0 | 94.8 | 100.0 | 167 | 0.30 |
| heldout_v2 | mini_low_auto | state_canonical | 192 | 0 | 0 | 94.8 | 94.8 | 380 | 0.59 |
| heldout_v2 | mini_low_auto | state_raw | 192 | 0 | 0 | 69.3 | 69.3 | 770 | 0.99 |
| heldout_v2 | mini_medium | canonical | 192 | 0 | 0 | 46.9 | 66.1 | 616 | 0.86 |
| heldout_v2 | mini_medium | raw | 192 | 0 | 0 | 26.6 | 45.8 | 945 | 1.21 |
| heldout_v2 | mini_medium | snapshot | 192 | 0 | 0 | 97.9 | 100.0 | 254 | 0.37 |
| heldout_v2 | oss120b_high | canonical | 192 | 65 | 65 | 66.1 | 66.1 | 5925 | 0.99 |
| heldout_v2 | oss120b_high | raw | 192 | 89 | 89 | 53.6 | 53.6 | 6539 | 1.11 |
| heldout_v2 | oss120b_high_auto | canonical | 192 | 60 | 60 | 68.8 | 68.8 | 5986 | 1.00 |
| heldout_v2 | oss120b_high_auto | raw | 192 | 98 | 98 | 49.0 | 49.0 | 6679 | 1.13 |
| heldout_v2 | oss120b_low | canonical | 192 | 0 | 0 | 69.3 | 79.7 | 664 | 0.24 |
| heldout_v2 | oss120b_low | raw | 192 | 0 | 0 | 45.8 | 53.6 | 941 | 0.30 |
| heldout_v2 | oss120b_low_auto | canonical | 192 | 12 | 0 | 73.4 | 78.1 | 713 | 0.24 |
| heldout_v2 | oss120b_low_auto | raw | 192 | 41 | 0 | 49.5 | 54.7 | 1023 | 0.32 |
| heldout_v2 | oss120b_low_auto | snapshot | 192 | 1 | 0 | 94.8 | 99.0 | 286 | 0.10 |
| heldout_v2 | oss120b_low_auto | state_canonical | 192 | 4 | 0 | 76.0 | 76.0 | 443 | 0.18 |
| heldout_v2 | oss120b_low_auto | state_raw | 192 | 16 | 0 | 57.8 | 57.8 | 1089 | 0.30 |
| heldout_v2 | oss20b_high | canonical | 192 | 65 | 0 | 66.1 | 66.1 | 9862 | 0.60 |
| heldout_v2 | oss20b_high | raw | 192 | 106 | 0 | 42.2 | 42.2 | 10545 | 0.64 |
| heldout_v2 | oss20b_high_auto | canonical | 192 | 75 | 58 | 59.4 | 60.4 | 11037 | 0.67 |
| heldout_v2 | oss20b_high_auto | raw | 192 | 112 | 97 | 39.1 | 40.6 | 12678 | 0.77 |
| heldout_v2 | oss20b_low | canonical | 192 | 59 | 0 | 52.1 | 58.3 | 482 | 0.06 |
| heldout_v2 | oss20b_low | raw | 192 | 85 | 0 | 23.4 | 31.2 | 494 | 0.06 |
| heldout_v2 | oss20b_low_auto | canonical | 192 | 51 | 0 | 51.0 | 62.5 | 598 | 0.07 |
| heldout_v2 | oss20b_low_auto | raw | 192 | 88 | 0 | 24.0 | 31.8 | 498 | 0.07 |
| heldout_v2 | oss20b_low_auto | snapshot | 192 | 0 | 0 | 82.8 | 100.0 | 293 | 0.03 |
| heldout_v2 | oss20b_low_auto | state_canonical | 192 | 32 | 0 | 71.4 | 71.4 | 424 | 0.05 |
| heldout_v2 | oss20b_low_auto | state_raw | 192 | 53 | 0 | 37.5 | 37.5 | 946 | 0.09 |
| heldout_v2 | qwen27b_high | canonical | 192 | 10 | 0 | 91.7 | 94.3 | 1225 | 1.20 |
| heldout_v2 | qwen27b_high | raw | 192 | 28 | 0 | 80.2 | 81.8 | 2103 | 1.90 |
| heldout_v2 | qwen27b_high_auto | canonical | 192 | 8 | 0 | 92.7 | 95.8 | 1212 | 1.52 |
| heldout_v2 | qwen27b_high_auto | raw | 192 | 19 | 4 | 88.5 | 88.5 | 2271 | 2.51 |
| heldout_v2 | qwen27b_low | canonical | 192 | 16 | 0 | 91.7 | 91.7 | 1607 | 1.50 |
| heldout_v2 | qwen27b_low | raw | 192 | 40 | 0 | 76.6 | 77.1 | 2379 | 2.04 |
| heldout_v2 | qwen27b_low_auto | canonical | 192 | 0 | 0 | 99.5 | 99.5 | 1683 | 1.86 |
| heldout_v2 | qwen27b_low_auto | raw | 192 | 3 | 1 | 95.3 | 95.3 | 2679 | 2.74 |
| heldout_v2 | qwen27b_low_auto | snapshot | 192 | 0 | 0 | 100.0 | 100.0 | 446 | 0.60 |
| heldout_v2 | qwen27b_low_auto | state_canonical | 192 | 0 | 0 | 100.0 | 100.0 | 1078 | 1.32 |
| heldout_v2 | qwen27b_low_auto | state_raw | 192 | 3 | 3 | 96.9 | 96.9 | 2394 | 2.50 |
| heldout_v2 | sonnet46 | canonical | 192 | 0 | 0 | 99.5 | 100.0 | n/a | 7.04 |
| heldout_v2 | sonnet46 | raw | 192 | 0 | 0 | 99.0 | 99.5 | n/a | 11.27 |
| heldout_v2 | sonnet46 | snapshot | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 2.70 |
| heldout_v2 | sonnet46 | state_canonical | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 5.60 |
| heldout_v2 | sonnet46 | state_raw | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 8.84 |
| heldout_v2 | sonnet46_thinking | canonical | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 11.81 |
| heldout_v2 | sonnet46_thinking | raw | 192 | 0 | 0 | 97.9 | 99.0 | n/a | 17.43 |
| heldout_v2 | sonnet46_thinking | snapshot | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 4.22 |
| heldout_v2 | sonnet46_thinking | state_canonical | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 9.74 |
| heldout_v2 | sonnet46_thinking | state_raw | 192 | 0 | 0 | 100.0 | 100.0 | n/a | 15.43 |
| profiles_v2 | dsflash_high | canonical | 96 | 1 | 0 | 1.0 | 10.4 | 0 | 0.03 |
| profiles_v2 | dsflash_high | raw | 96 | 8 | 0 | 1.0 | 5.2 | 0 | 0.04 |
| profiles_v2 | dsflash_high_auto | canonical | 96 | 0 | 0 | 99.0 | 99.0 | 3224 | 0.09 |
| profiles_v2 | dsflash_high_auto | raw | 96 | 3 | 1 | 94.8 | 94.8 | 10247 | 0.23 |
| profiles_v2 | dsflash_low | canonical | 96 | 4 | 0 | 1.0 | 10.4 | 0 | 0.03 |
| profiles_v2 | dsflash_low | raw | 96 | 0 | 0 | 0.0 | 7.3 | 0 | 0.04 |
| profiles_v2 | dsflash_low_auto | canonical | 96 | 1 | 0 | 96.9 | 97.9 | 2421 | 0.07 |
| profiles_v2 | dsflash_low_auto | raw | 96 | 1 | 0 | 94.8 | 94.8 | 7678 | 0.18 |
| profiles_v2 | dsflash_low_auto | snapshot | 96 | 0 | 0 | 99.0 | 100.0 | 689 | 0.02 |
| profiles_v2 | dspro_high | canonical | 96 | 20 | 1 | 78.1 | 78.1 | 4327 | 1.16 |
| profiles_v2 | dspro_high | raw | 96 | 19 | 4 | 79.2 | 79.2 | 10241 | 2.32 |
| profiles_v2 | dspro_high_auto | canonical | 96 | 0 | 0 | 100.0 | 100.0 | 5673 | 1.19 |
| profiles_v2 | dspro_high_auto | raw | 96 | 3 | 3 | 96.9 | 96.9 | 11693 | 2.32 |
| profiles_v2 | dspro_low | canonical | 96 | 2 | 1 | 96.9 | 97.9 | 4156 | 0.94 |
| profiles_v2 | dspro_low | raw | 96 | 7 | 0 | 91.7 | 91.7 | 8354 | 1.82 |
| profiles_v2 | dspro_low_auto | canonical | 96 | 0 | 0 | 100.0 | 100.0 | 4032 | 0.90 |
| profiles_v2 | dspro_low_auto | raw | 96 | 0 | 0 | 95.8 | 97.9 | 8516 | 1.76 |
| profiles_v2 | dspro_low_auto | snapshot | 96 | 0 | 0 | 95.8 | 100.0 | 574 | 0.19 |
| profiles_v2 | glmflash_high | canonical | 96 | 0 | 0 | 83.3 | 94.8 | 575 | 0.09 |
| profiles_v2 | glmflash_high | raw | 96 | 0 | 0 | 70.8 | 87.5 | 1703 | 0.22 |
| profiles_v2 | glmflash_high_auto | canonical | 96 | 0 | 0 | 84.4 | 94.8 | 671 | 0.09 |
| profiles_v2 | glmflash_high_auto | raw | 96 | 0 | 0 | 70.8 | 84.4 | 1870 | 0.23 |
| profiles_v2 | glmflash_low | canonical | 96 | 0 | 0 | 64.6 | 90.6 | 362 | 0.07 |
| profiles_v2 | glmflash_low | raw | 96 | 0 | 0 | 31.2 | 53.1 | 858 | 0.14 |
| profiles_v2 | glmflash_low_auto | canonical | 96 | 0 | 0 | 58.3 | 87.5 | 349 | 0.07 |
| profiles_v2 | glmflash_low_auto | raw | 96 | 0 | 0 | 26.0 | 51.0 | 809 | 0.13 |
| profiles_v2 | glmflash_low_auto | snapshot | 96 | 0 | 0 | 38.5 | 100.0 | 58 | 0.02 |
| profiles_v2 | gpt54_high | canonical | 96 | 0 | 0 | 88.5 | 90.6 | 878 | 2.00 |
| profiles_v2 | gpt54_high | raw | 96 | 0 | 0 | 99.0 | 99.0 | 2834 | 5.18 |
| profiles_v2 | gpt54_high_auto | canonical | 96 | 0 | 0 | 100.0 | 100.0 | 846 | 1.96 |
| profiles_v2 | gpt54_high_auto | raw | 96 | 0 | 0 | 100.0 | 100.0 | 2713 | 5.00 |
| profiles_v2 | gpt54_low | canonical | 96 | 0 | 0 | 91.7 | 100.0 | 555 | 1.54 |
| profiles_v2 | gpt54_low | raw | 96 | 0 | 0 | 90.6 | 90.6 | 1133 | 2.73 |
| profiles_v2 | gpt54_low | snapshot | 96 | 0 | 0 | 99.0 | 100.0 | 160 | 0.52 |
| profiles_v2 | gpt54_low | state_canonical | 96 | 0 | 0 | 99.0 | 99.0 | 401 | 1.18 |
| profiles_v2 | gpt54_low | state_raw | 96 | 0 | 0 | 90.6 | 90.6 | 1026 | 2.44 |
| profiles_v2 | gpt54_low | tool_canonical | 96 | 0 | 0 | 100.0 | 100.0 | 2266 | 4.93 |
| profiles_v2 | gpt54_low | tool_raw | 96 | 0 | 0 | 100.0 | 100.0 | 3820 | 8.18 |
| profiles_v2 | gpt54_low_auto | canonical | 96 | 0 | 0 | 100.0 | 100.0 | 554 | 1.54 |
| profiles_v2 | gpt54_low_auto | raw | 96 | 0 | 0 | 97.9 | 97.9 | 1150 | 2.75 |
| profiles_v2 | gpt54_low_auto | snapshot | 96 | 0 | 0 | 89.6 | 100.0 | 155 | 0.51 |
| profiles_v2 | gpt54_low_auto | state_canonical | 96 | 0 | 0 | 91.7 | 91.7 | 381 | 1.15 |
| profiles_v2 | gpt54_low_auto | state_raw | 96 | 0 | 0 | 95.8 | 95.8 | 1091 | 2.53 |
| profiles_v2 | gpt54_medium | canonical | 96 | 0 | 0 | 94.8 | 99.0 | 730 | 1.79 |
| profiles_v2 | gpt54_medium | raw | 96 | 0 | 0 | 95.8 | 95.8 | 1878 | 3.80 |
| profiles_v2 | haiku45 | canonical | 96 | 0 | 0 | 89.6 | 96.9 | n/a | 1.56 |
| profiles_v2 | haiku45 | raw | 96 | 0 | 0 | 6.2 | 7.3 | n/a | 2.31 |
| profiles_v2 | haiku45 | snapshot | 96 | 0 | 0 | 92.7 | 100.0 | n/a | 0.54 |
| profiles_v2 | haiku45 | state_canonical | 96 | 0 | 0 | 94.8 | 94.8 | n/a | 1.13 |
| profiles_v2 | haiku45 | state_raw | 96 | 0 | 0 | 6.2 | 6.2 | n/a | 2.02 |
| profiles_v2 | haiku45_thinking | canonical | 96 | 0 | 0 | 91.7 | 99.0 | n/a | 3.18 |
| profiles_v2 | haiku45_thinking | raw | 96 | 37 | 37 | 40.6 | 41.7 | n/a | 7.40 |
| profiles_v2 | haiku45_thinking | snapshot | 96 | 0 | 0 | 96.9 | 100.0 | n/a | 1.08 |
| profiles_v2 | haiku45_thinking | state_canonical | 96 | 0 | 0 | 99.0 | 99.0 | n/a | 2.60 |
| profiles_v2 | haiku45_thinking | state_raw | 96 | 21 | 22 | 59.4 | 59.4 | n/a | 6.89 |
| profiles_v2 | mini_high | canonical | 96 | 0 | 0 | 29.2 | 35.4 | 809 | 0.57 |
| profiles_v2 | mini_high | raw | 96 | 0 | 0 | 20.8 | 30.2 | 2402 | 1.37 |
| profiles_v2 | mini_high | snapshot | 96 | 0 | 0 | 93.8 | 100.0 | 354 | 0.24 |
| profiles_v2 | mini_high | state_canonical | 96 | 0 | 0 | 34.4 | 34.4 | 674 | 0.47 |
| profiles_v2 | mini_high | state_raw | 96 | 0 | 0 | 34.4 | 34.4 | 3162 | 1.65 |
| profiles_v2 | mini_high_auto | canonical | 96 | 1 | 0 | 94.8 | 96.9 | 1712 | 0.96 |
| profiles_v2 | mini_high_auto | raw | 96 | 1 | 1 | 49.0 | 49.0 | 6773 | 3.25 |
| profiles_v2 | mini_low | canonical | 96 | 0 | 0 | 46.9 | 90.6 | 604 | 0.48 |
| profiles_v2 | mini_low | raw | 96 | 0 | 0 | 12.5 | 14.6 | 1414 | 0.94 |
| profiles_v2 | mini_low | snapshot | 96 | 0 | 0 | 89.6 | 100.0 | 190 | 0.17 |
| profiles_v2 | mini_low | state_canonical | 96 | 0 | 0 | 99.0 | 99.0 | 464 | 0.38 |
| profiles_v2 | mini_low | state_raw | 96 | 0 | 0 | 17.7 | 17.7 | 1581 | 0.97 |
| profiles_v2 | mini_low | tool_canonical | 96 | 0 | 0 | 100.0 | 100.0 | 2309 | 1.49 |
| profiles_v2 | mini_low | tool_raw | 96 | 0 | 0 | 89.6 | 89.6 | 4027 | 2.48 |
| profiles_v2 | mini_low_auto | canonical | 96 | 1 | 0 | 82.3 | 92.7 | 673 | 0.51 |
| profiles_v2 | mini_low_auto | raw | 96 | 0 | 0 | 14.6 | 18.8 | 1884 | 1.14 |
| profiles_v2 | mini_low_auto | snapshot | 96 | 0 | 0 | 89.6 | 100.0 | 184 | 0.17 |
| profiles_v2 | mini_low_auto | state_canonical | 96 | 2 | 0 | 94.8 | 94.8 | 494 | 0.39 |
| profiles_v2 | mini_low_auto | state_raw | 96 | 1 | 0 | 19.8 | 19.8 | 1793 | 1.06 |
| profiles_v2 | mini_medium | canonical | 96 | 0 | 0 | 38.5 | 52.1 | 703 | 0.53 |
| profiles_v2 | mini_medium | raw | 96 | 0 | 0 | 16.7 | 24.0 | 1579 | 1.01 |
| profiles_v2 | mini_medium | snapshot | 96 | 0 | 0 | 94.8 | 100.0 | 278 | 0.21 |
| profiles_v2 | oss120b_high | canonical | 96 | 85 | 84 | 11.5 | 11.5 | 8096 | 0.68 |
| profiles_v2 | oss120b_high | raw | 96 | 96 | 96 | 0.0 | 0.0 | 8189 | 0.73 |
| profiles_v2 | oss120b_high_auto | canonical | 96 | 86 | 86 | 10.4 | 10.4 | 8083 | 0.68 |
| profiles_v2 | oss120b_high_auto | raw | 96 | 96 | 96 | 0.0 | 0.0 | 8189 | 0.73 |
| profiles_v2 | oss120b_low | canonical | 96 | 0 | 0 | 76.0 | 85.4 | 1281 | 0.19 |
| profiles_v2 | oss120b_low | raw | 96 | 0 | 0 | 7.3 | 17.7 | 818 | 0.21 |
| profiles_v2 | oss120b_low_auto | canonical | 96 | 1 | 0 | 72.9 | 83.3 | 1107 | 0.18 |
| profiles_v2 | oss120b_low_auto | raw | 96 | 47 | 0 | 5.2 | 10.4 | 635 | 0.19 |
| profiles_v2 | oss120b_low_auto | snapshot | 96 | 0 | 0 | 86.5 | 97.9 | 296 | 0.05 |
| profiles_v2 | oss20b_high | canonical | 96 | 49 | 0 | 47.9 | 47.9 | 12881 | 0.39 |
| profiles_v2 | oss20b_high | raw | 96 | 96 | 0 | 0.0 | 0.0 | 11847 | 0.37 |
| profiles_v2 | oss20b_high_auto | canonical | 96 | 50 | 46 | 46.9 | 47.9 | 14406 | 0.44 |
| profiles_v2 | oss20b_high_auto | raw | 96 | 96 | 96 | 0.0 | 0.0 | 16382 | 0.50 |
| profiles_v2 | oss20b_low | canonical | 96 | 53 | 0 | 11.5 | 17.7 | 348 | 0.03 |
| profiles_v2 | oss20b_low | raw | 96 | 73 | 0 | 1.0 | 3.1 | 410 | 0.04 |
| profiles_v2 | oss20b_low_auto | canonical | 96 | 58 | 0 | 17.7 | 19.8 | 349 | 0.03 |
| profiles_v2 | oss20b_low_auto | raw | 96 | 69 | 0 | 0.0 | 2.1 | 491 | 0.05 |
| profiles_v2 | oss20b_low_auto | snapshot | 96 | 1 | 0 | 77.1 | 97.9 | 294 | 0.02 |
| profiles_v2 | qwen27b_high_auto | canonical | 96 | 0 | 0 | 96.9 | 99.0 | 1888 | 1.09 |
| profiles_v2 | qwen27b_high_auto | raw | 96 | 0 | 0 | 97.9 | 97.9 | 4318 | 2.32 |
| profiles_v2 | qwen27b_low_auto | canonical | 96 | 0 | 0 | 99.0 | 100.0 | 2641 | 1.30 |
| profiles_v2 | qwen27b_low_auto | raw | 96 | 0 | 0 | 96.9 | 96.9 | 5163 | 2.39 |
| profiles_v2 | qwen27b_low_auto | snapshot | 96 | 0 | 0 | 100.0 | 100.0 | 517 | 0.33 |
| profiles_v2 | sonnet46 | canonical | 96 | 0 | 0 | 99.0 | 100.0 | n/a | 4.95 |
| profiles_v2 | sonnet46 | raw | 96 | 0 | 0 | 95.8 | 96.9 | n/a | 10.13 |
| profiles_v2 | sonnet46 | snapshot | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 1.67 |
| profiles_v2 | sonnet46 | state_canonical | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 4.06 |
| profiles_v2 | sonnet46 | state_raw | 96 | 0 | 0 | 95.8 | 95.8 | n/a | 8.65 |
| profiles_v2 | sonnet46_thinking | canonical | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 7.93 |
| profiles_v2 | sonnet46_thinking | raw | 96 | 0 | 0 | 97.9 | 99.0 | n/a | 14.43 |
| profiles_v2 | sonnet46_thinking | snapshot | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 2.62 |
| profiles_v2 | sonnet46_thinking | state_canonical | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 6.99 |
| profiles_v2 | sonnet46_thinking | state_raw | 96 | 0 | 0 | 100.0 | 100.0 | n/a | 14.62 |

| Cohort | Kind | Model | Detail | Metric | Difference [95% CI], pp |
| --- | --- | --- | --- | --- | --- |
| heldout_v2 | interface | GPT-5.4 mini | low raw | future_joint | +19.3 [+11.5, +27.1] |
| heldout_v2 | interface | GPT-5.4 mini | high raw | future_joint | +54.2 [+44.3, +63.5] |
| heldout_v2 | interface | GPT-5.4 mini | low raw | stock_exact | +8.3 [+1.6, +15.1] |
| heldout_v2 | interface | GPT-5.4 mini | high raw | stock_exact | +40.6 [+31.8, +49.5] |
| heldout_v2 | interface | GPT-5.4 mini | low canonical | future_joint | +10.4 [+3.1, +17.7] |
| heldout_v2 | interface | GPT-5.4 mini | high canonical | future_joint | +58.3 [+49.5, +66.7] |
| heldout_v2 | interface | GPT-5.4 mini | low canonical | stock_exact | +3.6 [-1.6, +8.9] |
| heldout_v2 | interface | GPT-5.4 mini | high canonical | stock_exact | +40.6 [+31.8, +49.5] |
| heldout_v2 | interface | GPT-5.4 | low raw | future_joint | +10.4 [+5.2, +16.1] |
| heldout_v2 | interface | GPT-5.4 | high raw | future_joint | +4.7 [+1.0, +8.3] |
| heldout_v2 | interface | GPT-5.4 | low raw | stock_exact | +7.3 [+2.6, +12.5] |
| heldout_v2 | interface | GPT-5.4 | high raw | stock_exact | +2.6 [+0.0, +5.2] |
| heldout_v2 | interface | GPT-5.4 | low canonical | future_joint | +0.0 [-2.6, +2.6] |
| heldout_v2 | interface | GPT-5.4 | high canonical | future_joint | +5.2 [+2.1, +8.9] |
| heldout_v2 | interface | GPT-5.4 | low canonical | stock_exact | -1.0 [-3.1, +1.0] |
| heldout_v2 | interface | GPT-5.4 | high canonical | stock_exact | +1.6 [+0.0, +3.6] |
| heldout_v2 | interface | gpt-oss-20b | low raw | future_joint | +0.5 [-5.7, +6.8] |
| heldout_v2 | interface | gpt-oss-20b | high raw | future_joint | -3.1 [-8.9, +2.1] |
| heldout_v2 | interface | gpt-oss-20b | low raw | stock_exact | +0.5 [-6.2, +7.3] |
| heldout_v2 | interface | gpt-oss-20b | high raw | stock_exact | -1.6 [-6.8, +3.6] |
| heldout_v2 | interface | gpt-oss-20b | low canonical | future_joint | -1.0 [-8.3, +6.2] |
| heldout_v2 | interface | gpt-oss-20b | high canonical | future_joint | -6.8 [-13.5, +0.0] |
| heldout_v2 | interface | gpt-oss-20b | low canonical | stock_exact | +4.2 [-2.1, +10.4] |
| heldout_v2 | interface | gpt-oss-20b | high canonical | stock_exact | -5.7 [-12.5, +1.0] |
| heldout_v2 | interface | gpt-oss-120b | low raw | future_joint | +3.6 [-3.1, +10.4] |
| heldout_v2 | interface | gpt-oss-120b | high raw | future_joint | -4.7 [-8.9, -1.0] |
| heldout_v2 | interface | gpt-oss-120b | low raw | stock_exact | +1.0 [-4.7, +6.8] |
| heldout_v2 | interface | gpt-oss-120b | high raw | stock_exact | -4.7 [-8.9, -1.0] |
| heldout_v2 | interface | gpt-oss-120b | low canonical | future_joint | +4.2 [-3.1, +12.0] |
| heldout_v2 | interface | gpt-oss-120b | high canonical | future_joint | +2.6 [-2.6, +7.8] |
| heldout_v2 | interface | gpt-oss-120b | low canonical | stock_exact | -1.6 [-7.3, +4.2] |
| heldout_v2 | interface | gpt-oss-120b | high canonical | stock_exact | +2.6 [-2.6, +7.8] |
| heldout_v2 | interface | Qwen3.8-27B | low raw | future_joint | +18.8 [+12.5, +25.5] |
| heldout_v2 | interface | Qwen3.8-27B | high raw | future_joint | +8.3 [+1.6, +15.1] |
| heldout_v2 | interface | Qwen3.8-27B | low raw | stock_exact | +18.2 [+12.0, +25.0] |
| heldout_v2 | interface | Qwen3.8-27B | high raw | stock_exact | +6.8 [+0.0, +13.5] |
| heldout_v2 | interface | Qwen3.8-27B | low canonical | future_joint | +7.8 [+4.2, +12.0] |
| heldout_v2 | interface | Qwen3.8-27B | high canonical | future_joint | +1.0 [-4.7, +6.8] |
| heldout_v2 | interface | Qwen3.8-27B | low canonical | stock_exact | +7.8 [+4.2, +12.0] |
| heldout_v2 | interface | Qwen3.8-27B | high canonical | stock_exact | +1.6 [-3.1, +5.7] |
| heldout_v2 | interface | DeepSeek V4 Flash | low raw | future_joint | +96.4 [+93.8, +99.0] |
| heldout_v2 | interface | DeepSeek V4 Flash | high raw | future_joint | +91.7 [+87.0, +95.8] |
| heldout_v2 | interface | DeepSeek V4 Flash | low raw | stock_exact | +92.2 [+88.0, +95.8] |
| heldout_v2 | interface | DeepSeek V4 Flash | high raw | stock_exact | +87.5 [+81.8, +92.7] |
| heldout_v2 | interface | DeepSeek V4 Flash | low canonical | future_joint | +96.9 [+94.3, +99.0] |
| heldout_v2 | interface | DeepSeek V4 Flash | high canonical | future_joint | +96.4 [+93.2, +99.0] |
| heldout_v2 | interface | DeepSeek V4 Flash | low canonical | stock_exact | +91.1 [+87.0, +94.8] |
| heldout_v2 | interface | DeepSeek V4 Flash | high canonical | stock_exact | +94.3 [+90.1, +97.9] |
| heldout_v2 | interface | GLM-5.3 Flash | low raw | future_joint | +3.1 [-6.2, +12.5] |
| heldout_v2 | interface | GLM-5.3 Flash | high raw | future_joint | +2.1 [-5.2, +9.4] |
| heldout_v2 | interface | GLM-5.3 Flash | low raw | stock_exact | -2.1 [-9.4, +4.7] |
| heldout_v2 | interface | GLM-5.3 Flash | high raw | stock_exact | +1.0 [-3.6, +5.7] |
| heldout_v2 | interface | GLM-5.3 Flash | low canonical | future_joint | +1.6 [-6.8, +9.9] |
| heldout_v2 | interface | GLM-5.3 Flash | high canonical | future_joint | +2.1 [-4.7, +8.9] |
| heldout_v2 | interface | GLM-5.3 Flash | low canonical | stock_exact | +1.6 [-5.2, +8.3] |
| heldout_v2 | interface | GLM-5.3 Flash | high canonical | stock_exact | +2.1 [-2.1, +6.2] |
| heldout_v2 | interface | DeepSeek V4 Pro | low raw | future_joint | +2.6 [-0.5, +5.7] |
| heldout_v2 | interface | DeepSeek V4 Pro | high raw | future_joint | +1.6 [-2.6, +5.7] |
| heldout_v2 | interface | DeepSeek V4 Pro | low raw | stock_exact | +3.1 [+0.0, +6.2] |
| heldout_v2 | interface | DeepSeek V4 Pro | high raw | stock_exact | +2.1 [-1.6, +5.7] |
| heldout_v2 | interface | DeepSeek V4 Pro | low canonical | future_joint | +0.5 [-1.6, +2.6] |
| heldout_v2 | interface | DeepSeek V4 Pro | high canonical | future_joint | +15.1 [+9.4, +20.8] |
| heldout_v2 | interface | DeepSeek V4 Pro | low canonical | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | interface | DeepSeek V4 Pro | high canonical | stock_exact | +14.1 [+8.3, +19.8] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->canonical | future_joint | +29.7 [+20.8, +38.5] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->snapshot | future_joint | +38.0 [+28.6, +47.9] |
| heldout_v2 | placement_auto | GPT-5.4 mini | canonical->snapshot | future_joint | +8.3 [+2.1, +15.1] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->state_raw | future_joint | +12.5 [+6.8, +18.8] |
| heldout_v2 | placement_auto | GPT-5.4 mini | canonical->state_canonical | future_joint | +8.3 [+3.6, +13.5] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->canonical | stock_exact | +32.8 [+24.5, +41.1] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->snapshot | stock_exact | +41.1 [+32.3, +49.5] |
| heldout_v2 | placement_auto | GPT-5.4 mini | canonical->snapshot | stock_exact | +8.3 [+4.2, +13.0] |
| heldout_v2 | placement_auto | GPT-5.4 mini | raw->state_raw | stock_exact | +10.4 [+5.2, +16.1] |
| heldout_v2 | placement_auto | GPT-5.4 mini | canonical->state_canonical | stock_exact | +3.1 [-0.5, +7.3] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->canonical | future_joint | +33.3 [+24.0, +43.2] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->snapshot | future_joint | +40.1 [+30.7, +49.0] |
| heldout_v2 | placement_auto | Haiku 4.5 | canonical->snapshot | future_joint | +6.8 [+1.0, +12.5] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->state_raw | future_joint | +8.9 [+0.5, +17.2] |
| heldout_v2 | placement_auto | Haiku 4.5 | canonical->state_canonical | future_joint | +6.8 [+0.0, +13.5] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->canonical | stock_exact | +37.5 [+29.2, +45.8] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->snapshot | stock_exact | +40.6 [+31.8, +49.5] |
| heldout_v2 | placement_auto | Haiku 4.5 | canonical->snapshot | stock_exact | +3.1 [+0.5, +6.2] |
| heldout_v2 | placement_auto | Haiku 4.5 | raw->state_raw | stock_exact | +2.1 [-5.7, +10.4] |
| heldout_v2 | placement_auto | Haiku 4.5 | canonical->state_canonical | stock_exact | -4.2 [-8.3, +0.5] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->canonical | future_joint | +8.3 [+3.1, +14.1] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->snapshot | future_joint | +10.4 [+5.2, +15.6] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | canonical->snapshot | future_joint | +2.1 [-0.5, +5.2] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->state_raw | future_joint | -0.5 [-6.8, +5.7] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | canonical->state_canonical | future_joint | +3.1 [+1.0, +5.7] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->canonical | stock_exact | +9.9 [+5.7, +14.6] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->snapshot | stock_exact | +9.9 [+5.7, +14.6] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | raw->state_raw | stock_exact | -2.1 [-7.8, +3.6] |
| heldout_v2 | placement_auto | Haiku 4.5 + thinking | canonical->state_canonical | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->canonical | future_joint | +27.1 [+19.8, +34.4] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->snapshot | future_joint | +58.9 [+49.0, +68.2] |
| heldout_v2 | placement_auto | gpt-oss-20b | canonical->snapshot | future_joint | +31.8 [+21.4, +42.2] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->state_raw | future_joint | +13.5 [+6.2, +21.4] |
| heldout_v2 | placement_auto | gpt-oss-20b | canonical->state_canonical | future_joint | +20.3 [+12.0, +28.6] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->canonical | stock_exact | +30.7 [+23.4, +38.5] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->snapshot | stock_exact | +68.2 [+60.4, +75.5] |
| heldout_v2 | placement_auto | gpt-oss-20b | canonical->snapshot | stock_exact | +37.5 [+29.2, +46.4] |
| heldout_v2 | placement_auto | gpt-oss-20b | raw->state_raw | stock_exact | +5.7 [-1.6, +13.0] |
| heldout_v2 | placement_auto | gpt-oss-20b | canonical->state_canonical | stock_exact | +8.9 [+0.5, +17.2] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->canonical | future_joint | +24.0 [+16.1, +31.8] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->snapshot | future_joint | +45.3 [+35.9, +54.7] |
| heldout_v2 | placement_auto | gpt-oss-120b | canonical->snapshot | future_joint | +21.4 [+13.5, +29.7] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->state_raw | future_joint | +8.3 [+1.0, +15.6] |
| heldout_v2 | placement_auto | gpt-oss-120b | canonical->state_canonical | future_joint | +2.6 [-4.2, +9.4] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->canonical | stock_exact | +23.4 [+16.1, +30.7] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->snapshot | stock_exact | +44.3 [+35.9, +53.1] |
| heldout_v2 | placement_auto | gpt-oss-120b | canonical->snapshot | stock_exact | +20.8 [+14.1, +28.1] |
| heldout_v2 | placement_auto | gpt-oss-120b | raw->state_raw | stock_exact | +3.1 [-3.6, +9.9] |
| heldout_v2 | placement_auto | gpt-oss-120b | canonical->state_canonical | stock_exact | -2.1 [-7.8, +3.6] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->canonical | future_joint | +4.2 [+1.0, +7.8] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->snapshot | future_joint | +4.7 [+1.6, +8.3] |
| heldout_v2 | placement_auto | Qwen3.8-27B | canonical->snapshot | future_joint | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->state_raw | future_joint | +1.6 [-1.6, +5.2] |
| heldout_v2 | placement_auto | Qwen3.8-27B | canonical->state_canonical | future_joint | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->canonical | stock_exact | +4.2 [+1.0, +7.8] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->snapshot | stock_exact | +4.7 [+1.6, +8.3] |
| heldout_v2 | placement_auto | Qwen3.8-27B | canonical->snapshot | stock_exact | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Qwen3.8-27B | raw->state_raw | stock_exact | +1.6 [-1.6, +5.2] |
| heldout_v2 | placement_auto | Qwen3.8-27B | canonical->state_canonical | stock_exact | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->canonical | future_joint | +0.5 [-1.6, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->snapshot | future_joint | +0.5 [-1.6, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | canonical->snapshot | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->state_raw | future_joint | +1.0 [-1.0, +3.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | canonical->state_canonical | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->canonical | stock_exact | +0.5 [-1.6, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->snapshot | stock_exact | +1.6 [+0.0, +3.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | canonical->snapshot | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | raw->state_raw | stock_exact | +1.0 [-1.0, +3.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Flash | canonical->state_canonical | stock_exact | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->canonical | future_joint | +8.3 [+0.0, +16.7] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->snapshot | future_joint | +3.1 [-6.8, +13.5] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | canonical->snapshot | future_joint | -5.2 [-14.6, +4.7] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->state_raw | future_joint | +21.9 [+13.0, +30.2] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | canonical->state_canonical | future_joint | +22.9 [+15.1, +30.7] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->canonical | stock_exact | +9.9 [+2.6, +17.2] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->snapshot | stock_exact | +24.0 [+17.7, +30.7] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | canonical->snapshot | stock_exact | +14.1 [+8.9, +19.3] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | raw->state_raw | stock_exact | +1.6 [-5.7, +8.9] |
| heldout_v2 | placement_auto | GLM-5.3 Flash | canonical->state_canonical | stock_exact | +1.0 [-4.7, +6.8] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->canonical | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->snapshot | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | canonical->snapshot | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->state_raw | future_joint | -0.5 [-2.1, +1.0] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | canonical->state_canonical | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->canonical | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->snapshot | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | raw->state_raw | stock_exact | -0.5 [-2.1, +1.0] |
| heldout_v2 | placement_auto | DeepSeek V4 Pro | canonical->state_canonical | stock_exact | -1.0 [-2.6, +0.0] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->canonical | future_joint | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->snapshot | future_joint | -7.3 [-12.0, -3.1] |
| heldout_v2 | placement_auto | GPT-5.4 | canonical->snapshot | future_joint | -7.3 [-12.0, -2.6] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->state_raw | future_joint | -1.6 [-4.7, +1.6] |
| heldout_v2 | placement_auto | GPT-5.4 | canonical->state_canonical | future_joint | -14.6 [-21.4, -8.3] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->canonical | stock_exact | +0.0 [-2.1, +2.1] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->snapshot | stock_exact | +1.6 [+0.0, +3.6] |
| heldout_v2 | placement_auto | GPT-5.4 | canonical->snapshot | stock_exact | +1.6 [+0.0, +3.6] |
| heldout_v2 | placement_auto | GPT-5.4 | raw->state_raw | stock_exact | -1.6 [-4.7, +1.6] |
| heldout_v2 | placement_auto | GPT-5.4 | canonical->state_canonical | stock_exact | -14.6 [-21.4, -8.3] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->canonical | future_joint | +0.5 [-1.0, +2.1] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->snapshot | future_joint | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | canonical->snapshot | future_joint | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->state_raw | future_joint | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | canonical->state_canonical | future_joint | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->canonical | stock_exact | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->snapshot | stock_exact | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Sonnet 4.6 | raw->state_raw | stock_exact | +0.5 [+0.0, +1.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 | canonical->state_canonical | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->canonical | future_joint | +2.1 [+0.5, +4.2] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->snapshot | future_joint | +2.1 [+0.5, +4.2] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->snapshot | future_joint | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->state_raw | future_joint | +2.1 [+0.5, +4.2] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->state_canonical | future_joint | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->canonical | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->snapshot | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | raw->state_raw | stock_exact | +1.0 [+0.0, +2.6] |
| heldout_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->state_canonical | stock_exact | +0.0 [+0.0, +0.0] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | forced raw | future_joint | -12.5 [-21.9, -3.1] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | auto raw | future_joint | +22.4 [+14.1, +30.7] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | forced raw | stock_exact | -8.9 [-18.2, +0.0] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | auto raw | stock_exact | +23.4 [+15.6, +31.2] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | forced canonical | future_joint | -41.1 [-51.0, -31.2] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | auto canonical | future_joint | +6.8 [+0.5, +13.5] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | forced canonical | stock_exact | -31.8 [-40.6, -22.9] |
| heldout_v2 | effort_by_interface | GPT-5.4 mini | auto canonical | stock_exact | +5.2 [+0.5, +10.4] |
| heldout_v2 | effort_by_interface | GPT-5.4 | forced raw | future_joint | +6.2 [+0.0, +12.5] |
| heldout_v2 | effort_by_interface | GPT-5.4 | auto raw | future_joint | +0.5 [-1.6, +2.6] |
| heldout_v2 | effort_by_interface | GPT-5.4 | forced raw | stock_exact | +5.7 [+0.5, +11.5] |
| heldout_v2 | effort_by_interface | GPT-5.4 | auto raw | stock_exact | +1.0 [-1.0, +3.1] |
| heldout_v2 | effort_by_interface | GPT-5.4 | forced canonical | future_joint | -3.6 [-7.8, +0.0] |
| heldout_v2 | effort_by_interface | GPT-5.4 | auto canonical | future_joint | +1.6 [+0.0, +3.6] |
| heldout_v2 | effort_by_interface | GPT-5.4 | forced canonical | stock_exact | -1.0 [-3.1, +1.0] |
| heldout_v2 | effort_by_interface | GPT-5.4 | auto canonical | stock_exact | +1.6 [+0.0, +3.6] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | forced raw | future_joint | +18.8 [+11.5, +26.0] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | auto raw | future_joint | +15.1 [+8.3, +21.9] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | forced raw | stock_exact | +10.9 [+4.2, +17.7] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | auto raw | stock_exact | +8.9 [+2.1, +15.6] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | forced canonical | future_joint | +14.1 [+5.7, +22.9] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | auto canonical | future_joint | +8.3 [+0.0, +16.7] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | forced canonical | stock_exact | +7.8 [-1.0, +16.7] |
| heldout_v2 | effort_by_interface | gpt-oss-20b | auto canonical | stock_exact | -2.1 [-9.4, +5.2] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | forced raw | future_joint | +7.8 [+0.5, +15.6] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | auto raw | future_joint | -0.5 [-8.3, +7.3] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | forced raw | stock_exact | +0.0 [-7.3, +7.3] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | auto raw | stock_exact | -5.7 [-13.0, +2.1] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | forced canonical | future_joint | -3.1 [-9.4, +3.1] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | auto canonical | future_joint | -4.7 [-12.0, +2.1] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | forced canonical | stock_exact | -13.5 [-20.3, -7.3] |
| heldout_v2 | effort_by_interface | gpt-oss-120b | auto canonical | stock_exact | -9.4 [-16.7, -2.6] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | forced raw | future_joint | +3.6 [-4.7, +12.0] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | auto raw | future_joint | -6.8 [-12.0, -1.6] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | forced raw | stock_exact | +4.7 [-3.6, +13.0] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | auto raw | stock_exact | -6.8 [-12.0, -1.6] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | forced canonical | future_joint | +0.0 [-5.7, +5.7] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | auto canonical | future_joint | -6.8 [-10.4, -3.1] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | forced canonical | stock_exact | +2.6 [-2.6, +7.8] |
| heldout_v2 | effort_by_interface | Qwen3.8-27B | auto canonical | stock_exact | -3.6 [-6.8, -1.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | forced raw | future_joint | -0.5 [-3.1, +2.1] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | auto raw | future_joint | -5.2 [-9.9, -1.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | forced raw | stock_exact | +0.5 [-2.6, +4.2] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | auto raw | stock_exact | -4.2 [-8.9, +0.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | forced canonical | future_joint | -1.0 [-3.6, +1.6] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | auto canonical | future_joint | -1.6 [-4.7, +1.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | forced canonical | stock_exact | -4.2 [-7.8, -0.5] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Flash | auto canonical | stock_exact | -1.0 [-4.2, +1.6] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | forced raw | future_joint | +21.9 [+12.5, +31.2] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | auto raw | future_joint | +20.8 [+12.5, +29.2] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | forced raw | stock_exact | +13.0 [+5.7, +20.3] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | auto raw | stock_exact | +16.1 [+9.9, +22.9] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | forced canonical | future_joint | +19.8 [+12.0, +27.6] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | auto canonical | future_joint | +20.3 [+13.0, +28.1] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | forced canonical | stock_exact | +9.4 [+3.6, +15.1] |
| heldout_v2 | effort_by_interface | GLM-5.3 Flash | auto canonical | stock_exact | +9.9 [+5.2, +15.1] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | forced raw | future_joint | -4.7 [-8.3, -1.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | auto raw | future_joint | -5.7 [-10.4, -2.1] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | forced raw | stock_exact | -4.2 [-8.3, +0.0] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | auto raw | stock_exact | -5.2 [-9.9, -1.6] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | forced canonical | future_joint | -16.1 [-21.4, -10.9] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | auto canonical | future_joint | -1.6 [-4.2, +0.5] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | forced canonical | stock_exact | -15.6 [-20.8, -10.9] |
| heldout_v2 | effort_by_interface | DeepSeek V4 Pro | auto canonical | stock_exact | -2.6 [-5.2, -0.5] |
| heldout_v2 | interaction | GPT-5.4 mini | raw | future_joint | +34.9 [+22.4, +46.9] |
| heldout_v2 | interaction | GPT-5.4 mini | raw | stock_exact | +32.3 [+20.8, +43.8] |
| heldout_v2 | interaction | GPT-5.4 mini | canonical | future_joint | +47.9 [+35.9, +59.9] |
| heldout_v2 | interaction | GPT-5.4 mini | canonical | stock_exact | +37.0 [+26.6, +47.4] |
| heldout_v2 | interaction | GPT-5.4 | raw | future_joint | -5.7 [-12.5, +1.0] |
| heldout_v2 | interaction | GPT-5.4 | raw | stock_exact | -4.7 [-10.9, +1.0] |
| heldout_v2 | interaction | GPT-5.4 | canonical | future_joint | +5.2 [+1.0, +9.4] |
| heldout_v2 | interaction | GPT-5.4 | canonical | stock_exact | +2.6 [+0.0, +5.2] |
| heldout_v2 | interaction | gpt-oss-20b | raw | future_joint | -3.6 [-12.0, +4.7] |
| heldout_v2 | interaction | gpt-oss-20b | raw | stock_exact | -2.1 [-10.9, +6.2] |
| heldout_v2 | interaction | gpt-oss-20b | canonical | future_joint | -5.7 [-15.6, +4.2] |
| heldout_v2 | interaction | gpt-oss-20b | canonical | stock_exact | -9.9 [-18.8, -1.0] |
| heldout_v2 | interaction | gpt-oss-120b | raw | future_joint | -8.3 [-16.7, -0.5] |
| heldout_v2 | interaction | gpt-oss-120b | raw | stock_exact | -5.7 [-13.5, +1.6] |
| heldout_v2 | interaction | gpt-oss-120b | canonical | future_joint | -1.6 [-10.4, +6.8] |
| heldout_v2 | interaction | gpt-oss-120b | canonical | stock_exact | +4.2 [-3.6, +12.0] |
| heldout_v2 | interaction | Qwen3.8-27B | raw | future_joint | -10.4 [-20.3, -0.5] |
| heldout_v2 | interaction | Qwen3.8-27B | raw | stock_exact | -11.5 [-20.8, -2.1] |
| heldout_v2 | interaction | Qwen3.8-27B | canonical | future_joint | -6.8 [-14.1, +0.5] |
| heldout_v2 | interaction | Qwen3.8-27B | canonical | stock_exact | -6.2 [-12.5, +0.0] |
| heldout_v2 | interaction | DeepSeek V4 Flash | raw | future_joint | -4.7 [-9.9, +0.5] |
| heldout_v2 | interaction | DeepSeek V4 Flash | raw | stock_exact | -4.7 [-10.4, +1.0] |
| heldout_v2 | interaction | DeepSeek V4 Flash | canonical | future_joint | -0.5 [-4.7, +3.1] |
| heldout_v2 | interaction | DeepSeek V4 Flash | canonical | stock_exact | +3.1 [-1.6, +7.8] |
| heldout_v2 | interaction | GLM-5.3 Flash | raw | future_joint | -1.0 [-13.0, +10.9] |
| heldout_v2 | interaction | GLM-5.3 Flash | raw | stock_exact | +3.1 [-5.2, +12.0] |
| heldout_v2 | interaction | GLM-5.3 Flash | canonical | future_joint | +0.5 [-9.9, +11.5] |
| heldout_v2 | interaction | GLM-5.3 Flash | canonical | stock_exact | +0.5 [-7.3, +8.3] |
| heldout_v2 | interaction | DeepSeek V4 Pro | raw | future_joint | -1.0 [-6.2, +3.6] |
| heldout_v2 | interaction | DeepSeek V4 Pro | raw | stock_exact | -1.0 [-6.2, +3.6] |
| heldout_v2 | interaction | DeepSeek V4 Pro | canonical | future_joint | +14.6 [+8.3, +20.8] |
| heldout_v2 | interaction | DeepSeek V4 Pro | canonical | stock_exact | +13.0 [+7.3, +18.8] |
| profiles_v2 | interface | GPT-5.4 mini | low raw | future_joint | +2.1 [-6.2, +11.5] |
| profiles_v2 | interface | GPT-5.4 mini | high raw | future_joint | +28.1 [+15.6, +39.6] |
| profiles_v2 | interface | GPT-5.4 mini | low raw | stock_exact | +4.2 [-4.2, +13.5] |
| profiles_v2 | interface | GPT-5.4 mini | high raw | stock_exact | +18.8 [+7.3, +30.2] |
| profiles_v2 | interface | GPT-5.4 mini | low canonical | future_joint | +35.4 [+22.9, +47.9] |
| profiles_v2 | interface | GPT-5.4 mini | high canonical | future_joint | +65.6 [+55.2, +75.0] |
| profiles_v2 | interface | GPT-5.4 mini | low canonical | stock_exact | +2.1 [-6.2, +10.4] |
| profiles_v2 | interface | GPT-5.4 mini | high canonical | stock_exact | +61.5 [+50.0, +71.9] |
| profiles_v2 | interface | GPT-5.4 | low raw | future_joint | +7.3 [+3.1, +12.5] |
| profiles_v2 | interface | GPT-5.4 | high raw | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | interface | GPT-5.4 | low raw | stock_exact | +7.3 [+3.1, +12.5] |
| profiles_v2 | interface | GPT-5.4 | high raw | stock_exact | +1.0 [+0.0, +3.1] |
| profiles_v2 | interface | GPT-5.4 | low canonical | future_joint | +8.3 [+3.1, +13.5] |
| profiles_v2 | interface | GPT-5.4 | high canonical | future_joint | +11.5 [+6.2, +17.7] |
| profiles_v2 | interface | GPT-5.4 | low canonical | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | interface | GPT-5.4 | high canonical | stock_exact | +9.4 [+4.2, +15.6] |
| profiles_v2 | interface | gpt-oss-20b | low raw | future_joint | -1.0 [-3.1, +0.0] |
| profiles_v2 | interface | gpt-oss-20b | high raw | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | interface | gpt-oss-20b | low raw | stock_exact | -1.0 [-7.3, +4.2] |
| profiles_v2 | interface | gpt-oss-20b | high raw | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | interface | gpt-oss-20b | low canonical | future_joint | +6.2 [-3.1, +15.6] |
| profiles_v2 | interface | gpt-oss-20b | high canonical | future_joint | -1.0 [-14.6, +12.5] |
| profiles_v2 | interface | gpt-oss-20b | low canonical | stock_exact | +2.1 [-8.3, +12.5] |
| profiles_v2 | interface | gpt-oss-20b | high canonical | stock_exact | +0.0 [-13.5, +13.5] |
| profiles_v2 | interface | gpt-oss-120b | low raw | future_joint | -2.1 [-8.3, +3.1] |
| profiles_v2 | interface | gpt-oss-120b | high raw | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | interface | gpt-oss-120b | low raw | stock_exact | -7.3 [-13.6, -1.0] |
| profiles_v2 | interface | gpt-oss-120b | high raw | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | interface | gpt-oss-120b | low canonical | future_joint | -3.1 [-14.6, +9.4] |
| profiles_v2 | interface | gpt-oss-120b | high canonical | future_joint | -1.0 [-10.4, +8.3] |
| profiles_v2 | interface | gpt-oss-120b | low canonical | stock_exact | -2.1 [-11.5, +8.3] |
| profiles_v2 | interface | gpt-oss-120b | high canonical | stock_exact | -1.0 [-10.4, +8.3] |
| profiles_v2 | interface | DeepSeek V4 Flash | low raw | future_joint | +94.8 [+88.5, +99.0] |
| profiles_v2 | interface | DeepSeek V4 Flash | high raw | future_joint | +93.8 [+87.5, +99.0] |
| profiles_v2 | interface | DeepSeek V4 Flash | low raw | stock_exact | +87.5 [+79.2, +94.8] |
| profiles_v2 | interface | DeepSeek V4 Flash | high raw | stock_exact | +89.6 [+80.2, +96.9] |
| profiles_v2 | interface | DeepSeek V4 Flash | low canonical | future_joint | +95.8 [+91.7, +99.0] |
| profiles_v2 | interface | DeepSeek V4 Flash | high canonical | future_joint | +97.9 [+94.8, +100.0] |
| profiles_v2 | interface | DeepSeek V4 Flash | low canonical | stock_exact | +87.5 [+79.2, +94.8] |
| profiles_v2 | interface | DeepSeek V4 Flash | high canonical | stock_exact | +88.5 [+80.2, +95.8] |
| profiles_v2 | interface | GLM-5.3 Flash | low raw | future_joint | -5.2 [-18.8, +8.3] |
| profiles_v2 | interface | GLM-5.3 Flash | high raw | future_joint | +0.0 [-11.5, +11.5] |
| profiles_v2 | interface | GLM-5.3 Flash | low raw | stock_exact | -2.1 [-15.6, +11.5] |
| profiles_v2 | interface | GLM-5.3 Flash | high raw | stock_exact | -3.1 [-11.5, +5.2] |
| profiles_v2 | interface | GLM-5.3 Flash | low canonical | future_joint | -6.2 [-20.8, +7.3] |
| profiles_v2 | interface | GLM-5.3 Flash | high canonical | future_joint | +1.0 [-8.3, +10.4] |
| profiles_v2 | interface | GLM-5.3 Flash | low canonical | stock_exact | -3.1 [-12.5, +5.2] |
| profiles_v2 | interface | GLM-5.3 Flash | high canonical | stock_exact | +0.0 [-6.2, +6.2] |
| profiles_v2 | interface | DeepSeek V4 Pro | low raw | future_joint | +4.2 [-3.1, +11.5] |
| profiles_v2 | interface | DeepSeek V4 Pro | high raw | future_joint | +17.7 [+9.4, +26.0] |
| profiles_v2 | interface | DeepSeek V4 Pro | low raw | stock_exact | +6.2 [+0.0, +12.5] |
| profiles_v2 | interface | DeepSeek V4 Pro | high raw | stock_exact | +17.7 [+9.4, +26.0] |
| profiles_v2 | interface | DeepSeek V4 Pro | low canonical | future_joint | +3.1 [+0.0, +7.3] |
| profiles_v2 | interface | DeepSeek V4 Pro | high canonical | future_joint | +21.9 [+14.6, +29.2] |
| profiles_v2 | interface | DeepSeek V4 Pro | low canonical | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | interface | DeepSeek V4 Pro | high canonical | stock_exact | +21.9 [+14.6, +29.2] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->canonical | future_joint | +67.7 [+56.2, +78.2] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->snapshot | future_joint | +75.0 [+64.6, +85.4] |
| profiles_v2 | placement_auto | GPT-5.4 mini | canonical->snapshot | future_joint | +7.3 [-4.2, +18.8] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->state_raw | future_joint | +5.2 [-6.2, +15.6] |
| profiles_v2 | placement_auto | GPT-5.4 mini | canonical->state_canonical | future_joint | +12.5 [+3.1, +20.8] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->canonical | stock_exact | +74.0 [+64.6, +83.3] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->snapshot | stock_exact | +81.2 [+71.9, +89.6] |
| profiles_v2 | placement_auto | GPT-5.4 mini | canonical->snapshot | stock_exact | +7.3 [+3.1, +12.5] |
| profiles_v2 | placement_auto | GPT-5.4 mini | raw->state_raw | stock_exact | +1.0 [-10.4, +12.5] |
| profiles_v2 | placement_auto | GPT-5.4 mini | canonical->state_canonical | stock_exact | +2.1 [-4.2, +8.3] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->canonical | future_joint | +83.3 [+74.0, +91.7] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->snapshot | future_joint | +86.5 [+79.2, +92.7] |
| profiles_v2 | placement_auto | Haiku 4.5 | canonical->snapshot | future_joint | +3.1 [-3.1, +9.4] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->state_raw | future_joint | +0.0 [-6.2, +6.2] |
| profiles_v2 | placement_auto | Haiku 4.5 | canonical->state_canonical | future_joint | +5.2 [-2.1, +12.5] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->canonical | stock_exact | +89.6 [+81.2, +95.8] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->snapshot | stock_exact | +92.7 [+85.4, +97.9] |
| profiles_v2 | placement_auto | Haiku 4.5 | canonical->snapshot | stock_exact | +3.1 [+0.0, +7.3] |
| profiles_v2 | placement_auto | Haiku 4.5 | raw->state_raw | stock_exact | -1.0 [-7.3, +5.2] |
| profiles_v2 | placement_auto | Haiku 4.5 | canonical->state_canonical | stock_exact | -2.1 [-7.3, +3.1] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->canonical | future_joint | +51.0 [+39.6, +62.5] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->snapshot | future_joint | +56.2 [+46.9, +65.6] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | canonical->snapshot | future_joint | +5.2 [-2.1, +13.5] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->state_raw | future_joint | +18.8 [+3.1, +33.3] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | canonical->state_canonical | future_joint | +7.3 [+1.0, +15.6] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->canonical | stock_exact | +57.3 [+47.9, +66.7] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->snapshot | stock_exact | +58.3 [+50.0, +66.7] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | canonical->snapshot | stock_exact | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | raw->state_raw | stock_exact | +17.7 [+2.1, +32.3] |
| profiles_v2 | placement_auto | Haiku 4.5 + thinking | canonical->state_canonical | stock_exact | +0.0 [-3.1, +3.1] |
| profiles_v2 | placement_auto | gpt-oss-20b | raw->canonical | future_joint | +17.7 [+10.4, +25.0] |
| profiles_v2 | placement_auto | gpt-oss-20b | raw->snapshot | future_joint | +77.1 [+68.8, +85.4] |
| profiles_v2 | placement_auto | gpt-oss-20b | canonical->snapshot | future_joint | +59.4 [+47.9, +70.8] |
| profiles_v2 | placement_auto | gpt-oss-20b | raw->canonical | stock_exact | +17.7 [+10.4, +25.0] |
| profiles_v2 | placement_auto | gpt-oss-20b | raw->snapshot | stock_exact | +95.8 [+90.6, +100.0] |
| profiles_v2 | placement_auto | gpt-oss-20b | canonical->snapshot | stock_exact | +78.1 [+68.8, +86.5] |
| profiles_v2 | placement_auto | gpt-oss-120b | raw->canonical | future_joint | +67.7 [+58.3, +77.1] |
| profiles_v2 | placement_auto | gpt-oss-120b | raw->snapshot | future_joint | +81.2 [+71.9, +89.6] |
| profiles_v2 | placement_auto | gpt-oss-120b | canonical->snapshot | future_joint | +13.5 [+3.1, +22.9] |
| profiles_v2 | placement_auto | gpt-oss-120b | raw->canonical | stock_exact | +72.9 [+63.5, +82.3] |
| profiles_v2 | placement_auto | gpt-oss-120b | raw->snapshot | stock_exact | +87.5 [+80.2, +93.8] |
| profiles_v2 | placement_auto | gpt-oss-120b | canonical->snapshot | stock_exact | +14.6 [+6.2, +22.9] |
| profiles_v2 | placement_auto | Qwen3.8-27B | raw->canonical | future_joint | +2.1 [-2.1, +6.2] |
| profiles_v2 | placement_auto | Qwen3.8-27B | raw->snapshot | future_joint | +3.1 [+0.0, +7.3] |
| profiles_v2 | placement_auto | Qwen3.8-27B | canonical->snapshot | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Qwen3.8-27B | raw->canonical | stock_exact | +3.1 [+0.0, +7.3] |
| profiles_v2 | placement_auto | Qwen3.8-27B | raw->snapshot | stock_exact | +3.1 [+0.0, +7.3] |
| profiles_v2 | placement_auto | Qwen3.8-27B | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | raw->canonical | future_joint | +2.1 [-4.2, +9.4] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | raw->snapshot | future_joint | +4.2 [+0.0, +9.4] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | canonical->snapshot | future_joint | +2.1 [-2.1, +6.2] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | raw->canonical | stock_exact | +3.1 [-2.1, +9.4] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | raw->snapshot | stock_exact | +5.2 [+1.0, +11.5] |
| profiles_v2 | placement_auto | DeepSeek V4 Flash | canonical->snapshot | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | raw->canonical | future_joint | +32.3 [+18.8, +45.8] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | raw->snapshot | future_joint | +12.5 [-2.1, +27.1] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | canonical->snapshot | future_joint | -19.8 [-32.3, -6.2] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | raw->canonical | stock_exact | +36.5 [+22.9, +50.0] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | raw->snapshot | stock_exact | +49.0 [+37.5, +60.4] |
| profiles_v2 | placement_auto | GLM-5.3 Flash | canonical->snapshot | stock_exact | +12.5 [+5.2, +20.8] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | raw->canonical | future_joint | +4.2 [+1.0, +8.3] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | raw->snapshot | future_joint | +0.0 [-6.2, +6.2] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | canonical->snapshot | future_joint | -4.2 [-8.3, -1.0] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | raw->canonical | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | raw->snapshot | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | DeepSeek V4 Pro | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->canonical | future_joint | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->snapshot | future_joint | -8.3 [-15.6, -1.0] |
| profiles_v2 | placement_auto | GPT-5.4 | canonical->snapshot | future_joint | -10.4 [-17.7, -4.2] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->state_raw | future_joint | -2.1 [-6.2, +2.1] |
| profiles_v2 | placement_auto | GPT-5.4 | canonical->state_canonical | future_joint | -8.3 [-13.5, -3.1] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->canonical | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->snapshot | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | placement_auto | GPT-5.4 | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | GPT-5.4 | raw->state_raw | stock_exact | -2.1 [-6.2, +2.1] |
| profiles_v2 | placement_auto | GPT-5.4 | canonical->state_canonical | stock_exact | -8.3 [-13.5, -3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->canonical | future_joint | +3.1 [+0.0, +8.3] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->snapshot | future_joint | +4.2 [+0.0, +9.4] |
| profiles_v2 | placement_auto | Sonnet 4.6 | canonical->snapshot | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->state_raw | future_joint | +0.0 [-3.1, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 | canonical->state_canonical | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->canonical | stock_exact | +3.1 [+0.0, +8.3] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->snapshot | stock_exact | +3.1 [+0.0, +8.3] |
| profiles_v2 | placement_auto | Sonnet 4.6 | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 | raw->state_raw | stock_exact | -1.0 [-3.1, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 | canonical->state_canonical | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->canonical | future_joint | +2.1 [+0.0, +6.2] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->snapshot | future_joint | +2.1 [+0.0, +6.2] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->snapshot | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->state_raw | future_joint | +2.1 [+0.0, +6.2] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->state_canonical | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->canonical | stock_exact | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->snapshot | stock_exact | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->snapshot | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | raw->state_raw | stock_exact | +1.0 [+0.0, +3.1] |
| profiles_v2 | placement_auto | Sonnet 4.6 + thinking | canonical->state_canonical | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | forced raw | future_joint | +8.3 [-1.0, +17.7] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | auto raw | future_joint | +34.4 [+21.9, +46.9] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | forced raw | stock_exact | +15.6 [+6.2, +25.0] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | auto raw | stock_exact | +30.2 [+18.8, +41.7] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | forced canonical | future_joint | -17.7 [-30.2, -5.2] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | auto canonical | future_joint | +12.5 [+4.2, +19.8] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | forced canonical | stock_exact | -55.2 [-65.6, -44.8] |
| profiles_v2 | effort_by_interface | GPT-5.4 mini | auto canonical | stock_exact | +4.2 [-2.1, +10.4] |
| profiles_v2 | effort_by_interface | GPT-5.4 | forced raw | future_joint | +8.3 [+2.1, +14.6] |
| profiles_v2 | effort_by_interface | GPT-5.4 | auto raw | future_joint | +2.1 [+0.0, +5.2] |
| profiles_v2 | effort_by_interface | GPT-5.4 | forced raw | stock_exact | +8.3 [+2.1, +14.6] |
| profiles_v2 | effort_by_interface | GPT-5.4 | auto raw | stock_exact | +2.1 [+0.0, +5.2] |
| profiles_v2 | effort_by_interface | GPT-5.4 | forced canonical | future_joint | -3.1 [-10.4, +4.2] |
| profiles_v2 | effort_by_interface | GPT-5.4 | auto canonical | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort_by_interface | GPT-5.4 | forced canonical | stock_exact | -9.4 [-15.6, -4.2] |
| profiles_v2 | effort_by_interface | GPT-5.4 | auto canonical | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | forced raw | future_joint | -1.0 [-3.1, +0.0] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | auto raw | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | forced raw | stock_exact | -3.1 [-8.3, +0.0] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | auto raw | stock_exact | -2.1 [-5.2, +0.0] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | forced canonical | future_joint | +36.5 [+25.0, +46.9] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | auto canonical | future_joint | +29.2 [+17.7, +40.6] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | forced canonical | stock_exact | +30.2 [+18.8, +41.7] |
| profiles_v2 | effort_by_interface | gpt-oss-20b | auto canonical | stock_exact | +28.1 [+15.6, +40.6] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | forced raw | future_joint | -7.3 [-13.5, -2.1] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | auto raw | future_joint | -5.2 [-10.4, -1.0] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | forced raw | stock_exact | -17.7 [-27.1, -9.4] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | auto raw | stock_exact | -10.4 [-16.7, -5.2] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | forced canonical | future_joint | -64.6 [-76.0, -53.1] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | auto canonical | future_joint | -62.5 [-74.0, -51.0] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | forced canonical | stock_exact | -74.0 [-83.3, -64.6] |
| profiles_v2 | effort_by_interface | gpt-oss-120b | auto canonical | stock_exact | -72.9 [-83.3, -61.5] |
| profiles_v2 | effort_by_interface | Qwen3.8-27B | auto raw | future_joint | +1.0 [-3.1, +5.2] |
| profiles_v2 | effort_by_interface | Qwen3.8-27B | auto raw | stock_exact | +1.0 [-3.1, +5.2] |
| profiles_v2 | effort_by_interface | Qwen3.8-27B | auto canonical | future_joint | -2.1 [-6.2, +2.1] |
| profiles_v2 | effort_by_interface | Qwen3.8-27B | auto canonical | stock_exact | -1.0 [-3.1, +0.0] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | forced raw | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | auto raw | future_joint | +0.0 [-6.2, +6.2] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | forced raw | stock_exact | -2.1 [-7.3, +3.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | auto raw | stock_exact | +0.0 [-6.2, +6.2] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | forced canonical | future_joint | +0.0 [-3.1, +3.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | auto canonical | future_joint | +2.1 [-2.1, +6.2] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | forced canonical | stock_exact | +0.0 [-6.2, +5.2] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Flash | auto canonical | stock_exact | +1.0 [-2.1, +5.2] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | forced raw | future_joint | +39.6 [+22.9, +55.2] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | auto raw | future_joint | +44.8 [+32.3, +57.3] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | forced raw | stock_exact | +34.4 [+19.8, +49.0] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | auto raw | stock_exact | +33.3 [+19.8, +45.8] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | forced canonical | future_joint | +18.8 [+6.2, +31.2] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | auto canonical | future_joint | +26.0 [+15.6, +37.5] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | forced canonical | stock_exact | +4.2 [-4.2, +12.5] |
| profiles_v2 | effort_by_interface | GLM-5.3 Flash | auto canonical | stock_exact | +7.3 [-1.0, +16.7] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | forced raw | future_joint | -12.5 [-22.9, -2.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | auto raw | future_joint | +1.0 [-2.1, +4.2] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | forced raw | stock_exact | -12.5 [-22.9, -2.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | auto raw | stock_exact | -1.0 [-4.2, +2.1] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | forced canonical | future_joint | -18.8 [-27.1, -10.4] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | auto canonical | future_joint | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | forced canonical | stock_exact | -19.8 [-28.1, -11.5] |
| profiles_v2 | effort_by_interface | DeepSeek V4 Pro | auto canonical | stock_exact | +0.0 [+0.0, +0.0] |
| profiles_v2 | interaction | GPT-5.4 mini | raw | future_joint | +26.0 [+10.4, +40.6] |
| profiles_v2 | interaction | GPT-5.4 mini | raw | stock_exact | +14.6 [-1.0, +29.2] |
| profiles_v2 | interaction | GPT-5.4 mini | canonical | future_joint | +30.2 [+14.6, +44.8] |
| profiles_v2 | interaction | GPT-5.4 mini | canonical | stock_exact | +59.4 [+46.9, +71.9] |
| profiles_v2 | interaction | GPT-5.4 | raw | future_joint | -6.2 [-11.5, -1.0] |
| profiles_v2 | interaction | GPT-5.4 | raw | stock_exact | -6.2 [-11.5, -1.0] |
| profiles_v2 | interaction | GPT-5.4 | canonical | future_joint | +3.1 [-4.2, +10.4] |
| profiles_v2 | interaction | GPT-5.4 | canonical | stock_exact | +9.4 [+4.2, +15.6] |
| profiles_v2 | interaction | gpt-oss-20b | raw | future_joint | +1.0 [+0.0, +3.1] |
| profiles_v2 | interaction | gpt-oss-20b | raw | stock_exact | +1.0 [-4.2, +7.3] |
| profiles_v2 | interaction | gpt-oss-20b | canonical | future_joint | -7.3 [-24.0, +10.4] |
| profiles_v2 | interaction | gpt-oss-20b | canonical | stock_exact | -2.1 [-20.8, +17.7] |
| profiles_v2 | interaction | gpt-oss-120b | raw | future_joint | +2.1 [-3.1, +8.3] |
| profiles_v2 | interaction | gpt-oss-120b | raw | stock_exact | +7.3 [+1.0, +13.6] |
| profiles_v2 | interaction | gpt-oss-120b | canonical | future_joint | +2.1 [-13.5, +18.8] |
| profiles_v2 | interaction | gpt-oss-120b | canonical | stock_exact | +1.0 [-13.5, +16.7] |
| profiles_v2 | interaction | DeepSeek V4 Flash | raw | future_joint | -1.0 [-7.3, +5.2] |
| profiles_v2 | interaction | DeepSeek V4 Flash | raw | stock_exact | +2.1 [-4.2, +9.4] |
| profiles_v2 | interaction | DeepSeek V4 Flash | canonical | future_joint | +2.1 [-3.1, +7.3] |
| profiles_v2 | interaction | DeepSeek V4 Flash | canonical | stock_exact | +1.0 [-4.2, +7.3] |
| profiles_v2 | interaction | GLM-5.3 Flash | raw | future_joint | +5.2 [-13.5, +22.9] |
| profiles_v2 | interaction | GLM-5.3 Flash | raw | stock_exact | -1.0 [-18.8, +16.7] |
| profiles_v2 | interaction | GLM-5.3 Flash | canonical | future_joint | +7.3 [-8.3, +22.9] |
| profiles_v2 | interaction | GLM-5.3 Flash | canonical | stock_exact | +3.1 [-7.3, +14.6] |
| profiles_v2 | interaction | DeepSeek V4 Pro | raw | future_joint | +13.5 [+3.1, +24.0] |
| profiles_v2 | interaction | DeepSeek V4 Pro | raw | stock_exact | +11.5 [+1.0, +21.9] |
| profiles_v2 | interaction | DeepSeek V4 Pro | canonical | future_joint | +18.8 [+10.4, +27.1] |
| profiles_v2 | interaction | DeepSeek V4 Pro | canonical | stock_exact | +19.8 [+11.5, +28.1] |

## Transport

{
  "auto_mini_synthetic_v2": {
    "episodes": 576,
    "transport_attempts": {
      "1": 576
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "auto_mini_high_synthetic_v2": {
    "episodes": 192,
    "transport_attempts": {
      "1": 192
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "auto_gpt54_synthetic_v1": {
    "episodes": 960,
    "transport_attempts": {
      "1": 960
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "auto_gpt54_high_synthetic_v1": {
    "episodes": 384,
    "transport_attempts": {
      "1": 384
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "auto_profiles_v1": {
    "episodes": 960,
    "transport_attempts": {
      "1": 960
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "auto_high_profiles_v1": {
    "episodes": 384,
    "transport_attempts": {
      "1": 384
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "haiku_synthetic_v1": {
    "episodes": 1920,
    "transport_attempts": {
      "1": 1920
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "haiku_profiles_v1": {
    "episodes": 960,
    "transport_attempts": {
      "1": 960
    },
    "served_provider_counts": {},
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_synthetic_low_auto_v3": {
    "episodes": 5760,
    "transport_attempts": {
      "1": 5731,
      "2": 24,
      "3": 5
    },
    "served_provider_counts": {
      "Baidu": 1920,
      "Fireworks": 960,
      "Cerebras": 960,
      "Groq": 960,
      "AkashML": 960
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_synthetic_high_auto_v2": {
    "episodes": 2304,
    "transport_attempts": {
      "1": 2249,
      "2": 25,
      "3": 17,
      "4": 4,
      "5": 5,
      "6": 1,
      "7": 3
    },
    "served_provider_counts": {
      "Baidu": 768,
      "Fireworks": 384,
      "Cerebras": 384,
      "Groq": 384,
      "AkashML": 384
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_synthetic_forced_v1": {
    "episodes": 4608,
    "transport_attempts": {
      "1": 4512,
      "2": 51,
      "3": 14,
      "4": 9,
      "5": 3,
      "6": 3,
      "7": 14,
      "8": 2
    },
    "served_provider_counts": {
      "Baidu": 1536,
      "Fireworks": 768,
      "Cerebras": 768,
      "Groq": 768,
      "AkashML": 768
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_profiles_low_auto_v1": {
    "episodes": 1728,
    "transport_attempts": {
      "1": 1533,
      "2": 11,
      "3": 16,
      "5": 6,
      "6": 105,
      "7": 26,
      "8": 31
    },
    "served_provider_counts": {
      "Baidu": 576,
      "Fireworks": 288,
      "Cerebras": 288,
      "Groq": 288,
      "AkashML": 288
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_profiles_high_auto_v1": {
    "episodes": 1152,
    "transport_attempts": {
      "1": 1032,
      "2": 48,
      "3": 29,
      "4": 20,
      "5": 6,
      "6": 7,
      "7": 4,
      "8": 6
    },
    "served_provider_counts": {
      "Baidu": 384,
      "Fireworks": 192,
      "Cerebras": 192,
      "Groq": 192,
      "AkashML": 192
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  },
  "open_profiles_forced_v2": {
    "episodes": 1920,
    "transport_attempts": {
      "1": 1778,
      "2": 73,
      "3": 33,
      "4": 26,
      "5": 5,
      "6": 4,
      "8": 1
    },
    "served_provider_counts": {
      "Baidu": 768,
      "Fireworks": 384,
      "Cerebras": 384,
      "Groq": 384
    },
    "served_provider_mismatches": 0,
    "no_completion_no_provider": 0
  }
}
