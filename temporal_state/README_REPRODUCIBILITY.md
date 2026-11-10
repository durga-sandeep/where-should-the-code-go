# Anonymous temporal simulation supplement

This package contains a controlled study of report-time cutoffs, revision selection and lost-sales state replay under explicitly supplied future scenarios. Public retail sales profiles supply inputs to synthetic simulations; they are not uncensored demand or authentic correction histories. Preserve the dataset attribution and CC BY 4.0 information in `data/freshretail_SOURCE_README.md` when redistributing profiles.

## Contents and scope

Four final runs are included: `heldout_v2`, `hindsight_v2`, `display_v2`, and `profiles_v2`. Their manifests define the full expected Cartesian grids; `ARTIFACT_MANIFEST.json` at the archive root records exact counts and SHA-256 hashes. Each run includes raw requests/responses or recorded failures, manifest, analysis, and frozen source files. Failures remain part of the denominators. Final paired-control summaries, independent audit, anonymous manuscript, generated tables and figures are included. Early pilots, development runs, account credentials, billing ledgers and unrelated projects are excluded.

The sibling `completeness_pilot` directory contains only the two transport/import dependencies needed by `run.py`; its old experiments are not part of this study. Do not infer study membership from that transport directory name.

## Offline reproduction

From `temporal_state/` in the extracted archive, Python 3.10 or later is sufficient for the core checks. They do not make model calls:

```sh
python3 run.py --help
python3 -m unittest discover -s . -p 'test_*.py'
python3 audit_results.py --run runs/heldout_v2 --run runs/hindsight_v2 --run runs/display_v2 --run runs/profiles_v2 --output-dir /tmp/temporal-audit
python3 decompose_errors.py --run runs/heldout_v2 --run runs/hindsight_v2 --run runs/display_v2 --run runs/profiles_v2 --output-dir /tmp/temporal-decomposition
python3 audit_overlap.py --output-dir /tmp/temporal-overlap
```

The independent audit reconstructs oracle states, parses original provider responses, verifies scoring, source hashes, request representations and full run grids. Its required result is `passed: true`, zero mismatches, and the total specified by the manifests. Read `audits/final/audit.json` for the packaged audit. It does not validate the realism of synthetic reporting delays.

The decomposition independently parses responses and partitions observable starting-stock/future-rollout consistency. Compare the generated JSON to `audits/decomposition/decomposition.json`; its categories describe outputs, not hidden reasoning. Keep the run order shown above for byte/structure comparisons.

The overlap check is explicitly post-hoc. It uses frozen generators to recreate v2 development tasks, verifies final heldout regeneration, and compares exact public payloads, report-group content without identifiers/display order, profile quantity sequences, and source-store splits. Compare its outputs to `audits/overlap/`. It excludes early v1 development and intentional paired-control/repetition reuse. It is not a near-duplicate or provider-training contamination audit; public sales data may have appeared in model training. No observations are removed or rescored. Packaging regenerates both overlap output files and requires byte-identical results.

To recompute summaries and paired comparisons locally:

```sh
python3 analyze.py runs/heldout_v2
python3 analyze.py runs/hindsight_v2
python3 analyze.py runs/display_v2
python3 analyze.py runs/profiles_v2
python3 compare_controls.py --original runs/heldout_v2 --hindsight runs/hindsight_v2 --display runs/display_v2 --output-dir /tmp/temporal-comparison
python3 build_paper.py
python3 extension_analysis.py
python3 decision_analysis.py
python3 diagnostic_paper.py --decomposition audits/decomposition/decomposition.json --run runs/heldout_v2 --run runs/hindsight_v2 --run runs/display_v2 --run runs/profiles_v2 --output-dir paper
python3 make_figures.py
```

Summary commands rewrite derived files only. Run these in a disposable extracted copy if checking the original hash inventory. Figure regeneration requires Matplotlib. Rebuilding the manuscript requires a LaTeX installation and BibTeX; from `paper/`, run `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex` twice. The submitted PDF and source are already included.

The data subset is already local. Re-fetching it is optional and uses the public Internet, not a model API: `python3 external_data.py --output /tmp/temporal-data`. This requires PyArrow (extraction originally verified with version 23.0.0), downloads only the small pinned evaluation partition, verifies SHA-256, and applies the identifier-only selection described in `external_data.md`. It never recovers latent demand.

## Packaging checks

