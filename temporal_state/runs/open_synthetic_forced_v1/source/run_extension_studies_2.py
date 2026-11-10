"""Execute the Amendment 2 plan (protocol_v3_extensions.md): GPT-5.4 effort sweep and code-inside arms.

Uses real paid APIs through run.py, sequentially, stopping on any failed check. No retries,
schedules, uploads or submissions. Tasks come from the archived final-run manifests.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREFIX = 'temporal_state/'
PLAN = [
    ('effort_gpt54_synthetic_v1', ['gpt54_medium', 'gpt54_high'], ['raw', 'canonical'], ['--source-run', 'heldout_v2', '--n-base', '96']),
    ('effort_gpt54_profiles_v1', ['gpt54_medium', 'gpt54_high'], ['raw', 'canonical'], ['--source-run', 'profiles_v2', '--n-base', '48']),
    ('tool_synthetic_v1', ['mini_low', 'gpt54_low'], ['tool_raw', 'tool_canonical'], ['--source-run', 'heldout_v2', '--n-base', '96']),
    ('tool_profiles_v1', ['mini_low', 'gpt54_low'], ['tool_raw', 'tool_canonical'], ['--source-run', 'profiles_v2', '--n-base', '48']),
]
EXPECTED = 2 * (2 * 2 * 96 * 2 + 2 * 2 * 48 * 2)


def main():
    for name, *_ in PLAN:
        if (ROOT / 'runs' / name).exists():
            raise ValueError('Run already exists; never overwrite or silently resume: ' + name)
    commands = []
    for name, configs, arms, extra in PLAN:
        commands.append([sys.executable, PREFIX + 'run.py', '--run', name, '--split', 'heldout',
                         '--seed', '2026090802', '--configs', *configs, '--arms', *arms,
                         '--reps', '2', '--workers', '48', *extra])
    (ROOT / 'execution_plan_extensions_2.json').write_text(json.dumps(dict(
        created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        protocol='protocol_v3_extensions.md (Amendment 2)',
        commands=[['python3', *cmd[1:]] for cmd in commands], expected_episodes=EXPECTED,
        no_retry=True, cumulative_cap_usd=3000,
        note='Code-interpreter container charges are billed by the provider per session and are not in the token ledger.'), indent=2) + '\n')
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
    print(json.dumps({'status': 'amendment_2_complete', 'expected_episodes': EXPECTED}), flush=True)


if __name__ == '__main__':
    main()
