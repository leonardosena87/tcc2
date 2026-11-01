import copy
import json
import unittest
from pathlib import Path
from consolidar import normalize_tables, literal_check


class ReportControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real = json.loads((Path(__file__).parent / 'R107-resultado.json').read_text(encoding='utf-8'))

    def test_direction_discrepancy_not_erased_by_equal_tables(self):
        b = self.real['branches']
        self.assertEqual(normalize_tables(b['CAD']['tablesNative'], 'CAD'), normalize_tables(b['BIM']['tablesNative'], 'BIM'))
        for branch in ['CAD', 'BIM']:
            check = literal_check(b[branch]['tablesNormalized'], b[branch]['summary']['relative'], branch)
            self.assertFalse(check['sameLabelDisplayedValueMatches'])
            self.assertFalse(check['softwareBugDemonstrated'])

    def test_unknown_floor_or_reordered_directions_rejected(self):
        source = self.real['branches']['BIM']['tablesNative']
        unknown = copy.deepcopy(source)
        unknown[2][3][0] = 'OUTRO-N1'
        reordered = copy.deepcopy(source)
        reordered[2][1][1:3] = ['Vento X-', 'Vento X+']
        for tables in [unknown, reordered, source[:-1]]:
            with self.subTest(tables=tables), self.assertRaises(ValueError):
                normalize_tables(tables, 'BIM')


if __name__ == '__main__':
    unittest.main()
