import copy
import importlib.util
import json
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('temporal_controls',Path(__file__).with_name('compare_controls.py'))
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)


def task():
    return {'base_id':'b0','initial_stock':1,'target_time':100,'knowledge_cutoff':100,'horizon_time':130,
            'reports':[{'event_id':'a','revision':1,'event_time':10,'received_time':10,'kind':'receipt','quantity':2},
                       {'event_id':'b','revision':1,'event_time':20,'received_time':110,'kind':'demand','quantity':4}],
            'future_schedule':[{'event_id':'f','event_time':120,'kind':'demand','quantity':2}]}


def manifest(t):
    return {'args':{'configs':['m'],'arms':['raw'],'reps':1},'tasks':[t]}


def row(t, answer=None):
    answer=c.benchmark.solve(t) if answer is None else answer
    return {'base_id':'b0','configuration':'m','arm':'raw','rep':0,'status':'submitted',
            'answer':answer,'score':c.benchmark.score(t,answer),'cost_usd':.01,
            'request':{'model':'frozen','instructions':'rules','input':[{'role':'user','content':json.dumps(c.expected_input(t,'raw'))}]}}


class ControlTests(unittest.TestCase):
    def test_cutoff_sensitive_pair(self):
        a=task();b=copy.deepcopy(a);b['knowledge_cutoff']=130
        result=c.compare(manifest(a),[row(a)],manifest(b),[row(b)],'hindsight',20)
        self.assertEqual(result['truth_changed_bases'],1)
        d=result['cells'][0]['diagnostics']
        self.assertEqual(d['changed_when_required']['rate'],1)
        self.assertEqual(d['both_correct_when_required']['rate'],1)
        self.assertEqual(d['answer_invariant']['rate'],0)

    def test_display_invariance(self):
        a=task();b=copy.deepcopy(a);b['reports'].reverse()
        result=c.compare(manifest(a),[row(a)],manifest(b),[row(b)],'display',20)
        self.assertEqual(result['truth_changed_bases'],0)
        self.assertEqual(result['cells'][0]['diagnostics']['answer_invariant']['rate'],1)

    def test_reject_unintended_task_change(self):
        a=task();b=copy.deepcopy(a);b['initial_stock']+=1
        with self.assertRaises(ValueError):
            c.compare(manifest(a),[row(a)],manifest(b),[row(b)],'display',20)

    def test_reject_setting_change(self):
        a=task();b=copy.deepcopy(a);b['knowledge_cutoff']=130
        r=row(b);r['request']['model']='other'
        with self.assertRaises(ValueError):
            c.compare(manifest(a),[row(a)],manifest(b),[r],'hindsight',20)

    def test_reject_request_leak(self):
        a=task();r=row(a)
        body=json.loads(r['request']['input'][0]['content']);body['oracle']=c.benchmark.solve(a)
        r['request']['input'][0]['content']=json.dumps(body)
        with self.assertRaises(ValueError):
            c.compare(manifest(a),[row(a)],manifest(a),[r],'display',20)

    def test_invalid_does_not_count_as_invariance(self):
        a=task();r=row(a,{'bad':1})
        result=c.compare(manifest(a),[r],manifest(a),[r],'display',20)
        self.assertEqual(result['cells'][0]['diagnostics']['answer_invariant']['rate'],0)
        self.assertEqual(result['cells'][0]['diagnostics']['both_valid']['rate'],0)

    def test_within_view_repeat_baseline(self):
        t=task();a=row(t);b=copy.deepcopy(a);b['rep']=1
        result=c.within_view_repetitions([a,b],20)
        self.assertEqual(result['paired_bases'],1)
        self.assertEqual(result['diagnostics']['answer_invariant']['rate'],1)
        self.assertEqual(result['diagnostics']['both_correct']['rate'],1)
        b['answer']={**b['answer'],'future_lost':999}
        b['score']=c.benchmark.score(t,b['answer'])
        result=c.within_view_repetitions([a,b],20)
        self.assertEqual(result['diagnostics']['answer_invariant']['rate'],0)
        self.assertEqual(result['diagnostics']['both_correct']['rate'],0)
        self.assertEqual(result['diagnostics']['both_valid']['rate'],1)

    def test_missing_repeat_does_not_invent_pair(self):
        result=c.within_view_repetitions([row(task())],20)
        self.assertEqual(result['paired_bases'],0)
        self.assertIsNone(result['diagnostics']['answer_invariant']['rate'])
        self.assertEqual(result['excluded_bases_missing_r0_or_r1'],['b0'])

    def test_invalid_repeat_not_identical_answer_success(self):
        a=row(task(),{'bad':1});b=copy.deepcopy(a);b['rep']=1
        result=c.within_view_repetitions([a,b],20)
        self.assertEqual(result['diagnostics']['answer_invariant']['rate'],0)

    def test_missing_grid_rejected(self):
        a=task()
        with self.assertRaises(ValueError):
            c.compare(manifest(a),[row(a)],manifest(a),[],'display',20)


if __name__=='__main__':unittest.main()
