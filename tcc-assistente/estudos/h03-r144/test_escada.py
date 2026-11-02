import unittest
from estudar_escada import alternative

class StairGeometryTests(unittest.TestCase):
    def test_seventeen_closes_finished_floors_but_moves_landing(self):
        a=alternative(17,8)
        self.assertAlmostEqual(a['uniformRiserM']*17,3.03)
        self.assertAlmostEqual(a['proposedFinishedLandingM'],1.6458823529411764)
        self.assertAlmostEqual(a['upperTreadRunM'],2.24)
        self.assertFalse(a['acceptedArchitectureChange'])

    def test_eighteen_is_a_different_landing(self):
        a=alternative(18,9)
        self.assertAlmostEqual(a['proposedFinishedLandingM'],1.735)
        self.assertAlmostEqual(a['landingChangeM'],.035)
        self.assertFalse(a['footprintHeadroomStructuralCapacityOrAccessibilityApproved'])

    def test_invalid_geometry_or_counts_are_rejected(self):
        for kwargs in [{'total':17,'lower':17},{'total':17,'lower':1},{'total':17,'lower':8,'tread':0},{'total':17,'lower':8,'upper':.1}]:
            with self.assertRaises(ValueError):alternative(**kwargs)

if __name__=='__main__':unittest.main()
