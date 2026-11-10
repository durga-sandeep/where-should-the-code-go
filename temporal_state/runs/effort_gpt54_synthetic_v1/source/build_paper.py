"""Build manuscript assets only from complete temporal study outputs. No APIs."""
import argparse
import hashlib
import json
import math
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONFIGS=('mini_low','gpt54_low','sonnet46','sonnet46_thinking')
LABELS={'mini_low':'GPT-5.4 mini (low)','gpt54_low':'GPT-5.4 (low)',
        'sonnet46':'Sonnet 4.6','sonnet46_thinking':'Sonnet 4.6 (thinking)'}
TABLE_LABELS={'mini_low':'5.4 mini (low)','gpt54_low':'5.4 (low)',
              'sonnet46':'Sonnet 4.6','sonnet46_thinking':'Sonnet + thinking'}
ARMS=('raw','canonical','snapshot')
METRICS=('joint_exact','historical_joint','future_joint')
_spec=importlib.util.spec_from_file_location('temporal_asset_reference',Path(__file__).with_name('benchmark.py'))
_reference=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_reference)


def task_coverage(tasks):
    """One oracle outcome per manifest base, independent of model results."""
    if len({t['base_id'] for t in tasks})!=len(tasks):raise ValueError('Duplicate coverage base')
    truths=[_reference.replay_state(t) for t in tasks]
    return {'bases':len(tasks),
            'positive_historical_loss':sum(t['historical_lost']>0 for t in truths),
            'positive_future_loss':sum(t['future_lost']>0 for t in truths),
            'positive_terminal_stock':sum(t['stock_at_horizon']>0 for t in truths)}


def read(path):
    path=Path(path)
    if not path.is_file():raise ValueError(f'Required completed-study file absent: {path}')
    return json.loads(path.read_text())


def load_run(path):
    path=Path(path)
    analysis=read(path/'analysis.json');manifest=read(path/'manifest.json')
    if manifest['args'].get('split')!='heldout':raise ValueError('Manuscript assets require heldout cohorts, not development')
    if analysis.get('complete') is not True or analysis.get('missing') or analysis.get('unexpected'):
        raise ValueError(f'Incomplete study: {path.name}')
    if analysis['expected_episodes']!=analysis['observed_episodes'] or manifest['jobs']!=analysis['observed_episodes']:
        raise ValueError('Manifest/analysis episode mismatch')
    if set(manifest['args']['configs'])!=set(CONFIGS) or set(manifest['args']['arms'])!=set(ARMS):
        raise ValueError('Expected all four configurations and three protocols')
    cells={}
    for c in analysis['cells']:
        key=(c['configuration'],c['arm'])
        if key in cells:raise ValueError('Duplicate summary cell')
        if c['n'] != len(manifest['tasks'])*manifest['args']['reps']:raise ValueError('Cell denominator mismatch')
        for metric in METRICS:
            count=c['successes'][metric]
            if type(count) is not int or not 0<=count<=c['n'] or abs(c['rates'][metric]-count/c['n'])>1e-12:
                raise ValueError('Inconsistent metric count/rate')
        if c['missing_cost_records']:raise ValueError('Missing cost records; no zero substitution allowed')
        if not isinstance(c['estimated_cost_usd'],(int,float)) or not math.isfinite(c['estimated_cost_usd']) or c['estimated_cost_usd']<0:
            raise ValueError('Invalid cost estimate')
        cells[key]=c
    if set(cells)!={(c,a) for c in CONFIGS for a in ARMS}:raise ValueError('Missing required cell')
    if sum(c['n'] for c in cells.values())!=analysis['observed_episodes']:raise ValueError('Cell/total episode mismatch')
    if abs(sum(c['estimated_cost_usd'] for c in cells.values())-analysis['summary']['estimated_cost_usd'])>1e-8:
        raise ValueError('Cell/total cost mismatch')
    return dict(path=path,analysis=analysis,manifest=manifest,cells=cells)


