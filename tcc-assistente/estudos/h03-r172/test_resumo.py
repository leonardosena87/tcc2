import unittest
from pathlib import Path
from consolidar import extract,OUT

class Evidencias(unittest.TestCase):
    def test_parcelas_reais_e_ausencia_de_qt(self):
        cad=extract((OUT/'CAD-resumo-analise.txt').read_text(encoding='utf-8'),'CAD')
        bim=extract((OUT/'BIM-resumo-analise.txt').read_text(encoding='utf-8'),'BIM')
        self.assertEqual(cad['verticalLoadsDisplayedTf']['Total'],106.51)
        self.assertEqual(bim['verticalLoadsDisplayedTf']['Total'],102.38)
        self.assertIsNone(bim['verticalLoadsDisplayedTf']['Q_TELHADO_MANUTENCAO'])
        self.assertEqual(cad['relativeDisplayed']['direction'],'Y-')
        self.assertEqual(bim['relativeDisplayed']['direction'],'Y+')
    def test_projeto_incorreto_rejeitado(self):
        with self.assertRaises(ValueError):extract((OUT/'BIM-resumo-analise.txt').read_text(encoding='utf-8'),'CAD')
    def test_contradicao_rejeitada(self):
        s=(OUT/'BIM-resumo-analise.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):extract(s+s.replace('102.38 tf','103.38 tf'),'BIM')

if __name__=='__main__':unittest.main()
