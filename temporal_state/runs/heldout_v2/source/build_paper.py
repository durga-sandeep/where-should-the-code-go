"""Build manuscript assets only from complete temporal study outputs. No APIs."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONFIGS=('mini_low','gpt54_low','sonnet46','sonnet46_thinking')
LABELS={'mini_low':'GPT-5.4 mini (low)','gpt54_low':'GPT-5.4 (low)',
        'sonnet46':'Sonnet 4.6','sonnet46_thinking':'Sonnet 4.6 (thinking)'}
TABLE_LABELS={'mini_low':'5.4 mini (low)','gpt54_low':'5.4 (low)',
              'sonnet46':'Sonnet 4.6','sonnet46_thinking':'Sonnet + thinking'}
ARMS=('raw','canonical','snapshot')
METRICS=('joint_exact','historical_joint','future_joint')


def read(path):
    path=Path(path)
    if not path.is_file():raise ValueError(f'Required completed-study file absent: {path}')
    return json.loads(path.read_text())


def load_run(path):
    path=Path(path)
    analysis=read(path/'analysis.json');manifest=read(path/'manifest.json')
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
        cells[key]=c
    if set(cells)!={(c,a) for c in CONFIGS for a in ARMS}:raise ValueError('Missing required cell')
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
        raw={x['configuration']:x for x in study['cells'] if x['arm']=='raw'}
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


def build(primary,external,controls,outdir):
    # Validate everything before creating outputs; no development-run fallback.
    p,e,studies=load_inputs(primary,external,controls)
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    raw_controls={kind:{c['configuration']:c for c in study['cells'] if c['arm']=='raw'} for kind,study in studies.items()}
    rows=[]
    for cfg in CONFIGS:
        h=raw_controls['hindsight'][cfg]['diagnostics'];d=raw_controls['display'][cfg]['diagnostics']
        rows.append([TABLE_LABELS[cfg],pct(h['changed_when_required']['rate']),pct(h['both_correct_when_required']['rate']),
                     pct(d['answer_invariant']['rate']),pct(d['both_correct']['rate'])])
    control_table=table('Paired raw-input controls (\\%). K-change and K-correct condition on changed oracle answers: the former measures output change, the latter correctness in both views. Display invariant requires equal valid answers; Display correct requires both correct. Conditional denominators and intervals are preserved in provenance. A changed answer alone is not correct sensitivity.',
                        'tab:controls','Configuration & K-chg & K-both & D-same & D-both',rows,'lrrrr')
    costs={'primary':p['analysis']['summary']['estimated_cost_usd'],'external':e['analysis']['summary']['estimated_cost_usd']}
    counts={'PrimaryEpisodes':p['analysis']['observed_episodes'],'ExternalEpisodes':e['analysis']['observed_episodes'],
            'PrimaryBases':len(p['manifest']['tasks']),'ExternalBases':len(e['manifest']['tasks'])}
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
        return f"{100*c['difference']:+.1f} [{100*c['ci95'][0]:+.1f}, {100*c['ci95'][1]:+.1f}]"
    lines.append('Future-joint differences below are protocol minus raw, in percentage points, with descriptive 95\\% paired base-bootstrap intervals; repetitions remain grouped within base.')
    for cfg in CONFIGS:
        lines.append(f"{LABELS[cfg]}: canonical {contrast_text(cfg,'canonical')}; snapshot {contrast_text(cfg,'snapshot')}.")
    lines.append('Snapshot supplies exact historical state, so historical scores in that arm measure copying rather than reconstruction. Configuration comparisons do not isolate model size, provider, or reasoning budget; intervals are not multiplicity adjusted.')
    lines.append(f"The primary and external-profile evaluations contain {counts['PrimaryEpisodes']:,} and {counts['ExternalEpisodes']:,} calls, with token-price cost estimates of \\${costs['primary']:.2f} and \\${costs['external']:.2f}, respectively, excluding paired-control calls. External profiles drive a synthetic inventory scenario, not uncensored demand recovery or forecasting.")
    def interval_text(values):
        return pct(min(values))+'--'+pct(max(values))
    raw_range=interval_text([p['cells'][cfg,'raw']['rates']['joint_exact'] for cfg in CONFIGS])
    canonical_range=interval_text([p['cells'][cfg,'canonical']['rates']['joint_exact'] for cfg in CONFIGS])
    snapshot_future_range=interval_text([p['cells'][cfg,'snapshot']['rates']['future_joint'] for cfg in CONFIGS])
    abstract=(f"Across {counts['PrimaryBases']} synthetic bases, four model configurations, three protocols and two samples per cell, all-five exact accuracy ranges from {raw_range}\\% for raw reports to {canonical_range}\\% for executable canonical histories. "
              f"With exact historical state supplied, future-scenario exact accuracy ranges from {snapshot_future_range}\\%. "
              'Paired knowledge-cutoff and display-order controls distinguish changed evidence from harmless presentation changes; a profile-driven retail simulation extends the evaluation without claiming real-world forecasting accuracy.\n')
    discussion=('The protocols expose separable engineering stages: report selection and version resolution, chronological historical replay, and deterministic scenario propagation. '
                'Canonical histories and exact snapshots are executable preprocessing interventions, not evidence that a model internally represents event time correctly. '
                'Snapshot history scores reflect a supplied state; scenario errors can remain after reconstruction is removed. '
                'Knowledge-cutoff response changes must be evaluated for correctness in both views, while harmless display changes should preserve answers. '
                'The external profiles provide observed sales shapes only: inventory receipts, revision chains and reporting delays remain synthetic, and observed sales may be stockout-censored. '
                'Results concern exact simulation under specified inputs and model settings; they do not establish forecast calibration, learned world models, or independent real-world replication.\n')
    generated={'main_table.tex':accuracy_table(p),'external_table.tex':accuracy_table(e,True),'controls_table.tex':control_table,
               'results_text.tex':'\n'.join(lines)+'\n',
               'abstract_findings.tex':abstract,'discussion_findings.tex':discussion,
               'generated_numbers.tex':'\n'.join('\\newcommand{\\'+k+'}{'+str(v)+'}' for k,v in counts.items())+'\n'}
    inputs=[p['path']/'analysis.json',p['path']/'manifest.json',e['path']/'analysis.json',e['path']/'manifest.json',Path(controls),Path(__file__)]
    provenance={'inputs':{x.resolve().relative_to(ROOT.resolve()).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in inputs},
                'counts':counts,'recorded_cost_estimates_usd':costs,'configurations':{c:p['manifest']['configs'][c] for c in CONFIGS},
                'primary_cells':p['analysis']['cells'],'external_cells':e['analysis']['cells'],
                'controls':studies,'primary_paired_comparisons':p['analysis']['paired_comparisons'],
                'notes':['No estimates produced from missing cells.','Output percentages are success count / full planned cell denominator.',
                         'Control conditional denominators are not pooled with unconditional accuracies.','Costs are token-price estimates, not invoices.']}
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
