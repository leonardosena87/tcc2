import unittest
from definir import profile,r144
class Definition(unittest.TestCase):
    def setUp(self):self.a=r144.alternative(17,8);self.p,self.r=profile(self.a,.9017)
    def test_exact_levels_and_riser_count(self):
        self.assertEqual(len(self.r),17)
        self.assertAlmostEqual(self.r[7]['topM'],1.6458823529411764)
        self.assertAlmostEqual(self.r[-1]['topM'],3.25)
        self.assertAlmostEqual(self.p[0][1],.22)
        for row in self.r:self.assertAlmostEqual(row['topM']-row['bottomM'],3.03/17)
    def test_treads_and_landing_are_distinct(self):
        horizontals=[b[0]-a[0] for a,b in zip(self.p,self.p[1:]) if abs(b[1]-a[1])<1e-10]
        self.assertEqual(len(horizontals),16)
        self.assertEqual(sum(abs(x-.28)<1e-10 for x in horizontals),15)
        self.assertEqual(sum(abs(x-.9017)<1e-10 for x in horizontals),1)
        self.assertAlmostEqual(self.r[7]['xM'],1.96)
        self.assertAlmostEqual(self.r[-1]['xM']-self.r[8]['xM'],2.24)
    def test_current_choice_does_not_claim_native_application(self):
        self.assertFalse(self.a['nativeGeometryApplied'])
        self.assertFalse(self.a['footprintHeadroomStructuralCapacityOrAccessibilityApproved'])
if __name__=='__main__':unittest.main()
