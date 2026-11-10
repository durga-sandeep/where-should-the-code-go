# Extension studies: independent analysis

- Every response reparsed; truth recomputed with the independent auditor replay; hybrid answers rebuilt with a separate scenario simulator.
- Hybrid future-joint accuracy equals state-only starting-stock accuracy by conservation; verified on every valid hybrid answer.
- Extension tasks are byte-identical to the archived heldout cohorts; they add configurations and arms, not independent histories.
- Requested reasoning effort is a provider setting; reported reasoning tokens are provider usage fields, not a compute match.
- Tool arms count code_interpreter_call items in the provider response; container charges are not in the token ledger.
- All configurations, arms, invalid answers and truncations are retained; no retries, repairs or exclusions.

Audit passed: True; problems: {"effort_synthetic_v1": {}, "effort_profiles_v1": {}, "state_synthetic_v1": {}, "state_profiles_v1": {}, "effort_gpt54_synthetic_v1": {}, "effort_gpt54_profiles_v1": {}, "tool_synthetic_v1": {}, "tool_profiles_v2": {}, "effort_auto_synthetic_v1": {}, "auto_mini_synthetic_v2": {}, "auto_mini_high_synthetic_v2": {}, "auto_gpt54_synthetic_v1": {}, "auto_gpt54_high_synthetic_v1": {}, "auto_profiles_v1": {}, "auto_high_profiles_v1": {}, "haiku_synthetic_v1": {}, "haiku_profiles_v1": {}, "open_synthetic_low_auto_v3": {}, "open_synthetic_high_auto_v2": {}, "open_synthetic_forced_v1": {}, "open_profiles_low_auto_v1": {}, "open_profiles_high_auto_v1": {}, "open_profiles_forced_v2": {}}

