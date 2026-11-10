"""Small fixtures test extension-analysis wiring; never final study outputs. No API calls."""
import copy
import json
import unittest

import benchmark
import extension_analysis as ext
import run as runner


def task():
    return dict(base_id='t', initial_stock=4, target_time=100, knowledge_cutoff=100, horizon_time=130,
                reports=[dict(event_id='a', revision=1, event_time=5, received_time=5, kind='receipt', quantity=3),
                         dict(event_id='b', revision=1, event_time=7, received_time=7, kind='demand', quantity=9)],
                future_schedule=[dict(event_id='f1', event_time=110, kind='demand', quantity=5),
                                 dict(event_id='f2', event_time=120, kind='receipt', quantity=6)])


def openai_row(t, cfg, arm, answer, rep=0):
    payload = runner.request_for(t, cfg, arm)
    call = {'type': 'function_call', 'name': 'submit_answer', 'arguments': json.dumps(answer)}
    row = dict(base_id=t['base_id'], configuration=cfg, arm=arm, rep=rep, request=payload, status='submitted',
               response={'output': [call], 'usage': {'input_tokens': 10, 'output_tokens': 20, 'output_tokens_details': {'reasoning_tokens': 7}}},
               answer=answer, cost_usd=0.001)
    row['score'], hybrid = runner.score_for(t, arm, answer)
    if arm in runner.STATE_ARMS:
        row['hybrid_answer'] = hybrid
    return row


class ExtensionAnalysisTests(unittest.TestCase):
    def test_state_row_metrics_and_conservation(self):
        t = task()
        truth = benchmark.solve(t)
        row = openai_row(t, 'mini_high', 'state_raw', {'stock_at_target': truth['stock_at_target'], 'historical_lost': truth['historical_lost']})
        m, problems = ext.evaluate_row(t, row, 'openai')
        self.assertEqual(problems, [])
        self.assertTrue(m['valid'] and m['joint_exact'] and m['stock_exact'] and m['future_joint'])
        self.assertEqual(m['reasoning_tokens'], 7)
        wrong = openai_row(t, 'mini_high', 'state_canonical', {'stock_at_target': truth['stock_at_target'] + 9, 'historical_lost': 0})
        m, problems = ext.evaluate_row(t, wrong, 'openai')
        self.assertEqual(problems, [])
        self.assertTrue(m['valid'])
        self.assertFalse(m['stock_exact'])
        self.assertFalse(m['future_joint'])  # conservation: wrong stock implies wrong hybrid future

    def test_invalid_two_field_answer_fails_without_repair(self):
        t = task()
        row = openai_row(t, 'mini_low', 'state_raw', {'stock_at_target': -1, 'historical_lost': 0})
        m, problems = ext.evaluate_row(t, row, 'openai')
        self.assertEqual(problems, [])
        self.assertFalse(m['valid'])
        self.assertIsNone(row['hybrid_answer'])
        self.assertIsNone(m['predicted_stockout'])

    def test_tampered_score_hybrid_or_request_is_reported(self):
        t = task()
        truth = benchmark.solve(t)
        base = openai_row(t, 'mini_low', 'state_raw', {'stock_at_target': truth['stock_at_target'], 'historical_lost': truth['historical_lost']})
        bad_score = copy.deepcopy(base); bad_score['score']['joint_exact'] = False
        bad_hybrid = copy.deepcopy(base); bad_hybrid['hybrid_answer']['future_lost'] += 1
        bad_request = copy.deepcopy(base); bad_request['request']['instructions'] = 'changed'
        for row, expected in ((bad_score, 'score'), (bad_hybrid, 'hybrid_answer'), (bad_request, 'request')):
            _, problems = ext.evaluate_row(t, row, 'openai')
            self.assertIn(expected, problems)

    def test_full_arm_row_unchanged_semantics(self):
        t = task()
        answer = benchmark.solve(t)
        row = openai_row(t, 'mini_medium', 'raw', answer)
        m, problems = ext.evaluate_row(t, row, 'openai')
        self.assertEqual(problems, [])
        self.assertTrue(m['joint_exact'])
        self.assertEqual(row['request']['reasoning'], {'effort': 'medium'})

    def test_paired_matches_by_base_and_rep_and_averages_within_base(self):
        rows = {}
        for b in ('x', 'y'):
            for r in range(2):
                rows['mini_low', 'raw', b, r] = {'future_joint': False}
                rows['mini_low', 'canonical', b, r] = {'future_joint': (b == 'x')}
        out = ext.paired(rows, ('mini_low', 'raw'), rows, ('mini_low', 'canonical'), 'future_joint', 200, 1)
        self.assertEqual(out['bases'], 2)
        self.assertEqual(out['episodes'], 4)
        self.assertAlmostEqual(out['difference'], 0.5)
        del rows['mini_low', 'canonical', 'y', 1]
        with self.assertRaisesRegex(ValueError, 'Unmatched'):
            ext.paired(rows, ('mini_low', 'raw'), rows, ('mini_low', 'canonical'), 'future_joint', 200, 1)

    def test_cell_counts_and_decision_denominators(self):
        rows = {('c', 'a', 'b0', 0): dict(valid=True, joint_exact=True, stock_exact=True, historical_joint=True, future_joint=True,
                                          gold_stockout=True, predicted_stockout=True, output_tokens=5, reasoning_tokens=2, cost_usd=.1, truncated=False),
                ('c', 'a', 'b0', 1): dict(valid=False, joint_exact=False, stock_exact=False, historical_joint=False, future_joint=False,
                                          gold_stockout=False, predicted_stockout=None, output_tokens=None, reasoning_tokens=None, cost_usd=.1, truncated=True)}
        c = ext.cell(rows, 'c', 'a')
        self.assertEqual((c['n'], c['valid'], c['invalid'], c['truncated']), (2, 1, 1, 1))
        self.assertEqual((c['positives'], c['negatives'], c['false_alarms'], c['misses']), (1, 0, 0, 0))
        self.assertEqual(c['mean_reasoning_tokens'], 2)
        self.assertAlmostEqual(c['cost_usd'], .2)

    def test_task_identity_requires_heldout_source_and_identical_tasks(self):
        src = {'manifest': {'tasks': [task()]}}
        good = {'manifest': {'args': {'source_run': 'heldout_v2', 'split': 'heldout', 'n_base': 1}, 'tasks': [task()]}}
        ext.check_task_identity(good, src)
        changed = copy.deepcopy(good); changed['manifest']['tasks'][0]['initial_stock'] = 5
        with self.assertRaisesRegex(ValueError, 'differ'):
            ext.check_task_identity(changed, src)
        dev = copy.deepcopy(good); dev['manifest']['args']['split'] = 'dev'
        with self.assertRaisesRegex(ValueError, 'heldout'):
            ext.check_task_identity(dev, src)


if __name__ == '__main__':
    unittest.main()
