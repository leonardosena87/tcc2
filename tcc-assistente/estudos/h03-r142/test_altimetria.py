import unittest
from altimetria import altitude,relation

class AltimetryTests(unittest.TestCase):
    def test_upward_pdf_difference_increases_elevation(self):
        self.assertEqual(altitude(3.24,200,150,50),4.24)
        self.assertAlmostEqual(altitude(3.24,2018.719970703125,1816.4000244140625,56.67696439302885),6.809703290494991)
        self.assertRaises(ValueError,altitude,3.24,200,150,0)

    def test_unknown_plane_or_pedestal_does_not_become_zero(self):
        self.assertIsNone(relation(6.81,None)['baseAboveReferenceM'])
        r=relation(6.81,6.39)
        self.assertAlmostEqual(r['baseAboveReferenceM'],.42)
        self.assertIsNone(r['physicalPedestalHeightM'])

if __name__=='__main__':unittest.main()