| Cohort | Configuration | Arm | N | Valid | Missing | Used code | All five | Stock exact | Hist. joint | Future joint | False alarms / neg. | Misses / pos. | Mean reasoning tokens | Cost USD |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| heldout_v2 | dsflash_high | canonical | 192 | 174 | 15 | 0 | 2 | 7 | 2 | 2 | 33/64 | 25/110 | 24 | 0.05 |
| heldout_v2 | dsflash_high | raw | 192 | 180 | 10 | 0 | 3 | 13 | 3 | 3 | 44/65 | 24/115 | 78 | 0.05 |
| heldout_v2 | dsflash_high_auto | canonical | 192 | 192 | 0 | 0 | 185 | 188 | 186 | 187 | 0/70 | 0/122 | 2451 | 0.13 |
| heldout_v2 | dsflash_high_auto | raw | 192 | 190 | 2 | 0 | 177 | 181 | 179 | 179 | 0/70 | 0/120 | 4756 | 0.23 |
| heldout_v2 | dsflash_low | canonical | 192 | 182 | 6 | 0 | 4 | 15 | 5 | 4 | 39/66 | 34/116 | 32 | 0.03 |
| heldout_v2 | dsflash_low | raw | 192 | 184 | 4 | 0 | 4 | 12 | 4 | 4 | 31/67 | 41/117 | 103 | 0.05 |
| heldout_v2 | dsflash_low_auto | canonical | 192 | 192 | 0 | 0 | 188 | 190 | 188 | 190 | 0/70 | 1/122 | 1695 | 0.10 |
| heldout_v2 | dsflash_low_auto | raw | 192 | 192 | 0 | 0 | 181 | 189 | 181 | 189 | 0/70 | 0/122 | 3443 | 0.18 |
| heldout_v2 | dsflash_low_auto | snapshot | 192 | 192 | 0 | 0 | 190 | 192 | 192 | 190 | 0/70 | 0/122 | 612 | 0.05 |
| heldout_v2 | dsflash_low_auto | state_canonical | 192 | 191 | 0 | 0 | 187 | 190 | 187 | 190 | 0/70 | 0/121 | 1201 | 0.07 |
| heldout_v2 | dsflash_low_auto | state_raw | 192 | 192 | 0 | 0 | 182 | 191 | 182 | 191 | 0/70 | 0/122 | 3074 | 0.15 |
| heldout_v2 | dspro_high | canonical | 192 | 160 | 32 | 0 | 154 | 160 | 156 | 158 | 0/58 | 0/102 | 3191 | 1.65 |
| heldout_v2 | dspro_high | raw | 192 | 176 | 16 | 0 | 176 | 176 | 176 | 176 | 0/61 | 0/115 | 5211 | 2.30 |
| heldout_v2 | dspro_high_auto | canonical | 192 | 190 | 2 | 0 | 185 | 187 | 185 | 187 | 0/69 | 0/121 | 3971 | 1.69 |
| heldout_v2 | dspro_high_auto | raw | 192 | 180 | 12 | 0 | 178 | 180 | 179 | 179 | 0/63 | 0/117 | 5768 | 2.35 |
| heldout_v2 | dspro_low | canonical | 192 | 190 | 2 | 0 | 187 | 190 | 188 | 189 | 1/69 | 0/121 | 2523 | 1.18 |
| heldout_v2 | dspro_low | raw | 192 | 186 | 6 | 0 | 181 | 184 | 181 | 185 | 0/68 | 0/118 | 3662 | 1.68 |
| heldout_v2 | dspro_low_auto | canonical | 192 | 192 | 0 | 0 | 187 | 192 | 189 | 190 | 0/70 | 0/122 | 2461 | 1.16 |
| heldout_v2 | dspro_low_auto | raw | 192 | 192 | 0 | 0 | 189 | 190 | 189 | 190 | 1/70 | 0/122 | 4142 | 1.79 |
| heldout_v2 | dspro_low_auto | snapshot | 192 | 192 | 0 | 0 | 190 | 192 | 192 | 190 | 0/70 | 0/122 | 517 | 0.34 |
| heldout_v2 | dspro_low_auto | state_canonical | 192 | 192 | 0 | 0 | 186 | 190 | 186 | 190 | 0/70 | 1/122 | 1653 | 0.81 |
| heldout_v2 | dspro_low_auto | state_raw | 192 | 190 | 2 | 0 | 188 | 189 | 188 | 189 | 0/68 | 0/122 | 3615 | 1.54 |
| heldout_v2 | glmflash_high | canonical | 192 | 192 | 0 | 0 | 143 | 180 | 160 | 158 | 0/70 | 0/122 | 415 | 0.12 |
| heldout_v2 | glmflash_high | raw | 192 | 192 | 0 | 0 | 120 | 175 | 143 | 143 | 0/70 | 1/122 | 823 | 0.22 |
| heldout_v2 | glmflash_high_auto | canonical | 192 | 192 | 0 | 0 | 143 | 184 | 160 | 162 | 0/70 | 0/122 | 503 | 0.14 |
| heldout_v2 | glmflash_high_auto | raw | 192 | 191 | 1 | 0 | 128 | 177 | 152 | 147 | 0/70 | 0/121 | 991 | 0.24 |
| heldout_v2 | glmflash_low | canonical | 192 | 192 | 0 | 0 | 103 | 162 | 134 | 120 | 0/70 | 0/122 | 316 | 0.11 |
| heldout_v2 | glmflash_low | raw | 192 | 192 | 0 | 0 | 73 | 150 | 111 | 101 | 1/70 | 0/122 | 444 | 0.15 |
| heldout_v2 | glmflash_low_auto | canonical | 192 | 190 | 2 | 0 | 97 | 165 | 130 | 123 | 0/69 | 2/121 | 441 | 0.13 |
| heldout_v2 | glmflash_low_auto | raw | 192 | 192 | 0 | 0 | 84 | 146 | 114 | 107 | 3/70 | 1/122 | 441 | 0.15 |
| heldout_v2 | glmflash_low_auto | snapshot | 192 | 192 | 0 | 0 | 113 | 192 | 192 | 113 | 4/70 | 0/122 | 65 | 0.04 |
| heldout_v2 | glmflash_low_auto | state_canonical | 192 | 192 | 0 | 0 | 133 | 167 | 133 | 167 | 1/70 | 4/122 | 148 | 0.08 |
| heldout_v2 | glmflash_low_auto | state_raw | 192 | 192 | 0 | 0 | 101 | 149 | 101 | 149 | 1/70 | 1/122 | 313 | 0.12 |
| heldout_v2 | gpt54_high | canonical | 192 | 192 | 0 | 0 | 181 | 189 | 188 | 182 | 1/70 | 0/122 | 749 | 3.26 |
| heldout_v2 | gpt54_high | raw | 192 | 192 | 0 | 0 | 181 | 186 | 185 | 181 | 1/70 | 1/122 | 1602 | 5.91 |
| heldout_v2 | gpt54_high_auto | canonical | 192 | 192 | 0 | 0 | 191 | 192 | 191 | 192 | 0/70 | 0/122 | 688 | 3.08 |
| heldout_v2 | gpt54_high_auto | raw | 192 | 192 | 0 | 0 | 190 | 191 | 191 | 190 | 0/70 | 0/122 | 1554 | 5.77 |
| heldout_v2 | gpt54_low | canonical | 192 | 192 | 0 | 0 | 182 | 191 | 184 | 189 | 0/70 | 0/122 | 419 | 2.30 |
| heldout_v2 | gpt54_low | raw | 192 | 192 | 0 | 0 | 161 | 175 | 166 | 169 | 3/70 | 3/122 | 710 | 3.34 |
| heldout_v2 | gpt54_low | snapshot | 192 | 192 | 0 | 0 | 190 | 192 | 192 | 190 | 0/70 | 0/122 | 142 | 0.92 |
| heldout_v2 | gpt54_low | state_canonical | 192 | 192 | 0 | 0 | 186 | 189 | 186 | 189 | 1/70 | 0/122 | 290 | 1.72 |
| heldout_v2 | gpt54_low | state_raw | 192 | 192 | 0 | 0 | 170 | 176 | 170 | 176 | 4/70 | 0/122 | 618 | 2.86 |
| heldout_v2 | gpt54_low | tool_canonical | 192 | 192 | 0 | 161 | 186 | 189 | 188 | 187 | 0/70 | 0/122 | 1590 | 7.18 |
| heldout_v2 | gpt54_low | tool_raw | 192 | 192 | 0 | 176 | 192 | 192 | 192 | 192 | 0/70 | 0/122 | 2248 | 9.98 |
| heldout_v2 | gpt54_low_auto | canonical | 192 | 192 | 0 | 0 | 184 | 189 | 184 | 189 | 1/70 | 0/122 | 415 | 2.30 |
| heldout_v2 | gpt54_low_auto | raw | 192 | 192 | 0 | 0 | 185 | 189 | 185 | 189 | 0/70 | 0/122 | 707 | 3.33 |
| heldout_v2 | gpt54_low_auto | snapshot | 192 | 192 | 0 | 0 | 175 | 192 | 192 | 175 | 1/70 | 0/122 | 136 | 0.90 |
| heldout_v2 | gpt54_low_auto | state_canonical | 192 | 192 | 0 | 0 | 156 | 161 | 156 | 161 | 3/70 | 1/122 | 248 | 1.60 |
| heldout_v2 | gpt54_low_auto | state_raw | 192 | 192 | 0 | 0 | 185 | 186 | 185 | 186 | 0/70 | 0/122 | 622 | 2.87 |
| heldout_v2 | gpt54_medium | canonical | 192 | 192 | 0 | 0 | 180 | 188 | 183 | 184 | 1/70 | 1/122 | 576 | 2.76 |
| heldout_v2 | gpt54_medium | raw | 192 | 192 | 0 | 0 | 183 | 189 | 189 | 183 | 1/70 | 0/122 | 1159 | 4.63 |
| heldout_v2 | haiku45 | canonical | 192 | 192 | 0 | 0 | 152 | 186 | 167 | 165 | 0/70 | 0/122 | n/a | 2.27 |
| heldout_v2 | haiku45 | raw | 192 | 192 | 0 | 0 | 84 | 114 | 92 | 101 | 2/70 | 5/122 | n/a | 2.92 |
| heldout_v2 | haiku45 | snapshot | 192 | 192 | 0 | 0 | 178 | 192 | 192 | 178 | 0/70 | 0/122 | n/a | 0.97 |
| heldout_v2 | haiku45 | state_canonical | 192 | 192 | 0 | 0 | 166 | 178 | 166 | 178 | 1/70 | 1/122 | n/a | 1.56 |
| heldout_v2 | haiku45 | state_raw | 192 | 192 | 0 | 0 | 85 | 118 | 85 | 118 | 3/70 | 6/122 | n/a | 2.34 |
| heldout_v2 | haiku45_thinking | canonical | 192 | 192 | 0 | 0 | 182 | 192 | 185 | 186 | 0/70 | 0/122 | n/a | 5.05 |
| heldout_v2 | haiku45_thinking | raw | 192 | 182 | 10 | 0 | 158 | 173 | 160 | 170 | 0/66 | 0/116 | n/a | 7.87 |
| heldout_v2 | haiku45_thinking | snapshot | 192 | 192 | 0 | 0 | 190 | 192 | 192 | 190 | 0/70 | 0/122 | n/a | 1.78 |
| heldout_v2 | haiku45_thinking | state_canonical | 192 | 192 | 0 | 0 | 190 | 192 | 190 | 192 | 0/70 | 0/122 | n/a | 3.70 |
| heldout_v2 | haiku45_thinking | state_raw | 192 | 181 | 11 | 0 | 163 | 169 | 163 | 169 | 0/68 | 0/113 | n/a | 6.93 |
| heldout_v2 | mini_high | canonical | 192 | 191 | 0 | 0 | 65 | 108 | 100 | 67 | 22/70 | 31/121 | 708 | 0.94 |
| heldout_v2 | mini_high | raw | 192 | 192 | 0 | 0 | 43 | 80 | 66 | 48 | 28/70 | 43/122 | 1214 | 1.44 |
| heldout_v2 | mini_high | snapshot | 192 | 192 | 0 | 0 | 187 | 192 | 192 | 187 | 0/70 | 0/122 | 333 | 0.44 |
| heldout_v2 | mini_high | state_canonical | 192 | 191 | 0 | 0 | 124 | 137 | 124 | 137 | 8/69 | 1/122 | 544 | 0.73 |
| heldout_v2 | mini_high | state_raw | 192 | 192 | 0 | 0 | 87 | 104 | 87 | 104 | 26/70 | 3/122 | 1317 | 1.46 |
| heldout_v2 | mini_high_auto | canonical | 192 | 192 | 0 | 0 | 171 | 186 | 178 | 179 | 0/70 | 0/122 | 1425 | 1.56 |
| heldout_v2 | mini_high_auto | raw | 192 | 191 | 1 | 0 | 139 | 158 | 145 | 152 | 2/70 | 3/121 | 3054 | 3.03 |
| heldout_v2 | mini_high_auto | snapshot | 192 | 192 | 0 | 0 | 189 | 192 | 192 | 189 | 2/70 | 0/122 | 332 | 0.44 |
| heldout_v2 | mini_low | canonical | 192 | 192 | 0 | 0 | 118 | 169 | 133 | 146 | 5/70 | 7/122 | 515 | 0.77 |
| heldout_v2 | mini_low | raw | 192 | 192 | 0 | 0 | 63 | 97 | 83 | 72 | 14/70 | 11/122 | 790 | 1.07 |
| heldout_v2 | mini_low | snapshot | 192 | 192 | 0 | 0 | 172 | 192 | 192 | 172 | 2/70 | 2/122 | 172 | 0.30 |
| heldout_v2 | mini_low | state_canonical | 192 | 192 | 0 | 0 | 141 | 180 | 141 | 180 | 2/70 | 2/122 | 363 | 0.58 |
| heldout_v2 | mini_low | state_raw | 192 | 192 | 0 | 0 | 83 | 106 | 83 | 106 | 16/70 | 3/122 | 645 | 0.88 |
| heldout_v2 | mini_low | tool_canonical | 192 | 192 | 0 | 139 | 182 | 191 | 184 | 188 | 1/70 | 0/122 | 1265 | 1.81 |
| heldout_v2 | mini_low | tool_raw | 192 | 192 | 0 | 139 | 173 | 182 | 175 | 176 | 1/70 | 2/122 | 2044 | 2.68 |
| heldout_v2 | mini_low_auto | canonical | 192 | 192 | 0 | 0 | 139 | 176 | 147 | 166 | 2/70 | 1/122 | 565 | 0.82 |
| heldout_v2 | mini_low_auto | raw | 192 | 191 | 1 | 0 | 89 | 113 | 92 | 109 | 2/70 | 3/121 | 975 | 1.23 |
| heldout_v2 | mini_low_auto | snapshot | 192 | 192 | 0 | 0 | 182 | 192 | 192 | 182 | 3/70 | 1/122 | 167 | 0.30 |
| heldout_v2 | mini_low_auto | state_canonical | 192 | 192 | 0 | 0 | 154 | 182 | 154 | 182 | 0/70 | 0/122 | 380 | 0.59 |
| heldout_v2 | mini_low_auto | state_raw | 192 | 192 | 0 | 0 | 103 | 133 | 103 | 133 | 2/70 | 2/122 | 770 | 0.99 |
| heldout_v2 | mini_medium | canonical | 192 | 191 | 0 | 0 | 83 | 127 | 112 | 90 | 21/70 | 17/121 | 616 | 0.86 |
| heldout_v2 | mini_medium | raw | 192 | 190 | 0 | 0 | 45 | 88 | 68 | 51 | 22/69 | 38/121 | 945 | 1.21 |
| heldout_v2 | mini_medium | snapshot | 192 | 192 | 0 | 0 | 188 | 192 | 192 | 188 | 1/70 | 0/122 | 254 | 0.37 |
| heldout_v2 | oss120b_high | canonical | 192 | 127 | 65 | 0 | 127 | 127 | 127 | 127 | 0/49 | 0/78 | 5925 | 0.99 |
| heldout_v2 | oss120b_high | raw | 192 | 103 | 89 | 0 | 103 | 103 | 103 | 103 | 0/37 | 0/66 | 6539 | 1.11 |
| heldout_v2 | oss120b_high_auto | canonical | 192 | 132 | 60 | 0 | 132 | 132 | 132 | 132 | 0/48 | 0/84 | 5986 | 1.00 |
| heldout_v2 | oss120b_high_auto | raw | 192 | 94 | 98 | 0 | 94 | 94 | 94 | 94 | 0/32 | 0/62 | 6679 | 1.13 |
| heldout_v2 | oss120b_low | canonical | 192 | 192 | 0 | 0 | 119 | 153 | 132 | 133 | 2/70 | 21/122 | 664 | 0.24 |
| heldout_v2 | oss120b_low | raw | 192 | 192 | 0 | 0 | 82 | 103 | 89 | 88 | 4/70 | 43/122 | 941 | 0.30 |
| heldout_v2 | oss120b_low_auto | canonical | 192 | 180 | 12 | 0 | 130 | 150 | 134 | 141 | 3/64 | 14/116 | 713 | 0.24 |
| heldout_v2 | oss120b_low_auto | raw | 192 | 151 | 41 | 0 | 90 | 105 | 97 | 95 | 3/52 | 13/99 | 1023 | 0.32 |
| heldout_v2 | oss120b_low_auto | snapshot | 192 | 191 | 1 | 0 | 182 | 190 | 190 | 182 | 1/69 | 1/122 | 286 | 0.10 |
| heldout_v2 | oss120b_low_auto | state_canonical | 192 | 188 | 4 | 0 | 131 | 146 | 131 | 146 | 13/69 | 1/119 | 443 | 0.18 |
| heldout_v2 | oss120b_low_auto | state_raw | 192 | 176 | 16 | 0 | 93 | 111 | 93 | 111 | 10/65 | 1/111 | 1089 | 0.30 |
| heldout_v2 | oss20b_high | canonical | 192 | 127 | 65 | 0 | 127 | 127 | 127 | 127 | 0/46 | 0/81 | 9862 | 0.60 |
| heldout_v2 | oss20b_high | raw | 192 | 86 | 106 | 0 | 81 | 81 | 81 | 81 | 0/33 | 0/53 | 10545 | 0.64 |
| heldout_v2 | oss20b_high_auto | canonical | 192 | 117 | 75 | 0 | 114 | 116 | 116 | 114 | 0/44 | 0/73 | 11037 | 0.67 |
| heldout_v2 | oss20b_high_auto | raw | 192 | 80 | 112 | 0 | 75 | 78 | 78 | 75 | 1/33 | 0/47 | 12678 | 0.77 |
| heldout_v2 | oss20b_low | canonical | 192 | 133 | 59 | 0 | 97 | 112 | 105 | 100 | 2/50 | 7/83 | 482 | 0.06 |
| heldout_v2 | oss20b_low | raw | 192 | 107 | 85 | 0 | 39 | 60 | 51 | 45 | 4/39 | 8/68 | 494 | 0.06 |
| heldout_v2 | oss20b_low_auto | canonical | 192 | 141 | 51 | 0 | 89 | 120 | 100 | 98 | 2/47 | 8/94 | 598 | 0.07 |
| heldout_v2 | oss20b_low_auto | raw | 192 | 104 | 88 | 0 | 40 | 61 | 49 | 46 | 3/35 | 7/69 | 498 | 0.07 |
| heldout_v2 | oss20b_low_auto | snapshot | 192 | 192 | 0 | 0 | 159 | 192 | 192 | 159 | 1/70 | 0/122 | 293 | 0.03 |
| heldout_v2 | oss20b_low_auto | state_canonical | 192 | 160 | 32 | 0 | 111 | 137 | 111 | 137 | 3/62 | 1/98 | 424 | 0.05 |
| heldout_v2 | oss20b_low_auto | state_raw | 192 | 139 | 53 | 0 | 57 | 72 | 57 | 72 | 7/49 | 5/90 | 946 | 0.09 |
| heldout_v2 | qwen27b_high | canonical | 192 | 182 | 10 | 0 | 174 | 181 | 179 | 176 | 0/65 | 0/117 | 1225 | 1.20 |
| heldout_v2 | qwen27b_high | raw | 192 | 164 | 28 | 0 | 148 | 157 | 150 | 154 | 0/58 | 0/106 | 2103 | 1.90 |
| heldout_v2 | qwen27b_high_auto | canonical | 192 | 184 | 8 | 0 | 175 | 184 | 181 | 178 | 0/68 | 0/116 | 1212 | 1.52 |
| heldout_v2 | qwen27b_high_auto | raw | 192 | 173 | 19 | 0 | 165 | 170 | 165 | 170 | 0/64 | 0/109 | 2271 | 2.51 |
| heldout_v2 | qwen27b_low | canonical | 192 | 176 | 16 | 0 | 176 | 176 | 176 | 176 | 0/62 | 0/114 | 1607 | 1.50 |
| heldout_v2 | qwen27b_low | raw | 192 | 151 | 40 | 0 | 145 | 148 | 146 | 147 | 0/54 | 0/97 | 2379 | 2.04 |
| heldout_v2 | qwen27b_low_auto | canonical | 192 | 192 | 0 | 0 | 189 | 191 | 189 | 191 | 0/70 | 0/122 | 1683 | 1.86 |
| heldout_v2 | qwen27b_low_auto | raw | 192 | 189 | 3 | 0 | 177 | 183 | 177 | 183 | 1/69 | 0/120 | 2679 | 2.74 |
| heldout_v2 | qwen27b_low_auto | snapshot | 192 | 192 | 0 | 0 | 192 | 192 | 192 | 192 | 0/70 | 0/122 | 446 | 0.60 |
| heldout_v2 | qwen27b_low_auto | state_canonical | 192 | 192 | 0 | 0 | 191 | 192 | 191 | 192 | 0/70 | 0/122 | 1078 | 1.32 |
| heldout_v2 | qwen27b_low_auto | state_raw | 192 | 189 | 3 | 0 | 184 | 186 | 184 | 186 | 1/69 | 0/120 | 2394 | 2.50 |
| heldout_v2 | sonnet46 | canonical | 192 | 192 | 0 | 0 | 190 | 192 | 191 | 191 | 0/70 | 0/122 | n/a | 7.04 |
| heldout_v2 | sonnet46 | raw | 192 | 192 | 0 | 0 | 188 | 191 | 189 | 190 | 0/70 | 0/122 | n/a | 11.27 |
| heldout_v2 | sonnet46 | snapshot | 192 | 192 | 0 | 0 | 192 | 192 | 192 | 192 | 0/70 | 0/122 | n/a | 2.70 |
| heldout_v2 | sonnet46 | state_canonical | 192 | 192 | 0 | 0 | 190 | 192 | 190 | 192 | 0/70 | 0/122 | n/a | 5.60 |
| heldout_v2 | sonnet46 | state_raw | 192 | 192 | 0 | 0 | 191 | 192 | 191 | 192 | 0/70 | 0/122 | n/a | 8.84 |
| heldout_v2 | sonnet46_thinking | canonical | 192 | 192 | 0 | 0 | 192 | 192 | 192 | 192 | 0/70 | 0/122 | n/a | 11.81 |
| heldout_v2 | sonnet46_thinking | raw | 192 | 192 | 0 | 0 | 186 | 190 | 188 | 188 | 0/70 | 0/122 | n/a | 17.43 |
| heldout_v2 | sonnet46_thinking | snapshot | 192 | 192 | 0 | 0 | 192 | 192 | 192 | 192 | 0/70 | 0/122 | n/a | 4.22 |
| heldout_v2 | sonnet46_thinking | state_canonical | 192 | 192 | 0 | 0 | 191 | 192 | 191 | 192 | 0/70 | 0/122 | n/a | 9.74 |
| heldout_v2 | sonnet46_thinking | state_raw | 192 | 192 | 0 | 0 | 190 | 192 | 190 | 192 | 0/70 | 0/122 | n/a | 15.43 |
| profiles_v2 | dsflash_high | canonical | 96 | 95 | 1 | 0 | 0 | 10 | 0 | 1 | 17/45 | 18/50 | 0 | 0.03 |
| profiles_v2 | dsflash_high | raw | 96 | 85 | 8 | 0 | 0 | 5 | 2 | 1 | 16/43 | 15/42 | 0 | 0.04 |
| profiles_v2 | dsflash_high_auto | canonical | 96 | 95 | 0 | 0 | 95 | 95 | 95 | 95 | 0/45 | 0/50 | 3224 | 0.09 |
| profiles_v2 | dsflash_high_auto | raw | 96 | 93 | 3 | 0 | 90 | 91 | 90 | 91 | 0/46 | 0/47 | 10247 | 0.23 |
| profiles_v2 | dsflash_low | canonical | 96 | 89 | 4 | 0 | 0 | 10 | 0 | 1 | 22/42 | 13/47 | 0 | 0.03 |
| profiles_v2 | dsflash_low | raw | 96 | 96 | 0 | 0 | 0 | 7 | 1 | 0 | 14/46 | 27/50 | 0 | 0.04 |
| profiles_v2 | dsflash_low_auto | canonical | 96 | 95 | 1 | 0 | 92 | 94 | 93 | 93 | 0/45 | 0/50 | 2421 | 0.07 |
| profiles_v2 | dsflash_low_auto | raw | 96 | 94 | 1 | 0 | 88 | 91 | 88 | 91 | 0/46 | 1/48 | 7678 | 0.18 |
| profiles_v2 | dsflash_low_auto | snapshot | 96 | 96 | 0 | 0 | 95 | 96 | 96 | 95 | 0/46 | 0/50 | 689 | 0.02 |
| profiles_v2 | dspro_high | canonical | 96 | 76 | 20 | 0 | 75 | 75 | 75 | 75 | 1/34 | 0/42 | 4327 | 1.16 |
| profiles_v2 | dspro_high | raw | 96 | 77 | 19 | 0 | 76 | 76 | 76 | 76 | 1/35 | 0/42 | 10241 | 2.32 |
| profiles_v2 | dspro_high_auto | canonical | 96 | 96 | 0 | 0 | 95 | 96 | 95 | 96 | 0/46 | 0/50 | 5673 | 1.19 |
| profiles_v2 | dspro_high_auto | raw | 96 | 93 | 3 | 0 | 92 | 93 | 92 | 93 | 0/44 | 0/49 | 11693 | 2.32 |
| profiles_v2 | dspro_low | canonical | 96 | 94 | 2 | 0 | 92 | 94 | 93 | 93 | 0/46 | 0/48 | 4156 | 0.94 |
| profiles_v2 | dspro_low | raw | 96 | 89 | 7 | 0 | 87 | 88 | 87 | 88 | 0/43 | 0/46 | 8354 | 1.82 |
| profiles_v2 | dspro_low_auto | canonical | 96 | 96 | 0 | 0 | 95 | 96 | 95 | 96 | 0/46 | 0/50 | 4032 | 0.90 |
| profiles_v2 | dspro_low_auto | raw | 96 | 96 | 0 | 0 | 91 | 94 | 93 | 92 | 1/46 | 1/50 | 8516 | 1.76 |
| profiles_v2 | dspro_low_auto | snapshot | 96 | 96 | 0 | 0 | 92 | 96 | 96 | 92 | 0/46 | 0/50 | 574 | 0.19 |
| profiles_v2 | glmflash_high | canonical | 96 | 96 | 0 | 0 | 64 | 91 | 72 | 80 | 0/46 | 0/50 | 575 | 0.09 |
| profiles_v2 | glmflash_high | raw | 96 | 96 | 0 | 0 | 57 | 84 | 69 | 68 | 2/46 | 2/50 | 1703 | 0.22 |
| profiles_v2 | glmflash_high_auto | canonical | 96 | 96 | 0 | 0 | 66 | 91 | 73 | 81 | 0/46 | 1/50 | 671 | 0.09 |
| profiles_v2 | glmflash_high_auto | raw | 96 | 96 | 0 | 0 | 62 | 81 | 72 | 68 | 0/46 | 2/50 | 1870 | 0.23 |
| profiles_v2 | glmflash_low | canonical | 96 | 96 | 0 | 0 | 47 | 87 | 65 | 62 | 2/46 | 0/50 | 362 | 0.07 |
| profiles_v2 | glmflash_low | raw | 96 | 96 | 0 | 0 | 22 | 51 | 27 | 30 | 10/46 | 3/50 | 858 | 0.14 |
| profiles_v2 | glmflash_low_auto | canonical | 96 | 96 | 0 | 0 | 42 | 84 | 64 | 56 | 4/46 | 1/50 | 349 | 0.07 |
| profiles_v2 | glmflash_low_auto | raw | 96 | 96 | 0 | 0 | 11 | 49 | 21 | 25 | 4/46 | 1/50 | 809 | 0.13 |
| profiles_v2 | glmflash_low_auto | snapshot | 96 | 96 | 0 | 0 | 37 | 96 | 96 | 37 | 4/46 | 1/50 | 58 | 0.02 |
| profiles_v2 | gpt54_high | canonical | 96 | 96 | 0 | 0 | 85 | 87 | 87 | 85 | 2/46 | 1/50 | 878 | 2.00 |
| profiles_v2 | gpt54_high | raw | 96 | 96 | 0 | 0 | 95 | 95 | 95 | 95 | 0/46 | 0/50 | 2834 | 5.18 |
| profiles_v2 | gpt54_high_auto | canonical | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 846 | 1.96 |
| profiles_v2 | gpt54_high_auto | raw | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 2713 | 5.00 |
| profiles_v2 | gpt54_low | canonical | 96 | 96 | 0 | 0 | 88 | 96 | 96 | 88 | 0/46 | 0/50 | 555 | 1.54 |
| profiles_v2 | gpt54_low | raw | 96 | 96 | 0 | 0 | 85 | 87 | 85 | 87 | 1/46 | 0/50 | 1133 | 2.73 |
| profiles_v2 | gpt54_low | snapshot | 96 | 96 | 0 | 0 | 95 | 96 | 96 | 95 | 0/46 | 0/50 | 160 | 0.52 |
| profiles_v2 | gpt54_low | state_canonical | 96 | 96 | 0 | 0 | 95 | 95 | 95 | 95 | 0/46 | 0/50 | 401 | 1.18 |
| profiles_v2 | gpt54_low | state_raw | 96 | 96 | 0 | 0 | 82 | 87 | 82 | 87 | 3/46 | 2/50 | 1026 | 2.44 |
| profiles_v2 | gpt54_low | tool_canonical | 96 | 96 | 0 | 96 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 2266 | 4.93 |
| profiles_v2 | gpt54_low | tool_raw | 96 | 96 | 0 | 96 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 3820 | 8.18 |
| profiles_v2 | gpt54_low_auto | canonical | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 554 | 1.54 |
| profiles_v2 | gpt54_low_auto | raw | 96 | 96 | 0 | 0 | 92 | 94 | 92 | 94 | 0/46 | 0/50 | 1150 | 2.75 |
| profiles_v2 | gpt54_low_auto | snapshot | 96 | 96 | 0 | 0 | 86 | 96 | 96 | 86 | 0/46 | 0/50 | 155 | 0.51 |
| profiles_v2 | gpt54_low_auto | state_canonical | 96 | 96 | 0 | 0 | 88 | 88 | 88 | 88 | 1/46 | 0/50 | 381 | 1.15 |
| profiles_v2 | gpt54_low_auto | state_raw | 96 | 96 | 0 | 0 | 90 | 92 | 90 | 92 | 1/46 | 0/50 | 1091 | 2.53 |
| profiles_v2 | gpt54_medium | canonical | 96 | 96 | 0 | 0 | 91 | 95 | 95 | 91 | 1/46 | 0/50 | 730 | 1.79 |
| profiles_v2 | gpt54_medium | raw | 96 | 96 | 0 | 0 | 92 | 92 | 92 | 92 | 0/46 | 0/50 | 1878 | 3.80 |
| profiles_v2 | haiku45 | canonical | 96 | 96 | 0 | 0 | 69 | 93 | 74 | 86 | 0/46 | 0/50 | n/a | 1.56 |
| profiles_v2 | haiku45 | raw | 96 | 96 | 0 | 0 | 1 | 7 | 1 | 6 | 17/46 | 8/50 | n/a | 2.31 |
| profiles_v2 | haiku45 | snapshot | 96 | 96 | 0 | 0 | 89 | 96 | 96 | 89 | 1/46 | 0/50 | n/a | 0.54 |
| profiles_v2 | haiku45 | state_canonical | 96 | 96 | 0 | 0 | 75 | 91 | 75 | 91 | 0/46 | 0/50 | n/a | 1.13 |
| profiles_v2 | haiku45 | state_raw | 96 | 96 | 0 | 0 | 1 | 6 | 1 | 6 | 17/46 | 9/50 | n/a | 2.02 |
| profiles_v2 | haiku45_thinking | canonical | 96 | 96 | 0 | 0 | 84 | 95 | 90 | 88 | 1/46 | 0/50 | n/a | 3.18 |
| profiles_v2 | haiku45_thinking | raw | 96 | 59 | 37 | 0 | 32 | 40 | 33 | 39 | 1/31 | 1/28 | n/a | 7.40 |
| profiles_v2 | haiku45_thinking | snapshot | 96 | 96 | 0 | 0 | 93 | 96 | 96 | 93 | 0/46 | 0/50 | n/a | 1.08 |
| profiles_v2 | haiku45_thinking | state_canonical | 96 | 96 | 0 | 0 | 91 | 95 | 91 | 95 | 0/46 | 1/50 | n/a | 2.60 |
| profiles_v2 | haiku45_thinking | state_raw | 96 | 74 | 21 | 0 | 45 | 57 | 45 | 57 | 1/35 | 1/39 | n/a | 6.89 |
| profiles_v2 | mini_high | canonical | 96 | 96 | 0 | 0 | 26 | 34 | 27 | 28 | 9/46 | 17/50 | 809 | 0.57 |
| profiles_v2 | mini_high | raw | 96 | 95 | 0 | 0 | 13 | 29 | 13 | 20 | 10/46 | 20/49 | 2402 | 1.37 |
| profiles_v2 | mini_high | snapshot | 96 | 96 | 0 | 0 | 90 | 96 | 96 | 90 | 1/46 | 0/50 | 354 | 0.24 |
| profiles_v2 | mini_high | state_canonical | 96 | 96 | 0 | 0 | 25 | 33 | 25 | 33 | 17/46 | 5/50 | 674 | 0.47 |
| profiles_v2 | mini_high | state_raw | 96 | 96 | 0 | 0 | 21 | 33 | 21 | 33 | 16/46 | 7/50 | 3162 | 1.65 |
| profiles_v2 | mini_high_auto | canonical | 96 | 95 | 1 | 0 | 90 | 93 | 92 | 91 | 0/45 | 0/50 | 1712 | 0.96 |
| profiles_v2 | mini_high_auto | raw | 96 | 95 | 1 | 0 | 34 | 47 | 34 | 47 | 3/46 | 7/49 | 6773 | 3.25 |
| profiles_v2 | mini_low | canonical | 96 | 96 | 0 | 0 | 39 | 87 | 71 | 45 | 15/46 | 7/50 | 604 | 0.48 |
| profiles_v2 | mini_low | raw | 96 | 95 | 0 | 0 | 4 | 14 | 4 | 12 | 15/46 | 10/49 | 1414 | 0.94 |
| profiles_v2 | mini_low | snapshot | 96 | 96 | 0 | 0 | 86 | 96 | 96 | 86 | 0/46 | 1/50 | 190 | 0.17 |
| profiles_v2 | mini_low | state_canonical | 96 | 96 | 0 | 0 | 86 | 95 | 86 | 95 | 0/46 | 0/50 | 464 | 0.38 |
| profiles_v2 | mini_low | state_raw | 96 | 96 | 0 | 0 | 3 | 17 | 3 | 17 | 9/46 | 8/50 | 1581 | 0.97 |
| profiles_v2 | mini_low | tool_canonical | 96 | 96 | 0 | 95 | 94 | 96 | 94 | 96 | 0/46 | 0/50 | 2309 | 1.49 |
| profiles_v2 | mini_low | tool_raw | 96 | 96 | 0 | 96 | 84 | 86 | 84 | 86 | 3/46 | 0/50 | 4027 | 2.48 |
| profiles_v2 | mini_low_auto | canonical | 96 | 95 | 1 | 0 | 69 | 89 | 76 | 79 | 2/45 | 0/50 | 673 | 0.51 |
| profiles_v2 | mini_low_auto | raw | 96 | 96 | 0 | 0 | 4 | 18 | 5 | 14 | 12/46 | 11/50 | 1884 | 1.14 |
| profiles_v2 | mini_low_auto | snapshot | 96 | 96 | 0 | 0 | 86 | 96 | 96 | 86 | 1/46 | 0/50 | 184 | 0.17 |
| profiles_v2 | mini_low_auto | state_canonical | 96 | 94 | 2 | 0 | 81 | 91 | 81 | 91 | 0/46 | 0/48 | 494 | 0.39 |
| profiles_v2 | mini_low_auto | state_raw | 96 | 95 | 1 | 0 | 4 | 19 | 4 | 19 | 8/45 | 11/50 | 1793 | 1.06 |
| profiles_v2 | mini_medium | canonical | 96 | 96 | 0 | 0 | 35 | 50 | 40 | 37 | 11/46 | 8/50 | 703 | 0.53 |
| profiles_v2 | mini_medium | raw | 96 | 96 | 0 | 0 | 11 | 23 | 11 | 16 | 15/46 | 24/50 | 1579 | 1.01 |
| profiles_v2 | mini_medium | snapshot | 96 | 96 | 0 | 0 | 91 | 96 | 96 | 91 | 0/46 | 0/50 | 278 | 0.21 |
| profiles_v2 | oss120b_high | canonical | 96 | 11 | 85 | 0 | 11 | 11 | 11 | 11 | 0/8 | 0/3 | 8096 | 0.68 |
| profiles_v2 | oss120b_high | raw | 96 | 0 | 96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0/0 | 8189 | 0.73 |
| profiles_v2 | oss120b_high_auto | canonical | 96 | 10 | 86 | 0 | 10 | 10 | 10 | 10 | 0/5 | 0/5 | 8083 | 0.68 |
| profiles_v2 | oss120b_high_auto | raw | 96 | 0 | 96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0/0 | 8189 | 0.73 |
| profiles_v2 | oss120b_low | canonical | 96 | 96 | 0 | 0 | 67 | 82 | 75 | 73 | 2/46 | 8/50 | 1281 | 0.19 |
| profiles_v2 | oss120b_low | raw | 96 | 96 | 0 | 0 | 1 | 17 | 3 | 7 | 1/46 | 47/50 | 818 | 0.21 |
| profiles_v2 | oss120b_low_auto | canonical | 96 | 95 | 1 | 0 | 68 | 80 | 76 | 70 | 1/46 | 6/49 | 1107 | 0.18 |
| profiles_v2 | oss120b_low_auto | raw | 96 | 49 | 47 | 0 | 2 | 10 | 2 | 5 | 0/26 | 19/23 | 635 | 0.19 |
| profiles_v2 | oss120b_low_auto | snapshot | 96 | 95 | 0 | 0 | 83 | 94 | 94 | 83 | 1/45 | 0/50 | 296 | 0.05 |
| profiles_v2 | oss20b_high | canonical | 96 | 47 | 49 | 0 | 44 | 46 | 44 | 46 | 0/25 | 0/22 | 12881 | 0.39 |
| profiles_v2 | oss20b_high | raw | 96 | 0 | 96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0/0 | 11847 | 0.37 |
| profiles_v2 | oss20b_high_auto | canonical | 96 | 46 | 50 | 0 | 45 | 46 | 46 | 45 | 0/23 | 0/23 | 14406 | 0.44 |
| profiles_v2 | oss20b_high_auto | raw | 96 | 0 | 96 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0/0 | 16382 | 0.50 |
| profiles_v2 | oss20b_low | canonical | 96 | 43 | 53 | 0 | 7 | 17 | 9 | 11 | 2/20 | 11/23 | 348 | 0.03 |
| profiles_v2 | oss20b_low | raw | 96 | 23 | 73 | 0 | 0 | 3 | 0 | 1 | 1/15 | 6/8 | 410 | 0.04 |
| profiles_v2 | oss20b_low_auto | canonical | 96 | 38 | 58 | 0 | 14 | 19 | 16 | 17 | 2/24 | 5/14 | 349 | 0.03 |
| profiles_v2 | oss20b_low_auto | raw | 96 | 27 | 69 | 0 | 0 | 2 | 0 | 0 | 0/11 | 12/16 | 491 | 0.05 |
| profiles_v2 | oss20b_low_auto | snapshot | 96 | 95 | 1 | 0 | 74 | 94 | 94 | 74 | 0/45 | 1/50 | 294 | 0.02 |
| profiles_v2 | qwen27b_high_auto | canonical | 96 | 96 | 0 | 0 | 92 | 95 | 94 | 93 | 0/46 | 0/50 | 1888 | 1.09 |
| profiles_v2 | qwen27b_high_auto | raw | 96 | 96 | 0 | 0 | 93 | 94 | 93 | 94 | 0/46 | 0/50 | 4318 | 2.32 |
| profiles_v2 | qwen27b_low_auto | canonical | 96 | 96 | 0 | 0 | 95 | 96 | 96 | 95 | 0/46 | 0/50 | 2641 | 1.30 |
| profiles_v2 | qwen27b_low_auto | raw | 96 | 96 | 0 | 0 | 90 | 93 | 90 | 93 | 0/46 | 0/50 | 5163 | 2.39 |
| profiles_v2 | qwen27b_low_auto | snapshot | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | 517 | 0.33 |
| profiles_v2 | sonnet46 | canonical | 96 | 96 | 0 | 0 | 94 | 96 | 95 | 95 | 0/46 | 0/50 | n/a | 4.95 |
| profiles_v2 | sonnet46 | raw | 96 | 96 | 0 | 0 | 88 | 93 | 88 | 92 | 0/46 | 0/50 | n/a | 10.13 |
| profiles_v2 | sonnet46 | snapshot | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | n/a | 1.67 |
| profiles_v2 | sonnet46 | state_canonical | 96 | 96 | 0 | 0 | 95 | 96 | 95 | 96 | 0/46 | 0/50 | n/a | 4.06 |
| profiles_v2 | sonnet46 | state_raw | 96 | 96 | 0 | 0 | 89 | 92 | 89 | 92 | 0/46 | 0/50 | n/a | 8.65 |
| profiles_v2 | sonnet46_thinking | canonical | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | n/a | 7.93 |
| profiles_v2 | sonnet46_thinking | raw | 96 | 96 | 0 | 0 | 93 | 95 | 94 | 94 | 0/46 | 0/50 | n/a | 14.43 |
| profiles_v2 | sonnet46_thinking | snapshot | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | n/a | 2.62 |
| profiles_v2 | sonnet46_thinking | state_canonical | 96 | 96 | 0 | 0 | 96 | 96 | 96 | 96 | 0/46 | 0/50 | n/a | 6.99 |
| profiles_v2 | sonnet46_thinking | state_raw | 96 | 96 | 0 | 0 | 93 | 96 | 93 | 96 | 0/46 | 0/50 | n/a | 14.62 |

