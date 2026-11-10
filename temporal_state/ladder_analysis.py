"""Independent analysis of Amendment 4 (protocol_v4_extensions.md). No API calls.

Reuses the extension analysis loaders (every response reparsed, truth recomputed with the
independent auditor's replay, hybrid answers rebuilt, grids and task identity verified) and adds
the prespecified Amendment 4 comparisons:

  E6  interface effect per placement for the closed OpenAI models (automatic minus forced call),
      and the placement decomposition under one interface;
  E7  the same decomposition for Claude Haiku 4.5;
  E8  the open-weight ladder: placement gains under automatic low effort, the effort effect under
      each interface, their difference (the forced-call x effort interaction), and the interface
      effect at each effort.

Whatever subset of the Amendment 4 runs is complete is analysed; every table marks absent cells.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import analyze
import extension_analysis as ea

ROOT = Path(__file__).resolve().parent
SOURCES = ('heldout_v2', 'profiles_v2')
COHORT = ea.COHORT_LABEL
# Runs whose cells participate (original cohorts, every earlier extension, Amendment 4).
RUNS = dict(ea.REQUIRED_STUDIES)
for kind, group in ea.OPTIONAL_STUDIES.items():
    for name, source in group.items():
        RUNS[name] = (kind, source)
AMENDMENT4 = {name for kind in ('auto2', 'haiku', 'open') for name in ea.OPTIONAL_STUDIES[kind]}
FULL_ARMS = ('raw', 'canonical', 'snapshot')
# Ladder rows: (config under automatic tool choice at the lowest requested effort, display label, family)
LADDER = [('mini_low_auto', 'GPT-5.4 mini', 'closed'), ('haiku45', 'Haiku 4.5', 'closed'), ('haiku45_thinking', 'Haiku 4.5 + thinking', 'closed'),
          *[(f'{m}_low_auto', label, 'open') for m, label in ea.OPEN_MODELS],
          ('gpt54_low_auto', 'GPT-5.4', 'closed'), ('sonnet46', 'Sonnet 4.6', 'closed'), ('sonnet46_thinking', 'Sonnet 4.6 + thinking', 'closed')]
# Effort x interface crosses: model key -> {(effort, interface): config}
CROSSES = {'GPT-5.4 mini': {('low', 'forced'): 'mini_low', ('high', 'forced'): 'mini_high', ('low', 'auto'): 'mini_low_auto', ('high', 'auto'): 'mini_high_auto'},
           'GPT-5.4': {('low', 'forced'): 'gpt54_low', ('high', 'forced'): 'gpt54_high', ('low', 'auto'): 'gpt54_low_auto', ('high', 'auto'): 'gpt54_high_auto'},
           **{label: {('low', 'forced'): f'{m}_low', ('high', 'forced'): f'{m}_high', ('low', 'auto'): f'{m}_low_auto', ('high', 'auto'): f'{m}_high_auto'}
              for m, label in ea.OPEN_MODELS}}
ROUTES = {}  # config -> pinned OpenRouter upstream (filled from run.CONFIGS)


def load_all():
    """Load every available run, verify identity and completeness, merge cells per cohort."""
    sources = {name: ea.load_rows(name) for name in SOURCES}
    available = {name: spec for name, spec in RUNS.items() if (ROOT / 'runs' / name / 'analysis.json').exists()}
    loaded = {name: ea.load_rows(name) for name in available}
    for name, (kind, source) in available.items():
        ea.check_task_identity(loaded[name], sources[source])
    merged = {s: dict(sources[s]['rows']) for s in SOURCES}
    for name, (kind, source) in available.items():
        for key, m in loaded[name]['rows'].items():
            if key in merged[source]:
                raise ValueError(f'{name} duplicates a cell already present: {key}')
            merged[source][key] = m
    cells = {}
    for source, rows in merged.items():
        cells[source] = defaultdict(dict)
        for (cfg, arm, _, _) in rows:
            if arm not in cells[source][cfg]:
                cells[source][cfg][arm] = ea.cell(rows, cfg, arm)
    return sources, loaded, available, merged, cells


def transport_summary(available):
    """Retry counts and served-provider agreement for the OpenRouter runs (raw records, not metrics)."""
    import run as runner
    out = {}
    for name in available:
        if name not in AMENDMENT4:
            continue
        attempts = defaultdict(int)
        served_mismatch = 0
        no_completion = 0
        served = defaultdict(int)
        n = 0
        for file in sorted((ROOT / 'runs' / name).glob('*__*.json')):
            row = json.loads(file.read_text())
            n += 1
            attempts[row.get('transport_attempts', 1)] += 1
            cfg = runner.CONFIGS[row['configuration']]
            if cfg['provider'] == 'openrouter':
                response = row.get('response') or {}
                provider = response.get('provider') or ''
                if not provider and not response.get('choices'):
                    no_completion += 1  # accepted request that returned no completion and no provider (a missing answer)
                    continue
                served[provider] += 1
                if provider.lower().replace(' ', '') != cfg['route']:
                    served_mismatch += 1
        out[name] = {'episodes': n, 'transport_attempts': dict(sorted(attempts.items())), 'served_provider_counts': dict(served),
                     'served_provider_mismatches': served_mismatch, 'no_completion_no_provider': no_completion}
    return out


def missing_kind(row):
    """Classify a missing answer from the raw provider response (chat completions and Responses/Anthropic shapes)."""
    r = row.get('response') or {}
    usage = r.get('usage') or {}
    if r.get('status') == 'incomplete' or r.get('stop_reason') == 'max_tokens' or (usage.get('completion_tokens') or usage.get('output_tokens') or 0) >= 16384:
        return 'truncated'  # includes a tool-call argument string cut off at the output limit
    choices = r.get('choices') or []
    if choices:
        ch = choices[0]; m = ch.get('message') or {}
        if ch.get('finish_reason') == 'length':
            return 'truncated'
        if ch.get('finish_reason') == 'error':
            return 'stream_error'
        calls = m.get('tool_calls') or []
        if len(calls) > 1:
            return 'multiple_calls'
        if calls:
            return 'other_tool'
        text = (m.get('content') or '').lower()
        if any(k in text for k in ("sorry", "can't", "cannot", "unable", "i can\u2019t")):
            return 'refusal'
        return 'text_only' if text.strip() else 'empty'
    content = r.get('content') or r.get('output') or []
    return 'text_only' if content else 'empty'


def missing_breakdown(available):
    """Per (cohort, configuration, arm): counts of missing answers by kind, from the stored raw responses."""
    out = defaultdict(lambda: defaultdict(int))
    for name, (kind, source) in available.items():
        for file in sorted((ROOT / 'runs' / name).glob('*__*.json')):
            row = json.loads(file.read_text())
            if row.get('status') == 'missing_answer':
                out[f"{source}/{row['configuration']}/{row['arm']}"][missing_kind(row)] += 1
    return {k: dict(v) for k, v in sorted(out.items())}


def has(cells, source, cfg, arm):
    return arm in cells[source].get(cfg, {})


def pct(c):
    return f"{100 * c['future_joint'] / c['n']:.1f}"


def contrast(rows, plus, minus, metric, draws, seed):
    """Per-history mean of sum(plus cells) - sum(minus cells), matched by (base, rep); bootstrap over histories.

    With plus = [(hi, auto), (lo, forced)] and minus = [(lo, auto), (hi, forced)] this is the
    interaction (auto effort effect minus forced effort effect).
    """
    tables = []
    for key in plus + minus:
        t = {(b, r): int(m[metric]) for (c, a, b, r), m in rows.items() if (c, a) == key}
        if not t:
            raise KeyError(key)
        tables.append(t)
    idx = set(tables[0])
    if any(set(t) != idx for t in tables):
        raise ValueError('Unmatched cells in contrast')
    groups = defaultdict(list)
    for k in sorted(idx):
        groups[k[0]].append(sum(t[k] for t in tables[:len(plus)]) - sum(t[k] for t in tables[len(plus):]))
    diffs = [sum(v) / len(v) for _, v in sorted(groups.items())]
    return {'metric': metric, 'plus': [list(k) for k in plus], 'minus': [list(k) for k in minus], 'bases': len(diffs),
            'difference': sum(diffs) / len(diffs), 'ci95': analyze.bootstrap(diffs, draws, seed)}


def paired(rows, left, right, metric, draws, seed):
    return ea.paired(rows, left, rows, right, metric, draws, seed)


def fmt(c):
    lo, hi = c['ci95']
    return f"{100 * c['difference']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


def compute_comparisons(merged, cells, draws, seed):
    out = {s: {'interface': [], 'placement_auto': [], 'effort_by_interface': [], 'interaction': []} for s in SOURCES}
    for s in SOURCES:
        rows = merged[s]
        # Placement decomposition under automatic choice for every ladder row present.
        for cfg, label, _ in LADDER:
            if not has(cells, s, cfg, 'raw'):
                continue
            for metric in ('future_joint', 'stock_exact'):
                for arm in ('canonical', 'snapshot'):
                    if has(cells, s, cfg, arm):
                        out[s]['placement_auto'].append({'model': label, **paired(rows, (cfg, 'raw'), (cfg, arm), metric, draws, seed)})
                if has(cells, s, cfg, 'snapshot') and has(cells, s, cfg, 'canonical'):
                    out[s]['placement_auto'].append({'model': label, **paired(rows, (cfg, 'canonical'), (cfg, 'snapshot'), metric, draws, seed)})
                for arm in ('raw', 'canonical'):
                    if has(cells, s, cfg, 'state_' + arm) and has(cells, s, cfg, arm):
                        out[s]['placement_auto'].append({'model': label, **paired(rows, (cfg, arm), (cfg, 'state_' + arm), metric, draws, seed)})
        # Effort x interface crosses.
        for model, cross in CROSSES.items():
            for arm in ('raw', 'canonical'):
                present = {k: cfg for k, cfg in cross.items() if has(cells, s, cfg, arm)}
                for metric in ('future_joint', 'stock_exact'):
                    for effort in ('low', 'high'):
                        if (effort, 'forced') in present and (effort, 'auto') in present:
                            out[s]['interface'].append({'model': model, 'effort': effort, 'arm': arm,
                                                        **paired(rows, (present[(effort, 'forced')], arm), (present[(effort, 'auto')], arm), metric, draws, seed)})
                    for interface in ('forced', 'auto'):
                        if ('low', interface) in present and ('high', interface) in present:
                            out[s]['effort_by_interface'].append({'model': model, 'interface': interface, 'arm': arm,
                                                                  **paired(rows, (present[('low', interface)], arm), (present[('high', interface)], arm), metric, draws, seed)})
                    if len(present) == 4:
                        out[s]['interaction'].append({'model': model, 'arm': arm, **contrast(
                            rows, [(present[('high', 'auto')], arm), (present[('low', 'forced')], arm)],
                            [(present[('low', 'auto')], arm), (present[('high', 'forced')], arm)], metric, draws, seed)})
    return out


GPT54_REPLICATION = 'replication_gpt54_low_synthetic_v1'  # E6b addendum: same-period forced-call baseline, not merged into cells


def gpt54_replication(sources, merged, draws, seed):
    """E6b: drift (replication minus original forced cell) and interface effect against the contemporaneous baseline."""
    if not (ROOT / 'runs' / GPT54_REPLICATION / 'analysis.json').exists():
        return None
    rep = ea.load_rows(GPT54_REPLICATION)
    ea.check_task_identity(rep, sources['heldout_v2'])
    out = {'run': GPT54_REPLICATION, 'episodes': rep['episodes'], 'problems': rep['problems'], 'cells': {}, 'drift': {}, 'interface_vs_replication': {},
           'provenance': {'manifest_sha256': rep['manifest_sha256'], 'episode_hashes_digest': rep['episode_hashes_digest']}}
    for arm in ('snapshot', 'state_canonical'):
        orig = ea.cell(merged['heldout_v2'], 'gpt54_low', arm)  # state arms live in the extension runs, so use the merged cohort
        new = ea.cell(rep['rows'], 'gpt54_low', arm)
        auto = ea.cell(merged['heldout_v2'], 'gpt54_low_auto', arm)
        out['cells'][arm] = {'original': pct(orig), 'replication': pct(new), 'auto': pct(auto),
                             'original_wrong': orig['n'] - orig['future_joint'], 'replication_wrong': new['n'] - new['future_joint'], 'auto_wrong': auto['n'] - auto['future_joint']}
        for metric in ('future_joint', 'stock_exact'):
            out['drift'][f'{arm}/{metric}'] = ea.paired(merged['heldout_v2'], ('gpt54_low', arm), rep['rows'], ('gpt54_low', arm), metric, draws, seed)
            out['interface_vs_replication'][f'{arm}/{metric}'] = ea.paired(rep['rows'], ('gpt54_low', arm), merged['heldout_v2'], ('gpt54_low_auto', arm), metric, draws, seed)
    return out


def find(items, **where):
    for it in items:
        if all(it.get(k) == v for k, v in where.items()):
            return it
    return None


# ---------------------------------------------------------------- manuscript fragments

def ladder_table(cells):
    """Main table candidate: every model under automatic tool choice at its lowest requested effort."""
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\setlength{\\tabcolsep}{3.5pt}',
             '\\begin{tabular}{lrrrrrrr}', '\\toprule',
             ' & \\multicolumn{4}{c}{Synthetic} & \\multicolumn{3}{c}{Retail profiles} \\\\',
             '\\cmidrule(lr){2-5}\\cmidrule(lr){6-8}',
             'Model (automatic tool choice) & raw & canonical & hybrid & snapshot & raw & canonical & snapshot \\\\', '\\midrule']
    def v(source, cfg, arm):
        c = cells[source].get(cfg, {}).get(arm)
        return pct(c) if c else '--'
    for cfg, label, family in LADDER:
        if not any(has(cells, s, cfg, 'raw') for s in SOURCES):
            continue
        tag = '$^\\dagger$' if family == 'open' else ''
        lines.append(' & '.join([label + tag, v('heldout_v2', cfg, 'raw'), v('heldout_v2', cfg, 'canonical'), v('heldout_v2', cfg, 'state_canonical'), v('heldout_v2', cfg, 'snapshot'),
                                 v('profiles_v2', cfg, 'raw'), v('profiles_v2', cfg, 'canonical'), v('profiles_v2', cfg, 'snapshot')]) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Future-joint accuracy (\\%, all three scenario outputs exact) by input and code placement, every configuration under automatic tool choice at its lowest requested effort '
              '(OpenAI and open-weight models: requested effort low; Anthropic models: no or 4,096-token thinking); 192 synthetic and 96 profile calls per cell; invalid and missing answers fail. '
              '\\emph{raw}: model selects, replays and rolls out; \\emph{canonical}: code selects and orders eligible events; \\emph{hybrid}: model returns the two historical fields from canonical input and code applies the schedule (equals reconstruction accuracy by conservation); '
              '\\emph{snapshot}: exact state supplied, model rolls out. $^\\dagger$Open-weight models through OpenRouter, each pinned to one upstream provider (Appendix~\\ref{app:ladder}). Forced-call cells and all-five accuracy: Appendix~\\ref{app:tables}.}',
              '\\label{tab:ladder}', '\\end{table}', '']
    return '\n'.join(lines)


def interaction_table(cells, comparisons, source='heldout_v2', arm='canonical'):
    """Requested effort x tool-choice interface, one row per model that has all four cells."""
    lines = ['\\begin{table}[t]', '\\centering\\footnotesize', '\\setlength{\\tabcolsep}{3.5pt}',
             '\\begin{tabular}{lrrrrrrr}', '\\toprule',
             ' & \\multicolumn{3}{c}{Forced answer call} & \\multicolumn{3}{c}{Automatic tool choice} & \\\\',
             '\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}',
             'Model & low & high & high$-$low & low & high & high$-$low & Interaction \\\\', '\\midrule']
    n_rows = 0
    for model, cross in CROSSES.items():
        inter = find(comparisons[source]['interaction'], model=model, arm=arm, metric='future_joint')
        if inter is None:
            continue
        ef = find(comparisons[source]['effort_by_interface'], model=model, interface='forced', arm=arm, metric='future_joint')
        ea_ = find(comparisons[source]['effort_by_interface'], model=model, interface='auto', arm=arm, metric='future_joint')
        c = lambda e, i: pct(cells[source][cross[(e, i)]][arm])
        lines.append(' & '.join([model, c('low', 'forced'), c('high', 'forced'), f"{100 * ef['difference']:+.1f}",
                                 c('low', 'auto'), c('high', 'auto'), f"{100 * ea_['difference']:+.1f}", fmt(inter)]) + ' \\\\')
        n_rows += 1
    if not n_rows:
        return ''
    lines += ['\\bottomrule', '\\end{tabular}',
              f'\\caption{{Requested reasoning effort $\\times$ tool-choice interface, {COHORT[source].lower()} cohort, {arm} input, future-joint accuracy (\\%; 192 calls per cell). '
              'high$-$low: paired effort effect within an interface. Interaction: automatic-choice effort effect minus forced-call effort effect, paired by history, with a descriptive 95\\% history-bootstrap interval (10,000 draws); '
              'a positive interaction means the forced call turns extra effort into a liability. Requested effort is a family-specific provider setting, not a compute match (observed reasoning tokens: Appendix~\\ref{app:ladder}).}',
              f'\\label{{tab:interaction_{arm}}}', '\\end{table}', '']
    return '\n'.join(lines)


def appendix_ladder(cells, comparisons, transport, replication54=None, missing=None):
    """Appendix: forced-call ladder cells, reasoning tokens, missing/truncated counts, interface effects, transport."""
    parts = []
    # Reasoning tokens, missing and truncated per open-weight cell (synthetic), plus interface effects.
    lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\setlength{\\tabcolsep}{3pt}',
             '\\begin{tabular}{llrrrrrr}', '\\toprule',
             'Model & Configuration & Arm & Future joint & Missing & Truncated & Mean reasoning tok. & Retried calls \\\\', '\\midrule']
    for model, cross in CROSSES.items():
        first = True
        for (effort, interface), cfg in cross.items():
            for arm in ('raw', 'canonical'):
                c = cells['heldout_v2'].get(cfg, {}).get(arm)
                if not c:
                    continue
                rt = f"{c['mean_reasoning_tokens']:.0f}" if c['mean_reasoning_tokens'] is not None else 'n/a'
                lines.append(' & '.join([model if first else '', f'{effort}, {interface}', arm, pct(c), str(c['missing']), str(c['truncated']), rt, '']) + ' \\\\')
                first = False
        lines.append('\\midrule')
    lines = lines[:-1]
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Effort $\\times$ interface cells on the synthetic cohort (192 calls each): future-joint accuracy (\\%), calls with no answer (including refusals), calls truncated at the 16,384-token output limit, and mean provider-reported reasoning tokens. '
              'Each upstream maps the unified effort parameter onto its own control, so effort levels are comparable within a model family only.}',
              '\\label{tab:ladder_cells}', '\\end{table}', '']
    parts.append('\n'.join(lines))
    # Missing-answer breakdown table (cells with at least one missing answer).
    if missing:
        kinds = ('refusal', 'text_only', 'other_tool', 'multiple_calls', 'stream_error', 'truncated', 'empty')
        lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\setlength{\\tabcolsep}{2pt}', '\\resizebox{\\textwidth}{!}{%', '\\begin{tabular}{lll' + 'r' * len(kinds) + '}', '\\toprule',
                 'Cohort & Configuration & Arm & ' + ' & '.join(k.replace('_', ' ') for k in kinds) + ' \\\\', '\\midrule']
        for key, counts in missing.items():
            source, cfg, arm = key.split('/')
            if sum(counts.values()) < 3:
                continue
            lines.append(' & '.join([COHORT[source], ea.LABELS.get(cfg, cfg), arm.replace('_', '-'), *[str(counts.get(k, 0)) for k in kinds]]) + ' \\\\')
        lines += ['\\bottomrule', '\\end{tabular}}',
                  '\\caption{Missing answers by kind for every cell with at least three (all counted as failures in every accuracy): \\emph{refusal}, a text reply declining the task; \\emph{text only}, an answer written in the message instead of the tool call; '
                  '\\emph{other tool} and \\emph{multiple calls}, calls to a non-existent tool or more than one call; \\emph{stream error}, a provider-side error after the request was accepted; \\emph{truncated}, the 16,384-token output limit reached (for Anthropic thinking runs, entirely in thinking); \\emph{empty}, no content.}',
                  '\\label{tab:missing}', '\\end{table}', '']
        parts.append('\n'.join(lines))
    # Interface effects table.
    lines = ['\\begin{table}[htbp]', '\\centering\\scriptsize', '\\setlength{\\tabcolsep}{3pt}', '\\begin{tabular}{lllrr}', '\\toprule',
             'Cohort & Model, effort & Arm & Automatic $-$ forced (future joint) & Automatic $-$ forced (stock exact) \\\\', '\\midrule']
    for s in SOURCES:
        for it in comparisons[s]['interface']:
            if it['metric'] != 'future_joint':
                continue
            st = find(comparisons[s]['interface'], model=it['model'], effort=it['effort'], arm=it['arm'], metric='stock_exact')
            lines.append(' & '.join([COHORT[s], f"{it['model']}, {it['effort']}", it['arm'], fmt(it), fmt(st) if st else '--']) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}',
              '\\caption{Interface effect: automatic tool choice minus forced answer call at fixed model, effort, input and history; paired differences in percentage points with descriptive 95\\% history-bootstrap intervals.}',
              '\\label{tab:interface}', '\\end{table}', '']
    parts.append('\n'.join(lines))
    # E6b replication paragraph.
    if replication54:
        r = replication54
        cells_txt = '; '.join(f"{arm.replace('_', '-')}: original {r['cells'][arm]['original']}, same-period replication {r['cells'][arm]['replication']}, automatic choice {r['cells'][arm]['auto']}\\%" for arm in ('snapshot', 'state_canonical'))
        drift = '; '.join(f"{k.split('/')[0].replace('_', '-')} {fmt(v)}" for k, v in r['drift'].items() if k.endswith('future_joint'))
        iface = '; '.join(f"{k.split('/')[0].replace('_', '-')} {fmt(v)}" for k, v in r['interface_vs_replication'].items() if k.endswith('future_joint'))
        parts.insert(0, (f"\paragraph{{Same-period GPT-5.4 forced-call replication (E6b).}} Future-joint accuracy on synthetic histories, {cells_txt}. "
                         f"Paired drift, replication minus original forced cell: {drift}. Interface effect against the contemporaneous baseline, automatic minus replicated forced call: {iface}.\n\n"))
    # Transport paragraph.
    if transport:
        retried = sum(sum(v for k, v in t['transport_attempts'].items() if k != 1) for t in transport.values())
        total = sum(t['episodes'] for t in transport.values())
        mism = sum(t['served_provider_mismatches'] for t in transport.values())
        parts.insert(0, (f"\\paragraph{{Transport.}} Of the {total:,} Amendment~4 calls, {retried} needed a bounded transport retry (HTTP 429/5xx before any completion existed; attempt counts are stored per record and no model output was re-sampled), "
                         f"and {mism} open-weight calls were served by a provider other than the pinned one. Requested effort for the open-weight models is OpenRouter's unified \\texttt{{reasoning.effort}}, which each upstream maps onto its own control.\n\n"))
    return '\n'.join(parts)


def _c(cells, source, cfg, arm):
    return cells[source][cfg][arm]


def _pair(comparisons, source, model, left_arm, right_arm, metric='future_joint'):
    for it in comparisons[source]['placement_auto']:
        if it['model'] == model and it['left'][1] == left_arm and it['right'][1] == right_arm and it['metric'] == metric:
            return it
    raise KeyError((model, left_arm, right_arm))


def placement_findings(cells, comparisons):
    """Results paragraph on code before the model, one interface, across the ladder (synthetic cohort)."""
    s = 'heldout_v2'
    weak = [(cfg, label) for cfg, label, _ in LADDER if has(cells, s, cfg, 'raw') and _c(cells, s, cfg, 'raw')['future_joint'] / 192 < 0.9]
    strong = [(cfg, label) for cfg, label, _ in LADDER if has(cells, s, cfg, 'raw') and _c(cells, s, cfg, 'raw')['future_joint'] / 192 >= 0.9]
    def g(label, l, r):
        return fmt(_pair(comparisons, s, label, l, r))
    def v(cfg, arm):
        return pct(_c(cells, s, cfg, arm))
    short = {'GPT-5.4 mini': 'mini', 'Haiku 4.5': 'Haiku', 'Haiku 4.5 + thinking': 'Haiku+thinking', 'gpt-oss-20b': 'gpt-oss-20b', 'gpt-oss-120b': 'gpt-oss-120b', 'GLM-5.3 Flash': 'GLM'}
    gains = '; '.join(f"{short.get(l, l)} {g(l, 'raw', 'canonical')}" for _, l in weak if l != 'GLM-5.3 Flash')
    resid = ', '.join(f"{short.get(l, l)} {v(c, 'snapshot')}" for c, l in weak)
    text = (f"Table~\\ref{{tab:ladder}} reports every configuration under one interface; {len(weak)} of {len(weak) + len(strong)} start below 90\\% on raw reports and the rest are near ceiling there, so placement is a question about weak components. "
            f"For the weak ones, canonical input raises future-joint accuracy by {gains}. "
            f"Exact state does not make them exact: with only the 12-event rollout left, every weak model stays below 100\\% on snapshot input (Table~\\ref{{tab:ladder}}). ")
    glm = 'GLM-5.3 Flash'
    if any(l == glm for _, l in weak):
        text += (f"The decomposition also locates different errors in different models. For GLM canonical input adds {g(glm, 'raw', 'canonical')} and exact state adds nothing over it ({g(glm, 'canonical', 'snapshot')}), yet code after the model on the same canonical answers adds {g(glm, 'canonical', 'state_canonical')}: its error is almost entirely rollout. "
                 f"For gpt-oss-20b both stages fail ({g('gpt-oss-20b', 'raw', 'canonical')} from canonical input, {g('gpt-oss-20b', 'canonical', 'snapshot')} more from exact state). ")
    return text + '\n'


def after_findings(cells, comparisons):
    s = 'heldout_v2'
    weak = [(cfg, label) for cfg, label, _ in LADDER if has(cells, s, cfg, 'state_canonical') and _c(cells, s, cfg, 'raw')['future_joint'] / 192 < 0.9 and label != 'Haiku 4.5 + thinking']
    short = {'GPT-5.4 mini': 'mini', 'Haiku 4.5': 'Haiku', 'gpt-oss-20b': 'gpt-oss-20b', 'gpt-oss-120b': 'gpt-oss-120b', 'GLM-5.3 Flash': 'GLM'}
    def g(label, l, r):
        return fmt(_pair(comparisons, s, label, l, r))
    canon = '; '.join(f"{short.get(l, l)} {g(l, 'canonical', 'state_canonical')}" for _, l in weak)
    raw_max = max((_c(cells, s, c, 'state_raw')['future_joint'] / 192 for c, _ in weak), default=0)
    return (f"Run prospectively, the state-only hybrid's gain over the model's own rollout on canonical input is {canon}. "
            f"On raw input the hybrid never exceeds {100 * raw_max:.0f}\\% for a weak model: code after the model removes rollout error wherever the reconstruction was right and cannot repair a stock that is wrong because the wrong reports were selected.\n")


def interface_findings(cells, comparisons, replication54=None):
    """Effort x interface paragraph across the ladder (synthetic cohort)."""
    s = 'heldout_v2'
    def inter(model, arm='canonical'):
        return find(comparisons[s]['interaction'], model=model, arm=arm, metric='future_joint')
    def iface(model, effort, arm):
        return find(comparisons[s]['interface'], model=model, effort=effort, arm=arm, metric='future_joint')
    def eff(model, interface, arm):
        return find(comparisons[s]['effort_by_interface'], model=model, interface=interface, arm=arm, metric='future_joint')
    def v(cfg, arm):
        return pct(_c(cells, s, cfg, arm))
    def tok(cfg, arm):
        return f"{_c(cells, s, cfg, arm)['mean_reasoning_tokens']:.0f}"
    text = []
    # DeepSeek Flash: forced call suppresses reasoning
    if inter('DeepSeek V4 Flash'):
        text.append(f"Table~\\ref{{tab:interaction_canonical}} crosses requested effort with the tool-calling interface. For DeepSeek V4 Flash on its provider the forced call effectively disabled reasoning: forced canonical calls averaged {tok('dsflash_low', 'canonical')} reasoning tokens against {tok('dsflash_low_auto', 'canonical')} under automatic choice, and accuracy is {v('dsflash_low', 'canonical')} against {v('dsflash_low_auto', 'canonical')}\\%; effort changes nothing under either interface. ")
    # mini and dspro interaction
    m = inter('GPT-5.4 mini'); dp = inter('DeepSeek V4 Pro')
    if m and dp:
        text.append(f"For GPT-5.4 mini and for DeepSeek V4 Pro on its provider the forced call interacts with effort: mini's high-minus-low effect on canonical input is {fmt(eff('GPT-5.4 mini', 'forced', 'canonical'))} under the forced call and {fmt(eff('GPT-5.4 mini', 'auto', 'canonical'))} under automatic choice, and DeepSeek V4 Pro falls from {v('dspro_low', 'canonical')} to {v('dspro_high', 'canonical')}\\% under the forced call at high effort ({_c(cells, s, 'dspro_high', 'canonical')['missing']} of 192 calls with no answer) while staying at {v('dspro_high_auto', 'canonical')}\\% under automatic choice. ")
    g54 = inter('GPT-5.4')
    if g54:
        text.append(f"GPT-5.4 shows a small interaction of the same sign ({fmt(g54)}). ")
    # no interaction models
    others = [(mdl, inter(mdl)) for mdl in ('gpt-oss-20b', 'gpt-oss-120b', 'Qwen3.8-27B', 'GLM-5.3 Flash') if inter(mdl)]
    if others:
        names = [mdl for mdl, _ in others]
        text.append("For " + (', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else names[0]) + " the interaction interval covers zero: effort acts the same way under both interfaces. ")
    # truncation
    o120 = _c(cells, s, 'oss120b_high', 'canonical'); o120a = _c(cells, s, 'oss120b_high_auto', 'raw'); o20a = _c(cells, s, 'oss20b_high_auto', 'raw')
    text.append(f"A third failure of \\emph{{reason harder}} is budget exhaustion: at high effort gpt-oss-120b spent the whole 16,384-token output limit on reasoning in {o120['truncated']} of 192 forced canonical calls and gpt-oss-20b in {o20a['truncated']} of 192 automatic raw calls, each a missing answer. ")
    # refusals
    text.append(f"gpt-oss-20b also refused the fictional task ({_c(cells, s, 'oss20b_low_auto', 'raw')['missing']} of 192 low-effort raw calls had no answer, mostly refusals), so its cells measure willingness as much as ability. "
                "Reasoning tokens and missing answers for every cell: Appendix~\\ref{app:ladder}.")
    return ''.join(text) + '\n'


MACRO_KEYS = {'oss20b': 'OssTwenty', 'oss120b': 'OssHundredTwenty', 'qwen27b': 'Qwen', 'dsflash': 'DsFlash', 'glmflash': 'GlmFlash', 'dspro': 'DsPro'}


def numbers(cells, comparisons, replication54=None, loaded=None):
    s, p = SOURCES
    macros = {}
    if replication54:
        r = replication54
        macros['GptReplicationSentence'] = ('a same-period forced-call replication of those two arms (Appendix~\\ref{app:ladder}) moved them by '
                                            + ' and '.join(f"{100 * r['drift'][f'{arm}/future_joint']['difference']:+.1f}" for arm in ('snapshot', 'state_canonical'))
                                            + ' points relative to the original cells, so the automatic-choice difference against the contemporaneous baseline is '
                                            + ' and '.join(f"{100 * r['interface_vs_replication'][f'{arm}/future_joint']['difference']:+.1f}" for arm in ('snapshot', 'state_canonical'))
                                            + ' points.')
    else:
        macros['GptReplicationSentence'] = 'a same-period forced-call replication of those two arms is reported in Appendix~\\ref{app:ladder}.'
    def cell_pct(source, cfg, arm):
        c = cells[source].get(cfg, {}).get(arm)
        return pct(c) if c else None
    for name, cfg in (('MiniAuto', 'mini_low_auto'), ('GptAuto', 'gpt54_low_auto'), ('Haiku', 'haiku45'), ('HaikuThink', 'haiku45_thinking'),
                      *[(MACRO_KEYS[m], f'{m}_low_auto') for m, _ in ea.OPEN_MODELS]):
        for arm, tag in (('raw', 'Raw'), ('canonical', 'Canon'), ('snapshot', 'Snap'), ('state_canonical', 'Hybrid'), ('state_raw', 'HybridRaw')):
            for source, st in ((s, 'Syn'), (p, 'Pro')):
                v = cell_pct(source, cfg, arm)
                if v is not None:
                    macros[f'ladder{name}{tag}{st}'] = v
    n_inter_pos = n_inter = 0
    for it in comparisons[s]['interaction']:
        if it['metric'] == 'future_joint' and it['arm'] == 'canonical':
            n_inter += 1
            n_inter_pos += it['ci95'][0] > 0
    macros['InteractionModels'] = str(n_inter)
    macros['InteractionPositive'] = str(n_inter_pos)
    macros['LadderRequests'] = f"{sum(c['n'] for src in SOURCES for cfg in cells[src] for arm, c in cells[src][cfg].items() if cfg in ea.OPEN_CONFIGS or cfg in ('haiku45', 'haiku45_thinking', 'gpt54_low_auto', 'gpt54_high_auto')):,}"
    # Every request in the manuscript: all merged cells (originals plus every extension and Amendment 4 run) plus the two
    # same-period replications, which are kept out of the cells. Overrides the extension-analysis macro, which predates E6b.
    total = 4224 + sum(loaded[n]['episodes'] for n in loaded)  # original grid with its controls, plus every extension run
    for rep in (ea.REPLICATION, GPT54_REPLICATION):
        path = ROOT / 'runs' / rep / 'analysis.json'
        if path.exists():
            total += json.loads(path.read_text())['observed_episodes']
    text = '\n'.join('\\newcommand{\\' + k + '}{' + v + '}' for k, v in macros.items()) + '\n'
    return text + '\\renewcommand{\\TotalRequests}{' + f'{total:,}' + '}\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'audits' / 'ladder')
    parser.add_argument('--paper-dir', type=Path, default=ROOT / 'paper')
    parser.add_argument('--bootstrap', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=20260908)
    a = parser.parse_args()
    sources, loaded, available, merged, cells = load_all()
    comparisons = compute_comparisons(merged, cells, a.bootstrap, a.seed)
    transport = transport_summary(available)
    replication54 = gpt54_replication(sources, merged, a.bootstrap, a.seed)
    missing = missing_breakdown({**available, 'heldout_v2': ('source', 'heldout_v2'), 'profiles_v2': ('source', 'profiles_v2')})
    result = {'gpt54_replication': replication54, 'missing_breakdown': missing,'analysis': 'amendment_4_ladder', 'protocol': 'protocol_v4_extensions.md', 'bootstrap_draws': a.bootstrap, 'seed': a.seed,
              'runs_analysed': sorted(available), 'amendment4_runs_present': sorted(n for n in available if n in AMENDMENT4),
              'amendment4_runs_absent': sorted(n for n in AMENDMENT4 if n not in available),
              'episodes': {n: loaded[n]['episodes'] for n in available},
              'audit_problems': {n: loaded[n]['problems'] for n in available},
              'provenance': {n: {'manifest_sha256': x['manifest_sha256'], 'episode_hashes_digest': x['episode_hashes_digest']} for n, x in {**sources, **loaded}.items()},
              'transport': transport,
              'cells': {s: {c: dict(v) for c, v in cells[s].items()} for s in cells},
              'comparisons': comparisons,
              'notes': ['Every response reparsed; truth recomputed with the independent auditor replay; hybrid answers rebuilt with a separate scenario simulator.',
                        'Open-weight models are served through OpenRouter with one pinned upstream per model; the served provider is recorded per call.',
                        'Requested effort is a family-specific provider setting; observed reasoning tokens are reported next to every effort comparison.',
                        'Interaction = (auto high - auto low) - (forced high - forced low), paired by history; positive means the forced call penalizes extra effort.',
                        'All configurations, arms, invalid answers, refusals and truncations are retained; transport retries never re-sample a model output.']}
    result['audit_passed'] = (not any(loaded[n]['problems'] for n in available) and not any(sources[n]['problems'] for n in sources)
                              and not (replication54 and replication54['problems']))
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / 'ladder.json').write_text(json.dumps(result, indent=2) + '\n')
    md = ['# Amendment 4: independent analysis', '', *['- ' + n for n in result['notes']], '',
          f"Audit passed: {result['audit_passed']}; runs present: {result['amendment4_runs_present']}; absent: {result['amendment4_runs_absent']}", '',
          '| Cohort | Configuration | Arm | N | Missing | Truncated | Future joint | Stock exact | Mean reasoning tok. | Cost USD |', '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for s in SOURCES:
        for cfg in sorted(cells[s]):
            for arm, c in sorted(cells[s][cfg].items()):
                rt = f"{c['mean_reasoning_tokens']:.0f}" if c['mean_reasoning_tokens'] is not None else 'n/a'
                md.append(f"| {s} | {cfg} | {arm} | {c['n']} | {c['missing']} | {c['truncated']} | {pct(c)} | {100*c['stock_exact']/c['n']:.1f} | {rt} | {c['cost_usd']:.2f} |")
    md += ['', '| Cohort | Kind | Model | Detail | Metric | Difference [95% CI], pp |', '| --- | --- | --- | --- | --- | --- |']
    for s in SOURCES:
        for kind, items in comparisons[s].items():
            for it in items:
                detail = ' '.join(str(it.get(k)) for k in ('effort', 'interface', 'arm') if it.get(k)) or f"{it.get('left', ['', ''])[1]}->{it.get('right', ['', ''])[1]}"
                md.append(f"| {s} | {kind} | {it.get('model')} | {detail} | {it['metric']} | {fmt(it)} |")
    md += ['', '## Transport', '', json.dumps(transport, indent=2)]
    (a.output_dir / 'ladder.md').write_text('\n'.join(md) + '\n')
    a.paper_dir.mkdir(parents=True, exist_ok=True)
    (a.paper_dir / 'ladder_table.tex').write_text(ladder_table(cells))
    (a.paper_dir / 'interaction_table.tex').write_text(interaction_table(cells, comparisons))
    (a.paper_dir / 'interaction_raw_table.tex').write_text(interaction_table(cells, comparisons, arm='raw'))
    (a.paper_dir / 'ladder_appendix.tex').write_text(appendix_ladder(cells, comparisons, transport, replication54, missing))
    (a.paper_dir / 'ladder_numbers.tex').write_text(numbers(cells, comparisons, replication54, loaded))
    (a.paper_dir / 'ladder_placement_findings.tex').write_text(placement_findings(cells, comparisons))
    (a.paper_dir / 'ladder_after_findings.tex').write_text(after_findings(cells, comparisons))
    (a.paper_dir / 'ladder_interface_findings.tex').write_text(interface_findings(cells, comparisons, replication54))
    print(json.dumps({'audit_passed': result['audit_passed'], 'present': result['amendment4_runs_present'], 'absent': result['amendment4_runs_absent']}))


if __name__ == '__main__':
    main()
