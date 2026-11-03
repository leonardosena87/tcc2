import unittest
from conferir_ligacao import area, clip_rectangle, section_at_y, beam_axis_shared_nodes


VERTICES=[(0,0,0),(2,0,0),(2,1,0),(0,1,0),
          (0,0,1),(2,0,1),(2,1,1),(0,1,1)]
FACES=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
       (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]


class GeometryTests(unittest.TestCase):
    def test_interior_section_uses_intersections(self):
        r=section_at_y(VERTICES,FACES,.5,(0,0,2,1))
        self.assertEqual(r['mode'],'closed_convex_section')
        self.assertAlmostEqual(r['areaM2'],2)

    def test_contact_face(self):
        self.assertAlmostEqual(section_at_y(VERTICES,FACES,0,(0,0,2,1))['areaM2'],2)

    def test_gap_is_not_contact(self):
        self.assertEqual(section_at_y(VERTICES,FACES,-.01,(0,0,2,1))['areaM2'],0)

    def test_rectangle_clips_partial_overlap(self):
        self.assertAlmostEqual(section_at_y(VERTICES,FACES,.5,(1,.25,3,.75))['areaM2'],.5)

    def test_duplicate_coplanar_triangle_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicada'):
            section_at_y(VERTICES,FACES+[(0,1,5)],0,(0,0,2,1))

    def test_open_section_rejected(self):
        with self.assertRaisesRegex(ValueError,'aberta'):
            section_at_y(VERTICES,FACES[:-1],.5,(0,0,2,1))

    def test_bbox_overlap_does_not_create_section_area(self):
        # Triangulo cuja bbox intercepta o canto de recorte, mas a face nao.
        triangle=[(0,0,0),(2,0,0),(0,0,2)]
        self.assertAlmostEqual(section_at_y(triangle,[(0,1,2)],0,(1.5,1.5,2,2))['areaM2'],0)

    def test_convex_triangle_clipping_area(self):
        self.assertAlmostEqual(area(clip_rectangle([(0,0),(2,0),(0,2)],(0,0,1,1))),1)


class ConnectivityTests(unittest.TestCase):
    def model(self,duplicate_id=False):
        joints={'a':(450,0,177.4),'b':(500,0,177.4),'c':(500,12.2,177.4),
                'same_position':(500,0,177.4)}
        return dict(joints=joints,tables={
            'FRAME SECTION ASSIGNMENTS':[dict(Frame='beam',AnalSect='R20x30B'),dict(Frame='slab',AnalSect='R48.8x14A')],
            'CONNECTIVITY - FRAME':[dict(Frame='beam',JointI='a',JointJ='b'),
                dict(Frame='slab',JointI='same_position' if duplicate_id else 'b',JointJ='c')]})

    def test_shared_id_detected(self):
        self.assertEqual([r['jointId'] for r in beam_axis_shared_nodes(self.model())],['b'])

    def test_coincident_but_distinct_ids_not_connected(self):
        self.assertEqual(beam_axis_shared_nodes(self.model(True)),[])


if __name__=='__main__':
    unittest.main()
