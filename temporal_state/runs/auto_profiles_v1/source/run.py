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
    # Extension study E1 (protocol_v3_extensions.md): same mini model, higher requested effort.
    'mini_medium': {'provider': 'openai', 'model': 'gpt-5.4-mini-2026-03-17', 'reasoning': 'medium'},
    'mini_high': {'provider': 'openai', 'model': 'gpt-5.4-mini-2026-03-17', 'reasoning': 'high'},
    # Extension study E3 (Amendment 2): GPT-5.4 at higher requested effort.
    'gpt54_medium': {'provider': 'openai', 'model': 'gpt-5.4-2026-03-05', 'reasoning': 'medium'},
    'gpt54_high': {'provider': 'openai', 'model': 'gpt-5.4-2026-03-05', 'reasoning': 'high'},
    # Extension study E5 (Amendment 3): automatic tool choice instead of a forced answer call.
    'mini_low_auto': {'provider': 'openai', 'model': 'gpt-5.4-mini-2026-03-17', 'reasoning': 'low', 'auto_tool_choice': True},
    'mini_high_auto': {'provider': 'openai', 'model': 'gpt-5.4-mini-2026-03-17', 'reasoning': 'high', 'auto_tool_choice': True},
    # Amendment 4 (protocol_v4_extensions.md): interface-matched GPT-5.4 cells and a second weak closed model.
    'gpt54_low_auto': {'provider': 'openai', 'model': 'gpt-5.4-2026-03-05', 'reasoning': 'low', 'auto_tool_choice': True},
    'gpt54_high_auto': {'provider': 'openai', 'model': 'gpt-5.4-2026-03-05', 'reasoning': 'high', 'auto_tool_choice': True},
    'haiku45': {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'haiku45_thinking': {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001', 'thinking_budget': 4096},
    # Amendment 4: open-weight ladder through OpenRouter chat completions, each pinned to one upstream provider.
    # Four cells per model: requested effort low/high crossed with forced/automatic tool choice (literal for the audit).
    'oss20b_low': {'provider': 'openrouter', 'model': 'openai/gpt-oss-20b', 'route': 'deepinfra', 'reasoning': 'low'},
    'oss20b_low_auto': {'provider': 'openrouter', 'model': 'openai/gpt-oss-20b', 'route': 'deepinfra', 'reasoning': 'low', 'auto_tool_choice': True},
    'oss20b_high': {'provider': 'openrouter', 'model': 'openai/gpt-oss-20b', 'route': 'deepinfra', 'reasoning': 'high'},
    'oss20b_high_auto': {'provider': 'openrouter', 'model': 'openai/gpt-oss-20b', 'route': 'deepinfra', 'reasoning': 'high', 'auto_tool_choice': True},
    'oss120b_low': {'provider': 'openrouter', 'model': 'openai/gpt-oss-120b', 'route': 'deepinfra', 'reasoning': 'low'},
    'oss120b_low_auto': {'provider': 'openrouter', 'model': 'openai/gpt-oss-120b', 'route': 'deepinfra', 'reasoning': 'low', 'auto_tool_choice': True},
    'oss120b_high': {'provider': 'openrouter', 'model': 'openai/gpt-oss-120b', 'route': 'deepinfra', 'reasoning': 'high'},
    'oss120b_high_auto': {'provider': 'openrouter', 'model': 'openai/gpt-oss-120b', 'route': 'deepinfra', 'reasoning': 'high', 'auto_tool_choice': True},
    'qwen27b_low': {'provider': 'openrouter', 'model': 'qwen/qwen3.8-27b', 'route': 'akashml', 'reasoning': 'low'},
    'qwen27b_low_auto': {'provider': 'openrouter', 'model': 'qwen/qwen3.8-27b', 'route': 'akashml', 'reasoning': 'low', 'auto_tool_choice': True},
    'qwen27b_high': {'provider': 'openrouter', 'model': 'qwen/qwen3.8-27b', 'route': 'akashml', 'reasoning': 'high'},
    'qwen27b_high_auto': {'provider': 'openrouter', 'model': 'qwen/qwen3.8-27b', 'route': 'akashml', 'reasoning': 'high', 'auto_tool_choice': True},
    'dsflash_low': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-flash-0731', 'route': 'baidu', 'reasoning': 'low'},
    'dsflash_low_auto': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-flash-0731', 'route': 'baidu', 'reasoning': 'low', 'auto_tool_choice': True},
    'dsflash_high': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-flash-0731', 'route': 'baidu', 'reasoning': 'high'},
    'dsflash_high_auto': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-flash-0731', 'route': 'baidu', 'reasoning': 'high', 'auto_tool_choice': True},
    'glmflash_low': {'provider': 'openrouter', 'model': 'z-ai/glm-5.3-flash', 'route': 'coreweave', 'reasoning': 'low'},
    'glmflash_low_auto': {'provider': 'openrouter', 'model': 'z-ai/glm-5.3-flash', 'route': 'coreweave', 'reasoning': 'low', 'auto_tool_choice': True},
    'glmflash_high': {'provider': 'openrouter', 'model': 'z-ai/glm-5.3-flash', 'route': 'coreweave', 'reasoning': 'high'},
    'glmflash_high_auto': {'provider': 'openrouter', 'model': 'z-ai/glm-5.3-flash', 'route': 'coreweave', 'reasoning': 'high', 'auto_tool_choice': True},
    'dspro_low': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-pro-0813', 'route': 'baidu', 'reasoning': 'low'},
    'dspro_low_auto': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-pro-0813', 'route': 'baidu', 'reasoning': 'low', 'auto_tool_choice': True},
    'dspro_high': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-pro-0813', 'route': 'baidu', 'reasoning': 'high'},
    'dspro_high_auto': {'provider': 'openrouter', 'model': 'deepseek/deepseek-v4-pro-0813', 'route': 'baidu', 'reasoning': 'high', 'auto_tool_choice': True},
}
FULL_ARMS = ('raw', 'canonical', 'snapshot')
# Extension study E2: the model returns only the two historical fields; code executes the future.
STATE_ARMS = ('state_raw', 'state_canonical')
# Extension study E4 (Amendment 2): same task, hosted code-execution tool available during the call.
TOOL_ARMS = ('tool_raw', 'tool_canonical')
ARMS = FULL_ARMS + STATE_ARMS + TOOL_ARMS
NETWORK_LIMITS = {p: threading.BoundedSemaphore(24) for p in ('openai', 'anthropic', 'openrouter')}
# Amendment 4: each pinned OpenRouter upstream also gets its own in-flight limit, and rate-limit or
# server-side transport errors (HTTP 429/5xx, no completion produced) are retried with backoff a
# bounded number of times. Model outputs are never re-sampled; every attempt count is stored.
ROUTE_LIMITS = {}
ROUTE_LIMIT_LOCK = threading.Lock()
ROUTE_IN_FLIGHT = 8
TRANSPORT_RETRY_CODES = ('provider_http_429', 'provider_http_5', 'provider_transport_')
TRANSPORT_MAX_ATTEMPTS = 6
TRANSPORT_BACKOFF_SECONDS = (5, 10, 20, 40, 80)


def route_limit(route):
    with ROUTE_LIMIT_LOCK:
        if route not in ROUTE_LIMITS:
            ROUTE_LIMITS[route] = threading.BoundedSemaphore(ROUTE_IN_FLIGHT)
        return ROUTE_LIMITS[route]


def transport_request(provider, cfg, payload, budget, episode):
    """One provider call for OpenAI/Anthropic; bounded transport retries for OpenRouter upstreams."""
    if provider != 'openrouter':
        return (*transport.request(provider, payload, budget, episode, timeout=420), 1)
    with route_limit(cfg['route']):
        for attempt in range(1, TRANSPORT_MAX_ATTEMPTS + 1):
            try:
                return (*transport.request(provider, payload, budget, episode, timeout=420), attempt)
            except RuntimeError as exc:
                retryable = str(exc).startswith(TRANSPORT_RETRY_CODES) and attempt < TRANSPORT_MAX_ATTEMPTS
                if not retryable:
                    raise
                time.sleep(TRANSPORT_BACKOFF_SECONDS[attempt - 1])
FIELDS = ('stock_at_target', 'historical_lost', 'stock_at_horizon', 'future_lost', 'first_future_stockout_time')
HISTORY_FIELDS = FIELDS[:2]
INSTRUCTIONS = '''Simulate a fictional lost-sales inventory system exactly. There is no stochastic prediction and no missing information beyond the explicit reporting cutoff.
Receipts add quantity to stock. Demands consume min(stock, quantity); any unmet quantity is lost (never backlogged). A stockout means strictly positive unmet demand, not merely ending with zero stock.
For raw report histories: first keep reports with received_time <= knowledge_cutoff. Then choose the highest visible revision for EACH event_id. Revisions REPLACE earlier reports, not add to them. Then keep chosen events with event_time <= target_time. Apply these events in (event_time, event_id) order, starting from initial_stock. Ignore any report not visible at the knowledge cutoff even if its event occurred earlier. Arrival order is not event order.
The canonical arm supplies the already selected eligible events in event-time order. The snapshot arm supplies the exactly replayed historical state. These are explicitly identified, executable preprocessing interventions.
After the historical reconstruction, apply every event in the given future_schedule in (event_time, event_id) order from the reconstructed stock. This is an explicitly known hypothetical scenario, not privileged knowledge about a real future.
Return five integers through submit_answer: stock_at_target; total historical_lost through target_time using visible revisions; stock_at_horizon after the scenario; future_lost for the scenario ONLY; first_future_stockout_time, the earliest future scenario event time with unmet demand, or -1 if no future demand is unmet. Do not count historical stockouts in that last field.'''
TOOL_INSTRUCTIONS = INSTRUCTIONS + '''
A Python code execution tool is available; you may use it to perform the replay exactly. The final answer must still be submitted through submit_answer.'''
_SPLIT = INSTRUCTIONS.index('After the historical reconstruction')
STATE_INSTRUCTIONS = INSTRUCTIONS[:_SPLIT] + '''There is no future scenario in this task: do not simulate or predict anything after target_time. A separate exact program will apply any future schedule to the state you report.
Return two integers through submit_answer: stock_at_target, the stock on hand at target_time after replaying the selected events; and historical_lost, the total unmet demand through target_time using visible revisions.'''


def input_for(task, arm):
    public = benchmark.public_task(task)
    if arm in TOOL_ARMS:
        base = input_for(task, arm.replace('tool_', ''))
        return {**base, 'input_representation': arm}
    if arm in STATE_ARMS:
        # Same history as the full arm; the future schedule and horizon are withheld.
        history = {k: v for k, v in public.items() if k not in ('future_schedule', 'horizon_time')}
        if arm == 'state_raw':
            return {'input_representation': 'state_raw', **history}
        history.pop('reports')
        return {'input_representation': 'state_canonical', **history, 'eligible_events': benchmark.canonical_events(task)}
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
    fields = HISTORY_FIELDS if arm in STATE_ARMS else FIELDS
    instructions = STATE_INSTRUCTIONS if arm in STATE_ARMS else TOOL_INSTRUCTIONS if arm in TOOL_ARMS else INSTRUCTIONS
    schema = {'type': 'object', 'properties': {k: {'type': 'integer'} for k in fields},
              'required': list(fields), 'additionalProperties': False}
    if cfg['provider'] == 'openai':
        tools = [dict(type='function', name='submit_answer', description='Submit exact simulated quantities.', parameters=schema, strict=True)]
        choice = 'auto' if cfg.get('auto_tool_choice') else {'type': 'function', 'name': 'submit_answer'}
        if arm in TOOL_ARMS:
            tools.append(dict(type='code_interpreter', container={'type': 'auto'}))
            choice = 'auto'
        return dict(model=cfg['model'], instructions=instructions,
                    input=[{'role': 'user', 'content': body}],
                    tools=tools, tool_choice=choice, parallel_tool_calls=False,
                    max_output_tokens=16384, reasoning={'effort': cfg['reasoning']}, store=False)
    if arm in TOOL_ARMS:
        raise ValueError('code-inside arms are defined for the OpenAI provider only')
    if cfg['provider'] == 'openrouter':
        # OpenAI-compatible chat completions. Same instructions, body, strict schema and output limit;
        # OpenRouter's unified reasoning.effort carries the requested effort; provider routing is pinned
        # with fallbacks disabled so every call in a cell is served by one upstream provider. Only
        # parameters the pinned endpoints advertise are sent (require_parameters rejects any other);
        # a response with two tool calls is a missing answer exactly as for the other providers.
        tools = [dict(type='function', function=dict(name='submit_answer', description='Submit exact simulated quantities.',
                                                     parameters=schema, strict=True))]
        choice = 'auto' if cfg.get('auto_tool_choice') else {'type': 'function', 'function': {'name': 'submit_answer'}}
        return dict(model=cfg['model'],
                    messages=[{'role': 'system', 'content': instructions}, {'role': 'user', 'content': body}],
                    tools=tools, tool_choice=choice,
                    max_tokens=16384, reasoning={'effort': cfg['reasoning']},
                    provider={'only': [cfg['route']], 'allow_fallbacks': False, 'require_parameters': True})
    payload = dict(model=cfg['model'], system=instructions, messages=[{'role': 'user', 'content': body}],
                tools=[dict(name='submit_answer', description='Submit exact simulated quantities.', input_schema=schema, strict=True)],
                tool_choice={'type': 'auto', 'disable_parallel_tool_use': True}, max_tokens=16384)
    if cfg.get('thinking_budget'):
        payload['thinking'] = {'type': 'enabled', 'budget_tokens': cfg['thinking_budget']}
    return payload


def chat_completion_answer(response):
    """Exactly one submit_answer tool call in the single chat-completions choice; otherwise None.

    Arguments arrive as a JSON string; a provider that returns an object is accepted unchanged.
    Reasoning text in the message content is ignored; only the tool call carries the answer.
    """
    choices = response.get('choices') or []
    if len(choices) != 1:
        return None
    calls = [c for c in (choices[0].get('message') or {}).get('tool_calls') or []
             if c.get('type', 'function') == 'function' and (c.get('function') or {}).get('name') == 'submit_answer']
    if len(calls) != 1:
        return None
    arguments = calls[0]['function'].get('arguments')
    return json.loads(arguments) if isinstance(arguments, str) else arguments


def hybrid_answer(task, answer):
    """Two-field state answer plus exact code execution of the supplied future schedule.

    Returns None when the two-field contract is invalid; nothing is repaired.
    """
    valid = (type(answer) is dict and set(answer) == set(HISTORY_FIELDS)
             and all(type(answer[f]) is int and answer[f] >= 0 for f in HISTORY_FIELDS))
    if not valid:
        return None
    # The reference simulator with no historical events starts the scenario from the emitted stock.
    rollout = benchmark.replay_state({**task, 'initial_stock': answer['stock_at_target']}, events=[])
    return {**answer, **{k: rollout[k] for k in FIELDS[2:]}}


def score_for(task, arm, answer):
    if arm in STATE_ARMS:
        hybrid = hybrid_answer(task, answer)
        return benchmark.score(task, hybrid), hybrid
    return benchmark.score(task, answer), None


def evaluate(task, cfg, arm, rep, budget, directory):
    key = f"{cfg}__{arm}__r{rep}__{task['base_id']}"
    payload = request_for(task, cfg, arm)
    provider = CONFIGS[cfg]['provider']
    row = dict(episode=key, base_id=task['base_id'], configuration=cfg, arm=arm, rep=rep,
               model=CONFIGS[cfg]['model'], request=payload, answer=None, status='error', cost_usd=0.)
    start = time.monotonic()
    try:
        with NETWORK_LIMITS[provider]:
            response, cost, attempts = transport_request(provider, CONFIGS[cfg], payload, budget, 'temporal__'+key)
        row.update(response=response, cost_usd=cost)
        if attempts != 1:
            row['transport_attempts'] = attempts
        if provider == 'openai':
            calls = [c for c in response.get('output', []) if c.get('type') == 'function_call' and c.get('name') == 'submit_answer']
            answer = json.loads(calls[0]['arguments']) if len(calls) == 1 else None
        elif provider == 'openrouter':
            answer = chat_completion_answer(response)
        else:
            calls = [c for c in response.get('content', []) if c.get('type') == 'tool_use' and c.get('name') == 'submit_answer']
            answer = calls[0]['input'] if len(calls) == 1 else None
        row.update(answer=answer, status='submitted' if answer is not None else 'missing_answer')
    except Exception as exc:
        row['error'] = str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__
    row['elapsed_seconds'] = time.monotonic()-start
    row['score'], hybrid = score_for(task, arm, row['answer'])
    if arm in STATE_ARMS:
        row['hybrid_answer'] = hybrid
    (directory/(key+'.json')).write_text(json.dumps(row, indent=2))
    return {k: row[k] for k in ('episode','status','score','cost_usd')} | ({'error':row['error']} if 'error' in row else {})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', required=True)
    p.add_argument('--split', choices=['dev','heldout'], default='dev')
    p.add_argument('--seed', type=int, default=2026090801)
    p.add_argument('--n-base', type=int, default=12)
    p.add_argument('--configs', nargs='+', choices=list(CONFIGS), default=list(CONFIGS))
    p.add_argument('--arms', nargs='+', choices=list(ARMS), default=list(FULL_ARMS))
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
                    state_instructions=STATE_INSTRUCTIONS,
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
