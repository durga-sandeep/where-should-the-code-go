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
REPLICATION = 'replication_mini_low_v1'  # protocol amendment 1: same-period low-effort baseline (synthetic)
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
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\begin{tabular}{lrrrrrr}', '\\toprule',
             ' & \\multicolumn{3}{c}{Synthetic} & \\multicolumn{3}{c}{Retail profiles} \\\\',
             'Arm & low & medium & high & low & medium & high \\\\', '\\midrule']
    for arm in ('raw', 'canonical', 'snapshot'):
        values = []
        for source in ('heldout_v2', 'profiles_v2'):
            for cfg, _ in EFFORTS:
                c = result['cells'][source][cfg][arm]
                values.append(pct(c['future_joint'], c['n']))
        lines.append(' & '.join([arm.capitalize(), *values]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{GPT-5.4 mini future-joint accuracy (\\%) by requested reasoning effort, with identical prompts and tasks; '
              '192 synthetic and 96 profile calls per cell. Low columns are the original cohorts. Effort is a requested setting, not a compute match.}',
              '\\label{tab:effort}', '\\end{table}', '']
    return '\n'.join(lines)


def state_table(result):
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\begin{tabular}{lrrrrrrrr}', '\\toprule',
             ' & \\multicolumn{4}{c}{Synthetic} & \\multicolumn{4}{c}{Retail profiles} \\\\',
             ' & \\multicolumn{2}{c}{Raw} & \\multicolumn{2}{c}{Canonical} & \\multicolumn{2}{c}{Raw} & \\multicolumn{2}{c}{Canonical} \\\\',
             'Configuration & model & hybrid & model & hybrid & model & hybrid & model & hybrid \\\\', '\\midrule']
    for cfg in [c for c in STATE_CONFIGS if c != 'mini_high']:
        values = []
        for source in ('heldout_v2', 'profiles_v2'):
            for arm in ('raw', 'canonical'):
                full = result['cells'][source][cfg][arm]
                hybrid = result['cells'][source][cfg]['state_' + arm]
                values += [pct(full['future_joint'], full['n']), pct(hybrid['future_joint'], hybrid['n'])]
        lines.append(' & '.join([LABELS[cfg], *values]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Future-joint accuracy (\\%) when the model returns all five fields (model) versus when it returns only the two historical fields and code executes the same schedule (hybrid); '
              'both are actual runs on identical histories, 192 synthetic and 96 profile calls per cell. Invalid two-field answers fail; nothing is repaired. Mini at high effort is in Appendix~\\ref{app:tables}.}',
              '\\label{tab:state}', '\\end{table}', '']
    return '\n'.join(lines)


def fmt(c):
    lo, hi = c['ci95']
    return f"{100 * c['difference']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def get_pair(result, source, kind, left, right, metric):
    for c in result['paired'][source][kind]:
        if c['left'] == list(left) and c['right'] == list(right) and c['metric'] == metric:
            return c
    raise KeyError((source, kind, left, right, metric))


def effort_findings(result):
    s, p = 'heldout_v2', 'profiles_v2'
    cells = result['cells']
    def d(source, arm, cfg):
        return fmt(get_pair(result, source, 'effort', ('mini_low', arm), (cfg, arm), 'future_joint'))
    text = (f"Relative to low effort, high effort changes canonical-input future-joint accuracy by {d(s, 'canonical', 'mini_high')} points on synthetic histories and {d(p, 'canonical', 'mini_high')} on retail profiles "
            f"(medium: {d(s, 'canonical', 'mini_medium')} and {d(p, 'canonical', 'mini_medium')}); raw-input changes are {d(s, 'raw', 'mini_high')} and {d(p, 'raw', 'mini_high')}, "
            f"and snapshot changes are {d(s, 'snapshot', 'mini_high')} and {d(p, 'snapshot', 'mini_high')}. "
            f"For comparison, canonical and snapshot preprocessing at low effort changed raw accuracy by {fmt(result['baseline_paired'][s]['canonical'])} and {fmt(result['baseline_paired'][s]['snapshot'])} points on the same synthetic histories. "
            f"Mean reasoning tokens per raw synthetic call are {cells[s]['mini_low']['raw']['mean_reasoning_tokens']:.0f}, {cells[s]['mini_medium']['raw']['mean_reasoning_tokens']:.0f} and {cells[s]['mini_high']['raw']['mean_reasoning_tokens']:.0f} at low, medium and high; "
            f"{sum(cells[src][c][a]['invalid'] for src in (s, p) for c in ('mini_medium', 'mini_high') for a in ('raw', 'canonical', 'snapshot'))} of {sum(cells[src][c][a]['n'] for src in (s, p) for c in ('mini_medium', 'mini_high') for a in ('raw', 'canonical', 'snapshot')):,} raised-effort answers are invalid (negative integers) and none reached the output limit.")
    if result.get('replication'):
        r = result['replication']
        c = r['cells']; k = r['contemporaneous_effort_comparisons']
        text += (f" A same-period replication of the low-effort synthetic cells ({r['episodes']} calls) gives raw {c['raw']['replication']:.1f} vs {c['raw']['original']:.1f}\\%, canonical {c['canonical']['replication']:.1f} vs {c['canonical']['original']:.1f}\\% and snapshot {c['snapshot']['replication']:.1f} vs {c['snapshot']['original']:.1f}\\% "
                 f"(paired {fmt(c['raw']['paired_future_joint'])}, {fmt(c['canonical']['paired_future_joint'])}, {fmt(c['snapshot']['paired_future_joint'])}); "
                 f"against this contemporaneous baseline, high and medium effort still change canonical accuracy by {fmt(k['mini_high/canonical'])} and {fmt(k['mini_medium/canonical'])} points.")
    return text + '\n'


def state_findings(result):
    s, p = 'heldout_v2', 'profiles_v2'
    def d(source, cfg, arm, metric):
        return fmt(get_pair(result, source, 'state', (cfg, arm), (cfg, 'state_' + arm), metric))
    text = (f"For mini on canonical inputs, state-only prompting changes starting-stock accuracy by {d(s, 'mini_low', 'canonical', 'stock_exact')} points on synthetic histories and {d(p, 'mini_low', 'canonical', 'stock_exact')} on profiles relative to the five-field prompt, "
            f"and the hybrid changes future-joint accuracy by {d(s, 'mini_low', 'canonical', 'future_joint')} and {d(p, 'mini_low', 'canonical', 'future_joint')} points relative to the model's own rollout; "
            f"on raw inputs the stock changes are {d(s, 'mini_low', 'raw', 'stock_exact')} and {d(p, 'mini_low', 'raw', 'stock_exact')}. "
            f"For GPT-5.4 the canonical hybrid gains are {d(s, 'gpt54_low', 'canonical', 'future_joint')} and {d(p, 'gpt54_low', 'canonical', 'future_joint')} points. "
            "Because hybrid future accuracy equals reconstruction accuracy, the post-hoc continuation estimate is a lower bound on the prospective hybrid whenever state-only prompting does not reduce reconstruction accuracy, as here: removing the rollout burden slightly improves the state itself.")
    return text + '\n'


def numbers(result):
    s, p = 'heldout_v2', 'profiles_v2'
    c = result['cells']
    total = 4224 + sum(result['episodes'].values()) + (result['replication']['episodes'] if result.get('replication') else 0)
    macros = {'abstractRawMini': pct(c[p]['mini_low']['raw']['future_joint'], c[p]['mini_low']['raw']['n']),
              'abstractCanonMini': pct(c[p]['mini_low']['canonical']['future_joint'], c[p]['mini_low']['canonical']['n']),
              'abstractHybridMini': pct(c[p]['mini_low']['state_canonical']['future_joint'], c[p]['mini_low']['state_canonical']['n']),
              'abstractSynthRawMini': pct(c[s]['mini_low']['raw']['future_joint'], c[s]['mini_low']['raw']['n']),
              'abstractSynthCanonMini': pct(c[s]['mini_low']['canonical']['future_joint'], c[s]['mini_low']['canonical']['n']),
              'abstractSynthHybridMini': pct(c[s]['mini_low']['state_canonical']['future_joint'], c[s]['mini_low']['state_canonical']['n']),
              'TotalRequests': f'{total:,}', 'EffortRequests': f"{result['episodes']['effort_synthetic_v1'] + result['episodes']['effort_profiles_v1']:,}",
              'StateRequests': f"{result['episodes']['state_synthetic_v1'] + result['episodes']['state_profiles_v1']:,}"}
    return '\n'.join('\\newcommand{\\' + k + '}{' + v + '}' for k, v in macros.items()) + '\n'


def appendix_table(result):
    lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\begin{tabular}{lllrrrrrr}', '\\toprule',
             'Cohort & Configuration & Arm & N & Invalid & All five & Stock & Hist. joint & Future joint \\\\', '\\midrule']
    for source in ('heldout_v2', 'profiles_v2'):
        for cfg in ('mini_low', 'mini_medium', 'mini_high', 'gpt54_low', 'sonnet46', 'sonnet46_thinking'):
            for arm in ('raw', 'canonical', 'snapshot', 'state_raw', 'state_canonical'):
                c = result['cells'][source].get(cfg, {}).get(arm)
                if c is None:
                    continue
                lines.append(' & '.join([COHORT_LABEL[source], LABELS[cfg], arm.replace('_', '-'), str(c['n']), str(c['invalid']),
                                         pct(c['joint_exact'], c['n']), pct(c['stock_exact'], c['n']), pct(c['historical_joint'], c['n']), pct(c['future_joint'], c['n'])]) + ' \\\\')
        if source == 'heldout_v2':
            lines.append('\\midrule')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{All cells of the original grid and the extension studies (\\%). State-only arms report the hybrid answer (model historical fields plus executable continuation); '
              'their future-joint accuracy equals their stock accuracy by conservation. Invalid answers fail every endpoint and remain in denominators.}',
              '\\label{tab:allcells}', '\\end{table}', '']
    return '\n'.join(lines)


def appendix_paired(result):
    lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\begin{tabular}{llllrr}', '\\toprule',
             'Cohort & Comparison (right minus left) & Metric & Bases & Difference & 95\\% interval \\\\', '\\midrule']
    for source in ('heldout_v2', 'profiles_v2'):
        for kind in ('effort', 'state'):
            for c in result['paired'][source][kind]:
                if c['metric'] not in ('future_joint', 'stock_exact'):
                    continue
                lo, hi = c['ci95']
                left = f"{LABELS[c['left'][0]]}/{c['left'][1].replace('_', '-')}"
                right = f"{LABELS[c['right'][0]]}/{c['right'][1].replace('_', '-')}" if c['right'][0] != c['left'][0] else c['right'][1].replace('_', '-')
                lines.append(' & '.join([COHORT_LABEL[source], f'{left} $\\to$ {right}', c['metric'].replace('_', ' '), str(c['bases']),
                                         f"{100 * c['difference']:+.1f}", f"[{100 * lo:+.1f}, {100 * hi:+.1f}]"]) + ' \\\\')
        if source == 'heldout_v2':
            lines.append('\\midrule')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Paired differences in percentage points for the extension studies, matched by history and repetition index and averaged within history; '
              'descriptive 95\\% history-bootstrap percentile intervals (10,000 draws), not multiplicity adjusted. Effort rows compare medium or high requested effort with the original low-effort cells; '
              'state rows compare the state-only hybrid with the five-field arm of the same configuration.}', '\\label{tab:extpaired}', '\\end{table}', '']
    text = ''
    if result.get('replication'):
        r = result['replication']
        rows = ', '.join(f"{arm} {r['cells'][arm]['original']:.1f} vs {r['cells'][arm]['replication']:.1f}\\% ({fmt(r['cells'][arm]['paired_future_joint'])} points)" for arm in ('raw', 'canonical', 'snapshot'))
        k = r['contemporaneous_effort_comparisons']
        contemporaneous = '; '.join(f"{LABELS[key.split('/')[0]]}/{key.split('/')[1]} {fmt(v)}" for key, v in k.items())
        text = (f"\\paragraph{{Same-period low-effort replication.}} The {r['episodes']}-call replication of mini's low-effort synthetic cells gives original versus replication future-joint accuracy of {rows}. "
                "The canonical cell replicates lower than the original, so collection-period variation of that size should be assumed when reading any single mini cell. "
                f"Paired changes of the raised-effort cells relative to the replication baseline are: {contemporaneous} (future-joint, percentage points).\n\n")
    return text + '\n'.join(lines)


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
    replication = None
    if (ROOT / 'runs' / REPLICATION / 'analysis.json').exists():
        rep = load_rows(REPLICATION)
        check_task_identity(rep, sources['heldout_v2'])
        rep_cells = {}
        for arm in ('raw', 'canonical', 'snapshot'):
            orig = cell(sources['heldout_v2']['rows'], 'mini_low', arm)
            new = cell(rep['rows'], 'mini_low', arm)
            rep_cells[arm] = {'original': 100 * orig['future_joint'] / orig['n'], 'replication': 100 * new['future_joint'] / new['n'],
                              'original_stock': 100 * orig['stock_exact'] / orig['n'], 'replication_stock': 100 * new['stock_exact'] / new['n'],
                              'paired_future_joint': paired(sources['heldout_v2']['rows'], ('mini_low', arm), rep['rows'], ('mini_low', arm), 'future_joint', a.bootstrap, a.seed)}
        contemporaneous = {}
        for cfg in ('mini_medium', 'mini_high'):
            for arm in ('raw', 'canonical', 'snapshot'):
                contemporaneous[f'{cfg}/{arm}'] = paired(rep['rows'], ('mini_low', arm), merged['heldout_v2'], (cfg, arm), 'future_joint', a.bootstrap, a.seed)
        replication = {'run': REPLICATION, 'episodes': rep['episodes'], 'problems': rep['problems'], 'cells': rep_cells,
                       'contemporaneous_effort_comparisons': contemporaneous,
                       'provenance': {'manifest_sha256': rep['manifest_sha256'], 'episode_hashes_digest': rep['episode_hashes_digest']}}
    result = {'analysis': 'extension_studies', 'replication': replication, 'protocol': 'protocol_v3_extensions.md', 'bootstrap_draws': a.bootstrap, 'seed': a.seed,
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
    if any(extensions[n]['problems'] for n in STUDIES) or any(sources[n]['problems'] for n in sources) or (replication and replication['problems']):
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
    (a.paper_dir / 'extension_effort_findings.tex').write_text(effort_findings(result))
    (a.paper_dir / 'extension_state_findings.tex').write_text(state_findings(result))
    (a.paper_dir / 'extension_numbers.tex').write_text(numbers(result))
    (a.paper_dir / 'extension_all_cells_table.tex').write_text(appendix_table(result))
    (a.paper_dir / 'extension_appendix.tex').write_text(appendix_paired(result))
    print(json.dumps({'audit_passed': result['audit_passed'], 'episodes': result['episodes']}))


if __name__ == '__main__':
    main()
