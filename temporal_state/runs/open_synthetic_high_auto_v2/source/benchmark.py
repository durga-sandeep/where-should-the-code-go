"""Deterministic event-time inventory benchmark; no network calls.

Public schema (public_task):
  initial_stock: nonnegative int
  target_time: int T; knowledge_cutoff: int K; horizon_time: int H
  reports: list of {event_id:str, revision:int>=1, event_time:int,
                    received_time:int, kind:'receipt'|'demand', quantity:int>=0}
  future_schedule: list of {event_id:str,event_time:int,kind,quantity}, T<time<=H

Reports are versions of logical historical events, not separate transactions.
Select received_time<=K, then highest revision for EACH event_id, then restrict
event_time<=T; sort by (event_time,event_id). A revised event can change time,
kind, or quantity. Received time is when a report was learned. Missing events
are not inferred. Future_schedule is an explicit hypothetical known schedule,
not a stochastic forecast and not subject to historical knowledge filtering.

Receipt adds quantity. Demand removes min(stock,quantity); unmet quantity is
lost immediately, never backordered. first_future_stockout_time is the earliest
scheduled demand time with positive loss through H, or -1 if none.
Zero inventory alone is not a stockout. All counts refer to the knowledge-cutoff
reconstruction, not an omniscient history. No input record is mutated.
"""
import copy
import hashlib
import itertools
import random

DEVELOPMENT_SEED = 2026090801
HELDOUT_SEED = 2026090802
FIELDS = ('stock_at_target', 'historical_lost', 'stock_at_horizon', 'future_lost', 'first_future_stockout_time')
PUBLIC_FIELDS = ('initial_stock', 'target_time', 'knowledge_cutoff', 'horizon_time', 'reports', 'future_schedule')


def public_task(task):
    return {key: copy.deepcopy(task[key]) for key in PUBLIC_FIELDS}


def canonical_events(task, apply_cutoff=True):
    latest = {}
    versions = set()
    for report in task['reports']:
        identity = (report['event_id'], report['revision'])
        if identity in versions:
            raise ValueError('duplicate event/revision')
        versions.add(identity)
        if apply_cutoff and report['received_time'] > task['knowledge_cutoff']:
            continue
        previous = latest.get(report['event_id'])
        if previous is None or report['revision'] > previous['revision']:
            latest[report['event_id']] = report
    # Time filtering must follow version resolution: a latest revision beyond T
    # excludes the event; its obsolete earlier-time revision must not reappear.
    return [copy.deepcopy(row) for row in sorted(latest.values(), key=lambda r: (r['event_time'], r['event_id']))
            if row['event_time'] <= task['target_time']]


def _step(stock, event):
    quantity = event['quantity']
    if event['kind'] == 'receipt':
        return stock + quantity, 0
    if event['kind'] == 'demand':
        return max(0, stock-quantity), max(0, quantity-stock)
    raise ValueError('unknown inventory event kind')


def replay_state(task, events=None):
    events = canonical_events(task) if events is None else events
    stock = task['initial_stock']
    historical_lost = 0
    first_stockout = -1
    for event in events:
        stock, lost = _step(stock, event)
        historical_lost += lost
    at_target = stock
    future_lost = 0
    for event in sorted(task['future_schedule'], key=lambda r: (r['event_time'], r['event_id'])):
        if not task['target_time'] < event['event_time'] <= task['horizon_time']:
            raise ValueError('future event outside scenario horizon')
        stock, lost = _step(stock, event)
        future_lost += lost
        if lost and first_stockout == -1:
            first_stockout = event['event_time']
    return dict(stock_at_target=at_target, historical_lost=historical_lost,
                stock_at_horizon=stock, future_lost=future_lost, first_future_stockout_time=first_stockout)


def solve(task):
    return replay_state(task)


def naive_arrival(task):
    """Diagnostic: latest visible versions, replayed in receive-time order."""
    events = sorted(canonical_events(task), key=lambda r: (r['received_time'], r['event_id']))
    return replay_state(task, events)


def latest_no_cutoff(task):
    """Diagnostic: omniscient latest versions, including unavailable reports."""
    return replay_state(task, canonical_events(task, apply_cutoff=False))


