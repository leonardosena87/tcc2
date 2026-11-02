import unittest
from triagem import box,inside_horizontal_face

class GeometryGuard(unittest.TestCase):
    def face(self,z=3.071764705882353):
        return dict(vertices=[[5.56,2.655,z],[6.47,2.655,z],[6.47,2.935,z],[5.56,2.935,z]])
    def test_last_tread_inside_slab_and_not_zero_overlap(self):
        e=dict(kind='slab',x=4.4,y=2.85,x2=6.55,y2=3.9,z=3.2,h=.14)
        r=inside_horizontal_face(self.face(),box(e))
        self.assertAlmostEqual(r['yOverlapM'],.085)
        self.assertAlmostEqual(r['areaM2'],.91*.085)
    def test_contact_or_vertical_gap_does_not_become_penetration(self):
        for z in (3.06,3.2,3.25):self.assertIsNone(inside_horizontal_face(self.face(z),[4.4,2.85,3.06,6.55,3.9,3.2]))
    def test_oblique_beam_is_rejected_instead_of_using_wrong_box(self):
        with self.assertRaises(ValueError):box(dict(kind='beam',x=0,y=0,x2=1,y2=1,z=3.2,b=.2,h=.3))
    def test_lateral_beam_overlap_is_not_omitted(self):
        e=dict(kind='beam',x=6.55,y=0,x2=6.55,y2=3.9,z=3.2,b=.2,h=.4)
        r=inside_horizontal_face(self.face(),box(e))
        self.assertAlmostEqual(r['xMaxM']-r['xMinM'],.02)

if __name__=='__main__':unittest.main()
