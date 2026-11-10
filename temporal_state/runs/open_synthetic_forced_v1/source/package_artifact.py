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
EXTENSION_RUNS = ('effort_synthetic_v1', 'effort_profiles_v1', 'state_synthetic_v1', 'state_profiles_v1', 'replication_mini_low_v1',
                  'effort_gpt54_synthetic_v1', 'effort_gpt54_profiles_v1', 'tool_synthetic_v1', 'tool_profiles_v2', 'effort_auto_synthetic_v1')
CODE = ('benchmark.py', 'run.py', 'run_final_studies.py', 'run_extension_studies.py', 'run_extension_studies_2.py', 'diagnose_effort_traces.py',
        'analyze.py', 'compare_controls.py',
        'extension_analysis.py', 'decision_analysis.py', 'test_extensions.py', 'test_extension_analysis.py',
        'audit_results.py', 'audit_overlap.py', 'continuation_analysis.py', 'external_benchmark.py', 'external_data.py',
        'build_paper.py', 'make_figures.py', 'package_artifact.py', 'decompose_errors.py', 'diagnostic_paper.py',
        'test_benchmark.py', 'test_analysis.py', 'test_compare_controls.py', 'test_external.py', 'test_decompose_errors.py', 'test_diagnostic_paper.py', 'test_paper_assets.py', 'test_continuation.py')
DOCS = ('protocol.md', 'protocol_v2_addendum.md', 'external_protocol.md', 'protocol_v3_extensions.md',
        'external_data.md', 'references.bib', 'README_REPRODUCIBILITY.md',
        'development_gate.md', 'execution_plan.json', 'execution_plan_extensions.json', 'execution_plan_extensions_2.json')
DATA = ('freshretail_profiles.jsonl', 'freshretail_manifest.json', 'freshretail_SOURCE_README.md')
PAPER = ('main.tex', 'main.pdf', 'background.tex', 'appendix.tex', 'neurips_2026.sty',
         'main_table.tex', 'external_table.tex', 'controls_table.tex',
         'results_text.tex', 'abstract_findings.tex', 'discussion_findings.tex', 'coverage_text.tex',
         'generated_numbers.tex', 'number_provenance.json',
         'diagnostic_table.tex', 'diagnostic_findings.tex', 'diagnostic_main.tex', 'diagnostic_provenance.json',
         'continuation_table.tex', 'continuation_full_table.tex', 'continuation_findings.tex', 'continuation_abstract.tex',
         'merged_table.tex', 'results_compact.tex', 'factor_text.tex', 'factor_table.tex', 'decision_findings.tex',
         'extension_effort_table.tex', 'extension_state_table.tex', 'extension_effort_findings.tex', 'extension_state_findings.tex',
         'extension_tool_findings.tex', 'extension_numbers.tex', 'extension_all_cells_table.tex', 'extension_appendix.tex')
FIGURES = ('historical_future_errors.pdf', 'historical_future_errors.png',
           'protocol_cost.pdf', 'protocol_cost.png', 'figure_provenance.json',
           'decision_margins.pdf', 'decision_margins.png')