def load_inputs(primary,external,controls):
    p,e=load_run(primary),load_run(external)
    for cfg in CONFIGS:
        if p['manifest']['configs'][cfg]!=e['manifest']['configs'][cfg]:raise ValueError('Primary/external configurations differ')
    c=read(controls)
    studies={x['kind']:x for x in c['controls']}
    if set(studies)!={'hindsight','display'} or len(c['controls'])!=2:raise ValueError('Both controls required exactly once')
    for study in studies.values():
        if study.get('complete') is not True:raise ValueError('Incomplete paired control')
        raw_rows=[x for x in study['cells'] if x['arm']=='raw']
        raw={x['configuration']:x for x in raw_rows}
        if len(raw)!=len(raw_rows):raise ValueError('Duplicate raw control configuration')
        if set(raw)!=set(CONFIGS):raise ValueError('Control missing raw configuration')
        for x in study['cells']:
            for pair in x['paired_differences']:
                if pair['unmatched_left'] or pair['unmatched_right']:raise ValueError('Unmatched control repetitions')
    return p,e,studies


def pct(value):
    return '--' if value is None else f'{100*value:.1f}'


def table(caption,label,header,rows,alignment):
    return ('\\begin{table}[t]\n\\centering\n\\small\n\\setlength{\\tabcolsep}{3pt}\n'
            +'\\begin{tabular}{'+alignment+'}\n\\toprule\n'+header+' \\\\\n\\midrule\n'
            +'\n'.join(' & '.join(row)+' \\\\' for row in rows)
            +'\n\\bottomrule\n\\end{tabular}\n\\caption{'+caption+'}\n\\label{'+label+'}\n\\end{table}\n')


def accuracy_table(run,external=False):
    rows=[]
    for cfg in CONFIGS:
        entries=[]
        for arm in ARMS:
            cell=run['cells'][cfg,arm]
            entries.append(pct(cell['rates']['joint_exact'])+' / '+pct(cell['rates']['future_joint']))
        rows.append([TABLE_LABELS[cfg],*entries])
    n=next(iter(run['cells'].values()))['n']
    caption=('External-profile simulation' if external else 'Held-out synthetic replay')+f': each cell is all-five / future-joint exact accuracy (\\%), {n} calls per configuration/protocol. The first endpoint requires all five outputs; the second requires all three future-scenario outputs. Invalid contracts fail. Thinking denotes a separate configuration.'
    return table(caption,'tab:external' if external else 'tab:main','Configuration & Raw & Canonical & Snapshot',rows,'lrrr')


def merged_future_table(primary,external):
    rows=[]
    for cfg in CONFIGS:
        rows.append([TABLE_LABELS[cfg],*[pct(run['cells'][cfg,arm]['rates']['future_joint']) for run in (primary,external) for arm in ARMS]])
    caption=('Future-joint exact accuracy (\\%): all three scenario outputs correct; 192 synthetic and 96 retail-profile calls per cell, invalid contracts fail. '
             'Snapshot supplies the exact historical state, so its column isolates rollout. All-five accuracies: Appendix~\\ref{app:tables}.')
    lines=['\\begin{table}[t]','\\centering\\footnotesize','\\begin{tabular}{lrrrrrr}','\\toprule',
           ' & \\multicolumn{3}{c}{Synthetic} & \\multicolumn{3}{c}{Retail profiles} \\\\',
           'Configuration & Raw & Canon. & Snap. & Raw & Canon. & Snap. \\\\','\\midrule',
           *[' & '.join(r)+' \\\\' for r in rows],'\\bottomrule','\\end{tabular}',
           '\\caption{'+caption+'}','\\label{tab:merged}','\\end{table}','']
    return '\n'.join(lines)


