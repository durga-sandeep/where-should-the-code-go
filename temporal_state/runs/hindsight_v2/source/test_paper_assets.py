"""Small artificial fixtures test asset wiring only; never final study outputs."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('temporal_paper_assets',Path(__file__).with_name('build_paper.py'))
assets=importlib.util.module_from_spec(spec);spec.loader.exec_module(assets)


def fixture(root):
    configs={c:{'model':c} for c in assets.CONFIGS}
    cells=[dict(configuration=c,arm=a,n=2,successes={m:2 for m in assets.METRICS},
                rates={m:1.0 for m in assets.METRICS},missing_cost_records=0,estimated_cost_usd=.1)
           for c in assets.CONFIGS for a in assets.ARMS]
    pairs=[dict(configuration=c,left='raw',right=a,metric='future_joint',unmatched_left=0,
                unmatched_right=0,matched_bases=1,matched_episodes=2,difference=0.0,ci95=[0.0,0.0])
           for c in assets.CONFIGS for a in ('canonical','snapshot')]
    analysis=dict(complete=True,missing=[],unexpected=[],expected_episodes=24,observed_episodes=24,
                  summary={'estimated_cost_usd':1.2},cells=cells,paired_comparisons=pairs)
    manifest=dict(jobs=24,args={'split':'heldout','configs':list(assets.CONFIGS),'arms':list(assets.ARMS),'reps':2},
                  tasks=[{'base_id':'fixture','initial_stock':1,'target_time':100,'knowledge_cutoff':100,
                          'horizon_time':130,'reports':[],'future_schedule':[]}],configs=configs)
    for name in ('primary','external'):
        d=root/name;d.mkdir();(d/'analysis.json').write_text(json.dumps(analysis));(d/'manifest.json').write_text(json.dumps(manifest))
    diag={name:{'rate':1.0,'bases':1,'episodes':2} for name in ('changed_when_required','both_correct_when_required','answer_invariant','both_correct')}
    studies=[dict(kind=kind,complete=True,cells=[dict(configuration=c,arm='raw',diagnostics=diag,paired_differences=[])
              for c in assets.CONFIGS]) for kind in ('hindsight','display')]
    (root/'comparison.json').write_text(json.dumps({'controls':studies}))
    (root/'build_paper.py').write_text('# isolated fixture source\n')
    (root/'benchmark.py').write_text('# isolated fixture provenance\n')
    return root/'primary',root/'external',root/'comparison.json'


class AssetTests(unittest.TestCase):
    def test_coverage_counts_bases_and_distinct_loss_stages(self):
        t={'base_id':'a','initial_stock':1,'target_time':100,'knowledge_cutoff':100,'horizon_time':130,
           'reports':[{'event_id':'d','revision':1,'event_time':1,'received_time':1,'kind':'demand','quantity':3}],
           'future_schedule':[{'event_id':'f','event_time':110,'kind':'receipt','quantity':2}]}
        u=copy.deepcopy(t);u['base_id']='b';u['reports']=[]
        u['future_schedule']=[{'event_id':'f','event_time':110,'kind':'demand','quantity':3}]
        c=assets.task_coverage([t,u])
        self.assertEqual(c,{'bases':2,'positive_historical_loss':1,'positive_future_loss':1,'positive_terminal_stock':1})
        with self.assertRaisesRegex(ValueError,'Duplicate coverage'):assets.task_coverage([t,t])
    def test_compact_tables_and_named_endpoints(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);primary,_,_=fixture(root)
            text=assets.accuracy_table(assets.load_run(primary))
            self.assertEqual(text.count('100.0 / 100.0'),12)
            self.assertIn('Configuration & Raw & Canonical & Snapshot',text)
            self.assertIn('all-five / future-joint',text)
            self.assertEqual(text.count('Sonnet + thinking'),1)

    def test_complete_build_relative_provenance_and_cis(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);paths=fixture(root);out=root/'smoke-output'
            with patch.object(assets,'ROOT',root),patch.object(assets,'__file__',str(root/'build_paper.py')):
                assets.build(*paths,out)
            result=(out/'results_text.tex').read_text()
            self.assertEqual(result.count('canonical +0.0 [+0.0, +0.0]'),4)
            self.assertEqual(result.count('snapshot +0.0 [+0.0, +0.0]'),4)
            self.assertIn('95\\%',result)
            hashes=json.loads((out/'number_provenance.json').read_text())['inputs']
            self.assertTrue(all(not Path(k).is_absolute() for k in hashes))
            self.assertIn('0/1 bases with positive historical loss',(out/'coverage_text.tex').read_text())

    def test_dev_incomplete_and_stale_paired_stats_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);paths=fixture(root)
            p=paths[0]/'manifest.json';original=json.loads(p.read_text())
            changed=copy.deepcopy(original);changed['args']['split']='dev';p.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'development'):assets.load_run(paths[0])
            p.write_text(json.dumps(original))
            a=paths[0]/'analysis.json';original=json.loads(a.read_text())
            changed=copy.deepcopy(original);changed['complete']=False;a.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'Incomplete'):assets.load_run(paths[0])
            changed=copy.deepcopy(original);changed['paired_comparisons'][0]['difference']=.5;a.write_text(json.dumps(changed))
            out=root/'should-not-exist'
            with self.assertRaisesRegex(ValueError,'difference disagrees'):assets.build(*paths,out)
            self.assertFalse(out.exists())


if __name__=='__main__':unittest.main()
