import unittest
from auditar_contorno import triangle_signature


class TriangleComparisonTest(unittest.TestCase):
    def test_vertex_and_triangle_order_do_not_change_spatial_mesh(self):
        a = triangle_signature([(0,0,0),(1,0,0),(0,1,0)], [(0,1,2)])
        b = triangle_signature([(0,1,0),(0,0,0),(1,0,0)], [(2,0,1)])
        self.assertEqual(a, b)

    def test_equal_bounds_are_not_enough_to_claim_equal_mesh(self):
        vertices = [(0,0,0),(1,0,0),(1,1,0),(0,1,0)]
        self.assertNotEqual(triangle_signature(vertices,[(0,1,2),(0,2,3)]),
                            triangle_signature(vertices,[(0,1,3)]))

    def test_duplicated_faces_are_not_silently_ignored(self):
        vertices = [(0,0,0),(1,0,0),(0,1,0)]
        self.assertNotEqual(triangle_signature(vertices,[(0,1,2)]),
                            triangle_signature(vertices,[(0,1,2),(0,1,2)]))


if __name__ == '__main__':
    unittest.main()
