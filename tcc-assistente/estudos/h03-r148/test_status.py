import unittest
from consolidar import OUT,parse_status


class StatusTests(unittest.TestCase):
    def test_actual_bim_error_preserved(self):
        t=(OUT/'BIM-erros-N1-V2-UI.txt').read_text(encoding='utf-8')
        r=parse_status(t,'BIM')
        self.assertEqual(r['N1','Viga(s)','com erro(s)'],1)
        self.assertIn('Erro D16 - Erro na armadura negativa (nó 2)',t)

    def test_cad_and_bim_piece_counts_are_different(self):
        cad=parse_status((OUT/'CAD-status-N1-vigas-UI.txt').read_text(encoding='utf-8'),'CAD')
        bim=parse_status((OUT/'BIM-erros-N1-V2-UI.txt').read_text(encoding='utf-8'),'BIM')
        self.assertEqual(cad['N1','Viga(s)','dimensionada(s)'],14)
        self.assertEqual(bim['N1','Viga(s)','dimensionada(s)'],10)

    def test_wrong_project_rejected(self):
        t=(OUT/'BIM-erros-N1-V2-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):parse_status(t,'CAD')


if __name__=='__main__':unittest.main()
