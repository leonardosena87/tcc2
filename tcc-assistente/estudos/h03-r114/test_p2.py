import unittest
from preparar_p2 import corner_loads


class GravityControls(unittest.TestCase):
    def test_four_corners_balance_force_and_first_moments(self):
        ns=corner_loads(.25,[6.55,0,9.65,3.9]);total=.25*12.09
        self.assertAlmostEqual(sum(n['FzKN'] for n in ns),-total)
        self.assertAlmostEqual(sum(n['yM']*n['FzKN'] for n in ns),-total*1.95)
        self.assertAlmostEqual(sum(-n['xM']*n['FzKN'] for n in ns),total*8.1)
        self.assertEqual(len({(n['xM'],n['yM']) for n in ns}),4)

    def test_degenerate_or_nonfinite_data_rejected(self):
        for g,box in [(0,[0,0,1,1]),(.25,[1,0,1,2]),(.25,[0,1,2,0]),(float('inf'),[0,0,1,1])]:
            with self.assertRaises(ValueError):corner_loads(g,box)


if __name__=='__main__':unittest.main()