EXTENSION_GENERATED = ('extension_effort_table.tex', 'extension_state_table.tex', 'extension_effort_findings.tex',
                       'extension_state_findings.tex', 'extension_tool_findings.tex', 'extension_numbers.tex',
                       'extension_all_cells_table.tex', 'extension_appendix.tex')


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
    for name in ('overlap.json', 'overlap.md'):
        own('audits/overlap/' + name)
    for name in ('continuation.json', 'continuation.md'):
        own('audits/continuation/' + name)
    for name in ('extensions.json', 'extensions.md'):
        own('audits/extensions/' + name)
    for name in ('decision.json', 'decision.md'):
        own('audits/decision/' + name)
    traces = ROOT / 'audits' / 'effort_traces'
    for path in sorted(traces.glob('*')):
        check(path.suffix in ('.json', '.md'), 'Unexpected trace artifact: ' + path.name)
        own('audits/effort_traces/' + path.name)
    counts = {}
    for run in RUNS + EXTENSION_RUNS:
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
            check(name in CODE + DOCS + ('run_pilot.py',), 'Unapproved source snapshot filename: ' + name)
            own(f'runs/{run}/source/{name}')
            check(sha(files[f'temporal_state/runs/{run}/source/{name}']) == digest, f'Source hash mismatch: {run}/{name}')
    audit = read(audit_dir/'audit.json')
    check(audit['passed'] is True and audit['mismatches'] == 0, 'Final audit failed')
    original = {run: counts[run] for run in RUNS}
    check(audit['episodes'] == sum(original.values()), 'Final audit total mismatch')
    check({r['run']: r['expected_episodes'] for r in audit['runs']} == original, 'Final audit run grid mismatch')
    extensions = read(ROOT/'audits'/'extensions'/'extensions.json')
    check(extensions['audit_passed'] is True, 'Extension audit failed')
    check({run: extensions['episodes'][run] for run in extensions['episodes']} == {run: counts[run] for run in EXTENSION_RUNS if run in extensions['episodes']}, 'Extension audit grid mismatch')
    check(extensions.get('replication') and extensions['replication']['episodes'] == counts['replication_mini_low_v1'], 'Replication audit mismatch')
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
        if name.endswith('.json'):
            # Provider ciphertext (reasoning `encrypted_content`) is opaque base64 and can contain any
            # short letter sequence by chance; exclude only those values from the identity-literal scan.
            # Credential-shaped tokens are still scanned on the full blob below.
            try:
                def strip(obj):
                    if isinstance(obj, dict):
                        return {k: ('' if k == 'encrypted_content' else strip(v)) for k, v in obj.items()}
                    if isinstance(obj, list):
                        return [strip(v) for v in obj]
                    return obj
                content = json.dumps(strip(json.loads(blob))).encode()
            except ValueError:
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
        if any(x in blob or x in content for x in secrets):
            issues.append((name, 'environment API credential'))
        if re.search(rb'(?:sk-proj-|sk-ant-api)[A-Za-z0-9_-]{12,}', blob) or re.search(rb'(?:sk-proj-|sk-ant-api)[A-Za-z0-9_-]{12,}', content):
            issues.append((name, 'credential-shaped token'))
    if issues:
        # Print file/category only; never echo matched values or raw source lines.
        raise ValueError('Anonymity/secret scan failed; no content rewritten: ' + json.dumps(issues))


