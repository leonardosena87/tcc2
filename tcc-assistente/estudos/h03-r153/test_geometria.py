import json
import unittest
from conferir import HERE,build,headroom

class NineEight(unittest.TestCase):
    def setUp(self):
        ref=json.loads((HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json').read_text(encoding='utf-8'))
        m=json.loads((HERE.parent/'h03-r147/R147-planta.json').read_text(encoding='utf-8'))['graphicalMeasurementsM']
        self.d=build(ref,m)
    def test_floors_landing_and_count(self):
        d=self.d
        self.assertEqual(len(d['risers']),17);self.assertEqual(len(d['treads']),15)
        self.assertAlmostEqual(d['geometry']['proposedFinishedLandingM'],1.8241176470588234)
        self.assertAlmostEqual(d['risers'][-1]['zTopM'],3.25)
        self.assertEqual(len(d['finishedSurfaceFaces']),33)
    def test_upper_arrival_preserved_to_graphic_precision(self):
        e=self.d['clearEnvelope']
        self.assertLess(abs(e['upperArrivalYM']-e['upperArrivalReferenceYM']),.0001)
        self.assertAlmostEqual(e['lowerStartYM']-e['upperArrivalYM'],.28)
        self.assertGreater(3.1263166666666664-e['upperArrivalYM'],.19)
    def test_parallel_treads_have_no_plan_overlap(self):
        f=self.d['finishedSurfaceFaces'];lower=[a for a in f if a['kind']=='tread' and a['number']<9];upper=[a for a in f if a['kind']=='tread' and a['number']>9]
        self.assertLess(max(v[0] for a in lower for v in a['vertices']),min(v[0] for a in upper for v in a['vertices']))
    def test_conditional_headroom_and_negative_control(self):
        d=self.d;edge=d['clearEnvelope']['upperArrivalReferenceYM']
        s=headroom(d['treads'],edge,3.02)
        self.assertEqual([r['tread'] for r in s['overlappedTreads']],[1,2])
        self.assertAlmostEqual(s['minimumConditionalClearanceM'],2.443529411764706)
        self.assertLess(headroom(d['treads'],edge,2.65)['minimumConditionalClearanceM'],2.10)
        self.assertFalse(s['actual3DObstructionSurveyOrComplianceVerified'])
    def test_candidate_is_not_a_structural_volume(self):
        self.assertTrue(self.d['noWaistThicknessOrVolume']);self.assertFalse(self.d['loadApplied']);self.assertFalse(self.d['nativeModelsEdited'])
if __name__=='__main__':unittest.main()
