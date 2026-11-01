import json
import unittest
from pathlib import Path
from consolidar import extract, r106


class SummaryControls(unittest.TestCase):
    def test_real_readbacks_keep_direction_disagreement(self):
        root = Path(__file__).parent
        cad = extract((root/'CAD-resumo-analise-UI.txt').read_text(encoding='utf-8'))
        bim = extract((root/'BIM-resumo-analise-UI.txt').read_text(encoding='utf-8'))
        self.assertEqual(cad['verticalLoadsDisplayedTf']['Total'], 104.44)
        self.assertEqual(cad['verticalLoadsDisplayedTf'], bim['verticalLoadsDisplayedTf'])
        self.assertEqual(cad['relative']['direction'], 'Y-')
        self.assertEqual(bim['relative']['direction'], 'Y+')
        self.assertFalse(r106.comparison(cad, bim)['relativeCriticalDirectionEqual'])

    def test_missing_load_or_duplicate_direction_rejected(self):
        text = (Path(__file__).parent/'CAD-resumo-analise-UI.txt').read_text(encoding='utf-8')
        for changed in [text.replace('Total = 104.44 tf', 'Total = desconhecido'),
                        text.replace('X- = 1.08 (limite 1.10)', 'X+ = 1.08 (limite 1.10)')]:
            with self.assertRaises(ValueError):
                extract(changed)


if __name__ == '__main__':
    unittest.main()
