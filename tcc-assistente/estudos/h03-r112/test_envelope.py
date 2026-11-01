import unittest
from envelope import envelope, linear_height


class EnvelopeControls(unittest.TestCase):
    def test_minimum_occurs_at_low_end_not_at_center_or_parapet(self):
        line=[[6.6, .9], [9.6, 1.2]]
        r=envelope(8.1,1.23,.68,line)
        self.assertAlmostEqual(r['optimisticVerticalClearanceM'],.3085)
        self.assertLess(r['optimisticVerticalClearanceM'],linear_height(8.1,line)-.68)
        self.assertIsNone(r['effectiveClearanceM'])
        self.assertAlmostEqual(envelope(8.1,1.23,.68,line,.1)['effectiveClearanceM'],.2085)

    def test_extrapolation_and_invalid_geometry_are_rejected(self):
        line=[[6.6,.9],[9.6,1.2]]
        for args in [(6.7,1,.68,line),(8.1,-1,.68,line),(8.1,1,.68,line,-.1),
                     (float('nan'),1,.68,line)]:
            with self.assertRaises(ValueError): envelope(*args)


if __name__=='__main__': unittest.main()
