import unittest
from estudar_planta import redistribution


class Footprint(unittest.TestCase):
    def test_extra_run_requires_space(self):
        r=redistribution(1.96,.90,.89,2.24)
        self.assertAlmostEqual(r['keepHallLandingDepthM'],.62)
        self.assertAlmostEqual(r['keepLandingHallDepthM'],.61)
        self.assertFalse(r['simultaneousPreservationPossible'])

    def test_no_extra_run(self):
        self.assertTrue(redistribution(1.96,.90,.89,1.96)['simultaneousPreservationPossible'])

    def test_invalid_measurement(self):
        with self.assertRaises(ValueError):
            redistribution(1.96,.90,float('nan'),2.24)


if __name__=='__main__':
    unittest.main()
