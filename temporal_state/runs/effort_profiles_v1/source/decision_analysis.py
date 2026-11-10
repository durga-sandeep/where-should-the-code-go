"""Post-hoc decision-consequence analysis of the original cohorts. Offline; no API calls.

For each supplied future schedule, any future lost demand occurs exactly when the
starting stock is below the schedule's peak cumulative net demand B. This lets each
valid answer be placed in one of three state categories: exact stock, wrong stock on
the same side of B as the truth (decision-equivalent), or wrong stock across B. The
model's own binary stockout decision and the decision implied by exact code
continuation from its emitted stock are then compared within each category.

The threshold identity is elementary inventory algebra, verified here exhaustively
against independent replay; the empirical content is where the responses fall.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import audit_results as audit
import decompose_errors as decomposition

ROOT = Path(__file__).resolve().parent
RUNS = ('heldout_v2', 'hindsight_v2', 'display_v2', 'profiles_v2')
MAIN = ('heldout_v2', 'profiles_v2')
CONFIGS = ('mini_low', 'gpt54_low', 'sonnet46', 'sonnet46_thinking')
LABELS = {'mini_low': 'GPT-5.4 mini (low)', 'gpt54_low': 'GPT-5.4 (low)', 'sonnet46': 'Sonnet 4.6', 'sonnet46_thinking': 'Sonnet + thinking'}
CATEGORIES = ('exact', 'same_side', 'crossing')


def threshold(task):
    """Peak prefix net demand B (>=0) and terminal net demand of the supplied schedule."""
    net = peak = 0
    for event in sorted(task['future_schedule'], key=lambda e: (e['event_time'], e['event_id'])):
        net += event['quantity'] * (1 if event['kind'] == 'demand' else -1)
        peak = max(peak, net)
    return peak, net


def verify_threshold(task, limit_extra=3):
    """Exhaustively check the identity against independent replay for every stock through B+extra."""
    B, net = threshold(task)
    truth, _ = audit.replay(task)
    checks = 0
    for start in range(max(B, truth['stock_at_target']) + limit_extra):
        replayed = decomposition.future_from_stock(task, start)
        if (start < B) != (replayed['first_future_stockout_time'] >= 0):
            raise ValueError('Threshold identity violated')
        if replayed['future_lost'] != max(0, B - start) or replayed['stock_at_horizon'] != start - net + max(0, B - start):
            raise ValueError('Loss/terminal identity violated')
        checks += 1
    return checks


def classify_response(task, answer):
    d = decomposition.classify(task, answer)
    if not d['valid']:
        return {'valid': False}
    B, _ = threshold(task)
    s = d['truth']['stock_at_target']
    emitted = answer['stock_at_target']
    gold = s < B
    code = emitted < B
    if code != (d['future_from_emitted_stock']['first_future_stockout_time'] >= 0):
        raise ValueError('Code decision disagrees with replay')
    model = d['predicted_stockout']
    category = 'exact' if emitted == s else ('same_side' if code == gold else 'crossing')
    return {'valid': True, 'category': category, 'gold_stockout': gold, 'model_wrong': model != gold,
            'code_wrong': code != gold, 'stock_error': emitted - s, 'margin': s - B}


def summarize(items):
    valid = [x for x in items if x['valid']]
    out = {'n': len(items), 'valid': len(valid), 'invalid': len(items) - len(valid),
           'model_wrong': sum(x['model_wrong'] for x in valid), 'code_wrong': sum(x['code_wrong'] for x in valid),
           'corrected': sum(x['model_wrong'] and not x['code_wrong'] for x in valid),
           'harmed': sum(not x['model_wrong'] and x['code_wrong'] for x in valid),
           'wrong_stock': sum(x['category'] != 'exact' for x in valid),
           'model_false_alarms': sum(x['model_wrong'] and not x['gold_stockout'] for x in valid),
           'model_misses': sum(x['model_wrong'] and x['gold_stockout'] for x in valid),
           'positives': sum(x['gold_stockout'] for x in valid), 'negatives': sum(not x['gold_stockout'] for x in valid)}
    for cat in CATEGORIES:
        sub = [x for x in valid if x['category'] == cat]
        out[cat] = {'n': len(sub), 'model_wrong': sum(x['model_wrong'] for x in sub), 'code_wrong': sum(x['code_wrong'] for x in sub)}
    # Structural facts, asserted rather than reported as discoveries.
    if out['exact']['code_wrong'] or out['same_side']['code_wrong'] or out['crossing']['code_wrong'] != out['crossing']['n']:
        raise ValueError('Category definition violated')
    return out


def analyze():
    cells = {}
    per_run = {}
    checks = 0
    provenance = {}
    for run in RUNS:
        path = ROOT / 'runs' / run
        checked = decomposition.analyze_run(path)
        manifest = json.loads((path / 'manifest.json').read_text())
        tasks = {t['base_id']: t for t in manifest['tasks']}
        provenance[run] = {'manifest_sha256': checked['provenance']['manifest_sha256'], 'episodes': checked['episodes'],
                           'episode_hashes_digest': hashlib.sha256(json.dumps(checked['provenance']['episode_files_sha256'], sort_keys=True).encode()).hexdigest()}
        for task in tasks.values():
            checks += verify_threshold(task)
        groups = defaultdict(list)
        for filename in checked['provenance']['episode_files_sha256']:
            row = json.loads((path / filename).read_text())
            answer, _ = audit.parse_answer(row, manifest['configs'][row['configuration']]['provider'])
            groups[row['configuration'], row['arm']].append(classify_response(tasks[row['base_id']], answer))
        per_run[run] = {f'{c}/{a}': summarize(items) for (c, a), items in sorted(groups.items())}
        for (c, a), items in groups.items():
            cells[run, c, a] = items
    pooled = {}
    for label, cfgs, arms in (('mini_main_raw_canonical', ('mini_low',), ('raw', 'canonical')),
                              ('all_configs_main_raw_canonical', CONFIGS, ('raw', 'canonical')),
                              ('all_configs_all_cohorts_all_arms', CONFIGS, ('raw', 'canonical', 'snapshot'))):
        runs = RUNS if 'all_cohorts' in label else MAIN
        items = [x for (r, c, a), v in cells.items() if r in runs and c in cfgs and a in arms for x in v]
        pooled[label] = summarize(items)
    return {'analysis': 'post_hoc_decision_consequences', 'threshold_checks': checks, 'provenance': provenance,
            'cells': per_run, 'pooled': pooled,
            'notes': ['Post hoc: conceived after the original outcomes; all cohorts, configurations, arms and invalid answers retained.',
                      'B is the peak prefix cumulative net demand of the supplied schedule; any future loss occurs iff starting stock < B. Verified exhaustively against independent replay.',
                      'Code decisions are zero-error by definition in the exact and same-side categories and always wrong in the crossing category; the empirical content is the category sizes and the model decisions.',
                      'Responses share histories and repetitions; counts are descriptive, not independent samples.',
                      'Binary decision correctness ignores quantity and timing errors and does not make an answer operationally sufficient.']}


def findings(result):
    p = result['pooled']['mini_main_raw_canonical']
    q = result['pooled']['all_configs_main_raw_canonical']
    same = p['same_side']['n']
    wrong = p['wrong_stock']
    dec_ok = p['exact']['model_wrong'] + p['same_side']['model_wrong']
    return (f"Pooling GPT-5.4 mini's raw and canonical answers on both main cohorts ({p['valid']} valid of {p['n']}), "
            f"{same} of {wrong} wrong starting stocks ({100 * same / wrong:.0f}\\%) lie on the same side of the stockout threshold as the truth, so exact continuation from them still yields the correct binary decision; "
            f"conversely, {dec_ok} of the model's {p['model_wrong']} wrong stockout decisions ({100 * dec_ok / p['model_wrong']:.0f}\\%) occur with decision-sufficient state, {p['exact']['model_wrong']} of them with exactly correct stock. "
            f"Exact continuation corrects {p['corrected']} model decisions and damages {p['harmed']}; every damaged case pairs a threshold-crossing stock with a model decision that was inconsistent with that stock yet accidentally right. "
            f"Across all four configurations on the same cells, {q['model_wrong']} decisions are wrong among {q['valid']} valid answers, and {q['exact']['model_wrong'] + q['same_side']['model_wrong']} of those occur with decision-sufficient state.\n")


def figure(result, outdir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams.update({'font.size': 7.5, 'axes.titlesize': 8, 'pdf.fonttype': 42, 'font.family': 'DejaVu Sans'})
    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.0), sharex=True)
    colors = {'model': '#2166AC', 'code': '#B45F06'}
    panels = [('heldout_v2', 'raw', 'Synthetic, raw'), ('heldout_v2', 'canonical', 'Synthetic, canonical'),
              ('profiles_v2', 'raw', 'Profiles, raw'), ('profiles_v2', 'canonical', 'Profiles, canonical')]
    names = {'exact': 'Exact stock', 'same_side': 'Wrong stock,\nsame side', 'crossing': 'Wrong stock,\ncrosses'}
    for ax, (run, arm, title) in zip(axes, panels):
        c = result['cells'][run][f'mini_low/{arm}']
        for y, cat in enumerate(CATEGORIES):
            g = c[cat]
            for method, offset in (('model', -.18), ('code', .18)):
                value = 100 * g[method + '_wrong'] / g['n'] if g['n'] else 0
                ax.barh(y + offset, value, height=.32, color=colors[method], zorder=3)
                ax.text(min(value, 100) + 2, y + offset, f"{g[method + '_wrong']}/{g['n']}", va='center', fontsize=6.5, color=colors[method])
        ax.set_yticks(range(3), [names[k] for k in CATEGORIES] if ax is axes[0] else ['', '', ''])
        ax.invert_yaxis(); ax.set_xlim(0, 135); ax.set_xticks([0, 50, 100])
        ax.grid(axis='x', alpha=.2, zorder=0); ax.tick_params(axis='y', length=0)
        for spine in ('top', 'right', 'left'):
            ax.spines[spine].set_visible(False)
        ax.set_title(f"{title} (valid {c['valid']}/{c['n']})\ncontinuation fixes {c['corrected']}, breaks {c['harmed']}", loc='left', fontsize=6.8)
    fig.text(.5, .01, 'Wrong binary stockout decisions (% within state category)', ha='center', fontsize=7.5)
    fig.legend(handles=[Patch(color=colors['model'], label='Model decision'), Patch(color=colors['code'], label='Exact continuation from emitted stock')],
               loc='upper center', bbox_to_anchor=(.5, 1.02), ncol=2, frameon=False, fontsize=7.5)
    fig.subplots_adjust(left=.14, right=.99, top=.74, bottom=.2, wspace=.32)
    outdir.mkdir(parents=True, exist_ok=True)
    saved = []
    for ext in ('pdf', 'png'):
        name = 'decision_margins.' + ext
        fig.savefig(outdir / name, dpi=240, facecolor='white')
        saved.append(name)
    plt.close(fig)
    return saved


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'decision')
    p.add_argument('--paper-dir', type=Path, default=ROOT / 'paper')
    p.add_argument('--no-figure', action='store_true')
    a = p.parse_args()
    result = analyze()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / 'decision.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Post-hoc decision-consequence analysis', '', *['- ' + n for n in result['notes']], '',
             f"Exhaustive threshold checks: {result['threshold_checks']:,}", '',
             '| Cohort | Configuration/arm | valid/N | wrong stock | same side | crossing | model wrong | code wrong | corrected / harmed | exact-stock model wrong |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for run, cells in result['cells'].items():
        for key, c in cells.items():
            lines.append(f"| {run} | {key} | {c['valid']}/{c['n']} | {c['wrong_stock']} | {c['same_side']['n']} | {c['crossing']['n']} | {c['model_wrong']} | {c['code_wrong']} | {c['corrected']}/{c['harmed']} | {c['exact']['model_wrong']} |")
    (a.output_dir / 'decision.md').write_text('\n'.join(lines) + '\n')
    a.paper_dir.mkdir(parents=True, exist_ok=True)
    (a.paper_dir / 'decision_findings.tex').write_text(findings(result))
    saved = [] if a.no_figure else figure(result, a.paper_dir / 'figures')
    print(json.dumps({'threshold_checks': result['threshold_checks'], 'figures': saved,
                      'pooled_mini': {k: v for k, v in result['pooled']['mini_main_raw_canonical'].items() if not isinstance(v, dict)}}))


if __name__ == '__main__':
    main()
