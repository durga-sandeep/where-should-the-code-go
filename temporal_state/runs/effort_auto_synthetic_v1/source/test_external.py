import copy
from decimal import Decimal
import unittest
from external_benchmark import load_profiles,quantities,generate_tasks,DEVELOPMENT_SEED
from benchmark import solve,canonical_events,public_task


class ExternalTests(unittest.TestCase):
    def test_source_split_allzero_and_no_future_normalization(self):
        profiles=load_profiles()
        self.assertEqual(len(profiles),64)
        zero=[rows for rows in profiles.values() if all(v==0 for row in rows for v in row['hours_sale'])]
        self.assertEqual(len(zero),1)
        history,future,normalizer=quantities(zero[0])
        self.assertEqual(history,[0]*36);self.assertEqual(future,[0]*12)
        self.assertEqual(Decimal(normalizer),1)
        altered=copy.deepcopy(zero[0]);altered[3]['hours_sale'][0]=2
        h,f,n=quantities(altered)
        self.assertEqual(h,history);self.assertEqual(n,normalizer);self.assertEqual(f[0],20)
        held=generate_tasks();dev=generate_tasks(seed=DEVELOPMENT_SEED,split='dev')
        self.assertEqual(len(held),48);self.assertEqual(len(dev),16)
        heldstores={t['source_store_id'] for t in held};devstores={t['source_store_id'] for t in dev}
        self.assertFalse(heldstores&devstores);self.assertEqual(heldstores|devstores,set(profiles))
        self.assertTrue(any(t['source_store_id']==zero[0][0]['store_id'] for t in held+dev))
        with self.assertRaises(ValueError):generate_tasks(49)

    def test_quantization_halfup_and_source_mapping(self):
        profiles=load_profiles()
        # Explicit exact half boundary: 10*0.05/1 = .5 -> 1, not bankers' rounding.
        rows=copy.deepcopy(next(iter(profiles.values())))
        for row in rows:row['hours_sale']=[0]*24
        rows[0]['hours_sale'][0]=1;rows[0]['hours_sale'][2]=.05
        history,_,_=quantities(rows);self.assertEqual(history[:2],[10,1])
        for t in generate_tasks():
            history,future,_=quantities(profiles[t['source_store_id']])
            latest={}
            for r in t['reports']:
                if r['event_id'] not in latest or r['revision']>latest[r['event_id']]['revision']:latest[r['event_id']]=r
            clean=sorted(latest.values(),key=lambda r:r['event_time'])
            self.assertEqual([r['quantity'] for r in clean if r['kind']=='demand'],history)
            self.assertEqual([r['quantity'] for r in t['future_schedule'] if r['kind']=='demand'],future)
            self.assertEqual(sum(r['quantity'] for r in clean if r['kind']=='receipt'),t['historical_receipt_budget'])
            self.assertEqual(sum(r['quantity'] for r in t['future_schedule'] if r['kind']=='receipt'),t['future_receipt_budget'])

    def test_shape_public_schema_and_independent_carry(self):
        tasks=generate_tasks();self.assertEqual(tasks,generate_tasks())
        for t in tasks:
            self.assertEqual(len(t['reports']),96)
            self.assertEqual(len(t['future_schedule']),18)
            self.assertTrue(all(r['received_time']>=r['event_time'] for r in t['reports']))
            # Reconstruct without shared canonical/replay functions.
            selected=[]
            for eid in {r['event_id'] for r in t['reports']}:
                visible=[r for r in t['reports'] if r['event_id']==eid and r['received_time']<=100]
                if visible:selected.append(max(visible,key=lambda r:r['revision']))
            selected=sorted([r for r in selected if r['event_time']<=100],key=lambda r:(r['event_time'],r['event_id']))
            stock=12;losses=[0,0];first=-1
            for stage,events in enumerate((selected,t['future_schedule'])):
                for e in events:
                    if e['kind']=='receipt':stock+=e['quantity']
                    else:
                        used=min(stock,e['quantity']);stock-=used
                        lost=e['quantity']-used;losses[stage]+=lost
                        if stage==1 and lost and first==-1:first=e['event_time']
                if stage==0:target=stock
            self.assertEqual(solve(t),dict(stock_at_target=target,historical_lost=losses[0],stock_at_horizon=stock,future_lost=losses[1],first_future_stockout_time=first))
            p=public_task(t)
            self.assertNotIn('source_store_id',p);self.assertNotIn('source_sha256',p)
            self.assertEqual(canonical_events(t),selected)


if __name__=='__main__':unittest.main()
