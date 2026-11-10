"""Check continuation semantics on constructed counterexamples, not final results."""
import unittest
import continuation_analysis as c


class ContinuationTests(unittest.TestCase):
    def task(self):
        return {'initial_stock': 0, 'target_time': 100, 'knowledge_cutoff': 100,
                'horizon_time': 130, 'reports': [],
                'future_schedule': [{'event_id': 'd', 'event_time': 110, 'kind': 'demand', 'quantity': 5},
                                    {'event_id': 'r', 'event_time': 120, 'kind': 'receipt', 'quantity': 3}]}

    def test_late_receipt_cannot_fill_lost_demand(self):
        answer = dict(stock_at_target=0, historical_lost=0, stock_at_horizon=0,
                      future_lost=2, first_future_stockout_time=110)
        self.assertEqual({k: v for k, v in c.evaluate(self.task(), answer).items() if k in ('valid', 'model_future', 'code_future')},
                         {'valid': True, 'model_future': False, 'code_future': True})

    def test_accidentally_correct_future_can_regress(self):
        answer = dict(stock_at_target=1, historical_lost=0, stock_at_horizon=3,
                      future_lost=5, first_future_stockout_time=110)
        self.assertEqual({k: v for k, v in c.evaluate(self.task(), answer).items() if k in ('valid', 'model_future', 'code_future')},
                         {'valid': True, 'model_future': True, 'code_future': False})

    def test_invalid_full_contract_not_repaired(self):
        answer = dict(stock_at_target=0, historical_lost=-1, stock_at_horizon=3,
                      future_lost=5, first_future_stockout_time=110)
        self.assertEqual({k: v for k, v in c.evaluate(self.task(), answer).items() if k in ('valid', 'model_future', 'code_future')},
                         {'valid': False, 'model_future': False, 'code_future': False})

    def test_pairing_keeps_repeated_bases_together(self):
        rows = [dict(base_id='a', valid=True, model_future=False, code_future=True),
                dict(base_id='a', valid=True, model_future=True, code_future=True),
                dict(base_id='b', valid=True, model_future=True, code_future=False),
                dict(base_id='b', valid=False, model_future=False, code_future=False)]
        result = c.summary(rows, 100, 1)
        self.assertEqual((result['n'], result['bases'], result['difference'], result['invalid']), (4, 2, 0, 1))
        self.assertEqual((result['corrected'], result['regressed']), (1, 1))
        self.assertEqual(result['ci95'], [-.5, .5])


if __name__ == '__main__':
    unittest.main()
