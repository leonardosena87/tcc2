import unittest
from consolidar import OUT, expected, parse


class NativeReadings(unittest.TestCase):
    def test_all_before_and_post_save_records(self):
        for branch in ('CAD', 'BIM'):
            for i in range(1, 7):
                name = f'L{i}'
                for stage in (['antes', 'reaberta'] if i <= 4 else ['controle']):
                    text = (OUT / f'{branch}-N1-{name}-{stage}-UI.txt').read_text(encoding='utf-8')
                    self.assertEqual(parse(text, branch, name), expected(name, stage != 'antes'))

    def test_reject_wrong_project_and_slab(self):
        text = (OUT / 'CAD-N1-L1-reaberta-UI.txt').read_text(encoding='utf-8')
        for branch, name in [('BIM','L1'), ('CAD','L2')]:
            with self.assertRaises(ValueError):
                parse(text, branch, name)

    def test_reject_conflicting_reading(self):
        text = (OUT / 'CAD-N1-L1-reaberta-UI.txt').read_text(encoding='utf-8')
        text += '\n999 editar (settable, string) Revestimento Value: 1 ID: 561\n'
        with self.assertRaises(ValueError):
            parse(text, 'CAD', 'L1')


if __name__ == '__main__':
    unittest.main()
