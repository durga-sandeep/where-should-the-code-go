"""Independent analysis of the extension studies (protocol_v3_extensions.md). No API calls.

Reparses every provider response, recomputes truth with the independent auditor's
replay, rebuilds hybrid answers for state-only arms with a separate scenario
simulator, checks the conservation identity, verifies the full planned grid and
task identity with the archived source runs, and only then computes paired
comparisons against the original cohorts.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import analyze
import audit_results as audit
import decompose_errors as decomposition
import run as runner

ROOT = Path(__file__).resolve().parent
FIELDS = runner.FIELDS
HISTORY = runner.HISTORY_FIELDS
STATE_ARMS = set(runner.STATE_ARMS)
STUDIES = {  # extension run -> (kind, source run)
    'effort_synthetic_v1': ('effort', 'heldout_v2'), 'effort_profiles_v1': ('effort', 'profiles_v2'),
    'state_synthetic_v1': ('state', 'heldout_v2'), 'state_profiles_v1': ('state', 'profiles_v2')}
COHORT_LABEL = {'heldout_v2': 'Synthetic', 'profiles_v2': 'Retail profiles'}
EFFORTS = (('mini_low', 'low'), ('mini_medium', 'medium'), ('mini_high', 'high'))
STATE_CONFIGS = ('mini_low', 'mini_high', 'gpt54_low', 'sonnet46', 'sonnet46_thinking')
LABELS = {'mini_low': 'GPT-5.4 mini (low)', 'mini_medium': 'GPT-5.4 mini (medium)', 'mini_high': 'GPT-5.4 mini (high)',
          'gpt54_low': 'GPT-5.4 (low)', 'sonnet46': 'Sonnet 4.6', 'sonnet46_thinking': 'Sonnet + thinking'}
METRICS = ('valid', 'joint_exact', 'stock_exact', 'historical_joint', 'future_joint')


def two_field_valid(answer):
    return (type(answer) is dict and set(answer) == set(HISTORY)
            and all(type(answer[f]) is int and answer[f] >= 0 for f in HISTORY))


def evaluate_row(task, row, provider):
    """Independent metrics for one episode; also returns audit mismatches."""
    truth, _ = audit.replay(task)
    answer, status = audit.parse_answer(row, provider)
    problems = []
    if status != row.get('status'):
        problems.append('status')
    arm = row['arm']
    if arm in STATE_ARMS:
        if two_field_valid(answer):
            hybrid = {**answer, **decomposition.future_from_stock(task, answer['stock_at_target'])}
        else:
            hybrid = None
        if row.get('hybrid_answer') != hybrid:
            problems.append('hybrid_answer')
        score = audit.expected_scores(truth, hybrid)
        if score['valid'] and all(score[f + '_exact'] for f in FIELDS[2:]) != score['stock_at_target_exact']:
            raise ValueError('Conservation identity violated for a hybrid answer')
    else:
        score = audit.expected_scores(truth, answer)
    if row.get('score') != score:
        problems.append('score')
    if row.get('request') != runner.request_for(task, row['configuration'], arm):
        problems.append('request')
    usage = (row.get('response') or {}).get('usage') or {}
    reasoning = (usage.get('output_tokens_details') or {}).get('reasoning_tokens')
    metrics = {'valid': score['valid'], 'joint_exact': score['joint_exact'],
               'stock_exact': score['stock_at_target_exact'],
               'historical_joint': score['stock_at_target_exact'] and score['historical_lost_exact'],
               'future_joint': all(score[f + '_exact'] for f in FIELDS[2:]),
               'gold_stockout': truth['first_future_stockout_time'] >= 0}
    final = hybrid if arm in STATE_ARMS else answer
    metrics['predicted_stockout'] = (final['first_future_stockout_time'] >= 0) if score['valid'] else None
    metrics.update(output_tokens=usage.get('output_tokens'), reasoning_tokens=reasoning,
                   cost_usd=row.get('cost_usd'), truncated=(row.get('response') or {}).get('status') == 'incomplete'
                   or (row.get('response') or {}).get('stop_reason') == 'max_tokens')
    return metrics, problems


def load_rows(name):
    path = ROOT / 'runs' / name
    manifest = json.loads((path / 'manifest.json').read_text())
    tasks = {t['base_id']: t for t in manifest['tasks']}
    rows = {}
    problems = defaultdict(int)
    hashes = {}
    for file in sorted(path.glob('*.json')):
        if file.name in ('manifest.json', 'analysis.json', 'requests_preview.json', 'interruption.json'):
            continue
        row = json.loads(file.read_text())
        hashes[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
        provider = manifest['configs'][row['configuration']]['provider']
        metrics, bad = evaluate_row(tasks[row['base_id']], row, provider)
        for b in bad:
            problems[b] += 1
        key = (row['configuration'], row['arm'], row['base_id'], int(row['rep']))
        if key in rows:
            raise ValueError('Duplicate episode ' + file.name)
        rows[key] = metrics
    args = manifest['args']
    expected = {(c, a, b, r) for c in args['configs'] for a in args['arms'] for b in tasks for r in range(args['reps'])}
    if set(rows) != expected:
        raise ValueError(f'{name}: grid incomplete ({len(rows)} of {len(expected)} episodes)')
    return {'manifest': manifest, 'rows': rows, 'problems': dict(problems), 'episodes': len(rows),
            'manifest_sha256': hashlib.sha256((path / 'manifest.json').read_bytes()).hexdigest(),
            'episode_hashes_digest': hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()}


def check_task_identity(extension, source):
    ext = extension['manifest']
    src = source['manifest']['tasks']
    n = ext['args']['n_base']
    if ext['args'].get('source_run') is None or ext['args']['split'] != 'heldout':
        raise ValueError('Extension run must reuse a heldout source run')
    if json.dumps(ext['tasks'], sort_keys=True) != json.dumps(src[:n], sort_keys=True) or len(ext['tasks']) != len(src):
        raise ValueError('Extension tasks differ from the archived source cohort')


def cell(rows, cfg, arm):
    items = [m for (c, a, _, _), m in rows.items() if c == cfg and a == arm]
    if not items:
        raise KeyError((cfg, arm))
    valid = [m for m in items if m['valid']]
    out = {'n': len(items), **{k: sum(m[k] for m in items) for k in METRICS},
           'invalid': sum(not m['valid'] for m in items), 'truncated': sum(bool(m['truncated']) for m in items),
           'false_alarms': sum(not m['gold_stockout'] and m['predicted_stockout'] for m in valid),
           'negatives': sum(not m['gold_stockout'] for m in valid),
           'misses': sum(m['gold_stockout'] and not m['predicted_stockout'] for m in valid),
           'positives': sum(m['gold_stockout'] for m in valid),
           'cost_usd': sum(m['cost_usd'] for m in items)}
    for k in ('output_tokens', 'reasoning_tokens'):
        vals = [m[k] for m in items if isinstance(m[k], int)]
        out['mean_' + k] = sum(vals) / len(vals) if vals else None
        out['known_' + k] = len(vals)
    return out


def paired(left_rows, left_key, right_rows, right_key, metric, draws, seed):
    """right minus left, matched by base and repetition index, averaged within base."""
    l = {(b, r): m[metric] for (c, a, b, r), m in left_rows.items() if (c, a) == left_key}
    rt = {(b, r): m[metric] for (c, a, b, r), m in right_rows.items() if (c, a) == right_key}
    if set(l) != set(rt) or not l:
        raise ValueError(f'Unmatched pairing for {left_key} vs {right_key}')
    groups = defaultdict(list)
    for key in sorted(l):
        groups[key[0]].append(int(rt[key]) - int(l[key]))
    diffs = [sum(v) / len(v) for _, v in sorted(groups.items())]
    return {'metric': metric, 'left': list(left_key), 'right': list(right_key), 'bases': len(diffs),
            'episodes': len(l), 'difference': sum(diffs) / len(diffs), 'ci95': analyze.bootstrap(diffs, draws, seed)}


def pct(count, n):
    return f'{100 * count / n:.1f}'


def effort_table(result):
    lines = ['\\begin{table}[t]', '\\centering\\small', '\\begin{tabular}{llrrrrrr}', '\\toprule',
             'Cohort & Effort & \\multicolumn{3}{c}{Future-joint exact (\\%)} & \\multicolumn{3}{c}{Reasoning tokens / call} \\\\',
             ' & & Raw & Canon. & Snap. & Raw & Canon. & Snap. \\\\', '\\midrule']
    for source in ('heldout_v2', 'profiles_v2'):
        for i, (cfg, effort) in enumerate(EFFORTS):
            cells = result['cells'][source][cfg]
            acc = [pct(cells[a]['future_joint'], cells[a]['n']) for a in ('raw', 'canonical', 'snapshot')]
            tok = [f"{cells[a]['mean_reasoning_tokens']:.0f}" for a in ('raw', 'canonical', 'snapshot')]
            label = COHORT_LABEL[source] if i == 0 else ''
            lines.append(' & '.join([label, effort, *acc, *tok]) + ' \\\\')
        if source == 'heldout_v2':
            lines.append('\\midrule')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{GPT-5.4 mini under requested reasoning effort low/medium/high with identical prompts and tasks. '
              'Future-joint accuracy requires all three scenario outputs; 192 synthetic and 96 profile calls per cell. '
              'Reasoning tokens are provider-reported means; effort is a requested setting, not a compute match. '
              'The low rows are the original cohorts.}', '\\label{tab:effort}', '\\end{table}', '']
    return '\n'.join(lines)


def state_table(result):
    lines = ['\\begin{table}[t]', '\\centering\\small', '\\begin{tabular}{lrrrrrrrr}', '\\toprule',
             ' & \\multicolumn{4}{c}{Synthetic} & \\multicolumn{4}{c}{Retail profiles} \\\\',
             ' & \\multicolumn{2}{c}{Raw} & \\multicolumn{2}{c}{Canonical} & \\multicolumn{2}{c}{Raw} & \\multicolumn{2}{c}{Canonical} \\\\',
             'Configuration & model & hybrid & model & hybrid & model & hybrid & model & hybrid \\\\', '\\midrule']
    for cfg in STATE_CONFIGS:
        values = []
        for source in ('heldout_v2', 'profiles_v2'):
            for arm in ('raw', 'canonical'):
                full = result['cells'][source][cfg][arm]
                hybrid = result['cells'][source][cfg]['state_' + arm]
                values += [pct(full['future_joint'], full['n']), pct(hybrid['future_joint'], hybrid['n'])]
        lines.append(' & '.join([LABELS[cfg], *values]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Prospective hybrid pipeline: future-joint accuracy (\\%) when the model returns all five fields (model) versus when it returns only the two historical fields and code executes the same supplied schedule (hybrid). '
              'Both are actual runs on identical histories; 192 synthetic and 96 profile calls per cell. Invalid two-field answers fail the hybrid endpoint; nothing is repaired. '
              'By conservation, hybrid future-joint accuracy equals state-only starting-stock accuracy.}',
              '\\label{tab:state}', '\\end{table}', '']
    return '\n'.join(lines)


def fmt(c):
    lo, hi = c['ci95']
    return f"{100 * c['difference']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def findings(result):
    P = result['paired']
    def get(source, kind, left, right, metric):
        for c in P[source][kind]:
            if c['left'] == list(left) and c['right'] == list(right) and c['metric'] == metric:
                return c
        raise KeyError((source, kind, left, right, metric))
    s, p = 'heldout_v2', 'profiles_v2'
    text = []
    e_raw = get(s, 'effort', ('mini_low', 'raw'), ('mini_high', 'raw'), 'future_joint')
    e_raw_p = get(p, 'effort', ('mini_low', 'raw'), ('mini_high', 'raw'), 'future_joint')
    e_snap = get(s, 'effort', ('mini_low', 'snapshot'), ('mini_high', 'snapshot'), 'future_joint')
    cells = result['cells']
    text.append(f"Raising mini's requested effort from low to high changes raw-history future-joint accuracy by {fmt(e_raw)} points on synthetic histories and {fmt(e_raw_p)} on retail profiles, "
                f"compared with {fmt(result['baseline_paired'][s]['canonical'])} and {fmt(result['baseline_paired'][s]['snapshot'])} for canonical and snapshot preprocessing at low effort on the same histories. "
                f"In the snapshot arm, high effort changes future-joint accuracy by {fmt(e_snap)} points; "
                f"mean reasoning tokens per raw call are {cells[s]['mini_low']['raw']['mean_reasoning_tokens']:.0f}, {cells[s]['mini_medium']['raw']['mean_reasoning_tokens']:.0f} and {cells[s]['mini_high']['raw']['mean_reasoning_tokens']:.0f} at low, medium and high.")
    for cfg in ('mini_low', 'gpt54_low'):
        for source, name in ((s, 'synthetic'), (p, 'profile')):
            a = get(source, 'state', (cfg, 'canonical'), (cfg, 'state_canonical'), 'stock_exact')
            b = get(source, 'state', (cfg, 'canonical'), (cfg, 'state_canonical'), 'future_joint')
            text.append(f"{LABELS[cfg]}, canonical {name} histories: state-only prompting changes starting-stock accuracy by {fmt(a)} points relative to the five-field prompt, and the prospective hybrid changes future-joint accuracy by {fmt(b)} points relative to model rollout.")
    text.append('Differences are right minus left, paired by history with repetitions matched by index and averaged within history; intervals are descriptive 95\\% base-bootstrap percentiles, not multiplicity adjusted.')
    return ' '.join(text) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'extensions')
    parser.add_argument('--paper-dir', type=Path, default=ROOT / 'paper')
    parser.add_argument('--bootstrap', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=20260907)
    a = parser.parse_args()
    sources = {name: load_rows(name) for name in ('heldout_v2', 'profiles_v2')}
    extensions = {name: load_rows(name) for name in STUDIES}
    for name, (kind, source) in STUDIES.items():
        check_task_identity(extensions[name], sources[source])
    # Merge rows per cohort: original cells plus extension cells keyed by (config, arm).
    merged = {src: dict(sources[src]['rows']) for src in sources}
    for name, (kind, source) in STUDIES.items():
        for key, m in extensions[name]['rows'].items():
            if key in merged[source]:
                raise ValueError('Extension duplicates an original cell')
            merged[source][key] = m
    cells = {}
    for source, rows in merged.items():
        cells[source] = defaultdict(dict)
        for (cfg, arm, _, _) in rows:
            if arm not in cells[source][cfg]:
                cells[source][cfg][arm] = cell(rows, cfg, arm)
    paired_out = {}
    for source, rows in merged.items():
        paired_out[source] = {'effort': [], 'state': []}
        for cfg, _ in EFFORTS[1:]:
            for arm in ('raw', 'canonical', 'snapshot'):
                for metric in ('future_joint', 'stock_exact', 'joint_exact'):
                    paired_out[source]['effort'].append(paired(rows, ('mini_low', arm), rows, (cfg, arm), metric, a.bootstrap, a.seed))
        for cfg in STATE_CONFIGS:
            for arm in ('raw', 'canonical'):
                for metric in ('stock_exact', 'future_joint', 'joint_exact', 'historical_joint'):
                    paired_out[source]['state'].append(paired(rows, (cfg, arm), rows, (cfg, 'state_' + arm), metric, a.bootstrap, a.seed))
    baseline_paired = {}
    for source, rows in merged.items():
        baseline_paired[source] = {arm: paired(rows, ('mini_low', 'raw'), rows, ('mini_low', arm), 'future_joint', a.bootstrap, a.seed)
                                   for arm in ('canonical', 'snapshot')}
    result = {'analysis': 'extension_studies', 'protocol': 'protocol_v3_extensions.md', 'bootstrap_draws': a.bootstrap, 'seed': a.seed,
              'episodes': {name: extensions[name]['episodes'] for name in STUDIES},
              'audit_problems': {name: extensions[name]['problems'] for name in STUDIES},
              'source_audit_problems': {name: sources[name]['problems'] for name in sources},
              'provenance': {name: {'manifest_sha256': x['manifest_sha256'], 'episode_hashes_digest': x['episode_hashes_digest'],
                                    'source_sha256': x['manifest']['source_sha256']} for name, x in {**sources, **extensions}.items()},
              'cells': {s: {c: dict(v) for c, v in cells[s].items()} for s in cells},
              'paired': paired_out, 'baseline_paired': baseline_paired,
              'notes': ['Every response reparsed; truth recomputed with the independent auditor replay; hybrid answers rebuilt with a separate scenario simulator.',
                        'Hybrid future-joint accuracy equals state-only starting-stock accuracy by conservation; verified on every valid hybrid answer.',
                        'Extension tasks are byte-identical to the archived heldout cohorts; they add configurations and arms, not independent histories.',
                        'Requested reasoning effort is a provider setting; reported reasoning tokens are provider usage fields, not a compute match.',
                        'All configurations, arms, invalid answers and truncations are retained; no retries, repairs or exclusions.']}
    if any(extensions[n]['problems'] for n in STUDIES) or any(sources[n]['problems'] for n in sources):
        result['audit_passed'] = False
    else:
        result['audit_passed'] = True
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / 'extensions.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Extension studies: independent analysis', '', *['- ' + n for n in result['notes']], '',
             f"Audit passed: {result['audit_passed']}; problems: {json.dumps(result['audit_problems'])}", '',
             '| Cohort | Configuration | Arm | N | Valid | All five | Stock exact | Hist. joint | Future joint | False alarms / neg. | Misses / pos. | Mean reasoning tokens | Cost USD |',
             '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for source in ('heldout_v2', 'profiles_v2'):
        for cfg in sorted(cells[source]):
            for arm, c in sorted(cells[source][cfg].items()):
                rt = f"{c['mean_reasoning_tokens']:.0f}" if c['mean_reasoning_tokens'] is not None else 'n/a'
                lines.append(f"| {source} | {cfg} | {arm} | {c['n']} | {c['valid']} | {c['joint_exact']} | {c['stock_exact']} | {c['historical_joint']} | {c['future_joint']} | {c['false_alarms']}/{c['negatives']} | {c['misses']}/{c['positives']} | {rt} | {c['cost_usd']:.2f} |")
    lines += ['', '| Cohort | Kind | Left | Right | Metric | Bases | Difference [95% CI], pp |', '| --- | --- | --- | --- | --- | ---: | --- |']
    for source in paired_out:
        for kind, items in paired_out[source].items():
            for c in items:
                lines.append(f"| {source} | {kind} | {'/'.join(c['left'])} | {'/'.join(c['right'])} | {c['metric']} | {c['bases']} | {fmt(c)} |")
    (a.output_dir / 'extensions.md').write_text('\n'.join(lines) + '\n')
    a.paper_dir.mkdir(parents=True, exist_ok=True)
    (a.paper_dir / 'extension_effort_table.tex').write_text(effort_table(result))
    (a.paper_dir / 'extension_state_table.tex').write_text(state_table(result))
    (a.paper_dir / 'extension_findings.tex').write_text(findings(result))
    print(json.dumps({'audit_passed': result['audit_passed'], 'episodes': result['episodes']}))


if __name__ == '__main__':
    main()
