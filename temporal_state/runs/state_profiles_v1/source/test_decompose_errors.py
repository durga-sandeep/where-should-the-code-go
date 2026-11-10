import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('decomposition',Path(__file__).with_name('decompose_errors.py'))
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)


def task():
    return {'initial_stock':5,'target_time':100,'knowledge_cutoff':100,'horizon_time':130,'reports':[],
            'future_schedule':[{'event_id':'f','event_time':110,'kind':'demand','quantity':7}]}


class DecompositionTests(unittest.TestCase):
    def test_all_five_categories(self):
        t=task();truth=d.audit.replay(t)[0]
        variants=[(truth,'stock_correct_future_correct'),
                  ({**truth,'future_lost':3},'stock_correct_future_wrong'),
                  ({**truth,'stock_at_target':4,**d.future_from_stock(t,4)},'stock_wrong_future_wrong_consistent'),
                  ({**truth,'stock_at_target':4,'future_lost':9},'stock_wrong_future_wrong_inconsistent'),
                  ({**truth,'stock_at_target':4},'stock_wrong_future_correct')]
        for answer,category in variants:self.assertEqual(d.classify(t,answer)['category'],category)

    def test_history_loss_is_separate(self):
        t=task();answer={**d.audit.replay(t)[0],'historical_lost':9}
        result=d.classify(t,answer)
        self.assertEqual(result['category'],'stock_correct_future_correct')
        self.assertFalse(result['historical_lost_correct'])

    def test_strict_invalid_and_no_loss_zero_stock(self):
        t=task();truth=d.audit.replay(t)[0]
        self.assertFalse(d.classify(t,{**truth,'future_lost':True})['valid'])
        self.assertEqual(d.future_from_stock(t,7),{'stock_at_horizon':0,'future_lost':0,'first_future_stockout_time':-1})

    def test_stockout_rate_denominators_and_partition(self):
        t=task();gold=d.audit.replay(t)[0]
        a={**gold,'future_lost':0,'first_future_stockout_time':-1}
        t2=task();t2['initial_stock']=9;gold2=d.audit.replay(t2)[0]
        b={**gold2,'future_lost':1,'first_future_stockout_time':110}
        items=[{'diagnostic':d.classify(t,a)},{'diagnostic':d.classify(t2,b)}, {'diagnostic':{'valid':False}}]
        result=d.summarize(items)
        self.assertEqual(result['missed_future_stockout'],{'numerator':1,'denominator':1,'rate':1})
        self.assertEqual(result['false_future_stockout'],{'numerator':1,'denominator':1,'rate':1})
        self.assertEqual(sum(result['categories'].values()),2)
        self.assertEqual(result['invalid'],1)

    def test_future_replay_ignores_history(self):
        t=task();expected=d.future_from_stock(t,3);t['reports']=[{'unusable':'history'}]
        self.assertEqual(d.future_from_stock(t,3),expected)

if __name__=='__main__':unittest.main()