Before building, set the local environment variable `ARTIFACT_IDENTITY_TERMS` to a comma-separated list of the authors' names, usernames and other identifying terms. This variable must be nonempty; its values are never written into package files or provenance. Avoid saving this private setting in the supplement or shell transcripts distributed with it.

`python3 package_artifact.py --output /tmp/temporal-supplement.zip` uses an explicit file allowlist. It refuses missing final files, incomplete grids, failed audits, identity matches and available environment API credentials. It scans PDF text and metadata using `pdftotext` and `pdfinfo` (Poppler required). Matches are reported by filename/category without printing sensitive values; source and raw responses are never silently modified. It extracts the candidate ZIP, verifies its hash inventory, runs offline tests and the full independent audit, and only then writes the requested archive and SHA-256 sidecar. The allowlist also requires the development gate, execution plan, and final decomposition outputs in `audits/decomposition/`; their absence fails the build rather than producing placeholders.

The extracted check also regenerates every run's analysis and the paired control comparison using their recorded bootstrap settings, and regenerates the decomposition, requiring equality with the archived JSON. It rebuilds manuscript text, tables and diagnostic fragments in the disposable paper directory and requires byte-identical generated assets and provenance; PDFs and figures are not rebuilt in this check. These checks may take several minutes. Verification subprocesses receive neither API-key environment variables nor private identity terms. Only the disposable extracted copy is modified; the archive retains original verified payload bytes. Its hash inventory excludes itself to avoid a circular hash, and the separate `.zip.sha256` covers the entire archive including the inventory.

Package inventory is a reproducibility check, not proof that every possible form of identity leakage is absent; manually inspect the anonymous PDF and source before submission. The identity-literal scan skips provider ciphertext (`encrypted_content` values), which is opaque base64 and can contain short letter sequences by chance; credential scans still cover every byte. Model-provider trace identifiers may remain in original responses. No package creation command uploads data or submits a manuscript.

Actual inference is separate, incurs charges and requires provider credentials. It is unnecessary for reproducing the reported scoring from the included raw outputs. Use each manifest and frozen source snapshot to inspect the exact model settings, tasks, repeats and instructions rather than assuming current runner defaults reproduce historical calls.

## Extension studies: reasoning effort, prospective state-only arms, replication

`protocol_v3_extensions.md` was frozen before these calls; `execution_plan_extensions.json` and `execution_plan_extensions_2.json` record the exact commands, executed sequentially by `run_extension_studies.py` (effort sweep, state-only arms) and `run_extension_studies_2.py` (Amendment 2: GPT-5.4 effort sweep and code-inside arms). The runs `effort_synthetic_v1`, `effort_profiles_v1`, `state_synthetic_v1`, `state_profiles_v1`, `replication_mini_low_v1`, `effort_gpt54_synthetic_v1`, `effort_gpt54_profiles_v1`, `tool_synthetic_v1` and `tool_profiles_v2` (after `tool_profiles_v1` was interrupted by a single provider HTTP 400 and preserved) read their tasks from the archived `heldout_v2` and `profiles_v2` manifests, so every history is byte-identical to the original cohorts. State-only arms (`state_raw`, `state_canonical`) use a two-integer schema; each episode stores the two-field `answer`, the code-continued `hybrid_answer`, and the ordinary five-field `score` of the hybrid. Code-inside arms (`tool_raw`, `tool_canonical`) add the provider's hosted `code_interpreter` tool with automatic tool choice; `code_interpreter_call` items in the stored response show whether code ran. Container charges are billed by the provider per session and are not in the token ledger. `diagnose_effort_traces.py --execute` re-issued twelve failing high-effort canonical requests with a detailed reasoning summary (exploratory diagnostic D1); its outputs under `audits/effort_traces/` are illustrative and excluded from every estimate.

```sh
python3 extension_analysis.py
python3 decision_analysis.py --no-figure
```

`extension_analysis.py` reparses every response of the original and extension runs independently of stored scores, verifies the full planned grids and task identity with the source cohorts, rebuilds hybrid answers with a separate scenario simulator, checks the conservation identity on every hybrid answer, and writes `audits/extensions/extensions.json`, `extensions.md` and the `paper/extension_*.tex` fragments. Its required result is `audit_passed: true`. `decision_analysis.py` places every valid original answer in a state category relative to the schedule's stockout threshold, verifies the threshold identity exhaustively against replay, and writes `audits/decision/` plus `paper/decision_findings.tex`; without `--no-figure` it also renders `paper/figures/decision_margins.{pdf,png}` (Matplotlib required). Packaging regenerates both analyses and all their manuscript fragments byte for byte. Use `--output-dir`/`--paper-dir` to write elsewhere when checking hashes.

