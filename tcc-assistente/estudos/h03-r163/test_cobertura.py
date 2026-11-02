import unittest
from auditar_cobertura import coverage, candidate, endpoint_supports, column_box, subtract_intervals


class CoverageTests(unittest.TestCase):
    def test_gap_is_not_hidden_by_summed_lengths(self):
        r = coverage([(0, .6), (.2, .6), (.8, 1)], 0, 1)
        self.assertEqual(r['uncoveredIntervalsM'], [[.6, .8]])
        self.assertAlmostEqual(r['coveredLengthM'], .8)

    def test_exclusion_does_not_mask_gap_outside_column(self):
        self.assertEqual(subtract_intervals([(0,1)],[(.4,.6)]),[[0,.4],[.6,1]])
        self.assertEqual(subtract_intervals([(0,.3),(.6,1)],[(.4,.6)]),[[0,.3],[.6,1]])

    def test_rounding_is_distinguished_from_real_gap(self):
        self.assertTrue(coverage([(0,.5),(.50002,1)],0,1)['noGapAboveTolerance'])
        self.assertFalse(coverage([(0,.5),(.501,1)],0,1)['noGapAboveTolerance'])

    def test_end_extension_requires_support_envelope(self):
        src = dict(Id=1,Mark='V',Kind='beam',AxisM=[0,0,3,2,0,3],BM=.2,HM=.3)
        part = dict(geometry=dict(minM=[-.1,-.1,2.7],maxM=[2.1,.1,3]))
        self.assertIsNone(candidate(part,src,[[],[]]))
        supports = [[dict(alongIntervalM=[-.1,.1])],[dict(alongIntervalM=[1.9,2.1])]]
        self.assertEqual(candidate(part,src,supports)['nativeId'],1)
        part['geometry']['maxM'][0]=2.11
        self.assertIsNone(candidate(part,src,supports))

    def test_wrong_section_and_top_remain_unmatched(self):
        src = dict(Id=1,Mark='V',Kind='beam',AxisM=[0,0,3,2,0,3],BM=.2,HM=.3)
        part = dict(geometry=dict(minM=[.1,-.1,2.7],maxM=[1.9,.1,3.01]))
        self.assertIsNone(candidate(part,src,[[],[]]))

    def test_rotated_column_dimensions_and_rejection(self):
        import math
        e=dict(Mark='P',AxisM=[0,0,0,3],BM=.2,HM=.3,RotationRad=math.pi/2)
        self.assertAlmostEqual(column_box(e)['maxM'][0],.15)
        e['RotationRad']=math.pi/4
        with self.assertRaises(ValueError):column_box(e)

    def test_column_above_beam_does_not_supply_end_support(self):
        beam=dict(Id=1,Mark='V',Kind='beam',AxisM=[0,0,3,2,0,3],BM=.2,HM=.3)
        col=dict(Id=2,Mark='P',Kind='column',AxisM=[0,0,3,6],BM=.2,HM=.3)
        self.assertFalse(endpoint_supports(beam,[beam,col])[0])


if __name__ == '__main__':unittest.main()
