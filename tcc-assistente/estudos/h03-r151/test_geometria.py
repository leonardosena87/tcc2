import math
import unittest
from estudar import candidate,rail

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def proper_intersection(a,b,c,d):return cross(a,b,c)*cross(a,b,d)<-1e-10 and cross(c,d,a)*cross(c,d,b)<-1e-10

class Geometry(unittest.TestCase):
    def setUp(self):self.c=candidate(2.002366666666666,.910166666666667)
    def test_eighteen_risers_are_seventeen_tread_intervals(self):
        c=self.c
        self.assertEqual(c['lowerStraightTreadIntervals']+c['compensatedTreadIntervals']+c['upperStraightTreadIntervals'],17)
        self.assertAlmostEqual(.22+18*c['riserM'],3.25)
    def test_inner_boundary_and_order(self):
        c=self.c
        self.assertGreaterEqual(c['minimumInnerBoundaryChordM'],.15)
        edges=c['transitionRiserSegments']
        for i,e in enumerate(edges):
            for f in edges[i+1:]:self.assertFalse(proper_intersection(e['inner'],e['outer'],f['inner'],f['outer']))
    def test_footprint_preserves_hall_boundary(self):
        c=self.c
        self.assertLess(c['requiredStairLengthM'],1.9600333333333353+.901699999999998)
        self.assertFalse(c['headroomVerified']);self.assertFalse(c['legalApproval']);self.assertFalse(c['nativeApplied'])
    def test_mid_turn_reaches_both_rails(self):
        c=self.c;R=c['outerRadiusM'];a=c['transitionStraightExtensionM']
        for e in c['transitionRiserSegments']:
            x,y=e['outer']
            if y<0:self.assertAlmostEqual(x*x+y*y,R*R)
            else:self.assertAlmostEqual(abs(x),R)
            self.assertLessEqual(y,a+1e-8)
    def test_invalid_width_rejected(self):
        with self.assertRaises(ValueError):candidate(1,.91)
    def test_refined_candidate_survives_walkline_sensitivity(self):
        for offset in (.50,.55):
            c=candidate(2.002366666666666,.910166666666667,1.00,offset,13)
            self.assertEqual(c['lowerStraightTreadIntervals']+c['compensatedTreadIntervals']+c['upperStraightTreadIntervals'],17)
            self.assertGreater(c['twoRisersPlusPitchM'],.63)
            self.assertLess(c['twoRisersPlusPitchM'],.65)
            self.assertGreater(c['minimumInnerBoundaryChordM'],.16)
            self.assertLess(c['requiredStairLengthM'],2.861733333333333)
            for i,e in enumerate(c['transitionRiserSegments']):
                for f in c['transitionRiserSegments'][i+1:]:
                    self.assertFalse(proper_intersection(e['inner'],e['outer'],f['inner'],f['outer']))
    def test_initial_eleven_is_sensitive_not_robustly_accepted(self):
        c=candidate(2.002366666666666,.910166666666667,.77,.55,11)
        self.assertGreater(c['twoRisersPlusPitchM'],.65)
        self.assertFalse(c['legalApproval'])
if __name__=='__main__':unittest.main()
