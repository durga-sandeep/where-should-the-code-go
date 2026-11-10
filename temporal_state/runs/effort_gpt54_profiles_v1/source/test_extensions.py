"""Extension-study wiring: effort configurations, state-only arms, hybrid scoring. No API calls."""
import json
import unittest

import benchmark
import run


def small_task():
    return dict(base_id='x', initial_stock=4, target_time=100, knowledge_cutoff=100, horizon_time=130,
                reports=[dict(event_id='a', revision=1, event_time=5, received_time=5, kind='receipt', quantity=3),
                         dict(event_id='b', revision=1, event_time=7, received_time=7, kind='demand', quantity=9),
                         dict(event_id='b', revision=2, event_time=7, received_time=120, kind='demand', quantity=1)],
                future_schedule=[dict(event_id='f1', event_time=110, kind='demand', quantity=5),
                                 dict(event_id='f2', event_time=120, kind='receipt', quantity=6)])


class ExtensionTests(unittest.TestCase):
    def test_effort_configs_differ_only_in_effort(self):
        base = run.CONFIGS['mini_low']
        for name, effort in (('mini_medium', 'medium'), ('mini_high', 'high')):
            cfg = run.CONFIGS[name]
            self.assertEqual({k: v for k, v in cfg.items() if k != 'reasoning'}, {k: v for k, v in base.items() if k != 'reasoning'})
            self.assertEqual(cfg['reasoning'], effort)
            self.assertEqual(run.request_for(small_task(), name, 'raw')['reasoning'], {'effort': effort})

    def test_default_arms_unchanged_and_state_arms_registered(self):
        self.assertEqual(run.FULL_ARMS, ('raw', 'canonical', 'snapshot'))
        self.assertEqual(run.STATE_ARMS, ('state_raw', 'state_canonical'))
        self.assertEqual(run.TOOL_ARMS, ('tool_raw', 'tool_canonical'))
        self.assertEqual(run.ARMS, run.FULL_ARMS + run.STATE_ARMS + run.TOOL_ARMS)

    def test_tool_arms_add_code_interpreter_and_keep_task_semantics(self):
        task = small_task()
        for arm, base in (('tool_raw', 'raw'), ('tool_canonical', 'canonical')):
            payload = run.request_for(task, 'mini_low', arm)
            types = [t['type'] for t in payload['tools']]
            self.assertEqual(types, ['function', 'code_interpreter'])
            self.assertEqual(payload['tool_choice'], 'auto')
            self.assertTrue(payload['instructions'].startswith(run.INSTRUCTIONS))
            self.assertIn('code execution tool', payload['instructions'])
            body = json.loads(payload['input'][0]['content'])
            plain = json.loads(run.request_for(task, 'mini_low', base)['input'][0]['content'])
            self.assertEqual({k: v for k, v in body.items() if k != 'input_representation'},
                             {k: v for k, v in plain.items() if k != 'input_representation'})
            self.assertEqual(body['input_representation'], arm)
            self.assertEqual(set(payload['tools'][0]['parameters']['properties']), set(run.FIELDS))
            with self.assertRaises(ValueError):
                run.request_for(task, 'sonnet46', arm)
        # Full arms are unchanged: forced tool choice, one function tool.
        full = run.request_for(task, 'mini_low', 'raw')
        self.assertEqual([t['type'] for t in full['tools']], ['function'])
        self.assertEqual(full['tool_choice'], {'type': 'function', 'name': 'submit_answer'})
        for name, effort in (('gpt54_medium', 'medium'), ('gpt54_high', 'high')):
            self.assertEqual(run.CONFIGS[name]['model'], run.CONFIGS['gpt54_low']['model'])
            self.assertEqual(run.CONFIGS[name]['reasoning'], effort)

    def test_state_request_withholds_future_and_uses_two_field_schema(self):
        task = small_task()
        for provider_cfg in ('mini_low', 'sonnet46'):
            for arm in run.STATE_ARMS:
                payload = run.request_for(task, provider_cfg, arm)
                tool = payload['tools'][0]
                schema = tool.get('parameters') or tool.get('input_schema')
                self.assertEqual(set(schema['properties']), set(run.HISTORY_FIELDS))
                self.assertEqual(set(schema['required']), set(run.HISTORY_FIELDS))
                text = payload.get('instructions') or payload.get('system')
                self.assertEqual(text, run.STATE_INSTRUCTIONS)
                self.assertIn('There is no future scenario', text)
                self.assertNotIn('future_schedule', text)
                body = json.loads((payload.get('input') or payload.get('messages'))[0]['content'])
                self.assertNotIn('future_schedule', body)
                self.assertNotIn('horizon_time', body)
                self.assertEqual(body['input_representation'], arm)
                if arm == 'state_raw':
                    self.assertEqual(body['reports'], task['reports'])
                    self.assertNotIn('eligible_events', body)
                else:
                    self.assertNotIn('reports', body)
                    self.assertEqual(body['eligible_events'], benchmark.canonical_events(task))
        # Full arms keep the original instructions and five-field schema.
        full = run.request_for(task, 'mini_low', 'raw')
        self.assertEqual(full['instructions'], run.INSTRUCTIONS)
        self.assertEqual(set(full['tools'][0]['parameters']['properties']), set(run.FIELDS))

    def test_state_instructions_share_history_rules(self):
        self.assertTrue(run.STATE_INSTRUCTIONS.startswith(run.INSTRUCTIONS[:run._SPLIT]))
        self.assertIn('Return two integers', run.STATE_INSTRUCTIONS)

    def test_hybrid_answer_executes_future_from_emitted_stock(self):
        task = small_task()
        truth = benchmark.solve(task)
        self.assertEqual(truth['stock_at_target'], 0)
        exact = {'stock_at_target': 0, 'historical_lost': 2}
        hybrid = run.hybrid_answer(task, exact)
        self.assertEqual(hybrid, truth)
        score, stored = run.score_for(task, 'state_raw', exact)
        self.assertTrue(score['joint_exact'])
        self.assertEqual(stored, truth)
        wrong_stock = run.hybrid_answer(task, {'stock_at_target': 7, 'historical_lost': 2})
        self.assertEqual(wrong_stock['future_lost'], 0)
        self.assertEqual(wrong_stock['first_future_stockout_time'], -1)
        self.assertEqual(wrong_stock['stock_at_horizon'], 8)
        score, _ = run.score_for(task, 'state_raw', {'stock_at_target': 7, 'historical_lost': 2})
        self.assertTrue(score['valid'])
        self.assertTrue(score['historical_lost_exact'])
        self.assertFalse(score['stock_at_target_exact'])
        self.assertFalse(score['future_lost_exact'])

    def test_invalid_two_field_contract_is_not_repaired(self):
        task = small_task()
        for bad in (None, {}, {'stock_at_target': 1}, {'stock_at_target': 1, 'historical_lost': 2, 'extra': 0},
                    {'stock_at_target': -1, 'historical_lost': 0}, {'stock_at_target': 1.0, 'historical_lost': 0},
                    {'stock_at_target': True, 'historical_lost': 0}, benchmark.solve(task)):
            self.assertIsNone(run.hybrid_answer(task, bad))
            score, hybrid = run.score_for(task, 'state_canonical', bad)
            self.assertFalse(score['valid'])
            self.assertIsNone(hybrid)

    def test_conservation_makes_hybrid_future_equivalent_to_stock(self):
        for task in benchmark.generate_tasks(n_base=12, seed=benchmark.DEVELOPMENT_SEED, split='dev'):
            truth = benchmark.solve(task)
            for stock in range(0, truth['stock_at_target'] + 40, 3):
                hybrid = run.hybrid_answer(task, {'stock_at_target': stock, 'historical_lost': truth['historical_lost']})
                future_ok = all(hybrid[k] == truth[k] for k in run.FIELDS[2:])
                self.assertEqual(future_ok, stock == truth['stock_at_target'])

    def test_full_arm_scoring_unchanged(self):
        task = small_task()
        answer = benchmark.solve(task)
        score, hybrid = run.score_for(task, 'raw', answer)
        self.assertEqual(score, benchmark.score(task, answer))
        self.assertIsNone(hybrid)


if __name__ == '__main__':
    unittest.main()
