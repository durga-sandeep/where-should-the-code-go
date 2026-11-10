"""Bounded synthetic tool-use pilot. Only fictional task content reaches APIs."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import random
import threading
import time
import urllib.error
import urllib.request

try:
    from . import benchmark
except ImportError:
    import benchmark

ROOT = Path(__file__).resolve().parent
MODELS = {
    'openai': ('gpt-5.4-mini-2026-03-17', .75, 4.50),
    'anthropic': ('claude-haiku-4-5-20251001', 1., 5.),
}
PRICING = {v[0]: v[1:] for v in MODELS.values()}
PRICING.update({'gpt-5.4-2026-03-05': (2.50, 15.), 'claude-sonnet-4-6': (3., 15.)})
SYSTEM = ('Solve the user task using list_records. Records are fictional. '
          'Call submit_answer to finish. Never invent record identifiers. '
          'The next_cursor value is an opaque pagination token; null means no more pages. '
          'For one/all use ids (empty if no matches); for count use count; '
          'for none use none=true iff no matching records exist. Submit only the applicable field.')
STRONG = (' Before finishing, check the evidence needed for the requested quantifier. '
          'For all or count, visit every page. For one, a matching witness suffices, '
          'but reporting no match requires visiting every page. For none, a matching '
          'witness establishes false; establishing true requires visiting every page. '
          'Follow each non-null next_cursor until null whenever exhaustive coverage is needed.')
SCHEMAS = [
    {'name': 'list_records', 'description': 'List a page of records. Omit cursor or use null for the first page; use returned next_cursor for subsequent pages.',
     'parameters': {'type': 'object', 'properties': {'cursor': {'type': ['string', 'null']}}, 'additionalProperties': False}},
    {'name': 'submit_answer', 'description': 'Submit the final answer for the requested task.',
     'parameters': {'type': 'object', 'properties': {'ids': {'type': 'array', 'items': {'type': 'string'}}, 'count': {'type': 'integer'}, 'none': {'type': 'boolean'}}, 'additionalProperties': False}},
]


class Budget:
    """Persistent conservative reservation ledger; ambiguous calls retain reservation."""
    def __init__(self, cap):
        self.path = ROOT / 'api_budget.json'
        self.lock = threading.Lock()
        self.cap = min(cap, 3000.)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {'calls': [], 'note': 'USD estimates, not provider invoice; unknown outcomes retain reserve.'}

    def save(self):
        tmp = self.path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.data, indent=2))
        tmp.replace(self.path)

    def reserve(self, provider, payload, episode):
        model = payload.get('model', MODELS[provider][0])
        inp, out = PRICING[model]
        max_output = payload.get('max_output_tokens', payload.get('max_tokens', 1600))
        # UTF-8 bytes bound ordinary text tokens; generous overhead covers tool framing.
        reserve = ((len(json.dumps(payload).encode()) + 10000) * inp + max_output * out) / 1e6
        with self.lock:
            total = sum(c.get('cost_usd', c['reserve_usd']) for c in self.data['calls'])
            if total + reserve > self.cap:
                raise RuntimeError('budget_cap_reached')
            i = len(self.data['calls'])
            self.data['calls'].append({'episode': episode, 'provider': provider, 'model': model, 'input_rate': inp, 'output_rate': out, 'reserve_usd': reserve, 'status': 'reserved'})
            self.save()
            return i

    def settle(self, i, usage):
        if not all(isinstance(usage.get(k), int) and usage[k] >= 0 for k in ('input_tokens', 'output_tokens')):
            with self.lock:
                self.data['calls'][i].update(status='unknown_usage', usage=usage)
                self.save()
            return self.data['calls'][i]['reserve_usd']
        provider = self.data['calls'][i]['provider']
        _, default_inp, default_out = MODELS[provider]
        inp = self.data['calls'][i].get('input_rate', default_inp)
        out = self.data['calls'][i].get('output_rate', default_out)
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        # No explicit prompt caching requested; uncached pricing is conservative.
        cost = (input_tokens * inp + output_tokens * out) / 1e6
        with self.lock:
            self.data['calls'][i].update(status='completed', usage=usage, cost_usd=cost)
            self.save()
        return cost


def request(provider, payload, budget, episode, timeout=90):
    idx = budget.reserve(provider, payload, episode)
    if provider == 'openai':
        url = 'https://api.openai.com/v1/responses'
        headers = {'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']}
    else:
        url = 'https://api.anthropic.com/v1/messages'
        headers = {'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01'}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        # Do not emit headers, request payloads, or credentials in errors.
        detail = ''
        try:
            error = json.loads(exc.read()).get('error', {})
            detail = str(error.get('message', ''))[:500]
            for name in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY'):
                value = os.environ.get(name)
                if value:
                    detail = detail.replace(value, '[REDACTED]')
        except Exception:
            pass
        raise RuntimeError('provider_http_' + str(exc.code) + (': ' + detail if detail else '')) from None
    except Exception as exc:
        raise RuntimeError('provider_transport_' + type(exc).__name__) from None
    cost = budget.settle(idx, result.get('usage', {}))
    return result, cost


def episode(task, provider, condition, metadata, budget, outdir):
    key = f"{provider}__{condition}__{metadata}__{task['task_id']}"
    destination = outdir / (key + '.json')
    if destination.exists():
        return {'episode': key, 'status': 'existing'}
    prompt = SYSTEM + (STRONG if condition == 'strong' else '')
    messages = [{'role': 'user', 'content': task['prompt']}]
    record = {'episode': key, 'task_id': task['task_id'], 'base_id': task['base_id'], 'query_type': task['query_type'], 'provider': provider, 'model': MODELS[provider][0], 'condition': condition, 'metadata': metadata, 'system_prompt': prompt, 'task_prompt': task['prompt'], 'trace': [], 'cost_usd': 0., 'status': 'max_steps', 'answer': None}
    visited = set()
    start = time.time()
    try:
        for step in range(12):
            if provider == 'openai':
                payload = {'model': MODELS[provider][0], 'instructions': prompt, 'input': messages, 'tools': [dict(type='function', strict=False, **s) for s in SCHEMAS], 'tool_choice': 'required', 'parallel_tool_calls': False, 'max_output_tokens': 1600, 'reasoning': {'effort': 'none'}, 'store': False}
            else:
                payload = {'model': MODELS[provider][0], 'system': prompt, 'messages': messages, 'tools': [{'name': s['name'], 'description': s['description'], 'input_schema': s['parameters']} for s in SCHEMAS], 'tool_choice': {'type': 'any', 'disable_parallel_tool_use': True}, 'max_tokens': 1600}
            result, cost = request(provider, payload, budget, key)
            record['cost_usd'] += cost
            record['trace'].append({'step': step, 'response': result})
            if provider == 'openai':
                messages.extend(result.get('output', []))
                calls = [c for c in result.get('output', []) if c['type'] == 'function_call']
            else:
                messages.append({'role': 'assistant', 'content': result['content']})
                calls = [c for c in result['content'] if c['type'] == 'tool_use']
            if not calls:
                record['status'] = 'no_tool_call'
                break
            tool_results = []
            for call in calls:
                args = json.loads(call['arguments']) if provider == 'openai' else call['input']
                if call['name'] == 'submit_answer':
                    record['answer'] = args
                    record['status'] = 'submitted'
                    break
                if call['name'] == 'list_records':
                    observation = benchmark.simulate_tool(task, 'list_records', args, metadata=metadata)
                    visited.update(r['id'] for r in observation.get('records', []))
                else:
                    observation = {'error': 'unknown_tool'}
                record['trace'].append({'tool': call['name'], 'arguments': args, 'observation': observation})
                if provider == 'openai':
                    messages.append({'type': 'function_call_output', 'call_id': call['call_id'], 'output': json.dumps(observation)})
                else:
                    tool_results.append({'type': 'tool_result', 'tool_use_id': call['id'], 'content': json.dumps(observation)})
            if record['status'] == 'submitted':
                break
            if provider == 'anthropic':
                messages.append({'role': 'user', 'content': tool_results})
    except Exception as exc:
        record['status'] = 'error'
        record['error'] = str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__
    record['elapsed_seconds'] = time.time() - start
    record['visited_ids'] = sorted(visited)
    record['coverage'] = len(visited) / len(task['records'])
    record['tool_calls'] = sum(1 for t in record['trace'] if t.get('tool') == 'list_records')
    record['score'] = benchmark.score_answer(task, record['answer'] or {})
    record['seen_matching_ids'] = sorted(visited.intersection(task['target_ids']))
    # Whether enough evidence was observed, independent of accidentally correct answers.
    witness = bool(record['seen_matching_ids'])
    record['sufficient_evidence'] = record['coverage'] == 1 or (task['query_type'] in ('one', 'none') and witness)
    destination.write_text(json.dumps(record, indent=2))
    return {k: record[k] for k in ('episode', 'status', 'score', 'cost_usd')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-base', type=int, default=12)
    parser.add_argument('--providers', nargs='+', default=list(MODELS))
    parser.add_argument('--conditions', nargs='+', default=['plain', 'strong'])
    parser.add_argument('--metadata', default='cursor', choices=['cursor', 'count'])
    parser.add_argument('--limit', type=int)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--cap', type=float, default=20.)
    parser.add_argument('--run', default='screen_v1')
    args = parser.parse_args()
    # One runner process at a time protects the shared budget ledger across launches.
    import fcntl
    lockfile = (ROOT / '.runner.lock').open('w')
    fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    tasks = benchmark.generate_tasks(n_base=args.n_base, seed=20260907)
    outdir = ROOT / 'runs' / args.run
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = [(t, p, c) for t in tasks for p in args.providers for c in args.conditions]
    random.Random(20260907).shuffle(jobs)
    if args.limit:
        jobs = jobs[:args.limit]
    manifest = {'created_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'args': vars(args), 'jobs': len(jobs), 'models': MODELS, 'tasks': tasks, 'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}, 'prices_sources': ['https://developers.openai.com/api/docs/models/gpt-5.4-mini', 'https://platform.claude.com/docs/en/about-claude/pricing']}
    manifest_path = outdir / 'manifest.json'
    if manifest_path.exists():
        raise RuntimeError('Choose a fresh run name; manifests are immutable.')
    manifest_path.write_text(json.dumps(manifest, indent=2))
    budget = Budget(args.cap)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(episode, t, p, c, args.metadata, budget, outdir) for t, p, c in jobs]
        for f in concurrent.futures.as_completed(futures):
            print(json.dumps(f.result()), flush=True)


if __name__ == '__main__':
    main()
