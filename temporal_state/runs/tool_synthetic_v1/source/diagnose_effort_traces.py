"""Exploratory trace diagnostic D1 (protocol_v3_extensions.md, Amendment 2). Paid calls.

Re-issues twelve failing mini_high canonical synthetic requests with a detailed reasoning
summary so the failure can be characterized qualitatively. Episodes are chosen by sorted
filename before any inspection of their content. Outputs are illustrative only and are
excluded from every accuracy estimate.
"""
import argparse
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from completeness_pilot import run_pilot as transport  # noqa: E402
from temporal_state import benchmark, run as runner  # noqa: E402

SOURCE = 'effort_synthetic_v1'
CONFIG = 'mini_high'
ARM = 'canonical'


def select(n):
    path = ROOT / 'runs' / SOURCE
    manifest = json.loads((path / 'manifest.json').read_text())
    tasks = {t['base_id']: t for t in manifest['tasks']}
    chosen = []
    for file in sorted(path.glob(f'{CONFIG}__{ARM}__*.json')):
        row = json.loads(file.read_text())
        if row['score']['valid'] and not row['score']['stock_at_target_exact']:
            chosen.append((file.name, tasks[row['base_id']], row))
        if len(chosen) == n:
            break
    return chosen


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--n', type=int, default=12)
    p.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'effort_traces')
    p.add_argument('--execute', action='store_true')
    a = p.parse_args()
    chosen = select(a.n)
    print(json.dumps({'selected': [c[0] for c in chosen], 'execute': a.execute}), flush=True)
    if not a.execute:
        return
    lock = (transport.ROOT / '.runner.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    a.output_dir.mkdir(parents=True, exist_ok=True)
    budget = transport.Budget(3000.)
    records = []
    for name, task, original in chosen:
        payload = runner.request_for(task, CONFIG, ARM)
        payload['reasoning'] = {'effort': runner.CONFIGS[CONFIG]['reasoning'], 'summary': 'detailed'}
        response, cost = transport.request('openai', payload, budget, 'trace__' + name, timeout=420)
        calls = [c for c in response.get('output', []) if c.get('type') == 'function_call' and c.get('name') == 'submit_answer']
        answer = json.loads(calls[0]['arguments']) if len(calls) == 1 else None
        summaries = [s.get('text', '') for o in response.get('output', []) if o.get('type') == 'reasoning' for s in (o.get('summary') or [])]
        record = {'source_episode': name, 'base_id': task['base_id'], 'truth': benchmark.solve(task),
                  'original_answer': original['answer'], 'trace_answer': answer, 'trace_score': benchmark.score(task, answer),
                  'reasoning_summary': summaries, 'usage': response.get('usage'), 'cost_usd': cost,
                  'canonical_events': benchmark.canonical_events(task), 'initial_stock': task['initial_stock'],
                  'request': payload, 'response': response}
        records.append(record)
        (a.output_dir / ('trace__' + name)).write_text(json.dumps(record, indent=2))
        print(json.dumps({'episode': name, 'truth_stock': record['truth']['stock_at_target'], 'original': original['answer']['stock_at_target'],
                          'trace': None if answer is None else answer['stock_at_target'], 'summary_chars': sum(len(s) for s in summaries)}), flush=True)
    lines = ['# Reasoning-summary traces for failing mini high-effort canonical episodes', '',
             'Exploratory diagnostic D1; illustrative only, excluded from all estimates. Each trace is a fresh call with an identical request plus a detailed reasoning summary; the model is stochastic, so the trace answer may differ from the original.', '',
             f'Created {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}.', '']
    for r in records:
        ev = r['canonical_events']
        lines += [f"## {r['source_episode']}", '',
                  f"initial stock {r['initial_stock']}; {len(ev)} canonical events ({sum(e['kind']=='receipt' for e in ev)} receipts totalling {sum(e['quantity'] for e in ev if e['kind']=='receipt')}, {sum(e['kind']=='demand' for e in ev)} demands totalling {sum(e['quantity'] for e in ev if e['kind']=='demand')}); "
                  f"truth stock {r['truth']['stock_at_target']}, loss {r['truth']['historical_lost']}; original answer stock {r['original_answer']['stock_at_target']}, loss {r['original_answer']['historical_lost']}; "
                  f"trace answer {r['trace_answer']}; trace stock exact: {r['trace_score']['stock_at_target_exact']}", '',
                  *(['```', *r['reasoning_summary'], '```'] if r['reasoning_summary'] else ['(no summary returned)']), '']
    (a.output_dir / 'TRACES.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'written': len(records), 'cost_usd': sum(r['cost_usd'] for r in records)}), flush=True)


if __name__ == '__main__':
    main()
