"""Temporal simulation experiments; no paid request unless explicitly invoked."""
import argparse
import concurrent.futures
import fcntl
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import time
import threading

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from completeness_pilot import run_pilot as transport
from temporal_state import benchmark

CONFIGS = {
    'mini_low': {'provider': 'openai', 'model': 'gpt-5.4-mini-2026-03-17', 'reasoning': 'low'},
    'gpt54_low': {'provider': 'openai', 'model': 'gpt-5.4-2026-03-05', 'reasoning': 'low'},
    'sonnet46': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'sonnet46_thinking': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6', 'thinking_budget': 4096},
}
NETWORK_LIMITS = {p: threading.BoundedSemaphore(24) for p in ('openai', 'anthropic')}
FIELDS = ('stock_at_target', 'historical_lost', 'stock_at_horizon', 'future_lost', 'first_future_stockout_time')
INSTRUCTIONS = '''Simulate a fictional lost-sales inventory system exactly. There is no stochastic prediction and no missing information beyond the explicit reporting cutoff.
Receipts add quantity to stock. Demands consume min(stock, quantity); any unmet quantity is lost (never backlogged). A stockout means strictly positive unmet demand, not merely ending with zero stock.
For raw report histories: first keep reports with received_time <= knowledge_cutoff. Then choose the highest visible revision for EACH event_id. Revisions REPLACE earlier reports, not add to them. Then keep chosen events with event_time <= target_time. Apply these events in (event_time, event_id) order, starting from initial_stock. Ignore any report not visible at the knowledge cutoff even if its event occurred earlier. Arrival order is not event order.
The canonical arm supplies the already selected eligible events in event-time order. The snapshot arm supplies the exactly replayed historical state. These are explicitly identified, executable preprocessing interventions.
After the historical reconstruction, apply every event in the given future_schedule in (event_time, event_id) order from the reconstructed stock. This is an explicitly known hypothetical scenario, not privileged knowledge about a real future.
Return five integers through submit_answer: stock_at_target; total historical_lost through target_time using visible revisions; stock_at_horizon after the scenario; future_lost for the scenario ONLY; first_future_stockout_time, the earliest future scenario event time with unmet demand, or -1 if no future demand is unmet. Do not count historical stockouts in that last field.'''


def input_for(task, arm):
    public = benchmark.public_task(task)
    if arm == 'raw':
        return {'input_representation': 'raw', **public}
    shared = {k: v for k, v in public.items() if k != 'reports'}
    if arm == 'canonical':
        return {'input_representation': 'canonical', **shared, 'eligible_events': benchmark.canonical_events(task)}
    if arm == 'snapshot':
        state = benchmark.replay_state(task)
        return {'input_representation': 'snapshot', **shared,
                'historical_state': {k: state[k] for k in ('stock_at_target', 'historical_lost')}}
    raise ValueError('unknown arm')


def request_for(task, config, arm):
    cfg = CONFIGS[config]
    body = json.dumps(input_for(task, arm), separators=(',', ':'))
    schema = {'type': 'object', 'properties': {k: {'type': 'integer'} for k in FIELDS},
              'required': list(FIELDS), 'additionalProperties': False}
    if cfg['provider'] == 'openai':
        return dict(model=cfg['model'], instructions=INSTRUCTIONS,
                    input=[{'role': 'user', 'content': body}],
                    tools=[dict(type='function', name='submit_answer', description='Submit exact simulated quantities.', parameters=schema, strict=True)],
                    tool_choice={'type': 'function', 'name': 'submit_answer'}, parallel_tool_calls=False,
                    max_output_tokens=16384, reasoning={'effort': cfg['reasoning']}, store=False)
    payload = dict(model=cfg['model'], system=INSTRUCTIONS, messages=[{'role': 'user', 'content': body}],
                tools=[dict(name='submit_answer', description='Submit exact simulated quantities.', input_schema=schema, strict=True)],
                tool_choice={'type': 'auto', 'disable_parallel_tool_use': True}, max_tokens=16384)
    if cfg.get('thinking_budget'):
        payload['thinking'] = {'type': 'enabled', 'budget_tokens': cfg['thinking_budget']}
    return payload


