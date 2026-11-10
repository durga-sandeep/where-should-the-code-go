"""Analyze temporal replay episodes without API calls or third-party dependencies.

Stored score fields are analyzed; this is not an independent implementation of
replay semantics. Completeness checks include every manifest grid coordinate.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random

FIELDS = ('stock_at_target', 'historical_lost', 'stock_at_horizon',
          'future_lost', 'first_future_stockout_time')
METRICS = ('valid', 'joint_exact', *(f'{x}_exact' for x in FIELDS),
           'historical_joint', 'future_joint')


def task_id(task):
    value = task.get('base_id', task.get('task_id'))
    if value is None:
        raise ValueError('Task missing base_id/task_id')
    return str(value)


def coordinate(row):
    return (str(row['base_id']), row['configuration'], row['arm'], int(row['rep']))


def metrics(row):
    score = row.get('score') or {}
    # Invalid contracts cannot enter primary task accuracy, even if an individual
    # field happened to be correct; unconditioned raw fields are not reconstructed.
    valid = score.get('valid') is True and row.get('status') != 'error'
    out = {'valid': valid}
    out.update({f'{f}_exact': valid and score.get(f'{f}_exact') is True for f in FIELDS})
    out['historical_joint'] = all(out[f'{f}_exact'] for f in FIELDS[:2])
    out['future_joint'] = all(out[f'{f}_exact'] for f in FIELDS[2:])
    out['joint_exact'] = all(out[f'{f}_exact'] for f in FIELDS)
    if 'joint_exact' in score and valid and bool(score['joint_exact']) != out['joint_exact']:
        raise ValueError(f'Inconsistent stored joint score at {coordinate(row)}')
    return out


def quantile(values, p):
    values = sorted(values)
    position = (len(values) - 1) * p
    lo = int(position)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (position - lo)


def bootstrap(differences, draws=10000, seed=20260907):
    if draws < 1:
        raise ValueError('bootstrap draws must be positive')
    if not differences:
        return None
    rng = random.Random(seed)
    means = [sum(rng.choices(differences, k=len(differences))) / len(differences)
             for _ in range(draws)]
    return [quantile(means, .025), quantile(means, .975)]


def summarize(rows):
    evaluated = [metrics(r) for r in rows]
    successes = {key: sum(m[key] for m in evaluated) for key in METRICS}
    historical_correct = successes['historical_joint']
    future_wrong = sum(m['historical_joint'] and not m['future_joint'] for m in evaluated)
    invalid_reasons = Counter((r.get('score') or {}).get('invalid_reason') or r.get('status', 'unknown')
                             for r, m in zip(rows, evaluated) if not m['valid'])
    costs = [r.get('cost_usd') for r in rows]
    return {'n': len(rows), 'successes': successes,
            'rates': {k: v / len(rows) if rows else None for k, v in successes.items()},
            'invalid': len(rows) - successes['valid'], 'invalid_reasons': dict(invalid_reasons),
            'future_wrong_given_historical_correct': {'numerator': future_wrong,
                'denominator': historical_correct,
                'rate': future_wrong / historical_correct if historical_correct else None},
            'estimated_cost_usd': sum(v for v in costs if isinstance(v, (int, float))),
            'missing_cost_records': sum(v is None for v in costs)}


def paired(left, right, metric, draws=10000, seed=20260907):
    l = {(str(r['base_id']), int(r['rep'])): metrics(r)[metric] for r in left}
    r = {(str(x['base_id']), int(x['rep'])): metrics(x)[metric] for x in right}
    matched = sorted(l.keys() & r.keys())
    groups = defaultdict(list)
    for key in matched:
        groups[key[0]].append(int(r[key]) - int(l[key]))
    diffs = [sum(v) / len(v) for _, v in sorted(groups.items())]
    return {'metric': metric, 'matched_bases': len(diffs), 'matched_episodes': len(matched),
            'unmatched_left': len(l.keys() - r.keys()), 'unmatched_right': len(r.keys() - l.keys()),
            'difference': sum(diffs) / len(diffs) if diffs else None,
            'ci95': bootstrap(diffs, draws, seed)}


def analyze(manifest, rows, draws=10000, seed=20260907):
    args = manifest['args']
    tasks = {task_id(t): t for t in manifest['tasks']}
    if len(tasks) != len(manifest['tasks']):
        raise ValueError('Duplicate manifest base IDs; define the independent base explicitly')
    expected = {(base, cfg, arm, rep) for base in tasks for cfg in args['configs']
                for arm in args['arms'] for rep in range(args['reps'])}
    seen = Counter(coordinate(r) for r in rows)
    duplicates = [list(k) for k, n in seen.items() if n != 1]
    if duplicates:
        raise ValueError(f'Duplicate episode coordinates: {duplicates[:3]}')
    actual = set(seen)
    missing, unexpected = sorted(expected - actual), sorted(actual - expected)
    included = [r for r in rows if coordinate(r) in expected]
    cells = defaultdict(list)
    strata = defaultdict(list)
    for row in included:
        key = (row['configuration'], row['arm'])
        cells[key].append(row)
        task = tasks[str(row['base_id'])]
        meta = task.get('metadata', {})
        for factor in ('n_events', 'late_arrival', 'corrections', 'future_pressure'):
            value = task.get(factor, meta.get(factor, 'missing'))
            strata[(*key, factor, json.dumps(value, sort_keys=True))].append(row)
    comparisons = []
    for cfg in args['configs']:
        for arm in ('canonical', 'snapshot'):
            if (cfg, 'raw') not in cells or (cfg, arm) not in cells:
                continue
            for metric in ('joint_exact', 'historical_joint', 'future_joint'):
                comparisons.append({'configuration': cfg, 'left': 'raw', 'right': arm,
                    **paired(cells[cfg, 'raw'], cells[cfg, arm], metric, draws, seed)})
    return {'complete': not missing and not unexpected, 'expected_episodes': len(expected),
            'observed_episodes': len(included), 'missing': [list(k) for k in missing],
            'unexpected': [list(k) for k in unexpected], 'bootstrap_draws': draws, 'seed': seed,
            'summary': summarize(included),
            'cells': [{'configuration': k[0], 'arm': k[1], **summarize(v)} for k, v in sorted(cells.items())],
            'factor_strata': [{'configuration': k[0], 'arm': k[1], 'factor': k[2],
                'level': json.loads(k[3]), **summarize(v)} for k, v in sorted(strata.items())],
            'paired_comparisons': comparisons,
            'notes': ['Stored scorer output analyzed; not independent replay validation.',
                'Primary accuracies require a valid full output contract.',
                'Paired differences average matched repetitions within independent base, then bootstrap bases.',
                'Intervals are descriptive, percentile, and not multiplicity adjusted.',
                'Missing grid entries are reported, not imputed as model failures; incomplete runs are provisional.',
                'Factor strata are descriptive; no independent-episode significance claims.']}


def render(result):
    def pct(x):
        return 'NA' if x is None else f'{100*x:.1f}%'
    lines = ['# Temporal state reconstruction results', '',
             f"Status: {'complete' if result['complete'] else 'INCOMPLETE — provisional'}. "
             f"{result['observed_episodes']}/{result['expected_episodes']} expected episodes.", '',
             '| Configuration | Arm | N | Valid | Joint exact | Historical joint | Future joint | Future wrong / history correct | Cost estimate |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for c in result['cells']:
        s, d = c['successes'], c['future_wrong_given_historical_correct']
        lines.append(f"| {c['configuration']} | {c['arm']} | {c['n']} | {s['valid']} | {s['joint_exact']} | {s['historical_joint']} | {s['future_joint']} | {d['numerator']}/{d['denominator']} | ${c['estimated_cost_usd']:.4f} |")
    lines += ['', 'All accuracy entries above are success counts. Full per-field metrics, invalid reasons and factor strata are in `analysis.json`.', '',
              '## Paired differences (right minus raw)', '',
              '| Configuration | Right arm | Metric | Bases | Difference | 95% interval |',
              '| --- | --- | --- | ---: | ---: | --- |']
    for c in result['paired_comparisons']:
        interval = 'NA' if c['ci95'] is None else ' to '.join(pct(x) for x in c['ci95'])
        lines.append(f"| {c['configuration']} | {c['right']} | {c['metric']} | {c['matched_bases']} | {pct(c['difference'])} | {interval} |")
    lines += ['', 'Differences and intervals are percentage-point differences, not relative percentage changes.', '', *[f'- {n}' for n in result['notes']], '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('--bootstrap', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=20260907)
    args = parser.parse_args()
    manifest = json.loads((args.run_dir / 'manifest.json').read_text())
    rows = []
    for path in sorted(args.run_dir.glob('*.json')):
        if path.name in ('manifest.json', 'analysis.json'):
            continue
        item = json.loads(path.read_text())
        if isinstance(item, dict) and all(k in item for k in ('configuration', 'arm', 'rep', 'base_id')):
            rows.append(item)
    result = analyze(manifest, rows, args.bootstrap, args.seed)
    (args.run_dir / 'analysis.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    (args.run_dir / 'results.md').write_text(render(result))
    print(json.dumps({k: result[k] for k in ('complete', 'expected_episodes', 'observed_episodes')}))


if __name__ == '__main__':
    main()
