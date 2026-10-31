"""Controles sinteticos do auditor; nao sao ensaios dentro do Eberick."""
from pathlib import Path
import tempfile
import unittest
from conferir_qt import build_plan, check_native, parse_native, audit_reads

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent


def plan():
    return build_plan(STUDIES/'h03-r65/R65-plano-Q.json', STUDIES/'h03-r64/R64-leituras-CAD.json',
                      STUDIES/'h03-r64/R64-leituras-BIM.json')


def fixture(action='Q_TELHADO_MANUTENCAO', fz='-1.0725'):
    lines = ['Window: 15-H03-R98-BIM-QT-NAO-EXECUTAR', f'Ação Value: {action} ID: 115']
    for key, value in [('X','110'), ('Y','0'), ('Fx','0'), ('Fy','0'), ('Fz',fz), ('Mx','0'), ('My','0'), ('Mz','0')]:
        lines.append(f'  1 editar (settable, string) {key} Value: {value} ID: 108')
        if key not in ('X','Y'):
            lines.append('  2 text ' + ('kN' if key.startswith('F') else 'kN.m') + ' ID: 107')
    return '\n'.join(lines)


class Checks(unittest.TestCase):
    def test_equilibrio_e_arredondamento_dados_reais(self):
        p = plan()
        self.assertEqual(len(p['rows']),13)
        self.assertAlmostEqual(p['analyticalDownKN'],13.985625,places=9)
        self.assertAlmostEqual(p['enteredDownKN'],13.985628,places=9)
        self.assertFalse(p['nativeLoadsAppliedByThisScript'])
        self.assertFalse(p['fullFlowRankingAllowed'])

    def test_leitura_valida_e_duplicacao_identica_da_arvore(self):
        t=fixture()
        self.assertTrue(check_native(t+'\n'+t,plan()['rows'][0],'QT','BIM')['matched'])

    def test_recusa_acao_coordenada_ramo_sinal_e_carga_zero(self):
        for text, branch in [(fixture('Adicional'),'BIM'),(fixture().replace('X Value: 110','X Value: 330'),'BIM'),
                             (fixture(),'CAD'),(fixture(fz='1.0725'),'BIM'),(fixture(fz='0'),'BIM')]:
            with self.subTest(text=text,branch=branch), self.assertRaises(ValueError):
                check_native(text,plan()['rows'][0],'QT',branch)

    def test_recusa_unidades_trocadas_ausentes_e_componentes_extras(self):
        for text in (fixture().replace('text kN ID:', 'text tf ID:'),
                     fixture().replace('text kN.m ID:', 'text tf.m ID:'),
                     fixture().replace('Fx Value: 0','Fx Value: 1'),
                     fixture().replace('Fz Value: -1.0725','Fz Value: NaN')):
            with self.subTest(text=text), self.assertRaises((ValueError,ArithmeticError)):
                check_native(text,plan()['rows'][0],'QT','BIM')

    def test_recusa_ambiguidade_e_campo_ausente(self):
        for text in (fixture()+'\nFz Value: 0',fixture().replace('Y Value:','Outro Value:')):
            with self.assertRaises(ValueError): parse_native(text)

    def test_g_preservado_precisao_nativa_e_desvio(self):
        point=plan()['rows'][0]
        self.assertTrue(check_native(fixture('Adicional','-1.41955'),point,'G','BIM')['matched'])
        with self.assertRaises(ValueError): check_native(fixture('Adicional','-1.4195'),point,'G','BIM')

    def test_ausencia_e_rejeicao_nao_viram_aprovacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=plan(); result=audit_reads(p,tmp)
            self.assertEqual(result['pendingReadings'],52)
            self.assertFalse(result['allReadingsMatched'])
            Path(tmp,'BIM-RC01-QT-apos-reabrir-UI.txt').write_text(fixture(fz='0'),encoding='utf-8')
            result=audit_reads(p,tmp)
            self.assertEqual(result['rejectedReadings'],1)
            self.assertEqual(result['matchedReadings'],0)
            self.assertFalse(result['saveReopenSequenceProvenByTextAlone'])


if __name__ == '__main__': unittest.main()
