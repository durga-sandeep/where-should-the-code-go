"""Independent temporal output/request audit. Standard library; no model calls.

Does not import the experiment generator, scorer, runner, or analyzer.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path

FIELDS=('stock_at_target','historical_lost','stock_at_horizon','future_lost','first_future_stockout_time')
PUBLIC=('initial_stock','target_time','knowledge_cutoff','horizon_time','reports','future_schedule')


def replay(task):
    chosen=[]
    for eid in sorted({r['event_id'] for r in task['reports']}):
        versions=[r for r in task['reports'] if r['event_id']==eid and r['received_time']<=task['knowledge_cutoff']]
        if versions:
            latest=max(versions,key=lambda r:r['revision'])
            if latest['event_time']<=task['target_time']:chosen.append(latest)
    chosen.sort(key=lambda r:(r['event_time'],r['event_id']))
    stock=task['initial_stock']; historical=0; future_loss=0; first=-1
    for r in chosen:
        if r['kind']=='receipt':stock+=r['quantity']
        elif r['kind']=='demand':
            fulfilled=min(stock,r['quantity']);stock-=fulfilled;historical+=r['quantity']-fulfilled
        else:raise ValueError('Unknown event kind')
    at_target=stock
    for r in sorted(task['future_schedule'],key=lambda r:(r['event_time'],r['event_id'])):
        if not task['target_time']<r['event_time']<=task['horizon_time']:raise ValueError('Invalid future horizon')
        if r['kind']=='receipt':stock+=r['quantity']
        elif r['kind']=='demand':
            fulfilled=min(stock,r['quantity']);stock-=fulfilled;loss=r['quantity']-fulfilled
            future_loss+=loss
            if loss and first==-1:first=r['event_time']
        else:raise ValueError('Unknown event kind')
    return dict(zip(FIELDS,(at_target,historical,stock,future_loss,first))),chosen


def parse_answer(row,provider):
    if 'response' not in row:return None,'error'
    response=row['response']
    try:
        if provider=='openai':
            calls=[x for x in response.get('output',[]) if x.get('type')=='function_call' and x.get('name')=='submit_answer']
            try:answer=json.loads(calls[0]['arguments']) if len(calls)==1 else None
            except ValueError:answer=None
        elif provider=='openrouter':
            choices=response.get('choices') or []
            calls=[x for x in ((choices[0].get('message') or {}).get('tool_calls') or []) if len(choices)==1
                   and x.get('type','function')=='function' and (x.get('function') or {}).get('name')=='submit_answer']
            if len(calls)==1:
                arguments=calls[0]['function'].get('arguments')
                if isinstance(arguments,str):
                    try:answer=json.loads(arguments)
                    except ValueError:answer=None  # malformed arguments are a missing answer (Amendment 4 transport note 11)
                else:answer=arguments
            else:answer=None
        else:
            calls=[x for x in response.get('content',[]) if x.get('type')=='tool_use' and x.get('name')=='submit_answer']
            answer=calls[0]['input'] if len(calls)==1 else None
        return answer,'submitted' if answer is not None else 'missing_answer'
    except (ValueError,TypeError,KeyError):return None,'error'


def expected_scores(truth,answer):
    valid=(type(answer) is dict and set(answer)==set(FIELDS) and
           all(type(answer[f]) is int and answer[f]>=(-1 if f==FIELDS[-1] else 0) for f in FIELDS))
    per={f:bool(valid and answer[f]==truth[f]) for f in FIELDS}
    return {'valid':valid,'exact':all(per.values()),'joint_exact':all(per.values()),
            'per_metric':per,**{f+'_exact':v for f,v in per.items()}}


def source_contract(source):
    tree=ast.parse(source)
    constants={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in ('CONFIGS','INSTRUCTIONS'):
                    constants[target.id]=ast.literal_eval(node.value)
    options={k:[] for k in ('tool_choice','max_tokens','max_output_tokens')}
    for node in ast.walk(tree):
        if isinstance(node,ast.keyword) and node.arg in options:
            try:options[node.arg].append(ast.literal_eval(node.value))
            except (ValueError,TypeError):pass
    return constants,options


def audit_run(path):
    m=json.loads((path/'manifest.json').read_text());issues=[]
    def check(ok,category,detail):
        if not ok:issues.append({'category':category,'detail':detail})
    for name,digest in m['source_sha256'].items():
        p=path/'source'/name
        check(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,'source_hash',name)
    constants,options=source_contract((path/'source'/'run.py').read_text())
    check(constants.get('CONFIGS')==m['configs'],'manifest_configs','Archived CONFIGS differs')
    check(constants.get('INSTRUCTIONS')==m['instructions'],'manifest_instructions','Archived instructions differs')
    tasks={t['base_id']:t for t in m['tasks']}
    check(len(tasks)==len(m['tasks']),'duplicate_tasks','Manifest base IDs')
    args=m['args'];expected={(b,c,a,r) for b in tasks for c in args['configs'] for a in args['arms'] for r in range(args['reps'])}
    check(m.get('jobs')==len(expected),'manifest_jobs','Cartesian grid size')
    seen=Counter();n=0
    for p in sorted(path.glob('*__*.json')):
        row=json.loads(p.read_text());n+=1
        key=(row['base_id'],row['configuration'],row['arm'],row['rep']);seen[key]+=1
        check(key in expected,'unexpected_episode',p.name)
        if key not in expected:continue
        task=tasks[key[0]];cfg=m['configs'][key[1]];arm=key[2];req=row['request']
        truth,events=replay(task)
        answer,status=parse_answer(row,cfg['provider'])
        check(answer==row.get('answer'),'stored_answer',p.name)
        check(status==row.get('status'),'stored_status',p.name)
        score=expected_scores(truth,answer)
        for field,value in score.items():
            stored=row.get('score',{}).get(field)
            check(stored==value and type(stored)==type(value),'score_'+field,p.name)
        public={k:task[k] for k in PUBLIC};body={'input_representation':arm,**public}
        if arm!='raw':body.pop('reports')
        if arm=='canonical':body['eligible_events']=events
        if arm=='snapshot':body['historical_state']={f:truth[f] for f in FIELDS[:2]}
        is_openai=cfg['provider']=='openai';is_chat=cfg['provider']=='openrouter'
        messages=req.get('input' if is_openai else 'messages',[])
        try:
            if is_chat:
                # Chat completions carry the instructions as a system message ahead of the single user body.
                check(len(messages)==2 and messages[0]['role']=='system' and messages[0]['content']==m['instructions'],'instructions',p.name)
                messages=messages[1:]
            observed=json.loads(messages[0]['content'])
            check(len(messages)==1 and messages[0]['role']=='user' and observed==body,'public_body',p.name)
        except (IndexError,KeyError,ValueError,TypeError):check(False,'public_body',p.name)
        check(req.get('model')==cfg['model'] and row.get('model')==cfg['model'],'model',p.name)
        if not is_chat:check(req.get('instructions' if is_openai else 'system')==m['instructions'],'instructions',p.name)
        tools=req.get('tools',[])
        schema={'type':'object','properties':{f:{'type':'integer'} for f in FIELDS},'required':list(FIELDS),'additionalProperties':False}
        schema_key='parameters' if (is_openai or is_chat) else 'input_schema'
        tool=(tools[0].get('function') or {}) if is_chat and tools and isinstance(tools[0],dict) else (tools[0] if tools else {})
        check(len(tools)==1 and tool.get('name')=='submit_answer' and tool.get('strict') is True and tool.get(schema_key)==schema,'tool_schema',p.name)
        if is_chat:
            expected_choice='auto' if cfg.get('auto_tool_choice') else {'type':'function','function':{'name':'submit_answer'}}
            check(req.get('tool_choice')==expected_choice,'archived_tool_choice',p.name)
        elif is_openai and cfg.get('auto_tool_choice'):
            check(req.get('tool_choice')=='auto','archived_tool_choice',p.name)
        else:
            choices=[v for v in options['tool_choice'] if isinstance(v,dict) and v.get('type') in (('function',) if is_openai else ('auto','tool'))]
            check(req.get('tool_choice') in choices,'archived_tool_choice',p.name)
        limit='max_output_tokens' if is_openai else 'max_tokens'
        check(req.get(limit) in options[limit],'archived_output_limit',p.name)
        if is_openai:
            check(req.get('reasoning')=={'effort':cfg['reasoning']} and req.get('parallel_tool_calls') is False and req.get('store') is False,'openai_settings',p.name)
        elif is_chat:
            check(req.get('reasoning')=={'effort':cfg['reasoning']} and 'parallel_tool_calls' not in req
                  and req.get('provider')=={'only':[cfg['route']],'allow_fallbacks':False,'require_parameters':True},'openrouter_settings',p.name)
            served=(row.get('response') or {}).get('provider')
            check(served is None or str(served).lower().replace(' ','')==cfg['route'].replace(' ',''),'served_provider',p.name)
        else:
            thinking={'type':'enabled','budget_tokens':cfg['thinking_budget']} if cfg.get('thinking_budget') else None
            check(req.get('thinking')==thinking,'anthropic_thinking',p.name)
    missing=expected-set(seen)
    for key in sorted(missing):check(False,'missing_episode',list(key))
    for key,count in seen.items():check(count==1,'duplicate_episode',list(key))
    return {'run':path.name,'expected_episodes':len(expected),'observed_episodes':n,
            'mismatches':len(issues),'issue_counts':dict(Counter(x['category'] for x in issues)),
            'issues':issues,'passed':not issues,
            'notes':['Independent replay and raw-provider-response parsing; no experiment modules imported.',
                     'Payload settings checked against manifest configuration and archived runner literals.',
                     'Historical snapshots and canonical records are disclosed interventions, not unintended oracle fields.',
                     'External CSV source validation is not implemented here; source data require a separate provenance check.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,action='append',required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args();runs=[audit_run(path) for path in args.run]
    result={'passed':all(x['passed'] for x in runs),'episodes':sum(x['observed_episodes'] for x in runs),
            'mismatches':sum(x['mismatches'] for x in runs),'runs':runs}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'audit.json').write_text(json.dumps(result,indent=2))
    lines=['# Independent temporal results audit','',f"Passed: {result['passed']}. Episodes: {result['episodes']}. Mismatches: {result['mismatches']}.",'',
           '| Run | Observed / expected | Mismatches |','| --- | ---: | ---: |']
    lines += [f"| {r['run']} | {r['observed_episodes']}/{r['expected_episodes']} | {r['mismatches']} |" for r in runs]
    lines += ['', 'All score fields were recomputed from raw provider responses with an independent replay. Source hashes, request bodies, model settings and complete grids were checked. See audit.json for individual issues. External CSV provenance requires a separate check.', '']
    (args.output_dir/'audit.md').write_text('\n'.join(lines))
    print(json.dumps({k:result[k] for k in ('passed','episodes','mismatches')}))

if __name__=='__main__':main()
