"""Independent analysis of the extension studies (protocol_v3_extensions.md). No API calls.

Reparses every provider response, recomputes truth with the independent auditor's
replay, rebuilds hybrid answers for state-only arms with a separate scenario
simulator, checks the conservation identity, verifies the full planned grid and
task identity with the archived source runs, and only then computes paired
comparisons against the original cohorts. Runs from Amendment 2 (GPT-5.4 effort
sweep, code-inside arms) and the Amendment 1 replication are included when both
cohorts of a study are present.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import analyze
import audit_results as audit
import benchmark
import decompose_errors as decomposition
import run as runner

ROOT = Path(__file__).resolve().parent
FIELDS = runner.FIELDS
HISTORY = runner.HISTORY_FIELDS
STATE_ARMS = set(runner.STATE_ARMS)
TOOL_ARMS = set(runner.TOOL_ARMS)
REQUIRED_STUDIES = {  # extension run -> (kind, source run)
    'effort_synthetic_v1': ('effort', 'heldout_v2'), 'effort_profiles_v1': ('effort', 'profiles_v2'),
    'state_synthetic_v1': ('state', 'heldout_v2'), 'state_profiles_v1': ('state', 'profiles_v2')}
OPTIONAL_STUDIES = {
    'effort2': {'effort_gpt54_synthetic_v1': 'heldout_v2', 'effort_gpt54_profiles_v1': 'profiles_v2'},
    'tool': {'tool_synthetic_v1': 'heldout_v2', 'tool_profiles_v2': 'profiles_v2'},
    'auto': {'effort_auto_synthetic_v1': 'heldout_v2'}}
REPLICATION = 'replication_mini_low_v1'  # Amendment 1: same-period low-effort baseline (synthetic)
COHORT_LABEL = {'heldout_v2': 'Synthetic', 'profiles_v2': 'Retail profiles'}
EFFORTS = (('mini_low', 'low'), ('mini_medium', 'medium'), ('mini_high', 'high'))
EFFORTS_54 = (('gpt54_low', 'low'), ('gpt54_medium', 'medium'), ('gpt54_high', 'high'))
STATE_CONFIGS = ('mini_low', 'mini_high', 'gpt54_low', 'sonnet46', 'sonnet46_thinking')
TOOL_CONFIGS = ('mini_low', 'gpt54_low')
ALL_CONFIGS = ('mini_low', 'mini_medium', 'mini_high', 'mini_low_auto', 'mini_high_auto', 'gpt54_low', 'gpt54_medium', 'gpt54_high', 'sonnet46', 'sonnet46_thinking')
ALL_ARMS = ('raw', 'canonical', 'snapshot', 'state_raw', 'state_canonical', 'tool_raw', 'tool_canonical')
LABELS = {'mini_low': 'GPT-5.4 mini (low)', 'mini_medium': 'GPT-5.4 mini (medium)', 'mini_high': 'GPT-5.4 mini (high)',
          'mini_low_auto': 'GPT-5.4 mini (low, auto tool choice)', 'mini_high_auto': 'GPT-5.4 mini (high, auto tool choice)',
          'gpt54_low': 'GPT-5.4 (low)', 'gpt54_medium': 'GPT-5.4 (medium)', 'gpt54_high': 'GPT-5.4 (high)',
          'sonnet46': 'Sonnet 4.6', 'sonnet46_thinking': 'Sonnet + thinking'}
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
    response = row.get('response') or {}
    usage = response.get('usage') or {}
    if 'prompt_tokens' in usage and 'input_tokens' not in usage:
        # Chat-completions usage shape (OpenRouter): map onto the Responses-API names used below.
        usage = {**usage, 'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens'),
                 'output_tokens_details': usage.get('completion_tokens_details') or {}}
    reasoning = (usage.get('output_tokens_details') or {}).get('reasoning_tokens')
    finish = [c.get('finish_reason') for c in (response.get('choices') or [])]
    metrics = {'valid': score['valid'], 'joint_exact': score['joint_exact'],
               'stock_exact': score['stock_at_target_exact'],
               'historical_joint': score['stock_at_target_exact'] and score['historical_lost_exact'],
               'future_joint': all(score[f + '_exact'] for f in FIELDS[2:]),
               'gold_stockout': truth['first_future_stockout_time'] >= 0}
    final = hybrid if arm in STATE_ARMS else answer
    metrics['predicted_stockout'] = (final['first_future_stockout_time'] >= 0) if score['valid'] else None
    metrics.update(output_tokens=usage.get('output_tokens'), reasoning_tokens=reasoning,
                   cost_usd=row.get('cost_usd'), missing=answer is None,
                   code_calls=sum(o.get('type') == 'code_interpreter_call' for o in response.get('output', [])),
                   truncated=response.get('status') == 'incomplete' or response.get('stop_reason') == 'max_tokens' or 'length' in finish)
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
           'invalid': sum(not m['valid'] for m in items), 'missing': sum(m['missing'] for m in items),
           'truncated': sum(bool(m['truncated']) for m in items),
           'used_code': sum(m['code_calls'] > 0 for m in items), 'code_calls': sum(m['code_calls'] for m in items),
           'future_joint_with_code': sum(m['future_joint'] for m in items if m['code_calls'] > 0),
           'future_joint_without_code': sum(m['future_joint'] for m in items if m['code_calls'] == 0),
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


def fmt(c):
    lo, hi = c['ci95']
    return f"{100 * c['difference']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def get_pair(result, source, kind, left, right, metric):
    for c in result['paired'][source].get(kind, []):
        if c['left'] == list(left) and c['right'] == list(right) and c['metric'] == metric:
            return c
    raise KeyError((source, kind, left, right, metric))


def has(result, source, cfg, arm):
    return arm in result['cells'][source].get(cfg, {})


# ---------------------------------------------------------------- manuscript fragments

def effort_table(result):
    """Future-joint accuracy by requested effort; GPT-5.4 rows appear when Amendment 2 data exist."""
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\begin{tabular}{llrrrrrr}', '\\toprule',
             ' & & \\multicolumn{3}{c}{Synthetic} & \\multicolumn{3}{c}{Retail profiles} \\\\',
             'Model & Arm & low & medium & high & low & medium & high \\\\', '\\midrule']
    blocks = [('GPT-5.4 mini, forced call', EFFORTS, ('raw', 'canonical', 'snapshot'))]
    if has(result, 'heldout_v2', 'gpt54_high', 'raw'):
        blocks.append(('GPT-5.4, forced call', EFFORTS_54, ('raw', 'canonical')))
    if has(result, 'heldout_v2', 'mini_high_auto', 'raw'):
        blocks.append(('GPT-5.4 mini, auto choice', (('mini_low_auto', 'low'), (None, 'medium'), ('mini_high_auto', 'high')), ('raw', 'canonical')))
    for bi, (model, efforts, arms) in enumerate(blocks):
        if bi:
            lines.append('\\midrule')
        for ai, arm in enumerate(arms):
            values = []
            for source in ('heldout_v2', 'profiles_v2'):
                for cfg, _ in efforts:
                    c = result['cells'][source].get(cfg, {}).get(arm) if cfg else None
                    values.append(pct(c['future_joint'], c['n']) if c else '--')
            lines.append(' & '.join([model if ai == 0 else '', arm.capitalize(), *values]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Future-joint accuracy (\\%) by requested reasoning effort, identical prompts and tasks; 192 synthetic and 96 profile calls per cell; the forced-call low columns are the original cohorts. '
              'Forced call: the answer function is the only permitted action; auto choice: the model may respond freely and a missing answer fails. Dashes: not run.}',
              '\\label{tab:effort}', '\\end{table}', '']
    return '\n'.join(lines)


def placement_table(result):
    """Where the code sits: model rollout, state-only hybrid, code inside the call, and exact-state snapshot."""
    tool = has(result, 'heldout_v2', 'mini_low', 'tool_raw')
    k = 3 if tool else 2
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\setlength{\\tabcolsep}{4pt}',
             '\\begin{tabular}{l' + 'r' * (2 * k + 1) + '}', '\\toprule',
             f' & \\multicolumn{{{k}}}{{c}}{{Raw input}} & \\multicolumn{{{k}}}{{c}}{{Canonical input}} & Snapshot \\\\',
             'Cohort, configuration & ' + ' & '.join((['model', 'hybrid', 'inside'] if tool else ['model', 'hybrid']) * 2) + ' & model \\\\', '\\midrule']
    for si, source in enumerate(('heldout_v2', 'profiles_v2')):
        if si:
            lines.append('\\midrule')
        for cfg in [c for c in STATE_CONFIGS if c != 'mini_high']:
            values = []
            for arm in ('raw', 'canonical'):
                full = result['cells'][source][cfg][arm]
                hybrid = result['cells'][source][cfg]['state_' + arm]
                values += [pct(full['future_joint'], full['n']), pct(hybrid['future_joint'], hybrid['n'])]
                if tool:
                    t = result['cells'][source][cfg].get('tool_' + arm)
                    values.append(pct(t['future_joint'], t['n']) if t else '--')
            snap = result['cells'][source][cfg]['snapshot']
            values.append(pct(snap['future_joint'], snap['n']))
            lines.append(' & '.join([f"{COHORT_LABEL[source]}, {LABELS[cfg]}", *values]) + ' \\\\')
    cap = ('Future-joint accuracy (\\%, all three scenario outputs exact) by input and code placement; 192 synthetic and 96 profile calls per cell; invalid answers fail. '
           '\\emph{model}: all five fields from the model; \\emph{hybrid}: model returns the two historical fields, code applies the schedule (equals reconstruction accuracy by conservation)')
    if tool:
        cap += '; \\emph{inside}: code-execution tool available during the call (OpenAI only)'
    cap += '; \\emph{snapshot}: exact state supplied, model rolls out; dashes mark arms not run. All-five accuracy: Appendix~\\ref{app:tables}.'
    lines += ['\\bottomrule', '\\end{tabular}', '\\caption{' + cap + '}', '\\label{tab:state}', '\\end{table}', '']
    return '\n'.join(lines)


def effort_findings(result):
    s, p = 'heldout_v2', 'profiles_v2'
    cells = result['cells']
    def d(source, arm, cfg, left='mini_low', kind='effort'):
        return fmt(get_pair(result, source, kind, (left, arm), (cfg, arm), 'future_joint'))
    text = (f"Under the forced answer call used in the original grid, high effort changes mini's canonical-input future-joint accuracy by {d(s, 'canonical', 'mini_high')} points on synthetic histories and {d(p, 'canonical', 'mini_high')} on profiles, raw-input accuracy by {d(s, 'raw', 'mini_high')} and {d(p, 'raw', 'mini_high')}, and snapshot accuracy by {d(s, 'snapshot', 'mini_high')} and {d(p, 'snapshot', 'mini_high')} (GPT-5.4: Table~\\ref{{tab:effort}}); "
            "its wrong canonical stocks are mostly exactly zero, and re-issued reasoning summaries show it planning the replay yet answering first (Appendix~\\ref{app:extensions}). ")
    if result.get('replication'):
        r = result['replication']; c = r['cells']; k = r['contemporaneous_effort_comparisons']
        text += (f"Against the same-period replication baseline, whose run-to-run shift sets a noise floor near nine points (Appendix~\\ref{{app:extensions}}), the canonical drop is still {fmt(k['mini_high/canonical'])}. ")
    if has(result, s, 'mini_high_auto', 'canonical'):
        lo_c = cells[s]['mini_low_auto']['canonical']; hi_c = cells[s]['mini_high_auto']['canonical']
        lo_r = cells[s]['mini_low_auto']['raw']; hi_r = cells[s]['mini_high_auto']['raw']
        text += (f"The decisive control removes the forced call: with automatic tool choice, mini at low and high effort reaches {pct(lo_c['future_joint'], lo_c['n'])} and {pct(hi_c['future_joint'], hi_c['n'])}\\% on canonical input ({fmt(get_pair(result, s, 'auto', ('mini_low_auto', 'canonical'), ('mini_high_auto', 'canonical'), 'future_joint'))}) "
                 f"and {pct(lo_r['future_joint'], lo_r['n'])} and {pct(hi_r['future_joint'], hi_r['n'])}\\% on raw input ({fmt(get_pair(result, s, 'auto', ('mini_low_auto', 'raw'), ('mini_high_auto', 'raw'), 'future_joint'))}), with {lo_c['missing'] + hi_c['missing'] + lo_r['missing'] + hi_r['missing']} of {2 * (lo_c['n'] + lo_r['n'])} calls returning no answer. "
                 f"The collapse is therefore an interaction between the forced answer call and requested effort rather than an effect of requested effort alone; the design cannot separate removing the forced call from permitting free text before the answer, and the canonical gain under automatic choice is within the noise floor while the raw gain is not. Automatic choice alone lifts mini's low-effort accuracy from {pct(cells[s]['mini_low']['raw']['future_joint'], 192)} to {pct(lo_r['future_joint'], lo_r['n'])}\\% (raw) and {pct(cells[s]['mini_low']['canonical']['future_joint'], 192)} to {pct(lo_c['future_joint'], lo_c['n'])}\\% (canonical), so the forced-call mini cells elsewhere are pessimistic by 10 to 19 points.")
    return text + '\n'


def state_findings(result):
    s, p = 'heldout_v2', 'profiles_v2'
    c = result['cells']
    def d(source, cfg, arm, metric):
        return fmt(get_pair(result, source, 'state', (cfg, arm), (cfg, 'state_' + arm), metric))
    text = (f"For mini on canonical inputs the hybrid raises future-joint accuracy by {d(s, 'mini_low', 'canonical', 'future_joint')} points on synthetic histories and {d(p, 'mini_low', 'canonical', 'future_joint')} on profiles relative to the model's own rollout, "
            f"while asking for the state alone changes reconstruction accuracy by amounts comparable to the run-to-run noise floor established by the replication below ({pct(c[s]['mini_low']['canonical']['stock_exact'], 192)} vs {pct(c[s]['mini_low']['state_canonical']['stock_exact'], 192)}\\% synthetic, {pct(c[p]['mini_low']['canonical']['stock_exact'], 96)} vs {pct(c[p]['mini_low']['state_canonical']['stock_exact'], 96)}\\% profiles). "
            f"On raw inputs the hybrid reaches only {pct(c[s]['mini_low']['state_raw']['future_joint'], 192)} and {pct(c[p]['mini_low']['state_raw']['future_joint'], 96)}\\%: code after the model never touches the state, so a stock that is wrong because the wrong reports were selected stays wrong. "
            "GPT-5.4's paired differences are in Appendix~\\ref{app:extensions}.")
    return text + '\n'


def tool_findings(result):
    s, p = 'heldout_v2', 'profiles_v2'
    if not has(result, s, 'mini_low', 'tool_raw'):
        return ''
    cells = result['cells']
    def d(source, cfg, arm, metric='future_joint'):
        return fmt(get_pair(result, source, 'tool', (cfg, arm), (cfg, 'tool_' + arm), metric))
    used = {cfg: sum(cells[src][cfg][a]['used_code'] for src in (s, p) for a in ('tool_raw', 'tool_canonical')) for cfg in TOOL_CONFIGS}
    n = {cfg: sum(cells[src][cfg][a]['n'] for src in (s, p) for a in ('tool_raw', 'tool_canonical')) for cfg in TOOL_CONFIGS}
    with_code = sum(cells[src]['mini_low'][a]['future_joint_with_code'] for src in (s, p) for a in ('tool_raw', 'tool_canonical'))
    without = sum(cells[src]['mini_low'][a]['future_joint_without_code'] for src in (s, p) for a in ('tool_raw', 'tool_canonical'))
    missing = sum(cells[src][cfg][a]['missing'] for src in (s, p) for cfg in TOOL_CONFIGS for a in ('tool_raw', 'tool_canonical'))
    text = (f"With a code-execution tool available, mini's raw-input future-joint accuracy rises by {d(s, 'mini_low', 'raw')} points on synthetic histories and {d(p, 'mini_low', 'raw')} on profiles, and its canonical-input accuracy by {d(s, 'mini_low', 'canonical')} and {d(p, 'mini_low', 'canonical')}; "
            f"GPT-5.4 reaches 100\\% on raw input in both cohorts (+{100*get_pair(result, s, 'tool', ('gpt54_low', 'raw'), ('gpt54_low', 'tool_raw'), 'future_joint')['difference']:.1f} and +{100*get_pair(result, p, 'tool', ('gpt54_low', 'raw'), ('gpt54_low', 'tool_raw'), 'future_joint')['difference']:.1f} points) while its canonical synthetic cell moves within noise ({pct(cells[s]['gpt54_low']['canonical']['future_joint'], 192)} to {pct(cells[s]['gpt54_low']['tool_canonical']['future_joint'], 192)}\\%). "
            f"Mini ran code in {used['mini_low']} of {n['mini_low']} calls and was exact in {with_code} of them, versus {without} of the {n['mini_low'] - used['mini_low']} calls it answered without code (Appendix~\\ref{{app:extensions}}); {missing} calls returned no answer. "
            + (f"The tool arms use automatic tool choice, so against the interface-matched automatic-choice baselines below the tool's own contribution on synthetic histories is {fmt(get_pair(result, s, 'auto_tool', ('mini_low_auto', 'raw'), ('mini_low', 'tool_raw'), 'future_joint'))} points on raw and {fmt(get_pair(result, s, 'auto_tool', ('mini_low_auto', 'canonical'), ('mini_low', 'tool_canonical'), 'future_joint'))} on canonical input. " if 'auto_tool' in result['paired'][s] else '')
            + "At fixed input, letting the model delegate selection and rollout to code it writes is the most effective single placement, though not error-free; the before/after decomposition matters when a tool is unavailable or untrusted.")
    return text + '\n'


def numbers(result):
    s, p = 'heldout_v2', 'profiles_v2'
    c = result['cells']
    total = 4224 + sum(result['episodes'].values()) + (result['replication']['episodes'] if result.get('replication') else 0)
    macros = {'abstractRawMini': pct(c[p]['mini_low']['raw']['future_joint'], c[p]['mini_low']['raw']['n']),
              'abstractCanonMini': pct(c[p]['mini_low']['canonical']['future_joint'], c[p]['mini_low']['canonical']['n']),
              'abstractHybridMini': pct(c[p]['mini_low']['state_canonical']['future_joint'], c[p]['mini_low']['state_canonical']['n']),
              'abstractCanonStockMini': pct(c[p]['mini_low']['canonical']['stock_exact'], c[p]['mini_low']['canonical']['n']),
              'abstractSynthRawMini': pct(c[s]['mini_low']['raw']['future_joint'], c[s]['mini_low']['raw']['n']),
              'abstractSynthCanonMini': pct(c[s]['mini_low']['canonical']['future_joint'], c[s]['mini_low']['canonical']['n']),
              'abstractSynthHybridMini': pct(c[s]['mini_low']['state_canonical']['future_joint'], c[s]['mini_low']['state_canonical']['n']),
              'TotalRequests': f'{total:,}',
              'EffortRequests': f"{sum(v for k, v in result['episodes'].items() if k.startswith('effort')):,}",
              'StateRequests': f"{result['episodes']['state_synthetic_v1'] + result['episodes']['state_profiles_v1']:,}",
              'ToolRequests': f"{sum(v for k, v in result['episodes'].items() if k.startswith('tool')):,}",
              'ReplicationRequests': f"{result['replication']['episodes'] if result.get('replication') else 0:,}"}
    if has(result, s, 'mini_high_auto', 'raw'):
        macros['abstractAutoLowRaw'] = pct(c[s]['mini_low_auto']['raw']['future_joint'], c[s]['mini_low_auto']['raw']['n'])
        macros['abstractAutoHighRaw'] = pct(c[s]['mini_high_auto']['raw']['future_joint'], c[s]['mini_high_auto']['raw']['n'])
        macros['abstractForcedHighCanon'] = pct(c[s]['mini_high']['canonical']['future_joint'], c[s]['mini_high']['canonical']['n'])
        macros['abstractForcedLowCanon'] = pct(c[s]['mini_low']['canonical']['future_joint'], c[s]['mini_low']['canonical']['n'])
    if has(result, s, 'mini_low', 'tool_canonical'):
        macros['abstractToolMini'] = pct(c[p]['mini_low']['tool_canonical']['future_joint'], c[p]['mini_low']['tool_canonical']['n'])
        macros['abstractToolRawMini'] = pct(c[p]['mini_low']['tool_raw']['future_joint'], c[p]['mini_low']['tool_raw']['n'])
    return '\n'.join('\\newcommand{\\' + k + '}{' + v + '}' for k, v in macros.items()) + '\n'


def appendix_table(result):
    lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\begin{tabular}{lllrrrrrrr}', '\\toprule',
             'Cohort & Configuration & Arm & N & Invalid & Missing & All five & Stock & Hist. joint & Future joint \\\\', '\\midrule']
    for si, source in enumerate(('heldout_v2', 'profiles_v2')):
        if si:
            lines.append('\\midrule')
        for cfg in ALL_CONFIGS:
            for arm in ALL_ARMS:
                c = result['cells'][source].get(cfg, {}).get(arm)
                if c is None:
                    continue
                lines.append(' & '.join([COHORT_LABEL[source], LABELS[cfg], arm.replace('_', '-'), str(c['n']), str(c['invalid']), str(c['missing']),
                                         pct(c['joint_exact'], c['n']), pct(c['stock_exact'], c['n']), pct(c['historical_joint'], c['n']), pct(c['future_joint'], c['n'])]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{All cells of the original grid and the extension studies (\\%). State-only arms report the hybrid answer (model historical fields plus executable continuation); '
              'their future-joint accuracy equals their stock accuracy by conservation. Tool arms had a code-execution tool available. Invalid answers (missing, malformed or negative) fail every endpoint and remain in denominators.}',
              '\\label{tab:allcells}', '\\end{table}', '']
    return '\n'.join(lines)


def appendix_paired(result):
    tables = []
    for source in ('heldout_v2', 'profiles_v2'):
        lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\setlength{\\tabcolsep}{3pt}', '\\renewcommand{\\arraystretch}{0.92}',
                 '\\begin{tabular}{lllrr}', '\\toprule',
                 'Comparison (right minus left) & Metric & Bases & Difference & 95\\% interval \\\\', '\\midrule']
        for kind in ('original', 'effort', 'effort2', 'auto', 'state', 'tool', 'auto_tool'):
            for c in result['paired'][source].get(kind, []):
                if c['metric'] not in ('future_joint', 'stock_exact'):
                    continue
                lo, hi = c['ci95']
                left = f"{LABELS[c['left'][0]]}/{c['left'][1].replace('_', '-')}"
                right = f"{LABELS[c['right'][0]]}/{c['right'][1].replace('_', '-')}" if c['right'][0] != c['left'][0] else c['right'][1].replace('_', '-')
                lines.append(' & '.join([f'{left} $\\to$ {right}', c['metric'].replace('_', ' '), str(c['bases']),
                                         f"{100 * c['difference']:+.1f}", f"[{100 * lo:+.1f}, {100 * hi:+.1f}]"]) + ' \\\\')
        lines += ['\\bottomrule', '\\end{tabular}',
                  f'\\caption{{Paired differences in percentage points, {COHORT_LABEL[source].lower()} cohort: matched by history and repetition index, averaged within history; '
                  'descriptive 95\\% history-bootstrap percentile intervals (10,000 draws), not multiplicity adjusted. The same-period replication moved one identical cell by $-8.9$ points, so differences of that size are within run-to-run variation. '
                  'Cells at or near 100\\% give degenerate intervals. Identical rows arise when two comparisons have identical per-history differences.}',
                  f'\\label{{tab:extpaired_{source.split("_")[0]}}}', '\\end{table}', '']
        tables.append('\n'.join(lines))
    text = ''
    if result.get('replication'):
        r = result['replication']
        rows = ', '.join(f"{arm} {r['cells'][arm]['original']:.1f} vs {r['cells'][arm]['replication']:.1f}\\% ({fmt(r['cells'][arm]['paired_future_joint'])} points)" for arm in ('raw', 'canonical', 'snapshot'))
        stocks = ', '.join(f"{arm} {r['cells'][arm]['original_stock']:.1f} vs {r['cells'][arm]['replication_stock']:.1f}\\%" for arm in ('raw', 'canonical'))
        k = r['contemporaneous_effort_comparisons']
        contemporaneous = '; '.join(f"{LABELS[key.split('/')[0]]}/{key.split('/')[1]} {fmt(v)}" for key, v in k.items())
        ks = r.get('contemporaneous_state_comparisons', {})
        state = '; '.join(f"{key.replace('/', ' ').replace('_', ' ')} {fmt(v)}" for key, v in ks.items())
        text += (f"\\paragraph{{Same-period low-effort replication.}} The {r['episodes']}-call replication of mini's low-effort synthetic cells gives original versus replication future-joint accuracy of {rows}, and starting-stock accuracy of {stocks}. "
                 "The canonical cell replicates lower than the original, so collection-period variation of that size should be assumed when reading any single mini cell. "
                 f"Paired changes of the raised-effort cells relative to the replication baseline (future-joint, percentage points): {contemporaneous}. "
                 f"Paired changes of the state-only arms relative to the replication baseline: {state}.\n\n")
    if result.get('effort_error_profile'):
        text += '\\paragraph{Character of the raised-effort canonical errors.} ' + result['effort_error_profile']['sentence'] + '\n\n'
    if result.get('tool_profile'):
        tp = result['tool_profile']
        parts = []
        for arm in ('tool_raw', 'tool_canonical'):
            parts.append(f"{arm.replace('_', '-')}: " + ', '.join(f"{n_ev} events {tp[f'{arm}/{n_ev}']['no_code']} of {tp[f'{arm}/{n_ev}']['n']} without code ({tp[f'{arm}/{n_ev}']['no_code_exact']} exact), {tp[f'{arm}/{n_ev}']['code_wrong']} wrong with code" for n_ev in (12, 36, 72)))
        text += ('\\paragraph{Code-inside arm for mini on synthetic histories, by history length.} ' + '; '.join(parts) +
                 '. Calls answered without code concentrate on the shortest histories; the answers that were wrong despite running code are counted per stratum and were not individually inspected. The Anthropic configurations were not run with a code tool because their tool interface differs and both are at ceiling without it.\n\n')
    return text + '\n'.join(tables)


def effort_error_profile(extensions):
    """Offline characterization of wrong canonical stocks at raised effort: sign, size, simple hypotheses."""
    out = {}
    for run in ('effort_synthetic_v1', 'effort_profiles_v1'):
        manifest = extensions[run]['manifest']
        tasks = {t['base_id']: t for t in manifest['tasks']}
        for cfg in ('mini_medium', 'mini_high'):
            stats = {'wrong': 0, 'under': 0, 'over': 0, 'zero_stock': 0, 'demands_only_stock': 0, 'net_clip': 0, 'abs_errors': []}
            for file in sorted((ROOT / 'runs' / run).glob(f'{cfg}__canonical__*.json')):
                row = json.loads(file.read_text())
                if not row['score']['valid'] or row['score']['stock_at_target_exact']:
                    continue
                task = tasks[row['base_id']]
                events = benchmark.canonical_events(task)
                truth = benchmark.solve(task)['stock_at_target']
                emitted = row['answer']['stock_at_target']
                init = task['initial_stock']
                receipts = sum(e['quantity'] for e in events if e['kind'] == 'receipt')
                demands = sum(e['quantity'] for e in events if e['kind'] == 'demand')
                demands_only = benchmark.replay_state(task, events=[e for e in events if e['kind'] == 'demand'])['stock_at_target']
                stats['wrong'] += 1
                stats['under'] += emitted < truth
                stats['over'] += emitted > truth
                stats['zero_stock'] += emitted == 0 and truth > 0
                stats['demands_only_stock'] += emitted == demands_only
                stats['net_clip'] += emitted == max(0, init + receipts - demands)
                stats['abs_errors'].append(abs(emitted - truth))
            stats['median_abs_error'] = sorted(stats['abs_errors'])[len(stats['abs_errors']) // 2] if stats['abs_errors'] else None
            del stats['abs_errors']
            out[f'{run}/{cfg}'] = stats
    h = out['effort_synthetic_v1/mini_high']
    hp = out['effort_profiles_v1/mini_high']
    sentence = (f"Among mini's wrong canonical starting stocks at high effort, {h['under']} of {h['wrong']} synthetic and {hp['under']} of {hp['wrong']} profile answers are underestimates, with median absolute errors of {h['median_abs_error']} and {hp['median_abs_error']} units; "
                f"{h['zero_stock']} and {hp['zero_stock']} are exactly zero although the true stock is positive, {h['demands_only_stock']} and {hp['demands_only_stock']} equal the stock obtained by replaying only the demands, and {h['net_clip']} and {hp['net_clip']} equal the clipped net total. "
                "In twelve re-issued requests with reasoning summaries (diagnostic D1, supplement), the summaries lay out the correct selection and replay procedure, yet several answers are still zero or far too low, and one summary states that it must call the answer tool immediately and considers submitting placeholder zeros. "
                "This suggests that, under forced tool choice at raised effort, the model sometimes emits an answer before completing the replay it planned; the traces are illustrative, not a measured mechanism.")
    return {'cells': out, 'sentence': sentence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'extensions')
    parser.add_argument('--paper-dir', type=Path, default=ROOT / 'paper')
    parser.add_argument('--bootstrap', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=20260907)
    a = parser.parse_args()
    sources = {name: load_rows(name) for name in ('heldout_v2', 'profiles_v2')}
    studies = dict(REQUIRED_STUDIES)
    for kind, runs in OPTIONAL_STUDIES.items():
        if all((ROOT / 'runs' / name / 'analysis.json').exists() for name in runs):
            for name, source in runs.items():
                studies[name] = (kind, source)
    extensions = {name: load_rows(name) for name in studies}
    for name, (kind, source) in studies.items():
        check_task_identity(extensions[name], sources[source])
    merged = {src: dict(sources[src]['rows']) for src in sources}
    for name, (kind, source) in studies.items():
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
        if 'gpt54_high' in cells[source]:
            paired_out[source]['effort2'] = []
            for cfg, _ in EFFORTS_54[1:]:
                for arm in ('raw', 'canonical'):
                    for metric in ('future_joint', 'stock_exact', 'joint_exact'):
                        paired_out[source]['effort2'].append(paired(rows, ('gpt54_low', arm), rows, (cfg, arm), metric, a.bootstrap, a.seed))
        if 'tool_raw' in cells[source].get('mini_low', {}) and 'mini_low_auto' in cells[source]:
            paired_out[source]['auto_tool'] = [paired(rows, ('mini_low_auto', arm), rows, ('mini_low', 'tool_' + arm), metric, a.bootstrap, a.seed)
                                                for arm in ('raw', 'canonical') for metric in ('future_joint', 'stock_exact')]
        if 'tool_raw' in cells[source].get('mini_low', {}):
            paired_out[source]['tool'] = []
            for cfg in TOOL_CONFIGS:
                for arm in ('raw', 'canonical'):
                    for metric in ('future_joint', 'stock_exact', 'joint_exact'):
                        paired_out[source]['tool'].append(paired(rows, (cfg, arm), rows, (cfg, 'tool_' + arm), metric, a.bootstrap, a.seed))
                    paired_out[source]['tool'].append(paired(rows, (cfg, 'state_' + arm), rows, (cfg, 'tool_' + arm), 'future_joint', a.bootstrap, a.seed))
        for cfg in ('mini_low', 'gpt54_low', 'sonnet46', 'sonnet46_thinking'):
            paired_out[source].setdefault('original', [])
            for arm in ('canonical', 'snapshot'):
                for metric in ('future_joint', 'stock_exact'):
                    paired_out[source]['original'].append(paired(rows, (cfg, 'raw'), rows, (cfg, arm), metric, a.bootstrap, a.seed))
        if 'mini_high_auto' in cells[source]:
            paired_out[source]['auto'] = []
            for arm in ('raw', 'canonical'):
                for metric in ('future_joint', 'stock_exact'):
                    paired_out[source]['auto'].append(paired(rows, ('mini_low_auto', arm), rows, ('mini_high_auto', arm), metric, a.bootstrap, a.seed))
                    paired_out[source]['auto'].append(paired(rows, ('mini_low', arm), rows, ('mini_low_auto', arm), metric, a.bootstrap, a.seed))
                    paired_out[source]['auto'].append(paired(rows, ('mini_high', arm), rows, ('mini_high_auto', arm), metric, a.bootstrap, a.seed))
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
                              'paired_future_joint': paired(sources['heldout_v2']['rows'], ('mini_low', arm), rep['rows'], ('mini_low', arm), 'future_joint', a.bootstrap, a.seed),
                              'paired_stock_exact': paired(sources['heldout_v2']['rows'], ('mini_low', arm), rep['rows'], ('mini_low', arm), 'stock_exact', a.bootstrap, a.seed)}
        contemporaneous = {}
        for cfg in ('mini_medium', 'mini_high'):
            for arm in ('raw', 'canonical', 'snapshot'):
                contemporaneous[f'{cfg}/{arm}'] = paired(rep['rows'], ('mini_low', arm), merged['heldout_v2'], (cfg, arm), 'future_joint', a.bootstrap, a.seed)
        contemporaneous_state = {}
        for arm in ('raw', 'canonical'):
            for metric in ('stock_exact', 'future_joint'):
                contemporaneous_state[f'{arm}/{metric}'] = paired(rep['rows'], ('mini_low', arm), merged['heldout_v2'], ('mini_low', 'state_' + arm), metric, a.bootstrap, a.seed)
        replication = {'run': REPLICATION, 'episodes': rep['episodes'], 'problems': rep['problems'], 'cells': rep_cells,
                       'contemporaneous_effort_comparisons': contemporaneous,
                       'contemporaneous_state_comparisons': contemporaneous_state,
                       'provenance': {'manifest_sha256': rep['manifest_sha256'], 'episode_hashes_digest': rep['episode_hashes_digest']}}
    tool_profile = None
    if 'tool_synthetic_v1' in studies:
        manifest = extensions['tool_synthetic_v1']['manifest']
        events = {t['base_id']: t['n_events'] for t in manifest['tasks']}
        by_len = {}
        wrong_with_code = {}
        for (cfg, arm, base, rep), m in extensions['tool_synthetic_v1']['rows'].items():
            if cfg != 'mini_low':
                continue
            key = (arm, events[base])
            d = by_len.setdefault(key, {'n': 0, 'no_code': 0, 'no_code_exact': 0, 'code_wrong': 0})
            d['n'] += 1
            if m['code_calls'] == 0:
                d['no_code'] += 1
                d['no_code_exact'] += m['future_joint']
            elif not m['future_joint']:
                d['code_wrong'] += 1
        tool_profile = {f'{arm}/{n}': v for (arm, n), v in sorted(by_len.items())}
    result = {'analysis': 'extension_studies', 'protocol': 'protocol_v3_extensions.md', 'bootstrap_draws': a.bootstrap, 'seed': a.seed,
              'tool_profile': tool_profile,
              'studies': studies, 'replication': replication,
              'episodes': {name: extensions[name]['episodes'] for name in studies},
              'audit_problems': {name: extensions[name]['problems'] for name in studies},
              'source_audit_problems': {name: sources[name]['problems'] for name in sources},
              'provenance': {name: {'manifest_sha256': x['manifest_sha256'], 'episode_hashes_digest': x['episode_hashes_digest'],
                                    'source_sha256': x['manifest']['source_sha256']} for name, x in {**sources, **extensions}.items()},
              'cells': {s: {c: dict(v) for c, v in cells[s].items()} for s in cells},
              'paired': paired_out, 'baseline_paired': baseline_paired,
              'effort_error_profile': effort_error_profile(extensions),
              'notes': ['Every response reparsed; truth recomputed with the independent auditor replay; hybrid answers rebuilt with a separate scenario simulator.',
                        'Hybrid future-joint accuracy equals state-only starting-stock accuracy by conservation; verified on every valid hybrid answer.',
                        'Extension tasks are byte-identical to the archived heldout cohorts; they add configurations and arms, not independent histories.',
                        'Requested reasoning effort is a provider setting; reported reasoning tokens are provider usage fields, not a compute match.',
                        'Tool arms count code_interpreter_call items in the provider response; container charges are not in the token ledger.',
                        'All configurations, arms, invalid answers and truncations are retained; no retries, repairs or exclusions.']}
    result['audit_passed'] = not (any(extensions[n]['problems'] for n in studies) or any(sources[n]['problems'] for n in sources)
                                  or (replication and replication['problems']))
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / 'extensions.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Extension studies: independent analysis', '', *['- ' + n for n in result['notes']], '',
             f"Audit passed: {result['audit_passed']}; problems: {json.dumps(result['audit_problems'])}", '',
             '| Cohort | Configuration | Arm | N | Valid | Missing | Used code | All five | Stock exact | Hist. joint | Future joint | False alarms / neg. | Misses / pos. | Mean reasoning tokens | Cost USD |',
             '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for source in ('heldout_v2', 'profiles_v2'):
        for cfg in sorted(cells[source]):
            for arm, c in sorted(cells[source][cfg].items()):
                rt = f"{c['mean_reasoning_tokens']:.0f}" if c['mean_reasoning_tokens'] is not None else 'n/a'
                lines.append(f"| {source} | {cfg} | {arm} | {c['n']} | {c['valid']} | {c['missing']} | {c['used_code']} | {c['joint_exact']} | {c['stock_exact']} | {c['historical_joint']} | {c['future_joint']} | {c['false_alarms']}/{c['negatives']} | {c['misses']}/{c['positives']} | {rt} | {c['cost_usd']:.2f} |")
    lines += ['', '| Cohort | Kind | Left | Right | Metric | Bases | Difference [95% CI], pp |', '| --- | --- | --- | --- | --- | ---: | --- |']
    for source in paired_out:
        for kind, items in paired_out[source].items():
            for c in items:
                lines.append(f"| {source} | {kind} | {'/'.join(c['left'])} | {'/'.join(c['right'])} | {c['metric']} | {c['bases']} | {fmt(c)} |")
    lines += ['', '## Raised-effort canonical error profile', '', result['effort_error_profile']['sentence'], '',
              json.dumps(result['effort_error_profile']['cells'], indent=2)]
    (a.output_dir / 'extensions.md').write_text('\n'.join(lines) + '\n')
    a.paper_dir.mkdir(parents=True, exist_ok=True)
    (a.paper_dir / 'extension_effort_table.tex').write_text(effort_table(result))
    (a.paper_dir / 'extension_state_table.tex').write_text(placement_table(result))
    (a.paper_dir / 'extension_effort_findings.tex').write_text(effort_findings(result))
    (a.paper_dir / 'extension_state_findings.tex').write_text(state_findings(result))
    (a.paper_dir / 'extension_tool_findings.tex').write_text(tool_findings(result))
    (a.paper_dir / 'extension_numbers.tex').write_text(numbers(result))
    (a.paper_dir / 'extension_all_cells_table.tex').write_text(appendix_table(result))
    (a.paper_dir / 'extension_appendix.tex').write_text(appendix_paired(result))
    print(json.dumps({'audit_passed': result['audit_passed'], 'episodes': result['episodes']}))


if __name__ == '__main__':
    main()
