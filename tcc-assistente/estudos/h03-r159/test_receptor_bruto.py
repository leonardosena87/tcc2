import unittest
from auditar_receptor_bruto import beam_candidates


class ReceiverTests(unittest.TestCase):
    def source(self):
        return [dict(Kind='beam',AxisM=[0,0,3.2,4,0,3.2],Mark='V1-N1',Id=1,BM=.2,HM=.45),
                dict(Kind='beam',AxisM=[0,0,6.39,4,0,6.39],Mark='V1-N2',Id=2,BM=.2,HM=.45)]

    def test_same_xy_selects_nearest_level_and_exposes_section_change(self):
        result=beam_candidates(dict(minM=[.1,-.1,6.09],maxM=[3.9,.1,6.25]),self.source())
        self.assertEqual(result['nativeId'],2)
        self.assertAlmostEqual(result['topDeltaM'],-.14)
        self.assertAlmostEqual(result['heightDeltaM'],-.29)

    def test_rounding_is_tolerated_but_one_cm_axis_change_is_not(self):
        box=dict(minM=[.1,-.1+.0000167,2.75],maxM=[3.9,.1+.0000167,3.2])
        self.assertIsNotNone(beam_candidates(box,self.source()))
        box['minM'][1]+=.01;box['maxM'][1]+=.01
        self.assertIsNone(beam_candidates(box,self.source()))

    def test_unexplained_extension_stays_unmatched(self):
        self.assertIsNone(beam_candidates(dict(minM=[.1,-.1,2.75],maxM=[4.15,.1,3.2]),self.source()))


if __name__=='__main__':unittest.main()
