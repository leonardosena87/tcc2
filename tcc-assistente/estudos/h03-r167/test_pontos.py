import unittest
from auditar_lajes import compare_points


class PointComparisonTests(unittest.TestCase):
    def test_accepts_quantization_and_reports_real_distance(self):
        r=compare_points([[0,0,0],[1,1,1]],[[0,0,0],[1.00001,1,1]])
        self.assertTrue(r['matches']);self.assertAlmostEqual(r['maxNearestDistanceM'],.00001)
    def test_same_bounding_box_does_not_hide_interior_point_change(self):
        self.assertFalse(compare_points([[0,0,0],[1,1,1],[.5,.5,.5]],[[0,0,0],[1,1,1],[.5,.6,.5]])['matches'])
    def test_rejects_nonunique_nearest_mapping(self):
        self.assertFalse(compare_points([[0,0,0],[0.00001,0,0]],[[0,0,0],[0,.00001,0]])['matches'])


if __name__=='__main__':unittest.main()
