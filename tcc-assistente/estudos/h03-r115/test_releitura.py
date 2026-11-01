import unittest
from consolidar import verify, expected, vector


class P2Readback(unittest.TestCase):
    def test_display_rounding_and_preserved_moment(self):
        verify({**expected('RP2-01', 'G'), 'Fz': -1.00014}, 'RP2-01', 'G')
        verify({**expected('RP2-04', 'QT'), 'Fz': -1.14938}, 'RP2-04', 'QT')
        for invalid in [{**expected('RP2-04', 'G'), 'My': 0},
                        {**expected('RP2-04', 'G'), 'Fz': -1.000138},
                        {**expected('RP2-04', 'G'), 'Fz': 1.521302}]:
            with self.assertRaises(ValueError):
                verify(invalid, 'RP2-04', 'G')

    def test_missing_or_ambiguous_action_and_component_rejected(self):
        text = 'caixa de combinação (settable, string) Ação Value: Adicional ID: 115\n' + '\n'.join(
            f'editar (settable, string) {c} Value: {v} ID: 108' for c, v in expected('RP2-01', 'G').items())
        self.assertEqual(vector(text, 'G'), expected('RP2-01', 'G'))
        for invalid in [text.replace('Adicional', 'Solo'), text.replace('Mx Value:', 'Outro Value:'),
                        text + '\neditar (settable, string) Fz Value: 0 ID: 108']:
            with self.assertRaises(ValueError):
                vector(invalid, 'G')


if __name__ == '__main__':
    unittest.main()
