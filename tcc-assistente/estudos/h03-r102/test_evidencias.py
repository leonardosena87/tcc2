import unittest
from consolidar import EXPECTED, read_combinations

class EvidenceControls(unittest.TestCase):
    def test_duplicate_equal_readback_is_accepted(self):
        text = '\n'.join(f'1 text {v} ID: {k}' for k, v in EXPECTED.items())
        self.assertEqual(read_combinations(text + '\n' + text), EXPECTED)

    def test_missing_or_zero_qt_is_rejected(self):
        for text in ['', '1 text G1+G2+Q+A ID: 1016', '\n'.join(f'1 text {v} ID: {k}' for k, v in EXPECTED.items()) + '\n2 text G1+G2+Q+A ID: 1016']:
            with self.assertRaises(ValueError):
                read_combinations(text)

if __name__ == '__main__':
    unittest.main()