def build(primary,external,controls,outdir):
    # Validate everything before creating outputs; no development-run fallback.
    p,e,studies=load_inputs(primary,external,controls)
    outdir=Path(outdir)
    raw_controls={kind:{c['configuration']:c for c in study['cells'] if c['arm']=='raw'} for kind,study in studies.items()}
    rows=[]
    for cfg in CONFIGS:
        h=raw_controls['hindsight'][cfg]['diagnostics'];d=raw_controls['display'][cfg]['diagnostics']
        rows.append([TABLE_LABELS[cfg],pct(h['changed_when_required']['rate']),pct(h['both_correct_when_required']['rate']),
                     pct(d['answer_invariant']['rate']),pct(d['both_correct']['rate'])])
    changed_bases={raw_controls['hindsight'][cfg]['diagnostics']['changed_when_required']['bases'] for cfg in CONFIGS}
    display_bases={raw_controls['display'][cfg]['diagnostics']['answer_invariant']['bases'] for cfg in CONFIGS}
    if len(changed_bases)!=1 or len(display_bases)!=1:raise ValueError('Control denominators differ by configuration')
    control_table=table(f'Paired raw controls (\\%). K-chg/K-both: changed answers/both correct on {next(iter(changed_bases))} bases with changed truth. D-same/D-both: equal valid answers/both correct on {next(iter(display_bases))} display-permuted bases. Rates average repetitions within base. Change alone does not establish correct sensitivity.',
                        'tab:controls','Configuration & K-chg & K-both & D-same & D-both',rows,'lrrrr')
    costs={'primary':p['analysis']['summary']['estimated_cost_usd'],'external':e['analysis']['summary']['estimated_cost_usd']}
    counts={'PrimaryEpisodes':p['analysis']['observed_episodes'],'ExternalEpisodes':e['analysis']['observed_episodes'],
            'PrimaryBases':len(p['manifest']['tasks']),'ExternalBases':len(e['manifest']['tasks'])}
    coverage={label:task_coverage(run['manifest']['tasks']) for label,run in (('primary',p),('external',e))}
    for name,c in coverage.items():
        prefix=name.capitalize()
        counts.update({prefix+'HistoricalLossBases':c['positive_historical_loss'],
                       prefix+'FutureLossBases':c['positive_future_loss'],
                       prefix+'PositiveTerminalStockBases':c['positive_terminal_stock']})
    coverage_sentences=['Oracle task coverage counts each base once, independently of model calls; these are scenario properties, not model success rates.']
    for name,c in coverage.items():
        label='The synthetic cohort' if name=='primary' else 'The external-profile cohort'
        coverage_sentences.append(f"{label} has {c['positive_historical_loss']}/{c['bases']} bases with positive historical loss, {c['positive_future_loss']}/{c['bases']} with positive future loss, and {c['positive_terminal_stock']}/{c['bases']} with positive terminal stock. These categories can overlap.")
    lines=[]
    paired={}
    for contrast in p['analysis']['paired_comparisons']:
        key=(contrast['configuration'],contrast['left'],contrast['right'],contrast['metric'])
        if key in paired:raise ValueError('Duplicate paired comparison')
        paired[key]=contrast
    def contrast_text(cfg,arm):
        c=paired[cfg,'raw',arm,'future_joint']
        if c['unmatched_left'] or c['unmatched_right'] or c['matched_bases']!=len(p['manifest']['tasks']):
            raise ValueError('Incomplete paired future-joint contrast')
        if c['difference'] is None or c['ci95'] is None or len(c['ci95'])!=2:
            raise ValueError('Missing paired future-joint interval')
        if c['matched_episodes']!=p['cells'][cfg,'raw']['n']:
            raise ValueError('Paired future-joint episode denominator mismatch')
        expected=p['cells'][cfg,arm]['rates']['future_joint']-p['cells'][cfg,'raw']['rates']['future_joint']
        if abs(expected-c['difference'])>1e-10:raise ValueError('Paired difference disagrees with cell accuracies')
        if not all(math.isfinite(v) and -1<=v<=1 for v in [c['difference'],*c['ci95']]) or c['ci95'][0]>c['ci95'][1]:
            raise ValueError('Invalid paired interval')
        return f"{100*c['difference']:+.1f} [{100*c['ci95'][0]:+.1f}, {100*c['ci95'][1]:+.1f}]"
    lines.append('Future-joint differences below are protocol minus raw, in percentage points, with descriptive 95\\% paired base-bootstrap intervals; repetitions remain grouped within base.')
    for cfg in CONFIGS:
        lines.append(f"{LABELS[cfg]}: canonical {contrast_text(cfg,'canonical')}; snapshot {contrast_text(cfg,'snapshot')}.")
    lines.append('Intervals are not multiplicity adjusted; configurations are not compute-matched.')
    compact=(f"paired canonical and snapshot gains over raw are {contrast_text('mini_low','canonical')} and {contrast_text('mini_low','snapshot')} points for mini and "
             f"{contrast_text('gpt54_low','canonical')} and {contrast_text('gpt54_low','snapshot')} for GPT-5.4 on synthetic histories, while both Sonnet configurations start within a few points of ceiling "
             "(all intervals in Appendix~\\ref{app:tables}).\n")
    lines.append(f"The primary and external-profile evaluations contain {counts['PrimaryEpisodes']:,} and {counts['ExternalEpisodes']:,} calls, with token-price cost estimates of \\${costs['primary']:.2f} and \\${costs['external']:.2f}, respectively, excluding paired-control calls. External profiles drive a synthetic inventory scenario, not uncensored demand recovery or forecasting.")
    def interval_text(values):
        return pct(min(values))+'--'+pct(max(values))
    reps=p['manifest']['args']['reps']
    def future(run,cfg,arm):
        return pct(run['cells'][cfg,arm]['rates']['future_joint'])
    abstract=(f"Across {counts['PrimaryBases']} synthetic bases and four configurations ({reps} calls per base/protocol/configuration), "
              f"GPT-5.4 mini's future-joint exact accuracy rises from {future(p,'mini_low','raw')} to {future(p,'mini_low','canonical')} to {future(p,'mini_low','snapshot')}\\% across raw, canonical and snapshot inputs; "
              f"Sonnet without thinking already achieves {future(p,'sonnet46','raw')}\\% on raw reports. "
              "Exact state preparation leaves residual rollout errors for mini.\n")
    discussion=('Both exact historical preparation and executable future continuation expose configuration-dependent reliability boundaries. '
                'Neither supplies evidence about hidden reasoning, and consistent simulation can still produce incorrect stockout decisions from an incorrect state.\n')
    generated={'main_table.tex':accuracy_table(p),'external_table.tex':accuracy_table(e,True),'controls_table.tex':control_table,
               'merged_table.tex':merged_future_table(p,e),
               'results_text.tex':'\n'.join(lines)+'\n','results_compact.tex':compact,
               'abstract_findings.tex':abstract,'discussion_findings.tex':discussion,
               'coverage_text.tex':'\n'.join(coverage_sentences)+'\n',
               'generated_numbers.tex':'\n'.join('\\newcommand{\\'+k+'}{'+str(v)+'}' for k,v in counts.items())+'\n'}
    inputs=[p['path']/'analysis.json',p['path']/'manifest.json',e['path']/'analysis.json',e['path']/'manifest.json',Path(controls),Path(__file__),ROOT/'benchmark.py']
    provenance={'inputs':{x.resolve().relative_to(ROOT.resolve()).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in inputs},
                'counts':counts,'oracle_task_coverage':coverage,'recorded_cost_estimates_usd':costs,'configurations':{c:p['manifest']['configs'][c] for c in CONFIGS},
                'primary_cells':p['analysis']['cells'],'external_cells':e['analysis']['cells'],
                'controls':studies,'primary_paired_comparisons':p['analysis']['paired_comparisons'],
                'notes':['No estimates produced from missing cells.','Output percentages are success count / full planned cell denominator.',
                         'Control conditional denominators are not pooled with unconditional accuracies.','Costs are token-price estimates, not invoices.']}
    outdir.mkdir(parents=True,exist_ok=True)
    for name,content in generated.items():(outdir/name).write_text(content)
    provenance['output_sha256']={name:hashlib.sha256((outdir/name).read_bytes()).hexdigest() for name in generated}
    (outdir/'number_provenance.json').write_text(json.dumps(provenance,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'generated':list(generated),'counts':counts}))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--primary',type=Path,default=ROOT/'runs'/'heldout_v2')
    p.add_argument('--external',type=Path,default=ROOT/'runs'/'profiles_v2')
    p.add_argument('--controls',type=Path,default=ROOT/'comparison.json')
    p.add_argument('--output-dir',type=Path,default=ROOT/'paper')
    a=p.parse_args()
    try:build(a.primary,a.external,a.controls,a.output_dir)
    except (ValueError,KeyError) as e:raise SystemExit(f'Assets not generated: {e}')


if __name__=='__main__':main()
