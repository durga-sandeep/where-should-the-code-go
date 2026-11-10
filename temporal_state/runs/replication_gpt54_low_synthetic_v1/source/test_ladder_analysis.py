"""Amendment 4 analysis wiring: interaction contrast, missing-answer classification, macro names. No API calls."""
import re
import unittest

import ladder_analysis as la


def rows(values):
    """values: {(cfg, arm): {(base, rep): 0/1}} -> merged rows dict keyed like extension_analysis."""
    out = {}
    for (cfg, arm), table in values.items():
        for (base, rep), v in table.items():
            out[(cfg, arm, base, rep)] = {'future_joint': v}
    return out


class ContrastTests(unittest.TestCase):
    def test_interaction_is_auto_effect_minus_forced_effect(self):
        bases = [(f'b{i}', r) for i in range(4) for r in range(2)]
        cells = {('lo_f', 'canonical'): {k: 1 for k in bases}, ('hi_f', 'canonical'): {k: 0 for k in bases},   # forced: -1.0
                 ('lo_a', 'canonical'): {k: 0 for k in bases}, ('hi_a', 'canonical'): {k: 1 for k in bases}}   # auto: +1.0
        c = la.contrast(rows(cells), [('hi_a', 'canonical'), ('lo_f', 'canonical')], [('lo_a', 'canonical'), ('hi_f', 'canonical')], 'future_joint', 50, 1)
        self.assertEqual(c['bases'], 4)
        self.assertAlmostEqual(c['difference'], 2.0)  # (+1) - (-1)
        with self.assertRaises(ValueError):
            la.contrast(rows({**cells, ('hi_a', 'canonical'): {k: 1 for k in bases[:4]}}), [('hi_a', 'canonical'), ('lo_f', 'canonical')], [('lo_a', 'canonical'), ('hi_f', 'canonical')], 'future_joint', 50, 1)


class MissingKindTests(unittest.TestCase):
    def test_kinds(self):
        def chat(content='', finish='stop', calls=None, tokens=10):
            return {'response': {'choices': [{'finish_reason': finish, 'message': {'content': content, 'tool_calls': calls or []}}], 'usage': {'completion_tokens': tokens}}}
        self.assertEqual(la.missing_kind(chat("I'm sorry, but I can't provide that.")), 'refusal')
        self.assertEqual(la.missing_kind(chat('**Answer:** {"stock_at_target": 1}')), 'text_only')
        self.assertEqual(la.missing_kind(chat('', 'error')), 'stream_error')
        self.assertEqual(la.missing_kind(chat('', 'length')), 'truncated')
        self.assertEqual(la.missing_kind(chat('x', 'tool_calls', tokens=16384)), 'truncated')
        self.assertEqual(la.missing_kind(chat('', 'tool_calls', calls=[{'function': {'name': 'other'}}])), 'other_tool')
        self.assertEqual(la.missing_kind(chat('', 'tool_calls', calls=[{}, {}])), 'multiple_calls')
        self.assertEqual(la.missing_kind({'response': {'stop_reason': 'max_tokens', 'content': [], 'usage': {'output_tokens': 16384}}}), 'truncated')
        self.assertEqual(la.missing_kind({'response': {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'hi'}]}}), 'text_only')


class MacroTests(unittest.TestCase):
    def test_macro_keys_are_letters_only(self):
        for key in la.MACRO_KEYS.values():
            self.assertTrue(re.fullmatch(r'[A-Za-z]+', key), key)
        for cfg, label, _ in la.LADDER:
            self.assertIn(cfg, __import__('run').CONFIGS)


if __name__ == '__main__':
    unittest.main()
