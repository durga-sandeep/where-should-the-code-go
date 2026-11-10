# Where Should the Code Go? Locating Foundation-Model Errors in Bitemporal Inventory Simulation

Code, data and every model request and response for the paper

> Durga Sandeep Saluru, Lanchen Song, Aditya Kumaran. *Where Should the Code Go? Locating Foundation-Model Errors in Bitemporal Inventory Simulation.* NeurIPS 2026 Workshop on Foundation Models for Temporal Systems (FMTS), poster.

The study asks where exact code should sit around a foundation-model component that reconstructs inventory state from late and revised reports and then rolls a supplied schedule forward: before the model (canonical input, exact snapshot), after it (state-only hybrid), inside the call (a code tool), or nowhere (more reasoning effort). The environment is exactly solvable, so every intermediate quantity has an executable ground truth.

## What is here

| Path | Contents |
|---|---|
| `temporal_state/runs/` | 36,672 scored requests: raw provider request and response (or recorded failure) per call, per-run manifests, analyses and frozen source snapshots |
| `temporal_state/*.py` | Environment generator (`benchmark.py`), runner (`run.py`), analyses, independent audit, packaging |
| `temporal_state/protocol*.md` | Protocols and amendments, each written before its calls |
| `temporal_state/audits/` | Independent re-parse and re-score of every response (zero mismatches), decomposition and overlap checks |
| `temporal_state/data/` | FreshRetailNet-50K profile subset with its original source card |
| `temporal_state/paper/` | LaTeX source, generated tables and the camera-ready PDF |
| `completeness_pilot/` | Two transport and import helpers that `run.py` depends on; not part of the study |
| `ARTIFACT_MANIFEST.json` | SHA-256 hash and episode count for every packaged file |

## Reproducing the results

Nothing below calls a model API. From `temporal_state/`, with Python 3.10 or later:

```sh
python3 -m unittest discover -s . -p 'test_*.py'
python3 audit_results.py --run runs/heldout_v2 --run runs/hindsight_v2 --run runs/display_v2 --run runs/profiles_v2 --output-dir /tmp/temporal-audit
python3 ladder_analysis.py --output-dir /tmp/ladder --paper-dir /tmp/ladder-paper --bootstrap 10000 --seed 20260908
```

`temporal_state/README_REPRODUCIBILITY.md` documents every analysis command, the audit, and how the package was built and verified. It was first written for the anonymous review supplement, which is why its title says "anonymous".

Re-running inference is not needed to reproduce the scores, costs money, and needs your own provider credentials. Each run's manifest and frozen `source/` snapshot record the exact models, settings, prompts and tasks used.

## Licenses

- **Code:** MIT (`LICENSE`).
- **Data, model outputs, protocols and paper text:** CC BY 4.0 (`LICENSE-DATA`).
- **FreshRetailNet-50K profiles:** derived from the dataset by Dingdong-Inc and Wang et al. (2025, arXiv:2505.16319) under CC BY 4.0; keep the attribution in `temporal_state/data/freshretail_SOURCE_README.md` when redistributing.

Model responses were produced by OpenAI, Anthropic and open-weight models served through OpenRouter. Reasoning fields marked `encrypted_content` or `signature` are opaque provider ciphertext.

## Citation

See `CITATION.cff`, or:

```bibtex
@inproceedings{saluru2026wherecode,
  title     = {Where Should the Code Go? Locating Foundation-Model Errors in Bitemporal Inventory Simulation},
  author    = {Saluru, Durga Sandeep and Song, Lanchen and Kumaran, Aditya},
  booktitle = {NeurIPS 2026 Workshop on Foundation Models for Temporal Systems},
  year      = {2026}
}
```
