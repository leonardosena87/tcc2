import unittest
from pathlib import Path
from consolidar import parse, expected, KEYS


class ConsultaTest(unittest.TestCase):
    def test_real_readings_match_reference(self):
        for branch in ['CAD', 'BIM']:
            for floor, name in KEYS:
                text = (Path(__file__).parent / f'{branch}-{floor}-{name}-UI.txt').read_text(encoding='utf-8')
                self.assertEqual(parse(text, branch, floor, name), expected(floor, name))

    def test_wrong_identity_and_conflicting_value_rejected(self):
        text = (Path(__file__).parent / 'CAD-N1-L1-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):
            parse(text, 'BIM', 'N1', 'L1')
        with self.assertRaises(ValueError):
            parse(text, 'CAD', 'N2', 'L1')
        with self.assertRaises(ValueError):
            parse(text + '\neditar (settable, string) Acidental Value: 99 ID: 562', 'CAD', 'N1', 'L1')


if __name__ == '__main__':
    unittest.main()
