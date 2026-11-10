"""Validate and compare complete paired temporal controls. No API calls."""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def local_module(name):
    spec = importlib.util.spec_from_file_location('temporal_control_' + name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

analysis = local_module('analyze')
benchmark = local_module('benchmark')


def load_run(path):
    manifest = json.loads((path / 'manifest.json').read_text())
    rows = []
    for p in sorted(path.glob('*.json')):
        if p.name in ('manifest.json', 'analysis.json', 'comparison.json'):
            continue
        item = json.loads(p.read_text())
        if isinstance(item, dict) and all(k in item for k in ('base_id','configuration','arm','rep')):
            rows.append(item)
    status = analysis.analyze(manifest, rows, draws=1)
    if not status['complete']:
        raise ValueError(f'Incomplete or unexpected grid in {path}')
    return manifest, rows


def expected_input(task, arm):
    public = benchmark.public_task(task)
    if arm == 'raw':
        return {'input_representation': arm, **public}
    public.pop('reports')
    if arm == 'canonical':
        return {'input_representation': arm, **public, 'eligible_events': benchmark.canonical_events(task)}
    if arm == 'snapshot':
        truth = benchmark.solve(task)
        return {'input_representation': arm, **public,
                'historical_state': {k: truth[k] for k in benchmark.FIELDS[:2]}}
    raise ValueError('Unknown arm')


def request_settings(row, task):
    payload = copy.deepcopy(row['request'])
    field = 'input' if 'input' in payload else 'messages'
    messages = payload.pop(field)
    if len(messages) != 1 or messages[0]['role'] != 'user':
        raise ValueError('Unexpected request message layout')
    body = json.loads(messages[0]['content'])
    if body != expected_input(task, row['arm']):
        raise ValueError(f"Request does not match intended task/arm: {analysis.coordinate(row)}")
    return payload


def verify_tasks(original, control, kind):
    if set(control) - set(original):
        raise ValueError('Control includes unknown bases')
    for base, ct in control.items():
        ot = copy.deepcopy(original[base]); ct = copy.deepcopy(ct)
        if kind == 'hindsight':
            if ot['knowledge_cutoff'] != 100 or ct['knowledge_cutoff'] != 130:
                raise ValueError('Expected K100 -> K130 intervention')
            ot.pop('knowledge_cutoff'); ct.pop('knowledge_cutoff')
        elif kind == 'display':
            ot['reports'] = sorted(ot['reports'], key=lambda x: json.dumps(x, sort_keys=True))
            ct['reports'] = sorted(ct['reports'], key=lambda x: json.dumps(x, sort_keys=True))
        else:
            raise ValueError('Unknown control')
        if ot != ct:
            raise ValueError(f'Unexpected task change for {kind} {base}')


def mean_interval(values_by_base, draws, seed):
    means = [sum(v)/len(v) for _,v in sorted(values_by_base.items())]
    return {'rate': sum(means)/len(means) if means else None,
            'ci95': analysis.bootstrap(means, draws, seed),
            'bases': len(means), 'episodes': sum(map(len, values_by_base.values()))}



def within_view_repetitions(rows, draws=10000, seed=20260907):
    """Post-hoc repeat baseline; one r0/r1 pair per base, not order attribution."""
    by_base={}
    for row in rows:
        by_base.setdefault(str(row['base_id']),{})[int(row['rep'])]=row
    diagnostics={k:{} for k in ('answer_invariant','both_correct','both_valid')}
    excluded=[]
    for base,reps in sorted(by_base.items()):
        if 0 not in reps or 1 not in reps:
            excluded.append(base);continue
        left,right=reps[0],reps[1]
        lm,rm=analysis.metrics(left),analysis.metrics(right)
        valid=lm['valid'] and rm['valid']
        diagnostics['both_valid'][base]=[int(valid)]
        diagnostics['answer_invariant'][base]=[int(valid and left['answer']==right['answer'])]
        diagnostics['both_correct'][base]=[int(lm['joint_exact'] and rm['joint_exact'])]
    return {'repetitions':[0,1],'paired_bases':len(diagnostics['both_valid']),
            'excluded_bases_missing_r0_or_r1':excluded,
            'diagnostics':{k:mean_interval(v,draws,seed) for k,v in diagnostics.items()},
            'interpretation':'Post-hoc descriptive diagnostic of existing repeated requests; not a prespecified endpoint or an isolated causal display-order effect.'}


def compare(original_manifest, original_rows, control_manifest, control_rows,
            kind, draws=10000, seed=20260907):
    for manifest, rows in ((original_manifest, original_rows),(control_manifest,control_rows)):
        if not analysis.analyze(manifest, rows, draws=1)['complete']:
            raise ValueError('Controls require complete expected grids')
    original_tasks = {analysis.task_id(t):t for t in original_manifest['tasks']}
    control_tasks = {analysis.task_id(t):t for t in control_manifest['tasks']}
    expected_bases = list(original_tasks)[:len(control_tasks)]
    if list(control_tasks) != expected_bases:
        raise ValueError('Control must use the prespecified leading source bases in source order')
    verify_tasks(original_tasks, control_tasks, kind)
    orig = {analysis.coordinate(r):r for r in original_rows}
    groups = {}
    truths = {b:(benchmark.solve(original_tasks[b]),benchmark.solve(t)) for b,t in control_tasks.items()}
    for row in control_rows:
        coordinate = analysis.coordinate(row)
        if coordinate not in orig:
            raise ValueError(f'Missing original paired episode {coordinate}')
        before = orig[coordinate]; base = coordinate[0]
        if kind == 'display' and row['arm'] != 'raw':
            raise ValueError('Display control is raw-only')
        if request_settings(before, original_tasks[base]) != request_settings(row, control_tasks[base]):
            raise ValueError(f'Provider/model/instruction/schema mismatch: {coordinate}')
        groups.setdefault((row['configuration'],row['arm']),[]).append((before,row))
    cells = []
    for (cfg,arm), pairs in sorted(groups.items()):
        diagnostics = {k:{} for k in ('both_correct','answer_invariant','both_valid',
            'changed_when_required','both_correct_when_required','changed_when_invariant')}
        n_changed_truth = 0
        for before,after in pairs:
            base = str(before['base_id'])
            m0,m1=analysis.metrics(before),analysis.metrics(after)
            valid=m0['valid'] and m1['valid']
            changed=valid and before['answer'] != after['answer']
            changed_truth=truths[base][0] != truths[base][1]
            n_changed_truth += changed_truth
            outcomes={'both_correct': m0['joint_exact'] and m1['joint_exact'],
                      'both_valid': valid,'answer_invariant':valid and not changed}
            if changed_truth:
                outcomes['changed_when_required']=changed
                outcomes['both_correct_when_required']=m0['joint_exact'] and m1['joint_exact']
            else:
                outcomes['changed_when_invariant']=changed
            for key,value in outcomes.items():
                diagnostics[key].setdefault(base,[]).append(int(value))
        if kind == 'display' and n_changed_truth:
            raise ValueError('Harmless display permutation changed oracle')
        cells.append({'configuration':cfg,'arm':arm,'paired_episodes':len(pairs),
                      'truth_changed_episodes':n_changed_truth,
                      'original':analysis.summarize([p[0] for p in pairs]),
                      'control':analysis.summarize([p[1] for p in pairs]),
                      'paired_differences':[analysis.paired([p[0] for p in pairs],[p[1] for p in pairs],m,draws,seed)
                          for m in ('joint_exact','historical_joint','future_joint')],
                      'diagnostics':{k:mean_interval(v,draws,seed) for k,v in diagnostics.items()},
                      **({'within_view_repetition_baselines':{
                          'original':within_view_repetitions([p[0] for p in pairs],draws,seed),
                          'display':within_view_repetitions([p[1] for p in pairs],draws,seed)}} if kind=='display' else {})})
    return {'kind':kind,'complete':True,'shared_bases':len(control_tasks),
            'truth_changed_bases':sum(a!=b for a,b in truths.values()),'bootstrap_draws':draws,
            'seed':seed,'cells':cells,'notes':[
                'Request bodies verified against task/arm; all remaining provider settings match within pairs.',
                'Task equality checked except intended cutoff or harmless report permutation.',
                'Repetitions and views remain clustered within latent base. Intervals are descriptive and unadjusted.',
                'Answer-change diagnostics require both valid; invalid pairs count as failures, with both-valid rate reported.',
                'Change when required does not establish correct sensitivity; both-correct-when-required is also reported.',
                'Display cross-view disagreement includes ordinary request stochasticity; within-view r0/r1 baselines are post-hoc and do not isolate causal order effects.',
                'Historical K130 view is retrospective reconstruction followed by a hypothetical scenario, not a T100 forecast.']}


def render(result):
    lines=['# Paired temporal controls','']
    for study in result['controls']:
        lines += [f"## {study['kind']}",'',f"{study['shared_bases']} shared bases; {study['truth_changed_bases']} have changed oracle answers.",'',
                  '| Configuration | Arm | Paired episodes | Original joint | Control joint | Both correct | Valid answer invariant |',
                  '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
        for c in study['cells']:
            percent=lambda x:'NA' if x is None else f'{100*x:.1f}%'
            lines.append(f"| {c['configuration']} | {c['arm']} | {c['paired_episodes']} | {c['original']['successes']['joint_exact']} | {c['control']['successes']['joint_exact']} | {percent(c['diagnostics']['both_correct']['rate'])} | {percent(c['diagnostics']['answer_invariant']['rate'])} |")
        if study['kind']=='display':
            lines += ['', '### Within-view repetition baselines (post-hoc)', '',
                      'Existing r0/r1 requests on the same control bases; one pair per base. These are descriptive stochasticity checks, not prespecified endpoints or isolated causal effects of display order.', '',
                      '| Configuration | View | r0/r1 base pairs | Valid identical answers | Both correct |',
                      '| --- | --- | ---: | ---: | ---: |']
            for cell in study['cells']:
                for view,baseline in cell['within_view_repetition_baselines'].items():
                    ds=baseline['diagnostics']
                    lines.append(f"| {cell['configuration']} | {view} | {baseline['paired_bases']} | {percent(ds['answer_invariant']['rate'])} | {percent(ds['both_correct']['rate'])} |")
        lines += ['', 'Exact joint columns are counts. Diagnostic rates average repetitions within bases. Full conditional denominators, paired differences and bootstrap intervals are in `comparison.json`.', '', *['- '+n for n in study['notes']], '']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--original',type=Path,required=True)
    p.add_argument('--hindsight',type=Path)
    p.add_argument('--display',type=Path)
    p.add_argument('--output-dir',type=Path,default=ROOT)
    p.add_argument('--bootstrap',type=int,default=10000)
    p.add_argument('--seed',type=int,default=20260907)
    args=p.parse_args()
    if not args.hindsight and not args.display:p.error('At least one control required')
    original=load_run(args.original)
    result={'controls':[]}
    for kind in ('hindsight','display'):
        path=getattr(args,kind)
        if path:
            result['controls'].append(compare(*original,*load_run(path),kind,args.bootstrap,args.seed))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'comparison.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    (args.output_dir/'comparison.md').write_text(render(result))
    print(json.dumps({'controls':len(result['controls']),'complete':True}))

if __name__=='__main__':main()
