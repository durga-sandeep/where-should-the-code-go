"""Inventory simulation driven by released, normalized observed retail sales.

This adapter creates synthetic inventory/reporting scenarios, not real inventory
ground truth or latent uncensored demand. Uses first 72 hours as historical
two-hour bins and next 24 hours as a fixed future scenario; remaining 72 hours
of the source seven-day window are unused. Scale uses history only: for bin sum
b and maximum historical bin M, quantity=ROUND_HALF_UP(10*b/M). If M=0 use M=1.
No cap; future values never choose M. Source stockout labels are not imputed.

Synthetic receipt calibration uses only quantized historical demand S: history
receipt budget ROUND_HALF_UP(3*S/4), future budget ROUND_HALF_UP(S/6) (half the
12-bin demand implied by the 36-bin past mean). Allocate each budget over 36/6
slots using seeded integer weights 1..8 and largest remainders, ties by slot.
This is a deliberately under-supplied synthetic scenario, not a learned policy.

Source windows remain store-disjoint across dev/heldout. Fixed store hash ranking
assigns first 48 to heldout, remaining 16 to dev, independently of run seed and
outcomes. Receipts, reports, corrections, and initial inventory are synthetic.
"""
import copy
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import random

SOURCE_SHA256 = '3131d97d614b0efcef07f8b1b840d3a9238c30ab1deacbe399328d1f3a8b23f7'
SOURCE_REVISION = '08c1fab7f9257bc73679d415d65d644165d351d4'
SOURCE_URL = 'https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K'
DATA = Path(__file__).parent/'data'/'freshretail_profiles.jsonl'
SPLIT_SEED = 'temporal-state-profile-split-v1'
HELDOUT_SEED = 2026090802
DEVELOPMENT_SEED = 2026090801


def load_profiles(path=DATA):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('external profile hash mismatch')
    stores = {}
    for line in raw.decode().splitlines():
        row = json.loads(line)
        stores.setdefault(row['store_id'], []).append(row)
    if len(stores) != 64:
        raise ValueError('expected 64 distinct source stores')
    for rows in stores.values():
        rows.sort(key=lambda r: r['dt'])
        if len(rows) != 7 or len({r['product_id'] for r in rows}) != 1:
            raise ValueError('expected one seven-day product window per store')
        start = date.fromisoformat(rows[0]['dt'])
        if [r['dt'] for r in rows] != [(start+timedelta(days=i)).isoformat() for i in range(7)]:
            raise ValueError('noncontiguous window')
        for row in rows:
            if len(row['hours_sale']) != 24 or any(Decimal(str(v)) < 0 for v in row['hours_sale']):
                raise ValueError('invalid hourly sales')
    return stores


def quantities(rows):
    hourly = [Decimal(str(value)) for row in rows for value in row['hours_sale']]
    historical = [sum(hourly[i:i+2]) for i in range(0, 72, 2)]
    future = [sum(hourly[i:i+2]) for i in range(72, 96, 2)]
    denominator = max(historical) or Decimal(1)
    convert = lambda b: int((Decimal(10)*b/denominator).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return [convert(b) for b in historical], [convert(b) for b in future], str(denominator)


def allocate_receipts(budget, slots, rng):
    weights=[rng.randint(1,8) for _ in range(slots)]
    total=sum(weights)
    result=[budget*w//total for w in weights]
    remaining=budget-sum(result)
    order=sorted(range(slots),key=lambda i:(-(budget*weights[i]%total),i))
    for i in order[:remaining]:result[i]+=1
    return result


def generate_tasks(n_base=None, seed=HELDOUT_SEED, split='heldout'):
    if split == 'development':
        split = 'dev'
    if split not in ('dev', 'heldout'):
        raise ValueError('invalid split')
    profiles = load_profiles()
    ranked = sorted(profiles, key=lambda store: hashlib.sha256(f'{SPLIT_SEED}:{store}'.encode()).hexdigest())
    pool = ranked[:48] if split == 'heldout' else ranked[48:]
    if n_base is None:
        n_base = len(pool)
    if type(n_base) is not int or not 0 <= n_base <= len(pool):
        raise ValueError('requested count exceeds distinct-store split')
    tasks = []
    for store in pool[:n_base]:
        rows = profiles[store]
        base = f'freshretail-{split}-store{store}-product{rows[0]["product_id"]}-s{seed}'
        rng = random.Random(base)
        history_q, future_q, denominator = quantities(rows)
        past_total=sum(history_q)
        historical_budget=int((Decimal(3)*past_total/4).quantize(Decimal(1),rounding=ROUND_HALF_UP))
        future_budget=int((Decimal(past_total)/6).quantize(Decimal(1),rounding=ROUND_HALF_UP))
        historical_receipts=allocate_receipts(historical_budget,36,rng)
        future_receipts=allocate_receipts(future_budget,6,rng)
        clean = []
        for i, demand in enumerate(history_q):
            for offset, kind, quantity in ((0,'receipt',historical_receipts[i]),(1,'demand',demand)):
                logical = 2*i+offset
                eid = 'E-'+hashlib.sha256(f'{base}:{logical}'.encode()).hexdigest()[:12]
                clean.append(dict(event_id=eid,event_time=logical+1,kind=kind,quantity=quantity))
        delayed = set(rng.sample(range(72),18))
        corrected = set(rng.sample(range(72),24))
        invisible_correction = set(rng.sample(sorted(corrected),12))
        reports = []
        for i, event in enumerate(clean):
            arrival = rng.randint(101,115) if i in delayed else event['event_time']+rng.randint(0,12)
            original = dict(event,revision=1,received_time=arrival)
            if i in corrected:
                # A mistaken first report, subsequently corrected to the profile-
                # driven/synthetic clean quantity. Cutoff semantics may keep v1.
                original['quantity'] = rng.choice([x for x in range(13) if x != event['quantity']])
                revision_arrival = (rng.randint(max(101,arrival),130) if i in invisible_correction or arrival>100
                                    else rng.randint(max(arrival,80),100))
                reports.append(dict(event,revision=2,received_time=revision_arrival))
            reports.append(original)
        reports.sort(key=lambda r:(r['received_time'],r['event_id'],r['revision']))
        future = []
        for block in range(6):
            time = 101+3*block
            future.append(dict(event_id=f'F-{3*block:02d}',event_time=time,kind='receipt',quantity=future_receipts[block]))
            for offset in (0,1):
                future.append(dict(event_id=f'F-{3*block+offset+1:02d}',event_time=time+offset+1,
                                   kind='demand',quantity=future_q[2*block+offset]))
        tasks.append(dict(base_id=base,seed=seed,split=split,n_events=72,late_arrival='present',corrections='present',
                          initial_stock=12,target_time=100,knowledge_cutoff=100,horizon_time=130,
                          reports=reports,future_schedule=future,dataset='freshretail_profiles',
                          generator_version='freshretail-profile-scenario-v1',source_revision=SOURCE_REVISION,
                          source_url=SOURCE_URL,source_sha256=SOURCE_SHA256,source_store_id=store,
                          source_product_id=rows[0]['product_id'],source_city_id=rows[0]['city_id'],
                          source_dates=[r['dt'] for r in rows],past_bin_normalizer=denominator,
                          past_quantized_demand_total=past_total,historical_receipt_budget=historical_budget,
                          future_receipt_budget=future_budget,
                          source_hours_used=96,source_hours_unused=72,
                          interpretation='synthetic inventory scenario driven by observed normalized sales; not latent demand'))
    return tasks
