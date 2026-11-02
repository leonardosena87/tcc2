import unittest
from consolidar import OUT, check_time, extract, read_summary


class Summaries(unittest.TestCase):
    def test_actual_pair_keeps_direction_difference(self):
        cad, bim = [read_summary(b) for b in ('CAD','BIM')]
        expected = {'Peso próprio':75.69,'Adicional':12.04,'Acidental':17.11,
                    'Q_TELHADO_MANUTENCAO':1.78,'Total':106.62}
        self.assertEqual(cad['verticalLoadsDisplayedTf'], expected)
        self.assertEqual(bim['verticalLoadsDisplayedTf'], expected)
        self.assertEqual(cad['relative']['direction'], 'Y-')
        self.assertEqual(bim['relative']['direction'], 'Y+')

    def test_reject_incomplete_summary(self):
        text = (OUT / 'CAD-resumo-analise-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):
            extract(text.replace('Adicional = 12.04 tf', 'Adicional indisponivel'))

    def test_reject_processing_outside_session(self):
        with self.assertRaises(ValueError):
            check_time(dict(start={'mono':1},end={'mono':5},wallMs=4),
                       dict(start={'mono':2},end={'mono':6},durationMs=4))


if __name__ == '__main__':
    unittest.main()
