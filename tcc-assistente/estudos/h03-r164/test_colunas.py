import unittest
from preparar_colunas import target_item


class ColumnGuardTests(unittest.TestCase):
    def item(self):return dict(Mark='P',Kind='column',AxisM=[1,2,.2,3.2],BM=.2,HM=.3,RotationRad=0)

    def test_preserves_nominal_endpoint_and_footprint(self):
        self.assertEqual(target_item(self.item()),dict(id='P',kind='column',x=1,y=2,z0=.2,z1=3.2,b=.2,h=.3))

    def test_refuses_other_kind_and_rotation(self):
        for field,value in [('Kind','beam'),('RotationRad',.01)]:
            e=self.item();e[field]=value
            with self.assertRaises(ValueError):target_item(e)

    def test_refuses_invalid_height_width_and_nonfinite(self):
        for change in [dict(AxisM=[1,2,3.2,.2]),dict(BM=0),dict(HM=float('nan'))]:
            with self.assertRaises(ValueError):target_item(self.item()|change)


if __name__=='__main__':unittest.main()
