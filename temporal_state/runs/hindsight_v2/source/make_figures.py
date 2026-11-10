"""Standalone temporal-history/scenario error and cost plots; completed data only."""
import argparse
import hashlib
import json
from pathlib import Path
from build_paper import ROOT,CONFIGS,LABELS,ARMS,load_run


def create(primary,external,outdir):
    runs=[('Synthetic',load_run(primary)),('External profiles',load_run(external))]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    colors={'raw':'#a63d40','canonical':'#2c7da0','snapshot':'#4c956c'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(2,2,figsize=(11,7),sharey=True,layout='constrained')
    width=.24
    for row,(label,run) in enumerate(runs):
        for col,metric in enumerate(('historical_joint','future_joint')):
            ax=axes[row,col]
            for i,arm in enumerate(ARMS):
                values=[100*(1-run['cells'][cfg,arm]['rates'][metric]) for cfg in CONFIGS]
                ax.bar([x+(i-1)*width for x in range(4)],values,width,color=colors[arm],label=arm.capitalize())
            ax.set_xticks(range(4),[LABELS[c].replace(' (','\n(') for c in CONFIGS],fontsize=8)
            ax.set_ylim(0,100);ax.set_ylabel('Exact-contract error (%)')
            ax.set_title(label+': '+('history' if col==0 else 'future scenario'))
            ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[0,0].legend(frameon=False,ncol=3,fontsize=8)
    saved=[]
    for ext in ('pdf','png'):
        name='historical_future_errors.'+ext;fig.savefig(outdir/name,dpi=200);saved.append(name)
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,3.8),layout='constrained')
    for ax,(label,run) in zip(axes,runs):
        for i,arm in enumerate(ARMS):
            values=[1000*run['cells'][cfg,arm]['estimated_cost_usd']/run['cells'][cfg,arm]['n'] for cfg in CONFIGS]
            ax.bar([x+(i-1)*width for x in range(4)],values,width,color=colors[arm],label=arm.capitalize())
        ax.set_xticks(range(4),[LABELS[c].replace(' (','\n(') for c in CONFIGS],fontsize=8)
        ax.set_title(label);ax.set_ylabel('Estimated USD / 1,000 calls')
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[0].legend(frameon=False,ncol=3,fontsize=8)
    for ext in ('pdf','png'):
        name='protocol_cost.'+ext;fig.savefig(outdir/name,dpi=200);saved.append(name)
    plt.close(fig)
    inputs=[Path(primary)/'analysis.json',Path(primary)/'manifest.json',Path(external)/'analysis.json',Path(external)/'manifest.json',Path(__file__),ROOT/'build_paper.py']
    provenance={'input_sha256':{p.resolve().relative_to(ROOT.resolve()).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                'output_sha256':{n:hashlib.sha256((outdir/n).read_bytes()).hexdigest() for n in saved},
                'notes':['Error=1 minus full-contract exact success; invalid outputs fail.',
                         'Snapshot historical state is supplied; historical accuracy does not measure reconstruction in that arm.',
                         'Configurations vary in model and reasoning settings; no causal cross-model attribution.',
                         'Costs are observed token-price estimates, not invoices. No intervals or independent-episode inference are implied by bars.']}
    (outdir/'figure_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(json.dumps({'figures':saved}))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--primary',type=Path,default=ROOT/'runs'/'heldout_v2')
    p.add_argument('--external',type=Path,default=ROOT/'runs'/'profiles_v2')
    p.add_argument('--output-dir',type=Path,default=ROOT/'paper'/'figures')
    a=p.parse_args()
    try:create(a.primary,a.external,a.output_dir)
    except (ValueError,KeyError) as e:raise SystemExit(f'Figures not generated: {e}')


if __name__=='__main__':main()
