import unittest
from consolidar_materiais import controls


class EvidenceControls(unittest.TestCase):
    def test_duplicacao_identica_e_aceita_sem_usar_indices_efemeros(self):
        text='10 editar (settable, string) fck Value: 25 ID: 303\n999 editar (settable, string) fck Value: 25 ID: 303\n'
        self.assertEqual(controls(text,[303]),{'303':'25'})

    def test_ausencia_e_conflito_sao_recusados(self):
        for text in ('', '10 editar fck Value: 25 ID: 303\n11 editar fck Value: 30 ID: 303'):
            with self.assertRaises(ValueError):
                controls(text,[303])

    def test_texto_estatico_nao_substitui_controle_editavel(self):
        with self.assertRaises(ValueError):
            controls('10 text fck Value: 25 ID: 303',[303])


if __name__=='__main__':
    unittest.main()
