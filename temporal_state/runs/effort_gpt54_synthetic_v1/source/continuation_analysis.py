"""Post-hoc executable continuation of original five-field answers. No API calls."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import analyze
import decompose_errors as decomposition

ROOT = Path(__file__).resolve().parent
RUNS = ('heldout_v2', 'hindsight_v2', 'display_v2', 'profiles_v2')
CONFIGS = ('mini_low', 'gpt54_low', 'sonnet46', 'sonnet46_thinking')
ARMS = ('raw', 'canonical', 'snapshot')
LABELS = ('GPT-5.4 mini (low)', 'GPT-5.4 (low)', 'Sonnet 4.6', 'Sonnet + thinking')


def evaluate(task, answer):
    d = decomposition.classify(task, answer)
    if not d['valid']:
        return {'valid': False, 'model_future': False, 'code_future': False}
    gold = {k: d['truth'][k] for k in decomposition.FUTURE}
    code_correct = d['future_from_emitted_stock'] == gold
    # Conservation makes exact code continuation equivalent to correct stock.
    if code_correct != d['stock_correct']:
        raise ValueError('Continuation violates starting-stock equivalence')
    return {'valid': True, 'model_future': d['future_correct'], 'code_future': code_correct,
            'gold_stockout': d['gold_stockout'], 'model_stockout': d['predicted_stockout'],
            'code_stockout': d['future_from_emitted_stock']['first_future_stockout_time'] >= 0}


def summary(rows, draws, seed):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['base_id']].append(int(row['code_future']) - int(row['model_future']))
    differences = [sum(v) / len(v) for _, v in sorted(grouped.items())]
    valid = [r for r in rows if r['valid'] and 'gold_stockout' in r]
    stockouts = {}
    for method in ('model', 'code'):
        stockouts[method] = {
            'false': sum(not r['gold_stockout'] and r[method + '_stockout'] for r in valid),
            'negative': sum(not r['gold_stockout'] for r in valid),
            'missed': sum(r['gold_stockout'] and not r[method + '_stockout'] for r in valid),
            'positive': sum(r['gold_stockout'] for r in valid)}
    return {'n': len(rows), 'bases': len(grouped), 'stockout_detection': stockouts,
            'invalid': sum(not r['valid'] for r in rows),
            'model_future': sum(r['model_future'] for r in rows),
            'code_future': sum(r['code_future'] for r in rows),
            'corrected': sum(r['code_future'] and not r['model_future'] for r in rows),
            'regressed': sum(r['model_future'] and not r['code_future'] for r in rows),
            'difference': sum(differences) / len(differences),
            'ci95': analyze.bootstrap(differences, draws, seed)}


def run_analysis(path, draws, seed):
    # Reparse provider responses and verify full grid before computing the new view.
    checked = decomposition.analyze_run(path)
    manifest = json.loads((path / 'manifest.json').read_text())
    tasks = {t['base_id']: t for t in manifest['tasks']}
    groups = defaultdict(list)
    for filename in sorted(checked['provenance']['episode_files_sha256']):
        row = json.loads((path / filename).read_text())
        answer, _ = decomposition.audit.parse_answer(row, manifest['configs'][row['configuration']]['provider'])
        groups[row['configuration'], row['arm']].append(
            {'base_id': row['base_id'], 'rep': row['rep'], **evaluate(tasks[row['base_id']], answer)})
    cells = [{'configuration': c, 'arm': a, **summary(rows, draws, seed)}
             for (c, a), rows in sorted(groups.items())]
    # Cross-check new counts against the independently regenerated planned partition.
    for cell, prior in zip(cells, checked['cells']):
        cats = prior['categories']
        assert (cell['configuration'], cell['arm']) == (prior['configuration'], prior['arm'])
        assert cell['code_future'] == cats['stock_correct_future_correct'] + cats['stock_correct_future_wrong']
        assert cell['model_future'] == cats['stock_correct_future_correct'] + cats['stock_wrong_future_correct']
    return {'run': path.name, 'episodes': checked['episodes'], 'cells': cells,
            'provenance': checked['provenance']}


def table(result, arms, label):
    lookup = {(r['run'], c['configuration'], c['arm']): c for r in result['runs'] for c in r['cells']}
    lines = ['\\begin{table}[htbp]', '\\centering\\small',
             '\\begin{tabular}{llrr}', '\\toprule',
             'Configuration & Input & Synthetic & Retail profiles \\\\', '\\midrule']
    for cfg, name in zip(CONFIGS, LABELS):
        for arm in arms:
            values = []
            for run in ('heldout_v2', 'profiles_v2'):
                c = lookup[run, cfg, arm]
                values.append(f"{100*c['model_future']/c['n']:.1f} / {100*c['code_future']/c['n']:.1f}")
            lines.append(' & '.join((name, arm, *values)) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Post-hoc future-joint accuracy (\\%): original model rollout / executable continuation from its emitted stock. '
              'Synthetic and profile cells contain 192 and 96 original calls, respectively. '
              'Invalid five-field answers fail both endpoints. No state-only prompts were run; full-code replay is exact on every task.}',
              '\\label{' + label + '}', '\\end{table}', '']
    return '\n'.join(lines)


def abstract_finding(result):
    cell = next(c for r in result['runs'] if r['run'] == 'profiles_v2'
                for c in r['cells'] if c['configuration'] == 'mini_low' and c['arm'] == 'canonical')
    return (f"A post-hoc executable continuation of mini's emitted stock improves canonical-profile future accuracy from {100*cell['model_future']/cell['n']:.1f} to {100*cell['code_future']/cell['n']:.1f}\\%, "
            "showing substantial residual rollout error after event selection.\n")


def findings(result):
    lookup = {(r['run'], c['configuration'], c['arm']): c for r in result['runs'] for c in r['cells']}
    clauses = []
    for run, name in (('heldout_v2', 'synthetic histories'), ('profiles_v2', 'retail profiles')):
        c = lookup[run, 'mini_low', 'canonical']
        lo, hi = c['ci95']
        clauses.append(f"{100*c['model_future']/c['n']:.1f} to {100*c['code_future']/c['n']:.1f}\\% on {name} "
                       f"({100*c['difference']:+.1f} points; 95\\% base-bootstrap interval [{100*lo:+.1f}, {100*hi:+.1f}])")
    return ('After canonicalization, replacing the emitted future triple with exact continuation improves mini from '
            + '; '.join(clauses) + '. '
            'Thus correct event selection can leave substantial future-rollout error even when the emitted stock is correct. '
            'This offline comparison retains the original prompts and validity gate; it does not measure a separately prompted state-estimation pipeline.\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'continuation')
    p.add_argument('--paper-dir', type=Path, default=ROOT / 'paper')
    p.add_argument('--bootstrap', type=int, default=10000)
    p.add_argument('--seed', type=int, default=20260907)
    a = p.parse_args()
    result = {'analysis': 'post_hoc_executable_continuation', 'bootstrap_draws': a.bootstrap, 'seed': a.seed,
              'notes': ['Added after final study outcomes; all configurations, arms, cohorts and invalid contracts retained.',
                        'Original model answer versus exact future replay from its emitted stock; no new prompts, repairs or provider calls.',
                        'The full original five-field validity gate applies to both endpoints, even when the stock alone is usable.',
                        'Correct code-continuation future triple is equivalent to correct stock by conservation; this is not independent evidence of temporal reasoning.',
                        'Repetitions averaged within base; descriptive percentile intervals are not multiplicity adjusted.',
                        'Code continuation may discard accidentally correct future answers paired with wrong stock; regressions are explicitly counted.',
                        'Full-code historical replay plus future rollout is the exact practical baseline, not a model competitor to outperform.'],
              'runs': [run_analysis(ROOT / 'runs' / run, a.bootstrap, a.seed) for run in RUNS]}
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / 'continuation.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Post-hoc executable continuation', '', *['- ' + n for n in result['notes']], '',
             '| Cohort | Configuration | Arm | N | Model correct | Code correct | Corrected / regressed | Difference [95% CI], pp |',
             '| --- | --- | --- | ---: | ---: | ---: | ---: | --- |']
    for r in result['runs']:
        for c in r['cells']:
            lo, hi = c['ci95']
            lines.append(f"| {r['run']} | {c['configuration']} | {c['arm']} | {c['n']} | {c['model_future']} | {c['code_future']} | {c['corrected']} / {c['regressed']} | {100*c['difference']:+.1f} [{100*lo:+.1f}, {100*hi:+.1f}] |")
    lines += ['', '| Cohort | Configuration | Arm | Model false / negatives | Code false / negatives | Model missed / positives | Code missed / positives |',
              '| --- | --- | --- | ---: | ---: | ---: | ---: |']
    for r in result['runs']:
        for cell in r['cells']:
            m, c = (cell['stockout_detection'][k] for k in ('model', 'code'))
            lines.append(f"| {r['run']} | {cell['configuration']} | {cell['arm']} | {m['false']}/{m['negative']} | {c['false']}/{c['negative']} | {m['missed']}/{m['positive']} | {c['missed']}/{c['positive']} |")
    (a.output_dir / 'continuation.md').write_text('\n'.join(lines) + '\n')
    a.paper_dir.mkdir(parents=True, exist_ok=True)
    for name, value in {'continuation_table.tex': table(result, ('canonical',), 'tab:continuation'),
                        'continuation_full_table.tex': table(result, ARMS, 'tab:continuationfull'),
                        'continuation_findings.tex': findings(result),
                        'continuation_abstract.tex': abstract_finding(result)}.items():
        (a.paper_dir / name).write_text(value)
    print(json.dumps({'complete': True, 'episodes': sum(r['episodes'] for r in result['runs'])}))


if __name__ == '__main__':
    main()