## Amendment 4: interface-matched cells, Haiku 4.5, and the open-weight ladder

`protocol_v4_extensions.md` was frozen before these calls and carries fifteen dated transport notes; notes 1–14 were each appended before the rerun they describe, and note 15 is an arithmetic correction to the frozen request count recorded after all runs. `run_extension_studies_3.py` executed the stages sequentially and `execution_plan_extensions_3.json` records every dispatch. Runs: `auto_mini_synthetic_v2`, `auto_mini_high_synthetic_v2`, `auto_gpt54_synthetic_v1`, `auto_gpt54_high_synthetic_v1`, `auto_profiles_v1`, `auto_high_profiles_v1` (E6, GPT-5.4 mini and GPT-5.4 under automatic tool choice); `haiku_synthetic_v1`, `haiku_profiles_v1` (E7); `open_synthetic_low_auto_v3`, `open_synthetic_high_auto_v2`, `open_synthetic_forced_v1`, `open_profiles_low_auto_v1`, `open_profiles_high_auto_v1`, `open_profiles_forced_v2` (E8, six open-weight models in a requested-effort by tool-choice cross); `replication_gpt54_low_synthetic_v1` (E6b, same-period GPT-5.4 forced-call baseline). All read their tasks from the archived `heldout_v2` and `profiles_v2` manifests.

Open-weight models are called through OpenRouter's chat-completions endpoint (`provider: openrouter` in `run.py`), each pinned to one upstream with fallbacks disabled and `require_parameters` set; the served provider is stored in every response and checked by `audit_results.py` and `ladder_analysis.py`. Because third-party upstreams rate-limit, the open-weight stages ran with `--transport-tolerant`: HTTP 429/5xx (including an error body inside an HTTP 200 response) is retried with bounded backoff before any completion exists, attempt counts are stored per record as `transport_attempts`, episodes that exhaust their attempts are moved to `transport_failures/` and re-issued with identical payloads in numbered completion passes (`completion_passes.json`, `completion_runs.json`), and a model output is never re-sampled. Interrupted grids (`open_synthetic_low_auto_v1`, `open_synthetic_low_auto_v2`, `open_synthetic_high_auto_v1`, `open_profiles_forced_v1`) and the smoke checks are preserved in the repository and excluded from every estimate; they are not in the supplement. Qwen3.8-27B's provider withdrew the model before the forced-call profile stage, so those four cells were not run.

```sh
python3 ladder_analysis.py
```

`ladder_analysis.py` reuses the extension loaders (independent reparsing, replay, hybrid rebuild, grid and task identity checks), computes the prespecified Amendment 4 comparisons (placement gains under one interface, interface effect, effort effect per interface, and their difference as the interaction, all paired by history with 10,000-draw history-bootstrap intervals), summarizes transport attempts and served providers, classifies missing answers by kind from the raw responses, and writes `audits/ladder/ladder.json`, `ladder.md` and the `paper/ladder_*.tex` and `paper/interaction_*.tex` fragments. Its required result is `audit_passed: true`. Packaging regenerates it byte for byte.

## Post-hoc executable continuation

`python3 continuation_analysis.py` reparses all four final cohorts and evaluates exact future execution from each valid original model-emitted stock. It writes `audits/continuation/continuation.json`, `continuation.md`, and the four `paper/continuation_*.tex` fragments. Use `--output-dir /tmp/temporal-continuation --paper-dir /tmp/temporal-continuation-paper` to avoid rewriting derived artifacts in place. Bootstrap defaults are 10,000 draws with seed 20260907; these settings are recorded in the JSON and replayed by packaging.

This analysis was added after results in response to skeptical review. It keeps original five-field prompts, the full validity gate, all repetitions, all configurations, all arms, and all cohorts. Invalid answers fail both accuracy endpoints. The original planned decomposition is unchanged. The new comparison is an offline transformation of existing answers, not a new state-only prompt experiment or measured code-agent deployment. False/missed-stockout counts condition on valid answers and preserve their separate denominators. Regressions, including accidentally correct future answers paired with wrong stock, remain explicit. The exact code-continuation endpoint equals emitted-stock accuracy by conservation; it is not new independent evidence of temporal reasoning. Packaging reproduces both analysis files and all four manuscript fragments byte for byte.
