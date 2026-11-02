import unittest
from validar_retorno import normalized_faces
class RoundTrip(unittest.TestCase):
    def test_order_and_vertex_winding_do_not_change_geometry_key(self):
        a=('pisada',[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])
        self.assertEqual(normalized_faces([a]),normalized_faces([(a[0],list(reversed(a[1])))]))
    def test_millimetre_change_or_missing_face_is_detected(self):
        a=('pisada',[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])
        b=('pisada',[(0,0,1.001),(1,0,1),(1,1,1),(0,1,1)])
        self.assertNotEqual(normalized_faces([a]),normalized_faces([b]))
        self.assertNotEqual(normalized_faces([a,a]),normalized_faces([a]))
if __name__=='__main__':unittest.main()
