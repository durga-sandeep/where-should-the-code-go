"""Planned observable error decomposition, not inference about hidden reasoning.

No APIs. Replays the explicit future scenario from the model-emitted stock.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('temporal_independent_audit',ROOT/'audit_results.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
FUTURE=('stock_at_horizon','future_lost','first_future_stockout_time')
CATEGORIES=('stock_correct_future_correct','stock_correct_future_wrong',
            'stock_wrong_future_wrong_consistent','stock_wrong_future_wrong_inconsistent',
            'stock_wrong_future_correct')


def future_from_stock(task, stock):
    """Independent scenario simulation; no access to historical reports."""
    lost=0; first=-1
    for event in sorted(task['future_schedule'],key=lambda e:(e['event_time'],e['event_id'])):
        if not task['target_time']<event['event_time']<=task['horizon_time']:
            raise ValueError('Scenario event outside horizon')
        quantity=event['quantity']
        if event['kind']=='receipt':stock+=quantity
        elif event['kind']=='demand':
            fulfilled=min(stock,quantity); stock-=fulfilled; unmet=quantity-fulfilled; lost+=unmet
            if unmet and first==-1:first=event['event_time']
        else:raise ValueError('Unknown event kind')
    return dict(zip(FUTURE,(stock,lost,first)))


def classify(task, answer):
    truth,_=audit.replay(task)
    score=audit.expected_scores(truth,answer)
    if not score['valid']:return {'valid':False}
    gold_future={f:truth[f] for f in FUTURE}
    emitted_future={f:answer[f] for f in FUTURE}
    from_emitted=future_from_stock(task,answer['stock_at_target'])
    stock_correct=answer['stock_at_target']==truth['stock_at_target']
    future_correct=emitted_future==gold_future
    consistent=emitted_future==from_emitted
    if stock_correct:
        category='stock_correct_future_correct' if future_correct else 'stock_correct_future_wrong'
    elif future_correct:category='stock_wrong_future_correct'
    else:category='stock_wrong_future_wrong_consistent' if consistent else 'stock_wrong_future_wrong_inconsistent'
    return {'valid':True,'category':category,'stock_correct':stock_correct,
            'future_correct':future_correct,'consistent_with_emitted_stock':consistent,
            'historical_lost_correct':answer['historical_lost']==truth['historical_lost'],
            'gold_stockout':truth['first_future_stockout_time']>=0,
            'predicted_stockout':answer['first_future_stockout_time']>=0,
            'truth':truth,'future_from_emitted_stock':from_emitted}


def summarize(items):
    counts=Counter({k:0 for k in CATEGORIES}); valid=0; history_wrong=0; history_wrong_stockright=0
    fp=fn=positive=negative=consistent=mask_consistent=0
    examples=[]
    for item in items:
        d=item['diagnostic']
        if not d['valid']:continue
        valid+=1;counts[d['category']]+=1
        history_wrong+=not d['historical_lost_correct']
        history_wrong_stockright+=not d['historical_lost_correct'] and d['stock_correct']
        positive+=d['gold_stockout'];negative+=not d['gold_stockout']
        fp+=not d['gold_stockout'] and d['predicted_stockout']
        fn+=d['gold_stockout'] and not d['predicted_stockout']
        consistent+=d['consistent_with_emitted_stock']
        mask_consistent+=d['category']=='stock_wrong_future_correct' and d['consistent_with_emitted_stock']
        if d['category']=='stock_wrong_future_wrong_consistent' and len(examples)<3:
            examples.append({k:item[k] for k in ('source','base_id','rep','answer')} |
                            {k:d[k] for k in ('truth','future_from_emitted_stock')})
    rate=lambda n,d:{'numerator':n,'denominator':d,'rate':n/d if d else None}
    return {'n':len(items),'valid':valid,'invalid':len(items)-valid,'categories':dict(counts),
            'historical_lost_wrong':history_wrong,'historical_lost_wrong_with_correct_stock':history_wrong_stockright,
            'future_consistent_with_emitted_stock':consistent,
            'stock_wrong_future_correct_and_consistent':mask_consistent,
            'false_future_stockout':rate(fp,negative),'missed_future_stockout':rate(fn,positive),
            'consistent_wrong_future_examples':examples}


def analyze_run(path):
    manifest_path=path/'manifest.json';manifest=json.loads(manifest_path.read_text())
    tasks={t['base_id']:t for t in manifest['tasks']};args=manifest['args']
    expected={(b,c,a,r) for b in tasks for c in args['configs'] for a in args['arms'] for r in range(args['reps'])}
    seen=set();groups=defaultdict(list);hashes={}
    for p in sorted(path.glob('*__*.json')):
        row=json.loads(p.read_text());key=(row['base_id'],row['configuration'],row['arm'],row['rep'])
        if key in seen or key not in expected:raise ValueError(f'Duplicate or unexpected episode {p.name}')
        seen.add(key)
        cfg=manifest['configs'][row['configuration']]
        answer,status=audit.parse_answer(row,cfg['provider'])
        if answer!=row.get('answer') or status!=row.get('status'):
            raise ValueError(f'Raw response and stored answer/status differ: {p.name}')
        item={'base_id':row['base_id'],'rep':row['rep'],'source':f"{path.name}/{p.name}",
              'answer':answer,'diagnostic':classify(tasks[row['base_id']],answer)}
        groups[row['configuration'],row['arm']].append(item)
        hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    if seen!=expected:raise ValueError(f'Incomplete run {path.name}: {len(seen)}/{len(expected)}')
    return {'run':path.name,'episodes':len(seen),'complete':True,
            'cells':[{'configuration':k[0],'arm':k[1],**summarize(v)} for k,v in sorted(groups.items())],
            'provenance':{'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                          'episode_files_sha256':hashes}}


def render(result):
    lines=['# Observable temporal error decomposition','',
           'Prespecified analysis amendment before heldout model outcomes. This partitions reported answers; it does not identify hidden reasoning or causal error paths. Future outputs are replayed from the model-emitted stock, independently of historical-lost correctness.','']
    for run in result['runs']:
        lines += [f"## {run['run']}",'',
                  '| Configuration | Arm | Valid / total | Stock right, future right | Stock right, future wrong | Both wrong, consistent | Both wrong, inconsistent | Stock wrong, future right |',
                  '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
        for c in run['cells']:
            values=' | '.join(str(c['categories'][k]) for k in CATEGORIES)
            lines.append(f"| {c['configuration']} | {c['arm']} | {c['valid']}/{c['n']} | {values} |")
        lines += ['', 'Categories partition valid outputs. Invalids remain outside the partition. Historical-loss errors, stockout-detection denominators and up to three consistently wrong examples per cell are in `decomposition.json`.','']
    lines += ['“Consistent” means the future triple exactly equals deterministic replay from the emitted starting stock. It does not prove the model used that stock internally. “Stock wrong, future right” is an observable masking/recovery pattern, not evidence of intentional recovery. Stockout-detection rates are conditional on valid contracts and do not measure timing accuracy.','']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,action='append',required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    result={'analysis':'planned_observable_propagation_decomposition',
            'notes':['Descriptive episode counts; repeated tasks are not independent statistical samples.',
                     'Partition uses correct starting stock, not historical joint, because historical loss does not drive the future.',
                     'Raw responses reparsed independently; no stored scorer used.',
                     'Relative example paths are relative to the parent runs directory.'],
            'runs':[analyze_run(path) for path in args.run]}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'decomposition.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    (args.output_dir/'decomposition.md').write_text(render(result))
    print(json.dumps({'complete':True,'runs':len(result['runs']),'episodes':sum(r['episodes'] for r in result['runs'])}))

if __name__=='__main__':main()
