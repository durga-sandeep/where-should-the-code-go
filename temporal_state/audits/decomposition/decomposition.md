# Observable temporal error decomposition

Prespecified analysis amendment before heldout model outcomes. This partitions reported answers; it does not identify hidden reasoning or causal error paths. Future outputs are replayed from the model-emitted stock, independently of historical-lost correctness.

## heldout_v2

| Configuration | Arm | Valid / total | Stock right, future right | Stock right, future wrong | Both wrong, consistent | Both wrong, inconsistent | Stock wrong, future right |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 192/192 | 189 | 2 | 1 | 0 | 0 |
| gpt54_low | raw | 192/192 | 169 | 6 | 7 | 10 | 0 |
| gpt54_low | snapshot | 192/192 | 190 | 2 | 0 | 0 | 0 |
| mini_low | canonical | 192/192 | 146 | 23 | 9 | 14 | 0 |
| mini_low | raw | 192/192 | 72 | 25 | 50 | 45 | 0 |
| mini_low | snapshot | 192/192 | 172 | 20 | 0 | 0 | 0 |
| sonnet46 | canonical | 192/192 | 191 | 1 | 0 | 0 | 0 |
| sonnet46 | raw | 192/192 | 190 | 1 | 1 | 0 | 0 |
| sonnet46 | snapshot | 192/192 | 192 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | canonical | 192/192 | 192 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | raw | 192/192 | 188 | 2 | 2 | 0 | 0 |
| sonnet46_thinking | snapshot | 192/192 | 192 | 0 | 0 | 0 | 0 |

Categories partition valid outputs. Invalids remain outside the partition. Historical-loss errors, stockout-detection denominators and up to three consistently wrong examples per cell are in `decomposition.json`.

## hindsight_v2

| Configuration | Arm | Valid / total | Stock right, future right | Stock right, future wrong | Both wrong, consistent | Both wrong, inconsistent | Stock wrong, future right |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 48/48 | 48 | 0 | 0 | 0 | 0 |
| gpt54_low | raw | 48/48 | 44 | 1 | 2 | 1 | 0 |
| gpt54_low | snapshot | 48/48 | 48 | 0 | 0 | 0 | 0 |
| mini_low | canonical | 48/48 | 31 | 8 | 4 | 5 | 0 |
| mini_low | raw | 48/48 | 27 | 4 | 9 | 8 | 0 |
| mini_low | snapshot | 48/48 | 44 | 4 | 0 | 0 | 0 |
| sonnet46 | canonical | 48/48 | 47 | 1 | 0 | 0 | 0 |
| sonnet46 | raw | 48/48 | 44 | 1 | 3 | 0 | 0 |
| sonnet46 | snapshot | 48/48 | 48 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | canonical | 48/48 | 48 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | raw | 48/48 | 48 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | snapshot | 48/48 | 48 | 0 | 0 | 0 | 0 |

Categories partition valid outputs. Invalids remain outside the partition. Historical-loss errors, stockout-detection denominators and up to three consistently wrong examples per cell are in `decomposition.json`.

## display_v2

| Configuration | Arm | Valid / total | Stock right, future right | Stock right, future wrong | Both wrong, consistent | Both wrong, inconsistent | Stock wrong, future right |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | raw | 48/48 | 41 | 0 | 5 | 2 | 0 |
| mini_low | raw | 48/48 | 23 | 0 | 8 | 17 | 0 |
| sonnet46 | raw | 48/48 | 45 | 0 | 3 | 0 | 0 |
| sonnet46_thinking | raw | 48/48 | 48 | 0 | 0 | 0 | 0 |

Categories partition valid outputs. Invalids remain outside the partition. Historical-loss errors, stockout-detection denominators and up to three consistently wrong examples per cell are in `decomposition.json`.

## profiles_v2

| Configuration | Arm | Valid / total | Stock right, future right | Stock right, future wrong | Both wrong, consistent | Both wrong, inconsistent | Stock wrong, future right |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt54_low | canonical | 96/96 | 88 | 8 | 0 | 0 | 0 |
| gpt54_low | raw | 96/96 | 87 | 0 | 3 | 6 | 0 |
| gpt54_low | snapshot | 96/96 | 95 | 1 | 0 | 0 | 0 |
| mini_low | canonical | 96/96 | 45 | 42 | 1 | 8 | 0 |
| mini_low | raw | 95/96 | 11 | 3 | 49 | 31 | 1 |
| mini_low | snapshot | 96/96 | 86 | 10 | 0 | 0 | 0 |
| sonnet46 | canonical | 96/96 | 95 | 1 | 0 | 0 | 0 |
| sonnet46 | raw | 96/96 | 92 | 1 | 3 | 0 | 0 |
| sonnet46 | snapshot | 96/96 | 96 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | canonical | 96/96 | 96 | 0 | 0 | 0 | 0 |
| sonnet46_thinking | raw | 96/96 | 94 | 1 | 1 | 0 | 0 |
| sonnet46_thinking | snapshot | 96/96 | 96 | 0 | 0 | 0 | 0 |

Categories partition valid outputs. Invalids remain outside the partition. Historical-loss errors, stockout-detection denominators and up to three consistently wrong examples per cell are in `decomposition.json`.

“Consistent” means the future triple exactly equals deterministic replay from the emitted starting stock. It does not prove the model used that stock internally. “Stock wrong, future right” is an observable masking/recovery pattern, not evidence of intentional recovery. Stockout-detection rates are conditional on valid contracts and do not measure timing accuracy.