| Cohort | Kind | Left | Right | Metric | Bases | Difference [95% CI], pp |
| --- | --- | --- | --- | --- | ---: | --- |
| heldout_v2 | effort | mini_low/raw | mini_medium/raw | future_joint | 96 | -10.9 [-18.8, -3.1] |
| heldout_v2 | effort | mini_low/raw | mini_medium/raw | stock_exact | 96 | -4.7 [-13.0, +3.6] |
| heldout_v2 | effort | mini_low/raw | mini_medium/raw | joint_exact | 96 | -9.4 [-16.1, -2.6] |
| heldout_v2 | effort | mini_low/canonical | mini_medium/canonical | future_joint | 96 | -29.2 [-38.0, -20.3] |
| heldout_v2 | effort | mini_low/canonical | mini_medium/canonical | stock_exact | 96 | -21.9 [-29.2, -14.6] |
| heldout_v2 | effort | mini_low/canonical | mini_medium/canonical | joint_exact | 96 | -18.2 [-28.1, -8.3] |
| heldout_v2 | effort | mini_low/snapshot | mini_medium/snapshot | future_joint | 96 | +8.3 [+4.2, +12.5] |
| heldout_v2 | effort | mini_low/snapshot | mini_medium/snapshot | stock_exact | 96 | +0.0 [+0.0, +0.0] |
| heldout_v2 | effort | mini_low/snapshot | mini_medium/snapshot | joint_exact | 96 | +8.3 [+4.2, +12.5] |
| heldout_v2 | effort | mini_low/raw | mini_high/raw | future_joint | 96 | -12.5 [-21.9, -3.1] |
| heldout_v2 | effort | mini_low/raw | mini_high/raw | stock_exact | 96 | -8.9 [-17.7, +0.5] |
| heldout_v2 | effort | mini_low/raw | mini_high/raw | joint_exact | 96 | -10.4 [-19.3, -1.6] |
| heldout_v2 | effort | mini_low/canonical | mini_high/canonical | future_joint | 96 | -41.1 [-51.0, -31.2] |
| heldout_v2 | effort | mini_low/canonical | mini_high/canonical | stock_exact | 96 | -31.8 [-40.6, -22.9] |
| heldout_v2 | effort | mini_low/canonical | mini_high/canonical | joint_exact | 96 | -27.6 [-38.5, -16.7] |
| heldout_v2 | effort | mini_low/snapshot | mini_high/snapshot | future_joint | 96 | +7.8 [+3.1, +12.5] |
| heldout_v2 | effort | mini_low/snapshot | mini_high/snapshot | stock_exact | 96 | +0.0 [+0.0, +0.0] |
| heldout_v2 | effort | mini_low/snapshot | mini_high/snapshot | joint_exact | 96 | +7.8 [+3.1, +12.5] |
| heldout_v2 | state | mini_low/raw | mini_low/state_raw | stock_exact | 96 | +4.7 [-2.1, +11.5] |
| heldout_v2 | state | mini_low/raw | mini_low/state_raw | future_joint | 96 | +17.7 [+9.9, +25.5] |
| heldout_v2 | state | mini_low/raw | mini_low/state_raw | joint_exact | 96 | +10.4 [+2.6, +18.2] |
| heldout_v2 | state | mini_low/raw | mini_low/state_raw | historical_joint | 96 | +0.0 [-6.8, +7.3] |
| heldout_v2 | state | mini_low/canonical | mini_low/state_canonical | stock_exact | 96 | +5.7 [+0.0, +11.5] |
| heldout_v2 | state | mini_low/canonical | mini_low/state_canonical | future_joint | 96 | +17.7 [+9.9, +25.5] |
| heldout_v2 | state | mini_low/canonical | mini_low/state_canonical | joint_exact | 96 | +12.0 [+2.6, +20.8] |
| heldout_v2 | state | mini_low/canonical | mini_low/state_canonical | historical_joint | 96 | +4.2 [-4.2, +12.5] |
| heldout_v2 | state | mini_high/raw | mini_high/state_raw | stock_exact | 96 | +12.5 [+3.6, +20.8] |
| heldout_v2 | state | mini_high/raw | mini_high/state_raw | future_joint | 96 | +29.2 [+19.8, +38.5] |
| heldout_v2 | state | mini_high/raw | mini_high/state_raw | joint_exact | 96 | +22.9 [+14.1, +31.8] |
| heldout_v2 | state | mini_high/raw | mini_high/state_raw | historical_joint | 96 | +10.9 [+2.6, +19.3] |
| heldout_v2 | state | mini_high/canonical | mini_high/state_canonical | stock_exact | 96 | +15.1 [+7.3, +22.9] |
| heldout_v2 | state | mini_high/canonical | mini_high/state_canonical | future_joint | 96 | +36.5 [+26.6, +46.4] |
| heldout_v2 | state | mini_high/canonical | mini_high/state_canonical | joint_exact | 96 | +30.7 [+20.3, +40.6] |
| heldout_v2 | state | mini_high/canonical | mini_high/state_canonical | historical_joint | 96 | +12.5 [+3.6, +20.8] |
| heldout_v2 | state | gpt54_low/raw | gpt54_low/state_raw | stock_exact | 96 | +0.5 [-5.2, +6.2] |
| heldout_v2 | state | gpt54_low/raw | gpt54_low/state_raw | future_joint | 96 | +3.6 [-2.6, +9.9] |
| heldout_v2 | state | gpt54_low/raw | gpt54_low/state_raw | joint_exact | 96 | +4.7 [-2.1, +12.0] |
| heldout_v2 | state | gpt54_low/raw | gpt54_low/state_raw | historical_joint | 96 | +2.1 [-4.7, +8.9] |
| heldout_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | stock_exact | 96 | -1.0 [-3.1, +1.0] |
| heldout_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | future_joint | 96 | +0.0 [-2.6, +2.6] |
| heldout_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | joint_exact | 96 | +2.1 [-1.6, +6.2] |
| heldout_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | historical_joint | 96 | +1.0 [-2.6, +4.7] |
| heldout_v2 | state | sonnet46/raw | sonnet46/state_raw | stock_exact | 96 | +0.5 [+0.0, +1.6] |
| heldout_v2 | state | sonnet46/raw | sonnet46/state_raw | future_joint | 96 | +1.0 [+0.0, +2.6] |
| heldout_v2 | state | sonnet46/raw | sonnet46/state_raw | joint_exact | 96 | +1.6 [-0.5, +4.2] |
| heldout_v2 | state | sonnet46/raw | sonnet46/state_raw | historical_joint | 96 | +1.0 [-1.0, +3.1] |
| heldout_v2 | state | sonnet46/canonical | sonnet46/state_canonical | stock_exact | 96 | +0.0 [+0.0, +0.0] |
| heldout_v2 | state | sonnet46/canonical | sonnet46/state_canonical | future_joint | 96 | +0.5 [+0.0, +1.6] |
| heldout_v2 | state | sonnet46/canonical | sonnet46/state_canonical | joint_exact | 96 | +0.0 [-1.6, +1.6] |
| heldout_v2 | state | sonnet46/canonical | sonnet46/state_canonical | historical_joint | 96 | -0.5 [-1.6, +0.0] |
| heldout_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | stock_exact | 96 | +1.0 [+0.0, +2.6] |
| heldout_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | future_joint | 96 | +2.1 [+0.5, +4.2] |
| heldout_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | joint_exact | 96 | +2.1 [-0.5, +5.2] |
| heldout_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | historical_joint | 96 | +1.0 [-1.6, +3.6] |
| heldout_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | stock_exact | 96 | +0.0 [+0.0, +0.0] |
| heldout_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | future_joint | 96 | +0.0 [+0.0, +0.0] |
| heldout_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | joint_exact | 96 | -0.5 [-1.6, +0.0] |
| heldout_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | historical_joint | 96 | -0.5 [-1.6, +0.0] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | future_joint | 96 | +7.3 [+1.0, +14.1] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | stock_exact | 96 | +7.3 [+2.6, +12.5] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | joint_exact | 96 | +11.5 [+4.7, +18.8] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | future_joint | 96 | -2.6 [-5.7, +0.5] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | stock_exact | 96 | -1.6 [-4.2, +0.5] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | joint_exact | 96 | -1.0 [-5.2, +3.1] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | future_joint | 96 | +6.2 [+0.0, +13.0] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | stock_exact | 96 | +5.7 [+0.5, +11.5] |
| heldout_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | joint_exact | 96 | +10.4 [+3.1, +17.7] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | future_joint | 96 | -3.6 [-7.8, +0.0] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | stock_exact | 96 | -1.0 [-3.1, +1.0] |
| heldout_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | joint_exact | 96 | -0.5 [-5.2, +4.2] |
| heldout_v2 | auto_tool | mini_low_auto/raw | mini_low/tool_raw | future_joint | 96 | +34.9 [+26.0, +43.8] |
| heldout_v2 | auto_tool | mini_low_auto/raw | mini_low/tool_raw | stock_exact | 96 | +35.9 [+27.1, +44.8] |
| heldout_v2 | auto_tool | mini_low_auto/canonical | mini_low/tool_canonical | future_joint | 96 | +11.5 [+6.2, +17.7] |
| heldout_v2 | auto_tool | mini_low_auto/canonical | mini_low/tool_canonical | stock_exact | 96 | +7.8 [+3.6, +12.5] |
| heldout_v2 | tool | mini_low/raw | mini_low/tool_raw | future_joint | 96 | +54.2 [+45.3, +62.5] |
| heldout_v2 | tool | mini_low/raw | mini_low/tool_raw | stock_exact | 96 | +44.3 [+35.4, +53.1] |
| heldout_v2 | tool | mini_low/raw | mini_low/tool_raw | joint_exact | 96 | +57.3 [+48.4, +65.6] |
| heldout_v2 | tool | mini_low/state_raw | mini_low/tool_raw | future_joint | 96 | +36.5 [+27.1, +45.8] |
| heldout_v2 | tool | mini_low/canonical | mini_low/tool_canonical | future_joint | 96 | +21.9 [+14.6, +29.2] |
| heldout_v2 | tool | mini_low/canonical | mini_low/tool_canonical | stock_exact | 96 | +11.5 [+6.2, +16.7] |
| heldout_v2 | tool | mini_low/canonical | mini_low/tool_canonical | joint_exact | 96 | +33.3 [+24.5, +42.2] |
| heldout_v2 | tool | mini_low/state_canonical | mini_low/tool_canonical | future_joint | 96 | +4.2 [+0.5, +8.3] |
| heldout_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | future_joint | 96 | +12.0 [+7.3, +17.2] |
| heldout_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | stock_exact | 96 | +8.9 [+4.7, +14.1] |
| heldout_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | joint_exact | 96 | +16.1 [+10.4, +22.4] |
| heldout_v2 | tool | gpt54_low/state_raw | gpt54_low/tool_raw | future_joint | 96 | +8.3 [+4.7, +12.5] |
| heldout_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | future_joint | 96 | -1.0 [-4.2, +1.6] |
| heldout_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | stock_exact | 96 | -1.0 [-3.1, +1.0] |
| heldout_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | joint_exact | 96 | +2.1 [-1.6, +6.2] |
| heldout_v2 | tool | gpt54_low/state_canonical | gpt54_low/tool_canonical | future_joint | 96 | -1.0 [-4.2, +1.6] |
| heldout_v2 | original | mini_low/raw | mini_low/canonical | future_joint | 96 | +38.5 [+28.6, +47.9] |
| heldout_v2 | original | mini_low/raw | mini_low/canonical | stock_exact | 96 | +37.5 [+28.6, +46.4] |
| heldout_v2 | original | mini_low/raw | mini_low/snapshot | future_joint | 96 | +52.1 [+43.8, +60.4] |
| heldout_v2 | original | mini_low/raw | mini_low/snapshot | stock_exact | 96 | +49.5 [+41.1, +58.3] |
| heldout_v2 | original | gpt54_low/raw | gpt54_low/canonical | future_joint | 96 | +10.4 [+5.7, +15.6] |
| heldout_v2 | original | gpt54_low/raw | gpt54_low/canonical | stock_exact | 96 | +8.3 [+3.6, +13.5] |
| heldout_v2 | original | gpt54_low/raw | gpt54_low/snapshot | future_joint | 96 | +10.9 [+6.2, +16.7] |
| heldout_v2 | original | gpt54_low/raw | gpt54_low/snapshot | stock_exact | 96 | +8.9 [+4.7, +14.1] |
| heldout_v2 | original | sonnet46/raw | sonnet46/canonical | future_joint | 96 | +0.5 [-1.0, +2.6] |
| heldout_v2 | original | sonnet46/raw | sonnet46/canonical | stock_exact | 96 | +0.5 [+0.0, +1.6] |
| heldout_v2 | original | sonnet46/raw | sonnet46/snapshot | future_joint | 96 | +1.0 [+0.0, +2.6] |
| heldout_v2 | original | sonnet46/raw | sonnet46/snapshot | stock_exact | 96 | +0.5 [+0.0, +1.6] |
| heldout_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/canonical | future_joint | 96 | +2.1 [+0.5, +4.2] |
| heldout_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/canonical | stock_exact | 96 | +1.0 [+0.0, +2.6] |
| heldout_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/snapshot | future_joint | 96 | +2.1 [+0.5, +4.2] |
| heldout_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/snapshot | stock_exact | 96 | +1.0 [+0.0, +2.6] |
| heldout_v2 | auto | mini_low_auto/raw | mini_high_auto/raw | future_joint | 96 | +22.4 [+14.1, +30.7] |
| heldout_v2 | auto | mini_low/raw | mini_low_auto/raw | future_joint | 96 | +19.3 [+11.5, +27.1] |
| heldout_v2 | auto | mini_high/raw | mini_high_auto/raw | future_joint | 96 | +54.2 [+44.3, +63.0] |
| heldout_v2 | auto | mini_low_auto/raw | mini_high_auto/raw | stock_exact | 96 | +23.4 [+15.1, +31.2] |
| heldout_v2 | auto | mini_low/raw | mini_low_auto/raw | stock_exact | 96 | +8.3 [+2.1, +15.1] |
| heldout_v2 | auto | mini_high/raw | mini_high_auto/raw | stock_exact | 96 | +40.6 [+31.2, +49.5] |
| heldout_v2 | auto | mini_low_auto/canonical | mini_high_auto/canonical | future_joint | 96 | +6.8 [+0.5, +13.5] |
| heldout_v2 | auto | mini_low/canonical | mini_low_auto/canonical | future_joint | 96 | +10.4 [+3.1, +18.2] |
| heldout_v2 | auto | mini_high/canonical | mini_high_auto/canonical | future_joint | 96 | +58.3 [+50.0, +66.7] |
| heldout_v2 | auto | mini_low_auto/canonical | mini_high_auto/canonical | stock_exact | 96 | +5.2 [+0.5, +10.4] |
| heldout_v2 | auto | mini_low/canonical | mini_low_auto/canonical | stock_exact | 96 | +3.6 [-1.6, +8.9] |
| heldout_v2 | auto | mini_high/canonical | mini_high_auto/canonical | stock_exact | 96 | +40.6 [+31.8, +49.5] |
| profiles_v2 | effort | mini_low/raw | mini_medium/raw | future_joint | 48 | +4.2 [-4.2, +12.5] |
| profiles_v2 | effort | mini_low/raw | mini_medium/raw | stock_exact | 48 | +9.4 [+1.0, +18.8] |
| profiles_v2 | effort | mini_low/raw | mini_medium/raw | joint_exact | 48 | +7.3 [+1.0, +14.6] |
| profiles_v2 | effort | mini_low/canonical | mini_medium/canonical | future_joint | 48 | -8.3 [-20.8, +4.2] |
| profiles_v2 | effort | mini_low/canonical | mini_medium/canonical | stock_exact | 48 | -38.5 [-50.0, -27.1] |
| profiles_v2 | effort | mini_low/canonical | mini_medium/canonical | joint_exact | 48 | -4.2 [-16.7, +8.3] |
| profiles_v2 | effort | mini_low/snapshot | mini_medium/snapshot | future_joint | 48 | +5.2 [-1.0, +11.5] |
| profiles_v2 | effort | mini_low/snapshot | mini_medium/snapshot | stock_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort | mini_low/snapshot | mini_medium/snapshot | joint_exact | 48 | +5.2 [-1.0, +11.5] |
| profiles_v2 | effort | mini_low/raw | mini_high/raw | future_joint | 48 | +8.3 [-1.0, +17.7] |
| profiles_v2 | effort | mini_low/raw | mini_high/raw | stock_exact | 48 | +15.6 [+6.2, +25.0] |
| profiles_v2 | effort | mini_low/raw | mini_high/raw | joint_exact | 48 | +9.4 [+1.0, +17.7] |
| profiles_v2 | effort | mini_low/canonical | mini_high/canonical | future_joint | 48 | -17.7 [-30.2, -5.2] |
| profiles_v2 | effort | mini_low/canonical | mini_high/canonical | stock_exact | 48 | -55.2 [-65.6, -44.8] |
| profiles_v2 | effort | mini_low/canonical | mini_high/canonical | joint_exact | 48 | -13.5 [-26.0, -1.0] |
| profiles_v2 | effort | mini_low/snapshot | mini_high/snapshot | future_joint | 48 | +4.2 [-4.2, +12.5] |
| profiles_v2 | effort | mini_low/snapshot | mini_high/snapshot | stock_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort | mini_low/snapshot | mini_high/snapshot | joint_exact | 48 | +4.2 [-4.2, +12.5] |
| profiles_v2 | state | mini_low/raw | mini_low/state_raw | stock_exact | 48 | +3.1 [-5.2, +11.5] |
| profiles_v2 | state | mini_low/raw | mini_low/state_raw | future_joint | 48 | +5.2 [-3.1, +13.5] |
| profiles_v2 | state | mini_low/raw | mini_low/state_raw | joint_exact | 48 | -1.0 [-5.2, +3.1] |
| profiles_v2 | state | mini_low/raw | mini_low/state_raw | historical_joint | 48 | -1.0 [-5.2, +3.1] |
| profiles_v2 | state | mini_low/canonical | mini_low/state_canonical | stock_exact | 48 | +8.3 [+3.1, +14.6] |
| profiles_v2 | state | mini_low/canonical | mini_low/state_canonical | future_joint | 48 | +52.1 [+42.7, +61.5] |
| profiles_v2 | state | mini_low/canonical | mini_low/state_canonical | joint_exact | 48 | +49.0 [+37.5, +59.4] |
| profiles_v2 | state | mini_low/canonical | mini_low/state_canonical | historical_joint | 48 | +15.6 [+5.2, +26.0] |
| profiles_v2 | state | mini_high/raw | mini_high/state_raw | stock_exact | 48 | +4.2 [-8.3, +16.7] |
| profiles_v2 | state | mini_high/raw | mini_high/state_raw | future_joint | 48 | +13.5 [+0.0, +27.1] |
| profiles_v2 | state | mini_high/raw | mini_high/state_raw | joint_exact | 48 | +8.3 [-3.1, +19.8] |
| profiles_v2 | state | mini_high/raw | mini_high/state_raw | historical_joint | 48 | +8.3 [-3.1, +19.8] |
| profiles_v2 | state | mini_high/canonical | mini_high/state_canonical | stock_exact | 48 | -1.0 [-11.5, +9.4] |
| profiles_v2 | state | mini_high/canonical | mini_high/state_canonical | future_joint | 48 | +5.2 [-7.3, +17.7] |
| profiles_v2 | state | mini_high/canonical | mini_high/state_canonical | joint_exact | 48 | -1.0 [-13.5, +11.5] |
| profiles_v2 | state | mini_high/canonical | mini_high/state_canonical | historical_joint | 48 | -2.1 [-13.5, +9.4] |
| profiles_v2 | state | gpt54_low/raw | gpt54_low/state_raw | stock_exact | 48 | +0.0 [-8.3, +8.3] |
| profiles_v2 | state | gpt54_low/raw | gpt54_low/state_raw | future_joint | 48 | +0.0 [-8.3, +8.3] |
| profiles_v2 | state | gpt54_low/raw | gpt54_low/state_raw | joint_exact | 48 | -3.1 [-13.5, +6.2] |
| profiles_v2 | state | gpt54_low/raw | gpt54_low/state_raw | historical_joint | 48 | -3.1 [-13.5, +6.2] |
| profiles_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | stock_exact | 48 | -1.0 [-3.1, +0.0] |
| profiles_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | future_joint | 48 | +7.3 [+2.1, +13.5] |
| profiles_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | joint_exact | 48 | +7.3 [+2.1, +13.5] |
| profiles_v2 | state | gpt54_low/canonical | gpt54_low/state_canonical | historical_joint | 48 | -1.0 [-3.1, +0.0] |
| profiles_v2 | state | sonnet46/raw | sonnet46/state_raw | stock_exact | 48 | -1.0 [-3.1, +0.0] |
| profiles_v2 | state | sonnet46/raw | sonnet46/state_raw | future_joint | 48 | +0.0 [-3.1, +3.1] |
| profiles_v2 | state | sonnet46/raw | sonnet46/state_raw | joint_exact | 48 | +1.0 [-5.2, +7.3] |
| profiles_v2 | state | sonnet46/raw | sonnet46/state_raw | historical_joint | 48 | +1.0 [-5.2, +7.3] |
| profiles_v2 | state | sonnet46/canonical | sonnet46/state_canonical | stock_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | state | sonnet46/canonical | sonnet46/state_canonical | future_joint | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | state | sonnet46/canonical | sonnet46/state_canonical | joint_exact | 48 | +1.0 [-2.1, +4.2] |
| profiles_v2 | state | sonnet46/canonical | sonnet46/state_canonical | historical_joint | 48 | +0.0 [-3.1, +3.1] |
| profiles_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | stock_exact | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | future_joint | 48 | +2.1 [+0.0, +6.2] |
| profiles_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | joint_exact | 48 | +0.0 [-4.2, +5.2] |
| profiles_v2 | state | sonnet46_thinking/raw | sonnet46_thinking/state_raw | historical_joint | 48 | -1.0 [-4.2, +2.1] |
| profiles_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | stock_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | future_joint | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | joint_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | state | sonnet46_thinking/canonical | sonnet46_thinking/state_canonical | historical_joint | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | future_joint | 48 | +5.2 [-2.1, +12.5] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | stock_exact | 48 | +5.2 [-2.1, +12.5] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_medium/raw | joint_exact | 48 | +7.3 [+0.0, +14.6] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | future_joint | 48 | +3.1 [-4.2, +10.4] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | stock_exact | 48 | -1.0 [-3.1, +0.0] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_medium/canonical | joint_exact | 48 | +3.1 [-4.2, +10.4] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | future_joint | 48 | +8.3 [+2.1, +14.6] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | stock_exact | 48 | +8.3 [+2.1, +14.6] |
| profiles_v2 | effort2 | gpt54_low/raw | gpt54_high/raw | joint_exact | 48 | +10.4 [+4.2, +16.7] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | future_joint | 48 | -3.1 [-11.5, +4.2] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | stock_exact | 48 | -9.4 [-15.6, -4.2] |
| profiles_v2 | effort2 | gpt54_low/canonical | gpt54_high/canonical | joint_exact | 48 | -3.1 [-11.5, +4.2] |
| profiles_v2 | auto_tool | mini_low_auto/raw | mini_low/tool_raw | future_joint | 48 | +75.0 [+64.6, +84.4] |
| profiles_v2 | auto_tool | mini_low_auto/raw | mini_low/tool_raw | stock_exact | 48 | +70.8 [+60.4, +81.2] |
| profiles_v2 | auto_tool | mini_low_auto/canonical | mini_low/tool_canonical | future_joint | 48 | +17.7 [+10.4, +25.0] |
| profiles_v2 | auto_tool | mini_low_auto/canonical | mini_low/tool_canonical | stock_exact | 48 | +7.3 [+3.1, +12.5] |
| profiles_v2 | tool | mini_low/raw | mini_low/tool_raw | future_joint | 48 | +77.1 [+68.8, +84.4] |
| profiles_v2 | tool | mini_low/raw | mini_low/tool_raw | stock_exact | 48 | +75.0 [+66.7, +83.3] |
| profiles_v2 | tool | mini_low/raw | mini_low/tool_raw | joint_exact | 48 | +83.3 [+76.0, +89.6] |
| profiles_v2 | tool | mini_low/state_raw | mini_low/tool_raw | future_joint | 48 | +71.9 [+60.4, +82.3] |
| profiles_v2 | tool | mini_low/canonical | mini_low/tool_canonical | future_joint | 48 | +53.1 [+43.8, +61.5] |
| profiles_v2 | tool | mini_low/canonical | mini_low/tool_canonical | stock_exact | 48 | +9.4 [+4.2, +16.7] |
| profiles_v2 | tool | mini_low/canonical | mini_low/tool_canonical | joint_exact | 48 | +57.3 [+49.0, +65.6] |
| profiles_v2 | tool | mini_low/state_canonical | mini_low/tool_canonical | future_joint | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | future_joint | 48 | +9.4 [+4.2, +15.6] |
| profiles_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | stock_exact | 48 | +9.4 [+4.2, +15.6] |
| profiles_v2 | tool | gpt54_low/raw | gpt54_low/tool_raw | joint_exact | 48 | +11.5 [+6.2, +17.7] |
| profiles_v2 | tool | gpt54_low/state_raw | gpt54_low/tool_raw | future_joint | 48 | +9.4 [+4.2, +15.6] |
| profiles_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | future_joint | 48 | +8.3 [+3.1, +13.5] |
| profiles_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | stock_exact | 48 | +0.0 [+0.0, +0.0] |
| profiles_v2 | tool | gpt54_low/canonical | gpt54_low/tool_canonical | joint_exact | 48 | +8.3 [+3.1, +13.5] |
| profiles_v2 | tool | gpt54_low/state_canonical | gpt54_low/tool_canonical | future_joint | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | original | mini_low/raw | mini_low/canonical | future_joint | 48 | +34.4 [+24.0, +44.8] |
| profiles_v2 | original | mini_low/raw | mini_low/canonical | stock_exact | 48 | +76.0 [+66.7, +84.4] |
| profiles_v2 | original | mini_low/raw | mini_low/snapshot | future_joint | 48 | +77.1 [+68.8, +85.4] |
| profiles_v2 | original | mini_low/raw | mini_low/snapshot | stock_exact | 48 | +85.4 [+78.1, +91.7] |
| profiles_v2 | original | gpt54_low/raw | gpt54_low/canonical | future_joint | 48 | +1.0 [-6.2, +8.3] |
| profiles_v2 | original | gpt54_low/raw | gpt54_low/canonical | stock_exact | 48 | +9.4 [+4.2, +15.6] |
| profiles_v2 | original | gpt54_low/raw | gpt54_low/snapshot | future_joint | 48 | +8.3 [+3.1, +14.6] |
| profiles_v2 | original | gpt54_low/raw | gpt54_low/snapshot | stock_exact | 48 | +9.4 [+4.2, +15.6] |
| profiles_v2 | original | sonnet46/raw | sonnet46/canonical | future_joint | 48 | +3.1 [+0.0, +8.3] |
| profiles_v2 | original | sonnet46/raw | sonnet46/canonical | stock_exact | 48 | +3.1 [+0.0, +8.3] |
| profiles_v2 | original | sonnet46/raw | sonnet46/snapshot | future_joint | 48 | +4.2 [+0.0, +9.4] |
| profiles_v2 | original | sonnet46/raw | sonnet46/snapshot | stock_exact | 48 | +3.1 [+0.0, +8.3] |
| profiles_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/canonical | future_joint | 48 | +2.1 [+0.0, +6.2] |
| profiles_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/canonical | stock_exact | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/snapshot | future_joint | 48 | +2.1 [+0.0, +6.2] |
| profiles_v2 | original | sonnet46_thinking/raw | sonnet46_thinking/snapshot | stock_exact | 48 | +1.0 [+0.0, +3.1] |
| profiles_v2 | auto | mini_low_auto/raw | mini_high_auto/raw | future_joint | 48 | +34.4 [+21.9, +46.9] |
| profiles_v2 | auto | mini_low/raw | mini_low_auto/raw | future_joint | 48 | +2.1 [-6.2, +10.4] |
| profiles_v2 | auto | mini_high/raw | mini_high_auto/raw | future_joint | 48 | +28.1 [+16.7, +39.6] |
| profiles_v2 | auto | mini_low_auto/raw | mini_high_auto/raw | stock_exact | 48 | +30.2 [+18.8, +41.7] |
| profiles_v2 | auto | mini_low/raw | mini_low_auto/raw | stock_exact | 48 | +4.2 [-5.2, +13.5] |
| profiles_v2 | auto | mini_high/raw | mini_high_auto/raw | stock_exact | 48 | +18.8 [+7.3, +30.2] |
| profiles_v2 | auto | mini_low_auto/canonical | mini_high_auto/canonical | future_joint | 48 | +12.5 [+4.2, +19.8] |
| profiles_v2 | auto | mini_low/canonical | mini_low_auto/canonical | future_joint | 48 | +35.4 [+24.0, +46.9] |
| profiles_v2 | auto | mini_high/canonical | mini_high_auto/canonical | future_joint | 48 | +65.6 [+56.2, +75.0] |
| profiles_v2 | auto | mini_low_auto/canonical | mini_high_auto/canonical | stock_exact | 48 | +4.2 [-2.1, +10.4] |
| profiles_v2 | auto | mini_low/canonical | mini_low_auto/canonical | stock_exact | 48 | +2.1 [-6.2, +11.5] |
| profiles_v2 | auto | mini_high/canonical | mini_high_auto/canonical | stock_exact | 48 | +61.5 [+51.0, +71.9] |

