import unittest
from auditar_receptor import association


class AssociationTests(unittest.TestCase):
    def test_quantized_top_is_retained_and_signed_delta_reported(self):
        source=dict(Id=1,Mark='V16',AxisM=[0,0,1.774117647,2,0,1.774117647],BM=.2,HM=.3)
        part=dict(geometry=dict(minM=[0,-.1,1.474],maxM=[2,.1,1.774]))
        found=association(part,source,[[],[]])
        self.assertIsNotNone(found)
        self.assertAlmostEqual(found['topDeltaM'],-.000117647)
        part['geometry']['maxM'][2]=1.773
        self.assertIsNone(association(part,source,[[],[]]))
    def test_increased_top_tolerance_does_not_allow_wrong_width(self):
        source=dict(Id=1,Mark='V16',AxisM=[0,0,1.774117647,2,0,1.774117647],BM=.2,HM=.3)
        part=dict(geometry=dict(minM=[0,-.11,1.474],maxM=[2,.11,1.774]))
        self.assertIsNone(association(part,source,[[],[]]))


if __name__=='__main__':unittest.main()
