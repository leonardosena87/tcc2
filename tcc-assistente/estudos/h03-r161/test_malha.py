import unittest
import numpy as np
from comparar_ifc_r159_r160 import triangulated_metrics


class MeshMetricTests(unittest.TestCase):
    def setUp(self):
        self.v=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
        self.f=np.array([[0,2,1],[0,1,3],[0,3,2],[1,2,3]])

    def test_closed_tetrahedron_has_known_volume_and_surface(self):
        r=triangulated_metrics(self.v,self.f)
        self.assertTrue(r['triangulatedClosedOrientedEdgeCheck'])
        self.assertAlmostEqual(r['triangulatedSignedVolumeAbsoluteM3'],1/6)
        self.assertAlmostEqual(r['triangulatedAreaM2'],1.5+3**.5/2)

    def test_open_surface_does_not_report_solid_volume(self):
        r=triangulated_metrics(self.v,self.f[:3])
        self.assertFalse(r['triangulatedClosedOrientedEdgeCheck'])
        self.assertIsNone(r['triangulatedSignedVolumeAbsoluteM3'])

    def test_duplicated_face_does_not_pass_edge_check(self):
        r=triangulated_metrics(self.v,np.concatenate([self.f,self.f[:1]]))
        self.assertFalse(r['triangulatedClosedOrientedEdgeCheck'])
        self.assertIsNone(r['triangulatedSignedVolumeAbsoluteM3'])


if __name__=='__main__':unittest.main()
