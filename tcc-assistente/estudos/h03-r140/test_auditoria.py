"""Protege comparação de rótulos contra renomeação e dados incompletos."""
import tempfile
import unittest
from pathlib import Path
from auditar import HERE, OUT, compare

BASE = HERE if (HERE/'CAD-W20-reacoes-N1-G2.dxf').exists() else OUT

class ReactionDiagramAudit(unittest.TestCase):
    def test_paired_actual_exports_match_despite_beam_renumbering(self):
        for case in ['W20','controle']:
            with self.subTest(case=case):
                report=compare(BASE/f'CAD-{case}-reacoes-N1-G2.dxf',BASE/f'BIM-{case}-reacoes-N1-G2.dxf')
                self.assertEqual(report['changedLabelCount'],0)
                self.assertEqual(report['numericLabelCount'],25)

    def test_signed_numeric_change_is_not_hidden_by_equal_counts(self):
        source=BASE/'CAD-W20-reacoes-N1-G2.dxf'
        raw=source.read_text(encoding='utf-8-sig')
        self.assertEqual(raw.count('\n-0.77\n'),1)
        with tempfile.TemporaryDirectory() as td:
            edited=Path(td)/'signed-change.dxf'
            edited.write_text(raw.replace('\n-0.77\n','\n0.77\n'),encoding='utf-8')
            report=compare(source,edited)
            self.assertEqual(report['changedLabelCount'],1)
            self.assertEqual(report['maxAbsDeltaDisplayed'],'1.54')

    def test_missing_result_label_rejects_partial_diagram(self):
        source=BASE/'CAD-W20-reacoes-N1-G2.dxf'
        raw=source.read_text(encoding='utf-8-sig')
        with tempfile.TemporaryDirectory() as td:
            edited=Path(td)/'partial.dxf'
            edited.write_text(raw.replace('\n-0.77\n','\nSEM_RESULTADO\n'),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'incompleto'):
                compare(source,edited)

if __name__ == '__main__':
    unittest.main()
