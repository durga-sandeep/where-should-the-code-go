"""Build a verified anonymous supplement locally. Never calls model APIs.

Fails closed on missing final files, incomplete grids, failed audits or identity
matches. Archived source and raw responses are never rewritten for anonymity.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
RUNS = ('heldout_v2', 'hindsight_v2', 'display_v2', 'profiles_v2')
CODE = ('benchmark.py', 'run.py', 'analyze.py', 'compare_controls.py',
        'audit_results.py', 'external_benchmark.py', 'external_data.py',
        'build_paper.py', 'make_figures.py', 'package_artifact.py', 'decompose_errors.py',
        'test_benchmark.py', 'test_analysis.py', 'test_compare_controls.py', 'test_external.py', 'test_decompose_errors.py')
DOCS = ('protocol.md', 'protocol_v2_addendum.md', 'external_protocol.md',
        'external_data.md', 'references.bib', 'README_REPRODUCIBILITY.md',
        'development_gate.md', 'execution_plan.json')
DATA = ('freshretail_profiles.jsonl', 'freshretail_manifest.json', 'freshretail_SOURCE_README.md')
PAPER = ('main.tex', 'main.pdf', 'background.tex', 'neurips_2026.sty',
         'main_table.tex', 'external_table.tex', 'controls_table.tex',
         'results_text.tex', 'abstract_findings.tex', 'discussion_findings.tex',
         'generated_numbers.tex', 'number_provenance.json')
FIGURES = ('historical_future_errors.pdf', 'historical_future_errors.png',
           'protocol_cost.pdf', 'protocol_cost.png', 'figure_provenance.json')


def read(path):
    return json.loads(path.read_text())


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def select_files(audit_dir):
    files = {}
    def add(path, relative):
        check(path.is_file() and not path.is_symlink(), f'Required regular file absent: {relative}')
        check('..' not in Path(relative).parts, 'Unsafe archive path')
        files[relative] = path.read_bytes()
    def own(relative):
        add(ROOT / relative, 'temporal_state/' + relative)
    for name in CODE + DOCS:
        own(name)
    for name in DATA:
        own('data/' + name)
    for name in PAPER:
        own('paper/' + name)
    for name in FIGURES:
        own('paper/figures/' + name)
    for name in ('run_pilot.py', 'benchmark.py'):
        add(ROOT.parent / 'completeness_pilot' / name, 'completeness_pilot/' + name)
    for name in ('comparison.json', 'comparison.md'):
        own(name)
    for name in ('audit.json', 'audit.md'):
        add(audit_dir / name, 'temporal_state/audits/final/' + name)
    for name in ('decomposition.json', 'decomposition.md'):
        own('audits/decomposition/' + name)
    counts = {}
    for run in RUNS:
        directory = ROOT / 'runs' / run
        for name in ('manifest.json', 'analysis.json', 'results.md'):
            own(f'runs/{run}/{name}')
        manifest, analysis = read(directory/'manifest.json'), read(directory/'analysis.json')
        args = manifest['args']
        expected = {(t['base_id'], c, arm, rep) for t in manifest['tasks']
                    for c in args['configs'] for arm in args['arms'] for rep in range(args['reps'])}
        check(len({t['base_id'] for t in manifest['tasks']}) == len(manifest['tasks']), 'Duplicate tasks')
        check(manifest['jobs'] == len(expected), f'Manifest grid mismatch: {run}')
        check(analysis['complete'] is True and not analysis['missing'] and not analysis['unexpected'], f'Incomplete analysis: {run}')
        check(analysis['expected_episodes'] == analysis['observed_episodes'] == len(expected), f'Analysis count mismatch: {run}')
        seen = set()
        for path in sorted(directory.glob('*__*.json')):
            row = read(path)
            key = (row['base_id'], row['configuration'], row['arm'], row['rep'])
            check(key in expected and key not in seen, f'Duplicate or unexpected episode: {run}/{path.name}')
            seen.add(key)
            own(f'runs/{run}/{path.name}')
        check(seen == expected, f'Missing episodes: {run}')
        counts[run] = len(expected)
        check(bool(manifest['source_sha256']), f'Missing source map: {run}')
        for name, digest in manifest['source_sha256'].items():
            check(Path(name).name == name, 'Unsafe source snapshot name')
            own(f'runs/{run}/source/{name}')
            check(sha(files[f'temporal_state/runs/{run}/source/{name}']) == digest, f'Source hash mismatch: {run}/{name}')
    audit = read(audit_dir/'audit.json')
    check(audit['passed'] is True and audit['mismatches'] == 0, 'Final audit failed')
    check(audit['episodes'] == sum(counts.values()), 'Final audit total mismatch')
    check({r['run']: r['expected_episodes'] for r in audit['runs']} == counts, 'Final audit run grid mismatch')
    return files, counts


def scan(files, identity_terms=None):
    # Terms are local inputs, never serialized into the artifact or logs.
    if identity_terms is None:
        identity_terms = os.environ.get('ARTIFACT_IDENTITY_TERMS', '').split(',')
    literals = [term.strip().encode().lower() for term in identity_terms if term.strip()]
    check(bool(literals), 'Set nonempty ARTIFACT_IDENTITY_TERMS before building the archive')
    secrets = [v.encode() for k, v in os.environ.items() if 'API_KEY' in k.upper() and len(v) >= 8]
    issues = []
    for name, blob in files.items():
        content = blob
        if name.endswith('.pdf'):
            with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
                tmp.write(blob); tmp.flush()
                # Text extraction and metadata inspect compressed PDF contents.
                for command in (['pdftotext', tmp.name, '-'], ['pdfinfo', tmp.name]):
                    result = subprocess.run(command, capture_output=True, check=True)
                    content += result.stdout
        if any(x in name.encode().lower() or x in content.lower() for x in literals):
            issues.append((name, 'author-identifying literal'))
        if any(x in content for x in secrets):
            issues.append((name, 'environment API credential'))
        if re.search(rb'(?:sk-proj-|sk-ant-api)[A-Za-z0-9_-]{12,}', content):
            issues.append((name, 'credential-shaped token'))
    if issues:
        # Print file/category only; never echo matched values or raw source lines.
        raise ValueError('Anonymity/secret scan failed; no content rewritten: ' + json.dumps(issues))


def command(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        raise ValueError('Offline verification failed for ' + Path(args[1]).name)


def verify_extracted(root, counts):
    study = root/'temporal_state'
    inventory = read(root/'ARTIFACT_MANIFEST.json')
    for name, entry in inventory['files'].items():
        blob = (root/name).read_bytes()
        check(len(blob) == entry['bytes'] and sha(blob) == entry['sha256'], 'Extracted hash mismatch: ' + name)
    command([sys.executable, 'run.py', '--help'], study)
    command([sys.executable, '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py'], study)
    args = [sys.executable, 'audit_results.py']
    for run in RUNS:
        args += ['--run', 'runs/' + run]
    args += ['--output-dir', str(root/'recomputed_audit')]
    command(args, study)
    result = read(root/'recomputed_audit'/'audit.json')
    check(result['passed'] is True and result['mismatches'] == 0 and result['episodes'] == sum(counts.values()), 'Extracted independent audit failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'submission_supplement.zip')
    parser.add_argument('--audit-dir', type=Path, default=ROOT/'audits'/'final')
    args = parser.parse_args()
    try:
        files, counts = select_files(args.audit_dir)
        scan(files)
        inventory = {'format_version': 1, 'run_episode_counts': counts,
                     'total_episodes': sum(counts.values()),
                     'files': {name: {'bytes': len(blob), 'sha256': sha(blob)} for name, blob in sorted(files.items())},
                     'note': 'Inventory hashes every payload file; the inventory itself is covered by the external archive SHA-256.'}
        files['ARTIFACT_MANIFEST.json'] = (json.dumps(inventory, indent=2, sort_keys=True)+'\n').encode()
        with tempfile.TemporaryDirectory(prefix='temporal-package-') as temp:
            staged = Path(temp)/'supplement.zip'
            with zipfile.ZipFile(staged, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, blob in sorted(files.items()):
                    info = zipfile.ZipInfo(name, date_time=(2026, 9, 7, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, blob)
            unpacked = Path(temp)/'unpacked'
            with zipfile.ZipFile(staged) as archive:
                archive.extractall(unpacked)
            verify_extracted(unpacked, counts)
            blob = staged.read_bytes()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(blob)
            args.output.with_suffix(args.output.suffix+'.sha256').write_text(sha(blob)+'  '+args.output.name+'\n')
        print(json.dumps({'verified': True, 'episodes': sum(counts.values()), 'files': len(files), 'sha256': sha(blob)}))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit('Package not written: ' + str(error))


if __name__ == '__main__':
    main()
