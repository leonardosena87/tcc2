import unittest
from reavaliar import evaluate


class Eighteen(unittest.TestCase):
    def test_floors_and_symmetric_landing(self):
        a=evaluate(.28,1.96,.90,.89)['geometry']
        self.assertAlmostEqual(a['uniformRiserM'],.16833333333333333)
        self.assertAlmostEqual(a['proposedFinishedLandingM'],1.735)
        self.assertEqual((a['lowerFlightRisers'],a['upperFlightRisers']),(9,9))
        self.assertAlmostEqual(a['lowerTreadRunM'],2.24)

    def test_eighteen_does_not_fix_footprint(self):
        a=evaluate(.28,1.96,.90,.89)
        self.assertFalse(a['planFitsWithoutChangingHallOrLanding'])
        self.assertAlmostEqual(a['landingIfHallPreservedM'],.62)

    def test_thirty_centimetre_hypothesis(self):
        a=evaluate(.30,1.96,.90,.89)
        self.assertAlmostEqual(a['extraRunM'],.44)
        self.assertAlmostEqual(a['geometry']['twoRisersPlusTreadM'],.6366666666666667)


if __name__=='__main__':unittest.main()
