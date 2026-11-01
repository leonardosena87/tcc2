import unittest
from consolidar import IDS, read_fields

class EvidenceControls(unittest.TestCase):
    def test_missing_and_conflicting_values_rejected(self):
        raw = '\n'.join(f'1 editar (settable, string) Value: x ID: {i}' for i in IDS)
        self.assertEqual(len(read_fields(raw + '\n' + raw)), len(IDS))
        for bad in [raw.split('\n', 1)[1], raw + '\n2 editar (settable, string) Value: y ID: 801']:
            with self.assertRaises(ValueError):
                read_fields(bad)

if __name__ == '__main__':
    unittest.main()