def command(args, cwd):
    # Offline verification children do not need credentials or private scan terms.
    environment = {k: v for k, v in os.environ.items()
                   if 'API_KEY' not in k.upper() and k != 'ARTIFACT_IDENTITY_TERMS'}
    result = subprocess.run(args, cwd=cwd, env=environment, capture_output=True, text=True)
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
    check(result['passed'] is True and result['mismatches'] == 0 and result['episodes'] == sum(counts[r] for r in RUNS), 'Extracted independent audit failed')
    # Recompute derived analysis in the disposable extracted copy, then compare.
    # This prevents a complete-looking but stale summary accompanying valid raw data.
    for run in RUNS:
        analysis_path = study/'runs'/run/'analysis.json'
        original_bytes = analysis_path.read_bytes()
        original = json.loads(original_bytes)
        command([sys.executable, 'analyze.py', 'runs/'+run,
                 '--bootstrap', str(original['bootstrap_draws']), '--seed', str(original['seed'])], study)
        check(read(analysis_path) == original, 'Recomputed analysis mismatch: ' + run)
        # Preserve original serialization for manuscript input-hash comparisons.
        analysis_path.write_bytes(original_bytes)
    args = [sys.executable, 'decompose_errors.py']
    for run in RUNS:
        args += ['--run', 'runs/'+run]
    args += ['--output-dir', str(root/'recomputed_decomposition')]
    command(args, study)
    check(read(root/'recomputed_decomposition'/'decomposition.json') ==
          read(study/'audits'/'decomposition'/'decomposition.json'), 'Recomputed decomposition mismatch')
    command([sys.executable, 'audit_overlap.py', '--output-dir', str(root/'recomputed_overlap')], study)
    for name in ('overlap.json', 'overlap.md'):
        check((root/'recomputed_overlap'/name).read_bytes() ==
              (study/'audits'/'overlap'/name).read_bytes(), 'Recomputed overlap audit mismatch')
    continuation = read(study/'audits'/'continuation'/'continuation.json')
    command([sys.executable, 'continuation_analysis.py', '--output-dir', str(root/'recomputed_continuation'),
             '--paper-dir', str(root/'continuation_paper'), '--bootstrap', str(continuation['bootstrap_draws']),
             '--seed', str(continuation['seed'])], study)
    for name in ('continuation.json', 'continuation.md'):
        check((root/'recomputed_continuation'/name).read_bytes() ==
              (study/'audits'/'continuation'/name).read_bytes(), 'Recomputed continuation mismatch')
    for name in ('continuation_table.tex', 'continuation_full_table.tex', 'continuation_findings.tex', 'continuation_abstract.tex'):
        check((root/'continuation_paper'/name).read_bytes() ==
              (study/'paper'/name).read_bytes(), 'Recomputed continuation manuscript mismatch')
    extensions = read(study/'audits'/'extensions'/'extensions.json')
    command([sys.executable, 'extension_analysis.py', '--output-dir', str(root/'recomputed_extensions'),
             '--paper-dir', str(root/'extension_paper'), '--bootstrap', str(extensions['bootstrap_draws']),
             '--seed', str(extensions['seed'])], study)
    for name in ('extensions.json', 'extensions.md'):
        check((root/'recomputed_extensions'/name).read_bytes() ==
              (study/'audits'/'extensions'/name).read_bytes(), 'Recomputed extension analysis mismatch')
    for name in EXTENSION_GENERATED:
        check((root/'extension_paper'/name).read_bytes() ==
              (study/'paper'/name).read_bytes(), 'Recomputed extension manuscript mismatch')
    command([sys.executable, 'decision_analysis.py', '--output-dir', str(root/'recomputed_decision'),
             '--paper-dir', str(root/'decision_paper'), '--no-figure'], study)
    for name in ('decision.json', 'decision.md'):
        check((root/'recomputed_decision'/name).read_bytes() ==
              (study/'audits'/'decision'/name).read_bytes(), 'Recomputed decision analysis mismatch')
    check((root/'decision_paper'/'decision_findings.tex').read_bytes() ==
          (study/'paper'/'decision_findings.tex').read_bytes(), 'Recomputed decision manuscript mismatch')
    comparison = read(study/'comparison.json')
    settings = {(control['bootstrap_draws'], control['seed']) for control in comparison['controls']}
    check(len(settings) == 1, 'Paired controls must use one recorded bootstrap configuration')
    draws, seed = next(iter(settings))
    command([sys.executable, 'compare_controls.py', '--original', 'runs/heldout_v2',
             '--hindsight', 'runs/hindsight_v2', '--display', 'runs/display_v2',
             '--bootstrap', str(draws), '--seed', str(seed),
             '--output-dir', str(root/'recomputed_comparison')], study)
    check(read(root/'recomputed_comparison'/'comparison.json') == comparison,
          'Recomputed control comparison mismatch')
    # Regenerate text/tables and provenance in the extracted paper directory.
    # Source-relative paths stay identical; do not rebuild timestamp-bearing PDFs.
    generated = ('main_table.tex', 'external_table.tex', 'controls_table.tex', 'merged_table.tex', 'results_compact.tex', 'factor_text.tex', 'factor_table.tex',
                 'results_text.tex', 'abstract_findings.tex', 'discussion_findings.tex',
                 'coverage_text.tex', 'generated_numbers.tex', 'number_provenance.json',
                 'diagnostic_table.tex', 'diagnostic_findings.tex', 'diagnostic_main.tex',
                 'diagnostic_provenance.json')
    originals = {name: (study/'paper'/name).read_bytes() for name in generated}
    command([sys.executable, 'build_paper.py'], study)
    args = [sys.executable, 'diagnostic_paper.py', '--decomposition',
            'audits/decomposition/decomposition.json']
    for run in RUNS:
        args += ['--run', 'runs/'+run]
    args += ['--output-dir', 'paper']
    command(args, study)
    for name, original in originals.items():
        check((study/'paper'/name).read_bytes() == original,
              'Recomputed manuscript asset mismatch: ' + name)


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
