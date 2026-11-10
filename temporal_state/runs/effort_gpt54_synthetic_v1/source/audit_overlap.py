"""Post-hoc exact-content/split check; no APIs or training-data access."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def frozen(run, name):
    manifest_path = ROOT / 'runs' / run / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    path = manifest_path.parent / 'source' / name
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != manifest['source_sha256'][name]:
        raise ValueError(f'Frozen source hash mismatch: {run}/{name}')
    spec = importlib.util.spec_from_file_location('overlap_' + run + name.replace('.', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, manifest, {'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                              'generator_sha256': actual}


def content(task):
    """Exact report-group content, ignoring arbitrary IDs and display order.

    Grouping of revisions is retained. Removing IDs also ignores their role in
    breaking tied event times; this is a content screen, not semantic equivalence.
    """
    groups = {}
    for row in task['reports']:
        groups.setdefault(row['event_id'], []).append({k: v for k, v in row.items() if k != 'event_id'})
    return {**{k: task[k] for k in ('initial_stock', 'target_time', 'knowledge_cutoff', 'horizon_time')},
            'report_groups': sorted(digest(sorted(rows, key=lambda r: r['revision'])) for rows in groups.values()),
            'future': sorted(digest({k: v for k, v in row.items() if k != 'event_id'})
                             for row in task['future_schedule'])}


def compare(development, heldout, transform):
    left = Counter(digest(transform(t)) for t in development)
    right = Counter(digest(transform(t)) for t in heldout)
    return {'development_count': len(development), 'heldout_count': len(heldout),
            'development_duplicate_excess': sum(n - 1 for n in left.values()),
            'heldout_duplicate_excess': sum(n - 1 for n in right.values()),
            'shared_distinct_hashes': sorted(left.keys() & right.keys())}


def audit():
    synthetic, sm, sp = frozen('heldout_v2', 'benchmark.py')
    profiles, pm, pp = frozen('profiles_v2', 'external_benchmark.py')
    # Frozen adapter's default data path points inside source/, where data are
    # not duplicated. Bind its existing hash-checking loader to packaged data.
    original_loader = profiles.load_profiles
    profiles.load_profiles = lambda: original_loader(ROOT / 'data' / 'freshretail_profiles.jsonl')
    sd = synthetic.generate_tasks(24, synthetic.DEVELOPMENT_SEED, 'dev')
    pd = profiles.generate_tasks(seed=profiles.DEVELOPMENT_SEED, split='dev')
    if synthetic.generate_tasks() != sm['tasks'] or profiles.generate_tasks() != pm['tasks']:
        raise ValueError('Frozen generator does not reproduce final manifest tasks')
    stores = profiles.load_profiles()
    def quantities(task):
        past, future, _ = profiles.quantities(stores[task['source_store_id']])
        return {'past': past, 'future': future}
    results = {
        'analysis': 'post_hoc_exact_content_and_source_split_audit',
        'provenance': {'synthetic': sp, 'profiles': pp,
                       'profile_data_sha256': profiles.SOURCE_SHA256},
        'synthetic_public_payload': compare(sd, sm['tasks'], synthetic.public_task),
        'synthetic_id_and_display_ignored_content': compare(sd, sm['tasks'], content),
        'profile_public_payload': compare(pd, pm['tasks'], synthetic.public_task),
        'profile_id_and_display_ignored_content': compare(pd, pm['tasks'], content),
        'profile_quantized_past_and_future_sequences': compare(pd, pm['tasks'], quantities),
        'profile_source_store_overlap': sorted({t['source_store_id'] for t in pd} &
                                             {t['source_store_id'] for t in pm['tasks']}),
        'notes': [
            'Added after final model results; no examples are removed or rescored.',
            'Final heldout tasks come from manifests; frozen hash-verified generators recreate 24 v2 development histories and all 16 profile development stores. Only four profile development stores received model calls. Early v1 development is outside this check.',
            'Generator reproduction of both complete heldout manifests is required. Development manifests are not needed by this packaged check.',
            'Public-payload checks retain event IDs. The additional content screen ignores IDs/display order but retains revision groups; it also ignores ID tie-breaking and is not a semantic-equivalence test.',
            'Quantity checks compare exact ordered 36 historical and 12 future quantized sales bins, without receipts or reporting anomalies.',
            'Paired controls and repetitions deliberately reuse bases and are not included as accidental duplicates.',
            'Exact matches only: no near-duplicate, linguistic similarity, or provider training-data audit. Public retail profiles may have appeared in training; provider training data are unavailable.',
            'Disjoint stores can share products, dates, cities and market conditions; source separation does not establish population independence.'
        ]}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'overlap')
    args = parser.parse_args()
    result = audit()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'overlap.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Post-hoc exact-content and source-split audit', '',
             '| Screen | Development / heldout | Duplicate excess (dev / heldout) | Shared distinct hashes |',
             '| --- | ---: | ---: | ---: |']
    for name, row in result.items():
        if isinstance(row, dict) and 'development_count' in row:
            lines.append(f"| {name} | {row['development_count']} / {row['heldout_count']} | {row['development_duplicate_excess']} / {row['heldout_duplicate_excess']} | {len(row['shared_distinct_hashes'])} |")
    lines += ['', f"Profile source-store overlap: {len(result['profile_source_store_overlap'])}.", '',
              *['- ' + note for note in result['notes']], '',
              'Reproduce offline: `python3 audit_overlap.py --output-dir /tmp/temporal-overlap`.', '']
    (args.output_dir / 'overlap.md').write_text('\n'.join(lines))
    print(json.dumps({'completed': True, 'output_files': ['overlap.json', 'overlap.md']}))


if __name__ == '__main__':
    main()
