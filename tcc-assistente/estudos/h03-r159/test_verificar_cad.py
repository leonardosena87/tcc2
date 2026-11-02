import copy
import unittest
from verificar_cad import compare

class ReturnGuard(unittest.TestCase):
    def setUp(self):self.rows=[dict(id='a',layer='apoio',vertices=[[0,0,0],[1,0,0],[1,1,0],[0,1,0]])]
    def test_cyclic_and_reversed_vertex_order_are_equivalent(self):
        other=copy.deepcopy(self.rows);other[0]['vertices']=[[1,1,0],[1,0,0],[0,0,0],[0,1,0]]
        self.assertEqual(compare(self.rows,other),0)
    def test_missing_face_is_rejected(self):
        with self.assertRaises(ValueError):compare(self.rows,[])
    def test_moved_vertex_is_rejected(self):
        other=copy.deepcopy(self.rows);other[0]['vertices'][0][2]=.01
        with self.assertRaises(ValueError):compare(self.rows,other)
    def test_crossed_topology_is_rejected(self):
        other=copy.deepcopy(self.rows);other[0]['vertices'][1],other[0]['vertices'][2]=other[0]['vertices'][2],other[0]['vertices'][1]
        with self.assertRaises(ValueError):compare(self.rows,other)
    def test_changed_layer_is_rejected(self):
        other=copy.deepcopy(self.rows);other[0]['layer']='outra'
        with self.assertRaises(ValueError):compare(self.rows,other)

if __name__=='__main__':unittest.main()
