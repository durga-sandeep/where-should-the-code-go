import copy
import random
import unittest
from collections import Counter
from benchmark import (generate_tasks, public_task, canonical_events, replay_state, solve,
                       score, naive_arrival, latest_no_cutoff, DEVELOPMENT_SEED)


def report(eid, time, received, kind, qty, revision=1):
    return dict(event_id=eid, event_time=time, received_time=received, kind=kind, quantity=qty, revision=revision)


def task(reports, stock=0, future=None, cutoff=100):
    return dict(initial_stock=stock, reports=reports, target_time=100, knowledge_cutoff=cutoff,
                horizon_time=130, future_schedule=future or [])


class TemporalTests(unittest.TestCase):
    def test_lost_sales_path_dependence_and_future(self):
        rows = [report('a', 2, 8, 'receipt', 5), report('b', 1, 9, 'demand', 4)]
        future = [dict(event_id='f1',event_time=110,kind='demand',quantity=7),
                  dict(event_id='f2',event_time=120,kind='receipt',quantity=3)]
        t = task(rows, future=future)
        self.assertEqual(solve(t), dict(stock_at_target=5,historical_lost=4,stock_at_horizon=3,future_lost=2,first_future_stockout_time=110))
        self.assertNotEqual(naive_arrival(t), solve(t))
        self.assertEqual(solve(task([report('b', 2, 9, 'demand', 4), report('a', 1, 8, 'receipt', 5)]))['historical_lost'], 0)

    def test_filter_revision_order_and_ties(self):
        rows = [report('a', 10, 10, 'receipt', 8), report('a', 10, 110, 'receipt', 2, 2),
                report('b', 20, 20, 'demand', 6)]
        t = task(rows)
        self.assertEqual(solve(t)['stock_at_target'], 2)
        self.assertEqual(latest_no_cutoff(t)['historical_lost'], 4)
        # Latest revision moves the event beyond target: never resurrect v1.
        shifted = task([report('a',10,10,'receipt',8),report('a',105,110,'receipt',8,2)],cutoff=130)
        self.assertEqual(canonical_events(shifted), [])
        # Revision number wins over received order; same-time ID tie is stable.
        t = task([report('a',1,4,'receipt',9,1),report('a',1,3,'receipt',2,2),report('b',1,2,'demand',3)])
        self.assertEqual(solve(t)['historical_lost'], 1)
        with self.assertRaises(ValueError):
            canonical_events(task([rows[0], rows[0]]))

    def test_zero_stock_no_loss_is_not_stockout_and_strict_score(self):
        t = task([report('a',1,1,'demand',3)],stock=3)
        self.assertEqual(solve(t)['first_future_stockout_time'], -1)
        answer = solve(t)
        self.assertTrue(score(t, answer)['joint_exact'])
        for bad in (None, {}, dict(answer, extra=0), dict(answer, historical_lost=True), dict(answer, stock_at_target=-1)):
            self.assertFalse(score(t, bad)['valid'])
        wrong = dict(answer, stock_at_target=1)
        self.assertTrue(score(t, wrong)['valid'])
        self.assertFalse(score(t, wrong)['joint_exact'])
        self.assertTrue(score(t, wrong)['historical_lost_exact'])

    def test_generator_balance_provenance_and_independent_replay(self):
        tasks = generate_tasks()
        self.assertEqual(tasks, generate_tasks())
        self.assertEqual(len({t['base_id'] for t in tasks}), 96)
        counts = Counter((t['n_events'],t['late_arrival'],t['corrections'],t['future_pressure']) for t in tasks)
        self.assertEqual(len(counts),24)
        self.assertEqual(set(counts.values()),{4})
        dev = generate_tasks(12, DEVELOPMENT_SEED, 'dev')
        self.assertFalse({t['base_id'] for t in dev}&{t['base_id'] for t in tasks})
        for t in tasks:
            original = copy.deepcopy(t)
            self.assertEqual(len({r['event_id'] for r in t['reports']}),t['n_events'])
            self.assertTrue(all(r['received_time']>=r['event_time'] for r in t['reports']))
            first = [r for r in t['reports'] if r['revision']==1]
            self.assertEqual(any(r['received_time']>100 for r in first),t['late_arrival']=='present')
            self.assertEqual(any(r['revision']==2 for r in t['reports']),t['corrections']=='present')
            visible = {}
            for eid in {r['event_id'] for r in t['reports']}:
                options = [r for r in t['reports'] if r['event_id']==eid and r['received_time']<=t['knowledge_cutoff']]
                if options:
                    visible[eid]=max(options,key=lambda r:r['revision'])
            history = sorted([r for r in visible.values() if r['event_time']<=100],key=lambda r:(r['event_time'],r['event_id']))
            stock=t['initial_stock']; losses=[0,0]; first_loss=-1
            for stage, events in enumerate((history,t['future_schedule'])):
                for e in events:
                    if e['kind']=='receipt':stock+=e['quantity']
                    else:
                        fulfilled=min(stock,e['quantity']); stock-=fulfilled
                        loss=e['quantity']-fulfilled; losses[stage]+=loss
                        if stage==1 and loss and first_loss==-1:first_loss=e['event_time']
                if stage==0:at_target=stock
            self.assertEqual(solve(t),dict(stock_at_target=at_target,historical_lost=losses[0],stock_at_horizon=stock,future_lost=losses[1],first_future_stockout_time=first_loss))
            self.assertEqual(t,original)
            shuffled=copy.deepcopy(t)
            random.Random(123).shuffle(shuffled['reports'])
            random.Random(456).shuffle(shuffled['future_schedule'])
            self.assertEqual(solve(t),solve(shuffled))
            public=public_task(t)
            self.assertNotIn('base_id',public)
            self.assertNotIn('generator_version',public)
            public['reports'][0]['quantity']=999
            self.assertEqual(t,original)


if __name__ == '__main__':
    unittest.main()
