"""Execute the fixed final study plan sequentially, stopping on any failed check.

Uses real paid APIs through run.py. No retries, schedules, uploads or submissions.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREFIX = 'temporal_state/'
CONFIGS = ['mini_low','gpt54_low','sonnet46','sonnet46_thinking']
PLAN = [
    ('heldout_v2', ['--n-base','96']),
    ('hindsight_v2', ['--source-run','heldout_v2','--n-base','24','--knowledge-cutoff','130']),
    ('display_v2', ['--source-run','heldout_v2','--n-base','24','--shuffle-reports','--arms','raw']),
    ('profiles_v2', ['--dataset','profiles','--n-base','48']),
]


def main():
    for name,_ in PLAN:
        if (ROOT/'runs'/name).exists():
            raise ValueError('Final run already exists; never overwrite or silently resume: '+name)
    commands=[]
    for name,extra in PLAN:
        commands.append([sys.executable,PREFIX+'run.py','--run',name,'--split','heldout',
                         '--seed','2026090802','--configs',*CONFIGS,'--reps','2','--workers','48',*extra])
    # Store interpreter-neutral relative commands for anonymous reproducibility.
    (ROOT/'execution_plan.json').write_text(json.dumps(dict(
        created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        commands=[['python3',*cmd[1:]] for cmd in commands], expected_episodes=4224,
        no_retry=True, cumulative_cap_usd=3000),indent=2))
    for (name,_),command in zip(PLAN,commands):
        print(json.dumps({'stage':name,'status':'starting'}),flush=True)
        with (ROOT/(name+'_progress.log')).open('w') as log:
            subprocess.run(command,cwd=REPO,stdout=log,stderr=subprocess.STDOUT,check=True)
        directory=PREFIX+'runs/'+name
        subprocess.run([sys.executable,PREFIX+'analyze.py',directory,'--bootstrap','10000'],cwd=REPO,check=True)
        analysis=json.loads((ROOT/'runs'/name/'analysis.json').read_text())
        if not analysis['complete']: raise RuntimeError('Incomplete study '+name)
        subprocess.run([sys.executable,PREFIX+'audit_results.py','--run',directory,
                        '--output-dir',PREFIX+'audits/'+name],cwd=REPO,check=True)
        print(json.dumps({'stage':name,'status':'complete','episodes':analysis['observed_episodes']}),flush=True)
    print(json.dumps({'status':'all_studies_complete','expected_episodes':4224}),flush=True)


if __name__=='__main__':main()