def generate_tasks(n_base=96, seed=HELDOUT_SEED, split='heldout'):
    if type(n_base) is not int or n_base < 0:
        raise ValueError('n_base must be nonnegative integer')
    if split == 'development':
        split = 'dev'
    if split not in ('dev', 'heldout'):
        raise ValueError('invalid split')
    conditions = list(itertools.product((12, 36, 72), ('none', 'present'), ('none', 'present'), ('balanced', 'demand_heavy')))
    random.Random(f'{seed}:{split}:conditions').shuffle(conditions)
    tasks = []
    for index in range(n_base):
        n, late, corrections, pressure = conditions[index % len(conditions)]
        base = f'temporal-{split}-s{seed}-b{index:04d}'
        rng = random.Random(base)
        times = sorted(rng.sample(range(1, 100), n))
        kinds = ['receipt']*(n//2) + ['demand']*(n-n//2)
        rng.shuffle(kinds)
        delayed = set(rng.sample(range(n), max(1, n//4))) if late == 'present' else set()
        revised = set(rng.sample(range(n), max(2, n//3))) if corrections == 'present' else set()
        # Half of revised events have unavailable future corrections regardless
        # of first-report delay condition. No selection by observed solver errors.
        unavailable_revisions = set(rng.sample(sorted(revised), len(revised)//2))
        reports = []
        for position, (time, kind) in enumerate(zip(times, kinds)):
            eid = 'E-' + hashlib.sha256(f'{base}:{position}'.encode()).hexdigest()[:12]
            received = (time if late == 'none' else
                        rng.randint(101, 115) if position in delayed else min(100, time+rng.randint(0, 12)))
            original = dict(event_id=eid, revision=1, event_time=time, received_time=received,
                            kind=kind, quantity=rng.randint(1, 12))
            reports.append(original)
            if position in revised:
                corrected = dict(original, revision=2)
                change = rng.choice(('quantity', 'kind', 'event_time'))
                if change == 'quantity':
                    corrected['quantity'] = rng.choice([q for q in range(1, 13) if q != original['quantity']])
                elif change == 'kind':
                    corrected['kind'] = 'demand' if kind == 'receipt' else 'receipt'
                else:
                    # Backdated corrections can change replay ordering while
                    # remaining physically observable after their event time.
                    corrected['event_time'] = rng.choice([t for t in range(max(1, time-6), min(99, time+6)+1) if t != time])
                earliest = max(received, corrected['event_time'])
                if position in unavailable_revisions or earliest > 100:
                    corrected['received_time'] = rng.randint(max(101, earliest), 130)
                else:
                    corrected['received_time'] = rng.randint(earliest, 100)
                reports.append(corrected)
        reports.sort(key=lambda r: (r['received_time'], r['event_id'], r['revision']))
        future_times = sorted(rng.sample(range(101, 131), 12))
        future_kinds = (['receipt']*6 + ['demand']*6 if pressure == 'balanced' else ['receipt']*3 + ['demand']*9)
        rng.shuffle(future_kinds)
        future = [dict(event_id=f'F-{j:02d}', event_time=time, kind=kind, quantity=(rng.randint(8, 16) if kind == 'demand' else rng.randint(1, 8)) if pressure == 'demand_heavy' else rng.randint(1, 12))
                  for j, (time, kind) in enumerate(zip(future_times, future_kinds))]
        tasks.append(dict(base_id=base, seed=seed, split=split, n_events=n, late_arrival=late,
                          corrections=corrections, future_pressure=pressure, initial_stock=rng.randint(8, 25),
                          target_time=100, knowledge_cutoff=100, horizon_time=130,
                          reports=reports, future_schedule=future, generator_version='temporal-state-v2'))
    return tasks


def score(task, answer):
    truth = solve(task)
    valid = type(answer) is dict and set(answer) == set(FIELDS)
    if valid:
        valid = all(type(answer[field]) is int and answer[field] >= (-1 if field == 'first_future_stockout_time' else 0)
                    for field in FIELDS)
    per_metric = {field: bool(valid and answer[field] == truth[field]) for field in FIELDS}
    return dict(valid=valid, exact=all(per_metric.values()), joint_exact=all(per_metric.values()),
                per_metric=per_metric, **{field+'_exact': value for field, value in per_metric.items()})
