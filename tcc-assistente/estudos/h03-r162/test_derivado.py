import unittest
from preparar_derivado import target_item,nominal_box


class NominalGeometryTests(unittest.TestCase):
    def source(self):return dict(Kind='beam',Mark='V1',AxisM=[4.4,0,1.774,6.55,0,1.774],BM=.2,HM=.3)

    def test_x_axis_beam_uses_top_reference(self):
        lo,hi=nominal_box(target_item(self.source()))
        self.assertEqual(lo[:2],[4.4,-.1]);self.assertEqual(hi,[6.55,.1,1.774])
        self.assertAlmostEqual(lo[2],1.474)

    def test_reversed_y_axis_beam_preserves_positive_box(self):
        e=self.source();e['AxisM']=[4.4,3,3.2,4.4,0,3.2]
        lo,hi=nominal_box(target_item(e))
        self.assertAlmostEqual(lo[0],4.3);self.assertEqual(lo[1],0)
        self.assertAlmostEqual(hi[0],4.5);self.assertEqual(hi[1],3)

    def test_diagonal_and_sloping_beams_are_rejected(self):
        for axis in ([0,0,3,1,1,3],[0,0,3,1,0,4]):
            e=self.source();e['AxisM']=axis
            with self.assertRaisesRegex(ValueError,'ortogonal horizontal'):target_item(e)

    def test_zero_section_and_nonfinite_are_rejected(self):
        for value in (0,float('nan')):
            e=self.source();e['BM']=value
            with self.assertRaises(ValueError):target_item(e)


if __name__=='__main__':unittest.main()
