import importlib.util
from pathlib import Path
import unittest
import tempfile
import json

spec=importlib.util.spec_from_file_location('diagnostic_paper',Path(__file__).with_name('diagnostic_paper.py'))
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)

class DiagnosticPaperTests(unittest.TestCase):
    def test_truncation_semantics(self):
        self.assertTrue(d.truncated({'response':{'stop_reason':'max_tokens'}}))
        self.assertTrue(d.truncated({'response':{'incomplete_details':{'reason':'max_output_tokens'}}}))
        self.assertFalse(d.truncated({'response':{'incomplete_details':{'reason':'content_filter'}}}))
        self.assertFalse(d.truncated({}))

    def test_fragment_denominators_and_caveat(self):
        cell={'configuration':'mini_low','arm':'raw','n':10,'valid':8,'invalid':2,
              'categories':dict(zip(d.CATEGORIES,(2,1,3,1,1))),
              'historical_lost_wrong_with_correct_stock':1,'output_limit_truncated':1,
              'invalid_and_output_limit_truncated':1}
        text,table=d.fragments([{'name':'heldout_v2','episodes':10,'cells':{('mini_low','raw'):cell}}])
        self.assertIn('3/4 valid outputs',text)
        self.assertIn('2/10 contracts are invalid',text)
        self.assertIn('1 responses hit',text)
        self.assertIn('not that the model internally used',text)
        self.assertIn('\\begin{table}',table)

    def test_incomplete_result_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            (path/'manifest.json').write_text(json.dumps({}))
            with self.assertRaisesRegex(ValueError,'Incomplete'):
                d.verify({'complete':False},path)

    def test_stale_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            (path/'manifest.json').write_text(json.dumps({}))
            with self.assertRaisesRegex(ValueError,'hash'):
                d.verify({'complete':True,'provenance':{'manifest_sha256':'bad'}},path)

    def test_main_requires_final_cohorts(self):
        with self.assertRaisesRegex(ValueError,'four final'):
            d.main_fragment([])

    def test_main_totals_and_length(self):
        cell={'configuration':'mini_low','arm':'raw','n':10,'valid':8,'invalid':2,
              'categories':dict(zip(d.CATEGORIES,(2,1,3,1,1))),
              'historical_lost_wrong_with_correct_stock':1,'output_limit_truncated':1,
              'invalid_and_output_limit_truncated':1}
        studies=[{'name':name,'episodes':n,'cells':{('mini_low','raw'):cell}}
                 for name,n in [('heldout_v2',2304),('hindsight_v2',576),('display_v2',192),('profiles_v2',1152)]]
        text=d.main_fragment(studies)
        self.assertIn('4224 requests',text)
        self.assertIn('invalid contracts total 8',text)
        self.assertIn('4 responses',text)
        self.assertGreaterEqual(len(text.split()),90)
        self.assertLessEqual(len(text.split()),120)

    def test_no_diagnostic_arm_rejected(self):
        with self.assertRaises(ValueError):d.fragments([{'name':'x','episodes':0,'cells':{}}])

if __name__=='__main__':unittest.main()
