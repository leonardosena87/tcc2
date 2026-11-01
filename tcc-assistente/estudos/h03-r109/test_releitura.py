"""Controles do extrator: unidade/componentes reais, acao e sinal obrigatorios."""
import unittest
from consolidar import vector, verify_expected, EXPECTED


def sample(action, components):
    return 'caixa de combinação (settable, string) Ação Value: ' + action + ' ID: 115\n' + '\n'.join(
        f'editar (settable, string) {c} Value: {v} ID: 108' for c, v in components.items())


class ReadbackTest(unittest.TestCase):
    def test_rejects_wrong_action_missing_component_and_conflicting_duplicate(self):
        text = sample('Q_TELHADO_MANUTENCAO', EXPECTED['QT'])
        self.assertEqual(vector(text + '\n' + text, 'QT'), EXPECTED['QT'])
        for invalid in [text.replace('Q_TELHADO_MANUTENCAO', 'Adicional'),
                        text.replace('My Value:', 'Outro Value:'),
                        text + '\neditar (settable, string) Fz Value: 0 ID: 108']:
            with self.assertRaises(ValueError):
                vector(invalid, 'QT')

    def test_force_without_eccentric_moment_or_wrong_sign_fails(self):
        verify_expected(EXPECTED['G'], 'G')
        for changed in [{**EXPECTED['G'], 'My': 0}, {**EXPECTED['G'], 'Fz': 0.521164}]:
            with self.assertRaises(ValueError):
                verify_expected(changed, 'G')


if __name__ == '__main__':
    unittest.main()
