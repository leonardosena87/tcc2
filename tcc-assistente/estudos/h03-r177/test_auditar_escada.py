import unittest
from auditar_escada import check_risers, finished_risers, fully_fixed_supports


class AuditTests(unittest.TestCase):
    def test_actual_first_concrete_riser_requires_finish_difference(self):
        lower=[.348,.52625,.7045,.88275,1.061,1.23925,1.4175,1.59575,1.774]
        upper=[1.95225,2.1305,2.30875,2.487,2.66525,2.8435,3.02175,3.2]
        result=check_risers(lower,upper)
        self.assertFalse(result['geometry17FinishedRisersWithinTolerance'])
        self.assertEqual((result['lowerCount'],result['upperCount']),(9,8))
        self.assertAlmostEqual(result['maxDifferenceCm'],0.0235294117647)
        self.assertAlmostEqual(result['lowerFinishedRisersCm'][0],17.8)
        self.assertFalse(check_risers(lower[1:],upper)['geometry17FinishedRisersWithinTolerance'])

    def test_uniform_geometry_passes_without_relaxing_tolerance(self):
        h=(3.25-.22)/17
        lower=[.22+i*h-.05 for i in range(1,10)]
        upper=[lower[-1]+i*h for i in range(1,9)]
        self.assertTrue(check_risers(lower,upper)['geometry17FinishedRisersWithinTolerance'])

    def test_count_does_not_mask_a_nonuniform_step(self):
        lower=[.348,.52625,.7045,.88275,1.061,1.23925,1.4175,1.59575,1.774]
        upper=[1.95225,2.1305,2.30875,2.487,2.66525,2.8435,3.02175,3.2]
        lower[3]+=.02
        self.assertFalse(check_risers(lower,upper)['geometry17FinishedRisersWithinTolerance'])

    def test_upper_rise_uses_measured_landing_not_a_fixed_reference(self):
        h=(3.25-.22)/17
        lower=[.22+i*h-.05 for i in range(1,10)]
        upper=[lower[-1]+i*h for i in range(1,9)]
        lower[-1]+=.01
        result=check_risers(lower,upper)
        self.assertFalse(result['geometry17FinishedRisersWithinTolerance'])
        self.assertAlmostEqual(result['upperFinishedRisersCm'][0],100*(h-.01))

    def test_missing_or_nonfinite_faces_are_not_inferred(self):
        for levels in ([],[float('nan')],[1.,1.],[2.,1.]):
            with self.assertRaises(ValueError):finished_risers(levels,.22,.05)

    def test_pinned_support_is_not_reported_as_fixed(self):
        fixed=dict(Joint='1',U1='YES',U2='YES',U3='YES',R1='YES',R2='YES',R3='YES')
        pinned=dict(fixed,Joint='2',R1='NO',R2='NO',R3='NO')
        result=fully_fixed_supports(dict(joints={'1':(450,321.58,0),'2':(0,0,0)},
            tables={'JOINT RESTRAINT ASSIGNMENTS':[fixed,pinned]}))
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['positionCm'],(450,321.58,0))


if __name__=='__main__':unittest.main()
