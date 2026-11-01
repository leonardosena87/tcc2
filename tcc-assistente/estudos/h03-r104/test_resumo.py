import unittest
from consolidar import summary

class EvidenceControls(unittest.TestCase):
    def test_missing_and_contradictory_summaries_rejected(self):
        for text in ['', 'editar Value: Cargas verticais: x\neditar Value: Cargas verticais: y', 'editar Value: Cargas verticais: x']:
            with self.assertRaises(ValueError):
                summary(text)

if __name__ == '__main__':
    unittest.main()
