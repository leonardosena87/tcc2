import unittest
from pathlib import Path
from consolidar import extract, check_time, OUT


class SummaryControls(unittest.TestCase):
    def test_actual_evidence_keeps_critical_direction_and_small_differences(self):
        cad, bim = [extract((OUT / f'{b}-resumo-analise-UI.txt').read_text(encoding='utf-8')) for b in ['CAD', 'BIM']]
        self.assertEqual(cad['verticalLoadsDisplayedTf'], bim['verticalLoadsDisplayedTf'])
        self.assertEqual(cad['verticalLoadsDisplayedTf']['Total'], 105.14)
        self.assertNotEqual(cad['relative']['direction'], bim['relative']['direction'])
        self.assertNotEqual(cad['topDisplacementsRawUnitNotExplicit']['Vento X+'],
                            bim['topDisplacementsRawUnitNotExplicit']['Vento X+'])

    def test_incomplete_top_and_outside_timing_rejected(self):
        text = (OUT / 'CAD-resumo-analise-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):
            extract(text.replace('Vento X+:', 'Caso desconhecido:'))
        session = {'wallMs': 10, 'start': {'mono': 0}, 'end': {'mono': 10}}
        check_time(session, {'durationMs': 2, 'start': {'mono': 2}, 'end': {'mono': 4}})
        with self.assertRaises(ValueError):
            check_time(session, {'durationMs': 9, 'start': {'mono': 2}, 'end': {'mono': 11}})


if __name__ == '__main__':
    unittest.main()
