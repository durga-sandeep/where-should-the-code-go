"""Execute the Amendment 4 plan (protocol_v4_extensions.md): interface-matched closed cells,
Haiku 4.5, and the open-weight capability ladder with the effort x tool-choice cross.

Uses real paid APIs through run.py, sequentially, stopping on any failed check. No retries,
schedules, uploads or submissions. Tasks come from the archived final-run manifests.
Pass --stage NAME to run a single stage (used to resume after an infrastructure interruption
with a fresh run name recorded in a transport note); the default runs every stage in order.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREFIX = 'temporal_state/'
OPEN = ('oss20b', 'oss120b', 'qwen27b', 'dsflash', 'glmflash', 'dspro')
FULL5 = ['raw', 'canonical', 'snapshot', 'state_raw', 'state_canonical']
SYN = ['--source-run', 'heldout_v2', '--n-base', '96']
PRO = ['--source-run', 'profiles_v2', '--n-base', '48']
PLAN = [
    # E6: interface-matched closed cells
    ('auto_mini_synthetic_v2', ['mini_low_auto'], ['snapshot', 'state_raw', 'state_canonical'], SYN),
    ('auto_mini_high_synthetic_v2', ['mini_high_auto'], ['snapshot'], SYN),
    ('auto_gpt54_synthetic_v1', ['gpt54_low_auto'], FULL5, SYN),
    ('auto_gpt54_high_synthetic_v1', ['gpt54_high_auto'], ['raw', 'canonical'], SYN),
    ('auto_profiles_v1', ['mini_low_auto', 'gpt54_low_auto'], FULL5, PRO),
    ('auto_high_profiles_v1', ['mini_high_auto', 'gpt54_high_auto'], ['raw', 'canonical'], PRO),
    # E7: second weak closed model
    ('haiku_synthetic_v1', ['haiku45', 'haiku45_thinking'], FULL5, SYN),
    ('haiku_profiles_v1', ['haiku45', 'haiku45_thinking'], FULL5, PRO),
    # E8: open-weight ladder
    # open_synthetic_low_auto_v1 was interrupted by exhausted 429 retries on CoreWeave GLM (transport note 9); preserved, excluded, repeated in full as v2.
    # open_synthetic_low_auto_v2 was interrupted by exhausted 429 retries on DeepInfra gpt-oss-20b (transport note 10); preserved, excluded, repeated in full as v3.
    ('open_synthetic_low_auto_v3', [f'{m}_low_auto' for m in OPEN], FULL5, SYN),
    # open_synthetic_high_auto_v1 was interrupted by a malformed tool-call argument string raising inside the parser (transport note 11); preserved, excluded, repeated as v2.
    ('open_synthetic_high_auto_v2', [f'{m}_high_auto' for m in OPEN], ['raw', 'canonical'], SYN),
    ('open_synthetic_forced_v1', [f'{m}_{e}' for m in OPEN for e in ('low', 'high')], ['raw', 'canonical'], SYN),
    ('open_profiles_low_auto_v1', [f'{m}_low_auto' for m in OPEN], ['raw', 'canonical', 'snapshot'], PRO),
    ('open_profiles_high_auto_v1', [f'{m}_high_auto' for m in OPEN], ['raw', 'canonical'], PRO),
    ('open_profiles_forced_v1', [f'{m}_{e}' for m in OPEN for e in ('low', 'high')], ['raw', 'canonical'], PRO),
    # E6b (addendum, written before its calls): same-period GPT-5.4 forced-call replication; run with --stage after the above.
    ('replication_gpt54_low_synthetic_v1', ['gpt54_low'], ['snapshot', 'state_canonical'], SYN),
]


def expected_episodes(plan):
    return sum(len(c) * len(a) * (96 if extra is SYN else 48) * 2 for _, c, a, extra in plan)


def command_for(name, configs, arms, extra):
    # Open-weight stages run transport-tolerant (transport note 10): a transport-exhausted episode does not abort
    # the grid; such episodes are preserved and re-issued in documented completion passes. First-party stages abort.
    tolerant = ['--transport-tolerant'] if name.startswith('open_') else []
    return [sys.executable, PREFIX + 'run.py', '--run', name, '--split', 'heldout', '--seed', '2026090802',
            '--configs', *configs, '--arms', *arms, '--reps', '2', '--workers', '48', *extra, *tolerant]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', action='append', help='run only these stage names (default: all, in order)')
    a = p.parse_args()
    plan = [s for s in PLAN if not a.stage or s[0] in a.stage]
    if a.stage and len(plan) != len(a.stage):
        raise ValueError('unknown stage name')
    for name, *_ in plan:
        if (ROOT / 'runs' / name).exists():
            raise ValueError('Run already exists; never overwrite or silently resume: ' + name)
    commands = [command_for(*stage) for stage in plan]
    record = ROOT / 'execution_plan_extensions_3.json'
    existing = json.loads(record.read_text()) if record.exists() else {'dispatches': []}
    existing['dispatches'].append(dict(
        created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        protocol='protocol_v4_extensions.md (Amendment 4)',
        commands=[['python3', *cmd[1:]] for cmd in commands], expected_episodes=expected_episodes(plan),
        no_retry=True, cumulative_cap_usd=3000))
    record.write_text(json.dumps(existing, indent=2) + '\n')
    for (name, *_), command in zip(plan, commands):
        print(json.dumps({'stage': name, 'status': 'starting'}), flush=True)
        with (ROOT / (name + '_progress.log')).open('w') as log:
            subprocess.run(command, cwd=REPO, stdout=log, stderr=subprocess.STDOUT, check=True)
        directory = PREFIX + 'runs/' + name
        subprocess.run([sys.executable, PREFIX + 'analyze.py', directory, '--bootstrap', '10000'], cwd=REPO, check=True)
        analysis = json.loads((ROOT / 'runs' / name / 'analysis.json').read_text())
        if not analysis['complete']:
            raise RuntimeError('Incomplete study ' + name)
        print(json.dumps({'stage': name, 'status': 'complete', 'episodes': analysis['observed_episodes'],
                          'estimated_cost_usd': analysis['summary']['estimated_cost_usd']}), flush=True)
    print(json.dumps({'status': 'amendment_4_stages_complete', 'stages': [s[0] for s in plan],
                      'expected_episodes': expected_episodes(plan)}), flush=True)


if __name__ == '__main__':
    main()
