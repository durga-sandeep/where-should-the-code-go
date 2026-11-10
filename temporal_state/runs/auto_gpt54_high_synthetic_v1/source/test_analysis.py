import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('temporal_analysis', Path(__file__).with_name('analyze.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def episode(base='b0', arm='raw', rep=0, wrong=(), valid=True):
    score = {'valid': valid, **{f'{f}_exact': f not in wrong for f in a.FIELDS}}
    score['joint_exact'] = valid and not wrong
    return {'base_id': base, 'configuration': 'model', 'arm': arm, 'rep': rep,
            'status': 'ok', 'score': score, 'cost_usd': .01}


class AnalysisTests(unittest.TestCase):
    def manifest(self):
        return {'args': {'configs': ['model'], 'arms': ['raw', 'canonical'], 'reps': 1},
                'tasks': [{'base_id': 'b0', 'n_events': 12, 'late_arrival': True, 'corrections': False}]}

    def test_grid_missing_and_unexpected(self):
        result = a.analyze(self.manifest(), [episode()], 20)
        self.assertFalse(result['complete'])
        self.assertEqual(len(result['missing']), 1)
        result = a.analyze(self.manifest(), [episode(), episode(arm='canonical'), episode(base='alien')], 20)
        self.assertFalse(result['complete'])
        self.assertEqual(result['observed_episodes'], 2)
        self.assertEqual(len(result['unexpected']), 1)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            a.analyze(self.manifest(), [episode(), episode()], 20)

    def test_conditional_future_error(self):
        result = a.summarize([episode(wrong=('future_lost',)), episode(wrong=('stock_at_target',)), episode()])
        self.assertEqual(result['future_wrong_given_historical_correct'],
                         {'numerator': 1, 'denominator': 2, 'rate': .5})
        self.assertEqual(result['successes']['joint_exact'], 1)

    def test_invalid_contract_gates_accuracy(self):
        result = a.summarize([episode(valid=False)])
        self.assertEqual(result['successes']['stock_at_target_exact'], 0)
        self.assertIsNone(result['future_wrong_given_historical_correct']['rate'])

    def test_base_weight_not_repetition_weight(self):
        left = [episode('b0', rep=i, wrong=('future_lost',)) for i in range(3)] + [episode('b1')]
        right = [episode('b0', arm='canonical', rep=i) for i in range(3)] + [episode('b1', arm='canonical', wrong=('future_lost',))]
        pair = a.paired(left, right, 'joint_exact', 100)
        self.assertEqual(pair['difference'], 0)
        self.assertEqual(pair['matched_bases'], 2)
        self.assertEqual(pair['matched_episodes'], 4)
        self.assertEqual(pair, a.paired(left, right, 'joint_exact', 100))

    def test_complete_strata_and_markdown(self):
        result = a.analyze(self.manifest(), [episode(), episode(arm='canonical')], 20)
        self.assertTrue(result['complete'])
        self.assertEqual(len(result['factor_strata']), 8)
        self.assertIn('complete', a.render(result))
        self.assertAlmostEqual(result['summary']['estimated_cost_usd'], .02)

    def test_bad_joint_score_detected(self):
        row = episode()
        row['score']['joint_exact'] = False
        with self.assertRaises(ValueError):
            a.metrics(row)


if __name__ == '__main__':
    unittest.main()
