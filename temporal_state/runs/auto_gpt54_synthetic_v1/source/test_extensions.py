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
        for name, effort in (('mini_low_auto', 'low'), ('mini_high_auto', 'high')):
            auto = run.request_for(task, name, 'raw')
            forced = run.request_for(task, 'mini_low' if effort == 'low' else 'mini_high', 'raw')
            self.assertEqual(auto['tool_choice'], 'auto')
            self.assertEqual({k: v for k, v in auto.items() if k != 'tool_choice'}, {k: v for k, v in forced.items() if k != 'tool_choice'})

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




class Amendment4Tests(unittest.TestCase):
    """Amendment 4 wiring: OpenRouter chat-completions payloads, Haiku, GPT-5.4 automatic choice."""

    def test_open_weight_configs_form_a_full_cross(self):
        for name in ('oss20b', 'oss120b', 'qwen27b', 'dsflash', 'glmflash', 'dspro'):
            cells = {k: run.CONFIGS[k] for k in (f'{name}_low', f'{name}_high', f'{name}_low_auto', f'{name}_high_auto')}
            models = {c['model'] for c in cells.values()}
            routes = {c['route'] for c in cells.values()}
            self.assertEqual(len(models), 1)
            self.assertEqual(len(routes), 1)
            self.assertTrue(all(c['provider'] == 'openrouter' for c in cells.values()))
            self.assertEqual(cells[f'{name}_low']['reasoning'], 'low')
            self.assertEqual(cells[f'{name}_high']['reasoning'], 'high')
            self.assertFalse(cells[f'{name}_low'].get('auto_tool_choice'))
            self.assertTrue(cells[f'{name}_high_auto']['auto_tool_choice'])

    def test_openrouter_payload_matches_openai_semantics(self):
        task = small_task()
        for arm in ('raw', 'canonical', 'snapshot', 'state_raw', 'state_canonical'):
            chat = run.request_for(task, 'oss20b_low', arm)
            resp = run.request_for(task, 'mini_low', arm)
            self.assertEqual(chat['messages'][0], {'role': 'system', 'content': resp['instructions']})
            self.assertEqual(chat['messages'][1]['content'], resp['input'][0]['content'])
            self.assertEqual(chat['tools'][0]['function']['parameters'], resp['tools'][0]['parameters'])
            self.assertTrue(chat['tools'][0]['function']['strict'])
            self.assertEqual(chat['tool_choice'], {'type': 'function', 'function': {'name': 'submit_answer'}})
            self.assertEqual(chat['max_tokens'], resp['max_output_tokens'])
            self.assertEqual(chat['reasoning'], {'effort': 'low'})
            self.assertNotIn('parallel_tool_calls', chat)
            self.assertNotIn('usage', chat)
            self.assertEqual(chat['provider'], {'only': ['deepinfra'], 'allow_fallbacks': False, 'require_parameters': True})
        auto = run.request_for(task, 'oss20b_low_auto', 'raw')
        self.assertEqual(auto['tool_choice'], 'auto')
        self.assertEqual({k: v for k, v in auto.items() if k != 'tool_choice'},
                         {k: v for k, v in run.request_for(task, 'oss20b_low', 'raw').items() if k != 'tool_choice'})
        with self.assertRaises(ValueError):
            run.request_for(task, 'oss20b_low', 'tool_raw')

    def test_chat_completion_answer_requires_exactly_one_call(self):
        call = {'type': 'function', 'function': {'name': 'submit_answer', 'arguments': '{"stock_at_target": 1, "historical_lost": 0}'}}
        good = {'choices': [{'message': {'content': '<think>reasoning</think>', 'tool_calls': [call]}}]}
        self.assertEqual(run.chat_completion_answer(good), {'stock_at_target': 1, 'historical_lost': 0})
        as_object = {'choices': [{'message': {'tool_calls': [{**call, 'function': {'name': 'submit_answer', 'arguments': {'stock_at_target': 2}}}]}}]}
        self.assertEqual(run.chat_completion_answer(as_object), {'stock_at_target': 2})
        self.assertIsNone(run.chat_completion_answer({'choices': [{'message': {'content': 'text only'}}]}))
        self.assertIsNone(run.chat_completion_answer({'choices': [{'message': {'tool_calls': [call, call]}}]}))
        self.assertIsNone(run.chat_completion_answer({'choices': []}))
        # The independent auditor's parser agrees.
        import audit_results
        self.assertEqual(audit_results.parse_answer({'response': good}, 'openrouter'), ({'stock_at_target': 1, 'historical_lost': 0}, 'submitted'))
        self.assertEqual(audit_results.parse_answer({'response': {'choices': [{'message': {}}]}}, 'openrouter'), (None, 'missing_answer'))

    def test_haiku_and_gpt54_auto_match_existing_shapes(self):
        task = small_task()
        for name, base in (('haiku45', 'sonnet46'), ('haiku45_thinking', 'sonnet46_thinking')):
            new = run.request_for(task, name, 'raw')
            old = run.request_for(task, base, 'raw')
            self.assertEqual({k: v for k, v in new.items() if k != 'model'}, {k: v for k, v in old.items() if k != 'model'})
            self.assertEqual(new['model'], 'claude-haiku-4-5-20251001')
        for name, base in (('gpt54_low_auto', 'gpt54_low'), ('gpt54_high_auto', 'gpt54_high')):
            new = run.request_for(task, name, 'canonical')
            old = run.request_for(task, base, 'canonical')
            self.assertEqual(new['tool_choice'], 'auto')
            self.assertEqual({k: v for k, v in new.items() if k != 'tool_choice'}, {k: v for k, v in old.items() if k != 'tool_choice'})

    def test_every_config_model_is_priced(self):
        from completeness_pilot import run_pilot
        for cfg in run.CONFIGS.values():
            self.assertIn(cfg['model'], run_pilot.PRICING)
            self.assertIn(cfg['provider'], run_pilot.MODELS)


