# Temporal reconstruction and conditional inventory simulation — protocol v1

Locally frozen before the development API pilot on September 7, 2026. This is not an externally registered protocol. The previous static-count study remains separate.

## Question and workshop connection

Can general-purpose foundation models correctly reconstruct state from delayed and revised event reports, and do reconstruction errors propagate into a known future scenario? This studies temporal-system simulation and reliability, not forecasting unknown demand. Inventory obeys noncommutative lost-sales dynamics: demand is fulfilled only from stock on hand; unmet demand is lost. Reordering transactions can change both current state and accumulated loss.

Bitemporal QA, temporal benchmarks, inventory control, and deterministic replay already exist. The intended contribution is a narrowly controlled empirical decomposition between report visibility/revision handling, historical replay, and downstream rollout. It is not a new temporal algorithm or inventory optimization method. FMTS fit depends on substantive simulation results, not adopting the template.

## Public semantics

Target event time T=100; knowledge cutoff K=100; future scenario horizon H=130. Reports have logical event IDs, revisions, event time, received time, receipt/demand kind, and integer quantity. Filter received_time<=K BEFORE choosing the largest visible revision per event ID. Revisions replace earlier reports. Then filter event_time<=T and replay by (event_time,event_id). Events absent at K are not inferred. All histories start from explicit initial_stock. The future schedule is a completely specified hypothetical sequence, not a withheld real future.

Outputs: stock_at_target, historical_lost, stock_at_horizon, future_lost, first_future_stockout_time (-1 for no unmet future demand). First stockout refers to strictly positive unmet demand, not zero inventory. Outputs must be exactly five integers with no additional fields; invalid contracts fail primary endpoints.

## Data and preprocessing interventions

Independent seeds: development2026090801 and heldout2026090802. Balanced 3×2×2 conditions: 12/36/72 logical historical events; immediate vs delayed initial reports; absent vs present corrections. Immediate original reports arrive at event time. In delayed conditions, 25% of initial reports arrive after K and other reports have bounded lag. Corrections independently add delay, including some revisions unavailable at K. Thus factor labels concern original reports and corrections separately, not a claim all reports are immediate in a correction-present cell. Event kinds, quantities, IDs, and times are seeded without model-outcome selection. Half the historical logical events are receipts; future schedules contain six receipts and six demands over twelve timestamps.

Same latent task and same five-field answer schema across three arms:

- **Raw:** all report versions in received-time display order. The model resolves visibility, revisions, event chronology, history, and future scenario.
- **Canonical:** executable preprocessing selects visible latest versions and orders eligible events. The model performs historical and future simulation.
- **Snapshot:** executable replay supplies exact stock_at_target and historical_lost. The model performs the future rollout and copies the supplied historical quantities.

These are deployable system decompositions with different input sizes and work allocation, not equal-token model mechanisms. A full deterministic replay+rollout baseline solves all generated tasks without an LLM. Snapshot is an explicit exact-state intervention, not model-discovered evidence. No algorithmic improvement over deterministic replay is claimed.

## Models, development gate, and heldout plan

Use GPT-5.4 mini low reasoning, GPT-5.4 low reasoning, and Sonnet4.6 without extended thinking, exact IDs recorded in manifest. All use strict tool schemas, 8192 maximum output tokens, provider default sampling, one request per trial, no retry/repair. Shared research budget ceiling is $3000; this study need not approach it.

Development pilot: 12 bases, three models, three arms, one repetition =108 requests. Inspect infrastructure validity, task ambiguity, ceiling/floor effects, and whether the hypothesized decomposition is observable. Any design/prompt changes after pilot must be recorded before heldout launch; development outcomes are excluded from heldout estimates. Do not expand merely to accumulate trials.

If supported, heldout:96 bases (8 per factorial cell), three models, three arms, two repetitions =1728 requests. Primary endpoint is joint exactness of all five fields. Also report historical joint (first two) and future joint (last three), individual fields, future error conditional on correct historical fields, invalids, and costs. All configurations and arms are reported. Paired raw→canonical and raw→snapshot differences average repetitions within each base and use10,000 base-bootstrap percentile intervals. Factor strata are descriptive; distinct factor cells are not matched counterfactuals. Intervals are unadjusted and do not establish internal mechanisms.

## Before expansion

Unit tests compare an independently implemented replay, visibility-before-revision ordering, correction replacement, path dependence, future-only stockout semantics, strict output types, source immutability, and harmless display permutations. Offline naive arrival-order and latest-without-cutoff baselines characterize shortcuts without selecting tasks. Paid display-order counterfactual checks and external operational profiles require a separately frozen addendum.

Synthetic histories do not establish performance on real operational corrections or general forecasting. The benchmark's exact rules and explicit scenario simplify deployment substantially. Model errors may combine arithmetic, attention, temporal selection, and output errors; the interventions isolate system stages, not hidden model cognition.