def evaluate(task, cfg, arm, rep, budget, directory):
    key = f"{cfg}__{arm}__r{rep}__{task['base_id']}"
    payload = request_for(task, cfg, arm)
    provider = CONFIGS[cfg]['provider']
    row = dict(episode=key, base_id=task['base_id'], configuration=cfg, arm=arm, rep=rep,
               model=CONFIGS[cfg]['model'], request=payload, answer=None, status='error', cost_usd=0.)
    start = time.monotonic()
    try:
        with NETWORK_LIMITS[provider]:
            response, cost = transport.request(provider, payload, budget, 'temporal__'+key, timeout=420)
        row.update(response=response, cost_usd=cost)
        if provider == 'openai':
            calls = [c for c in response.get('output', []) if c.get('type') == 'function_call' and c.get('name') == 'submit_answer']
            answer = json.loads(calls[0]['arguments']) if len(calls) == 1 else None
        else:
            calls = [c for c in response.get('content', []) if c.get('type') == 'tool_use' and c.get('name') == 'submit_answer']
            answer = calls[0]['input'] if len(calls) == 1 else None
        row.update(answer=answer, status='submitted' if answer is not None else 'missing_answer')
    except Exception as exc:
        row['error'] = str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__
    row['elapsed_seconds'] = time.monotonic()-start
    row['score'] = benchmark.score(task, row['answer'])
    (directory/(key+'.json')).write_text(json.dumps(row, indent=2))
    return {k: row[k] for k in ('episode','status','score','cost_usd')} | ({'error':row['error']} if 'error' in row else {})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', required=True)
    p.add_argument('--split', choices=['dev','heldout'], default='dev')
    p.add_argument('--seed', type=int, default=2026090801)
    p.add_argument('--n-base', type=int, default=12)
    p.add_argument('--configs', nargs='+', choices=list(CONFIGS), default=list(CONFIGS))
    p.add_argument('--arms', nargs='+', choices=['raw','canonical','snapshot'], default=['raw','canonical','snapshot'])
    p.add_argument('--reps', type=int, default=1)
    p.add_argument('--workers', type=int, default=6)
    p.add_argument('--cap', type=float, default=3000.)
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--dataset', choices=['synthetic','profiles'], default='synthetic')
    p.add_argument('--source-run')
    p.add_argument('--knowledge-cutoff', type=int)
    p.add_argument('--shuffle-reports', action='store_true')
    args = p.parse_args()
    if args.n_base<1 or args.reps<1 or args.workers<1 or '/' in args.run or args.run.startswith('.'):
        p.error('positive sizes and simple fresh run name required')
    lock = (transport.ROOT/'.runner.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
    if args.source_run:
        source_manifest = json.loads((ROOT/'runs'/args.source_run/'manifest.json').read_text())
        tasks = source_manifest['tasks'][:args.n_base]
        if len(tasks) != args.n_base: raise ValueError('insufficient source tasks')
    else:
        if args.dataset == 'profiles':
            from temporal_state import external_benchmark
            tasks = external_benchmark.generate_tasks(n_base=args.n_base, seed=args.seed, split=args.split)
        else:
            tasks = benchmark.generate_tasks(n_base=args.n_base, seed=args.seed, split=args.split)
    for task in tasks:
        if args.knowledge_cutoff is not None: task['knowledge_cutoff'] = args.knowledge_cutoff
        if args.shuffle_reports: random.Random('display:'+task['base_id']).shuffle(task['reports'])
    jobs = [(t,c,a,r) for t in tasks for c in args.configs for a in args.arms for r in range(args.reps)]
    random.Random(args.seed).shuffle(jobs)
    out = ROOT/'runs'/args.run
    out.mkdir(parents=True, exist_ok=False)
    (out/'source').mkdir()
    sources = list(ROOT.glob('*.py')) + list(ROOT.glob('*protocol*.md')) + [transport.ROOT/'run_pilot.py']
    hashes = {}
    for source in sources:
        frozen_bytes = source.read_bytes()
        (out/'source'/source.name).write_bytes(frozen_bytes)
        hashes[source.name] = hashlib.sha256(frozen_bytes).hexdigest()
    manifest = dict(created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()), args=vars(args),
                    jobs=len(jobs), tasks=tasks, configs=CONFIGS, instructions=INSTRUCTIONS,
                    source_sha256=hashes, notes='Same latent task paired across preprocessing arms. No retry or repair. Scenario simulation, not statistical forecasting.')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    if args.dry_run:
        (out/'requests_preview.json').write_text(json.dumps({a:request_for(tasks[0],args.configs[0],a) for a in args.arms},indent=2))
        print(json.dumps({'dry_run':True,'jobs':len(jobs),'outdir':str(out)}));return
    budget = transport.Budget(args.cap)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate,*job,budget,out) for job in jobs]
        for i,future in enumerate(concurrent.futures.as_completed(futures),1):
            result=future.result()
            print(json.dumps({'completed':i,'total':len(jobs),**result}),flush=True)
            if result['status']=='error':
                for pending in futures: pending.cancel()
                (out/'interruption.json').write_text(json.dumps(result,indent=2))
                raise RuntimeError('Study interrupted by infrastructure failure; see interruption.json')


if __name__=='__main__': main()