if __name__ == '__main__':
    unittest.main()


class TransportRetryTests(unittest.TestCase):
    """Amendment 4 transport note 5: bounded retries for OpenRouter rate limits only, attempt count returned."""

    def setUp(self):
        self.calls = []
        self.real_request, self.real_sleep = run.transport.request, run.time.sleep
        run.time.sleep = lambda s: self.calls.append(('sleep', s))

    def tearDown(self):
        run.transport.request, run.time.sleep = self.real_request, self.real_sleep

    def _fake(self, outcomes):
        it = iter(outcomes)
        def request(provider, payload, budget, episode, timeout):
            self.calls.append(('call', provider))
            o = next(it)
            if isinstance(o, Exception):
                raise o
            return o, 0.0
        run.transport.request = request

    def test_openrouter_retries_429_then_succeeds_with_attempt_count(self):
        self._fake([RuntimeError('provider_http_429: Provider returned error'), RuntimeError('provider_http_503'), {'ok': 1}])
        response, cost, attempts = run.transport_request('openrouter', run.CONFIGS['oss20b_low'], {}, None, 'e')
        self.assertEqual((response, attempts), ({'ok': 1}, 3))
        self.assertEqual([c for c in self.calls if c[0] == 'sleep'], [('sleep', 5), ('sleep', 10)])

    def test_openrouter_does_not_retry_rejected_parameters_or_beyond_limit(self):
        self._fake([RuntimeError('provider_http_404: No endpoints found')])
        with self.assertRaises(RuntimeError):
            run.transport_request('openrouter', run.CONFIGS['oss20b_low'], {}, None, 'e')
        self.assertEqual(len([c for c in self.calls if c[0] == 'call']), 1)
        self.calls.clear()
        self._fake([RuntimeError('provider_http_429')] * 6)
        with self.assertRaises(RuntimeError):
            run.transport_request('openrouter', run.CONFIGS['oss20b_low'], {}, None, 'e')
        self.assertEqual(len([c for c in self.calls if c[0] == 'call']), run.TRANSPORT_MAX_ATTEMPTS)

    def test_first_party_providers_never_retry(self):
        self._fake([RuntimeError('provider_http_429')])
        with self.assertRaises(RuntimeError):
            run.transport_request('openai', run.CONFIGS['mini_low'], {}, None, 'e')
        self.assertEqual(len(self.calls), 1)
