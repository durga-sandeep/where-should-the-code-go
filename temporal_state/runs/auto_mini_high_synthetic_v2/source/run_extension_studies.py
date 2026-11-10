"""Execute the fixed extension-study plan (protocol_v3_extensions.md) sequentially.

Uses real paid APIs through run.py. Stops on any failed check. No retries, schedules,
uploads or submissions. Tasks are read from the archived final-run manifests so every
history is byte-identical to the original heldout cohorts.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREFIX = 'temporal_state/'
EFFORT_CONFIGS = ['mini_medium', 'mini_high']
STATE_CONFIGS = ['mini_low', 'gpt54_low', 'sonnet46', 'sonnet46_thinking', 'mini_high']
PLAN = [
    ('effort_synthetic_v1', EFFORT_CONFIGS, ['raw', 'canonical', 'snapshot'], ['--source-run', 'heldout_v2', '--n-base', '96']),
    ('effort_profiles_v1', EFFORT_CONFIGS, ['raw', 'canonical', 'snapshot'], ['--source-run', 'profiles_v2', '--n-base', '48']),
    ('state_synthetic_v1', STATE_CONFIGS, ['state_raw', 'state_canonical'], ['--source-run', 'heldout_v2', '--n-base', '96']),
    ('state_profiles_v1', STATE_CONFIGS, ['state_raw', 'state_canonical'], ['--source-run', 'profiles_v2', '--n-base', '48']),
]
EXPECTED = 2 * 3 * 96 * 2 + 2 * 3 * 48 * 2 + 5 * 2 * 96 * 2 + 5 * 2 * 48 * 2


def main():
    for name, *_ in PLAN:
        if (ROOT / 'runs' / name).exists():
            raise ValueError('Extension run already exists; never overwrite or silently resume: ' + name)
    commands = []
    for name, configs, arms, extra in PLAN:
        commands.append([sys.executable, PREFIX + 'run.py', '--run', name, '--split', 'heldout',
                         '--seed', '2026090802', '--configs', *configs, '--arms', *arms,
                         '--reps', '2', '--workers', '48', *extra])
    (ROOT / 'execution_plan_extensions.json').write_text(json.dumps(dict(
        created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        protocol='protocol_v3_extensions.md',
        commands=[['python3', *cmd[1:]] for cmd in commands], expected_episodes=EXPECTED,
        no_retry=True, cumulative_cap_usd=3000), indent=2) + '\n')
    for (name, *_), command in zip(PLAN, commands):
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
    print(json.dumps({'status': 'all_extension_studies_complete', 'expected_episodes': EXPECTED}), flush=True)


if __name__ == '__main__':
    main()
