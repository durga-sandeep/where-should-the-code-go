"""Build diagnostic paper fragments from complete, hash-verified decompositions.

No APIs. Requires raw cohort paths to check completeness and output truncation.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

CATEGORIES=('stock_correct_future_correct','stock_correct_future_wrong',
            'stock_wrong_future_wrong_consistent','stock_wrong_future_wrong_inconsistent',
            'stock_wrong_future_correct')
LABELS={'mini_low':'GPT-5.4 mini (low)','gpt54_low':'GPT-5.4 (low)',
        'sonnet46':'Sonnet 4.6','sonnet46_thinking':'Sonnet + thinking'}


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def escape(text):
    return str(text).replace('\\','\\textbackslash{}').replace('_','\\_').replace('&','\\&').replace('%','\\%').replace('#','\\#')


def truncated(row):
    response=row.get('response') or {}
    details=response.get('incomplete_details') or {}
    return response.get('stop_reason')=='max_tokens' or details.get('reason')=='max_output_tokens'


def verify(run,path):
    manifest_path=path/'manifest.json';manifest=json.loads(manifest_path.read_text())
    if run.get('complete') is not True:raise ValueError('Incomplete decomposition')
    if digest(manifest_path)!=run['provenance']['manifest_sha256']:raise ValueError('Manifest hash mismatch')
    args=manifest['args'];tasks=manifest['tasks']
    bases=[t['base_id'] for t in tasks]
    if len(set(bases))!=len(bases):raise ValueError('Duplicate manifest bases')
    expected={(b,c,a,r) for b in bases for c in args['configs'] for a in args['arms'] for r in range(args['reps'])}
    if run['episodes']!=len(expected) or manifest['jobs']!=len(expected):raise ValueError('Episode denominator mismatch')
    hashes=run['provenance']['episode_files_sha256']
    actual_files={p.name for p in path.glob('*__*.json')}
    if set(hashes)!=actual_files:raise ValueError('Missing or unexpected raw files')
    seen=set();counts=Counter();truncations=Counter();invalid_truncated=Counter()
    for filename,sha in hashes.items():
        if Path(filename).name!=filename:raise ValueError('Nonlocal episode filename')
        file=path/filename
        if digest(file)!=sha:raise ValueError('Episode hash mismatch')
        row=json.loads(file.read_text());key=(row['base_id'],row['configuration'],row['arm'],row['rep'])
        if key in seen or key not in expected:raise ValueError('Duplicate or unexpected episode')
        seen.add(key);cell=(row['configuration'],row['arm']);counts[cell]+=1
        truncations[cell]+=truncated(row)
        invalid_truncated[cell]+=truncated(row) and not row['score']['valid']
    if seen!=expected:raise ValueError('Incomplete grid')
    cells={}
    for cell in run['cells']:
        key=(cell['configuration'],cell['arm'])
        if key in cells:raise ValueError('Duplicate cell')
        if cell['n']!=counts[key] or cell['valid']+cell['invalid']!=cell['n']:raise ValueError('Invalid cell denominator')
        if set(cell['categories'])!=set(CATEGORIES):raise ValueError('Missing diagnostic category')
        if any(type(v)is not int or v<0 for v in cell['categories'].values()):raise ValueError('Bad category count')
        if sum(cell['categories'].values())!=cell['valid']:raise ValueError('Categories do not partition valid outputs')
        cells[key]={**cell,'output_limit_truncated':truncations[key],
                    'invalid_and_output_limit_truncated':invalid_truncated[key]}
    if set(cells)!=set(counts):raise ValueError('Missing diagnostic cell')
    return {'name':run['run'],'cells':cells,'episodes':run['episodes'],
            'manifest_sha256':run['provenance']['manifest_sha256']}


def fragments(studies):
    paragraphs=[]
    table=['\\begin{table}[t]','\\centering\\small',
           '\\caption{Observable diagnostic counts for raw/canonical outputs. SC/FW: correct emitted starting stock, wrong future triple. SW/FW-C: wrong stock and future, consistent with replay from emitted stock. SW/FW-I: both wrong and inconsistent. SW/FC: wrong stock, correct future. Invalid contracts are outside these valid-output categories.}','\\label{tab:diagnostic}',
           '\\begin{tabular}{llrrrrr}','\\toprule',
           'Config. & Arm & Invalid & SC/FW & SW/FW-C & SW/FW-I & SW/FC \\\\', '\\midrule']
    for study in studies:
        label={'heldout_v2':'Primary synthetic','profiles_v2':'Retail profiles','hindsight_v2':'Later knowledge','display_v2':'Display permutation'}.get(study['name'],escape(study['name']))
        selected=[c for (cfg,arm),c in study['cells'].items() if arm in ('raw','canonical')]
        if not selected:raise ValueError('No raw/canonical diagnostic cells')
        counts=Counter()
        for c in selected:counts.update(c['categories'])
        valid=sum(c['valid'] for c in selected)
        bothwrong=counts['stock_wrong_future_wrong_consistent']+counts['stock_wrong_future_wrong_inconsistent']
        history=sum(c['historical_lost_wrong_with_correct_stock'] for c in selected)
        invalid=sum(c['invalid'] for c in study['cells'].values())
        trunc=sum(c['output_limit_truncated'] for c in study['cells'].values())
        overlap=sum(c['invalid_and_output_limit_truncated'] for c in study['cells'].values())
        propagation = (f"{counts['stock_wrong_future_wrong_consistent']}/{bothwrong} valid outputs with both wrong starting stock and wrong future quantities exactly match replay from the emitted stock" if bothwrong else "no valid output has both wrong starting stock and wrong future quantities")
        representation='raw requests' if {c['arm'] for c in selected}=={'raw'} else 'pooled raw and canonical requests'
        paragraphs.append(f"{label}: among {representation}, {propagation}. There are {counts['stock_correct_future_wrong']} correct-stock/wrong-future outputs and {counts['stock_wrong_future_correct']} wrong-stock/correct-future outputs among {valid} valid requests. Historical loss is wrong despite correct starting stock in {history} requests. Across all arms, {invalid}/{study['episodes']} contracts are invalid and {trunc} responses hit the output-token limit ({overlap} overlap).")
        table += [f'\\multicolumn{{7}}{{l}}{{{label}}} \\\\']
        for c in sorted(selected,key=lambda x:(x['configuration'],x['arm'])):
            ct=c['categories'];numbers=[c['invalid'],ct['stock_correct_future_wrong'],ct['stock_wrong_future_wrong_consistent'],ct['stock_wrong_future_wrong_inconsistent'],ct['stock_wrong_future_correct']]
            table.append(escape(LABELS.get(c['configuration'],c['configuration']))+' & '+escape(c['arm'])+' & '+' & '.join(map(str,numbers))+' \\\\')
    table += ['\\bottomrule','\\end{tabular}','\\end{table}','']
    caveat='These are descriptive counts over repeated requests, not independent failure probabilities. Replay agreement establishes observable consistency, not that the model internally used its emitted stock; correct future outputs after a wrong stock do not prove intentional recovery. Invalid and truncated counts overlap and must not be added.'
    return '\n\n'.join(paragraphs+[caveat])+'\n', '\n'.join(table)



def main_fragment(studies):
    required={'heldout_v2','hindsight_v2','display_v2','profiles_v2'}
    indexed={s['name']:s for s in studies}
    if set(indexed)!=required or len(studies)!=4:
        raise ValueError('Main-paper diagnostic requires all four final cohorts, including heldout_v2')
    selected=[c for (cfg,arm),c in indexed['heldout_v2']['cells'].items() if arm in ('raw','canonical')]
    if not selected:raise ValueError('No heldout raw/canonical diagnostics')
    counts=Counter()
    for c in selected:counts.update(c['categories'])
    valid=sum(c['valid'] for c in selected)
    denominator=counts['stock_wrong_future_wrong_consistent']+counts['stock_wrong_future_wrong_inconsistent']
    propagation=(f"{counts['stock_wrong_future_wrong_consistent']}/{denominator} wrong-stock/wrong-future responses match exact replay from the emitted stock" if denominator else "no response has both wrong starting stock and wrong future outputs")
    cells=[c for s in studies for c in s['cells'].values()]
    invalid=sum(c['invalid'] for c in cells);truncated_count=sum(c['output_limit_truncated'] for c in cells)
    overlap=sum(c['invalid_and_output_limit_truncated'] for c in cells)
    total=sum(s['episodes'] for s in studies)
    return (f"Among {valid} valid raw/canonical responses in the primary synthetic study, {propagation}. "
            f"Another {counts['stock_correct_future_wrong']} have correct starting stock but wrong future outputs; "
            f"{counts['stock_wrong_future_correct']} have wrong stock but correct future outputs. "
            "These are observable answer-consistency patterns, not evidence of internal causal error propagation or intentional recovery. "
            f"Across all four cohorts ({total} requests), invalid contracts total {invalid} and {truncated_count} responses "
            f"reach the output-token limit, with {overlap} overlapping cases; these counts must not be added. "
            "The artifact provides historical-loss and stockout-detection counts with complete denominators.\n")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--decomposition',type=Path,required=True)
    p.add_argument('--run',type=Path,action='append',required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args();data=json.loads(args.decomposition.read_text())
    paths={r.name:r for r in args.run}
    if len(paths)!=len(args.run):raise ValueError('Duplicate run names')
    indexed={r['run']:r for r in data['runs']}
    if len(indexed)!=len(data['runs']):raise ValueError('Duplicate decomposition runs')
    if set(paths)!=set(indexed):raise ValueError('Provide exactly all decomposed cohort paths')
    studies=[verify(indexed[name],path) for name,path in paths.items()]
    text,table=fragments(studies)
    short=main_fragment(studies)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'diagnostic_findings.tex').write_text(text)
    (args.output_dir/'diagnostic_main.tex').write_text(short)
    (args.output_dir/'diagnostic_table.tex').write_text(table)
    provenance={'decomposition_sha256':digest(args.decomposition),
                'cohorts':[{k:s[k] for k in ('name','episodes','manifest_sha256')} for s in studies],
                'fragments_sha256':{name:digest(args.output_dir/name) for name in ('diagnostic_findings.tex','diagnostic_table.tex','diagnostic_main.tex')}}
    (args.output_dir/'diagnostic_provenance.json').write_text(json.dumps(provenance,indent=2))
    print(json.dumps({'complete':True,'episodes':sum(s['episodes'] for s in studies)}))

if __name__=='__main__':main()