## Raised-effort canonical error profile

Among mini's wrong canonical starting stocks at high effort, 79 of 83 synthetic and 49 of 62 profile answers are underestimates, with median absolute errors of 32 and 14 units; 57 and 41 are exactly zero although the true stock is positive, 57 and 41 equal the stock obtained by replaying only the demands, and 13 and 13 equal the clipped net total. In twelve re-issued requests with reasoning summaries (diagnostic D1, supplement), the summaries lay out the correct selection and replay procedure, yet several answers are still zero or far too low, and one summary states that it must call the answer tool immediately and considers submitting placeholder zeros. This suggests that, under forced tool choice at raised effort, the model sometimes emits an answer before completing the replay it planned; the traces are illustrative, not a measured mechanism.

{
  "effort_synthetic_v1/mini_medium": {
    "wrong": 64,
    "under": 61,
    "over": 3,
    "zero_stock": 44,
    "demands_only_stock": 44,
    "net_clip": 10,
    "median_abs_error": 25
  },
  "effort_synthetic_v1/mini_high": {
    "wrong": 83,
    "under": 79,
    "over": 4,
    "zero_stock": 57,
    "demands_only_stock": 57,
    "net_clip": 13,
    "median_abs_error": 32
  },
  "effort_profiles_v1/mini_medium": {
    "wrong": 46,
    "under": 33,
    "over": 13,
    "zero_stock": 20,
    "demands_only_stock": 20,
    "net_clip": 10,
    "median_abs_error": 11
  },
  "effort_profiles_v1/mini_high": {
    "wrong": 62,
    "under": 49,
    "over": 13,
    "zero_stock": 41,
    "demands_only_stock": 41,
    "net_clip": 13,
    "median_abs_error": 14
  }
}
