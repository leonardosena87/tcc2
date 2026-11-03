import unittest
from consolidar_leitura import compare_displayed


def envelope(a='41.49', b='46.30', neg='-36.90'):
    return dict(initialShearMagnitudeKn=a, finalShearMagnitudeKn=b, positiveMdKnM='32.22',
        negativeMdKnM=neg, torsionEnvelopeMagnitudeKnM='0.05')


class EnvelopeTests(unittest.TestCase):
    def test_orientation_must_be_applied_before_matching(self):
        a, b = envelope(), envelope('46.30', '41.49')
        self.assertFalse(compare_displayed(a, b, False)['equalAtDisplayedPrecision'])
        r = compare_displayed(a, b, True)
        self.assertTrue(r['equalAtDisplayedPrecision'])
        self.assertTrue(r['exactInternalEqualityOrControllingCombinationNotVerified'])

    def test_negative_moment_sign_is_not_erased(self):
        self.assertFalse(compare_displayed(envelope(), envelope(neg='36.90'), False)['equalAtDisplayedPrecision'])

    def test_one_display_unit_difference_is_not_tolerated_away(self):
        self.assertFalse(compare_displayed(envelope(), envelope(neg='-36.91'), False)['equalAtDisplayedPrecision'])

    def test_missing_value_is_not_replaced_by_zero(self):
        bad = envelope()
        del bad['positiveMdKnM']
        with self.assertRaises(ValueError):
            compare_displayed(envelope(), bad, False)

    def test_non_finite_value_rejected(self):
        with self.assertRaises(ValueError):
            compare_displayed(envelope(), envelope(neg='NaN'), False)


if __name__ == '__main__':
    unittest.main()
