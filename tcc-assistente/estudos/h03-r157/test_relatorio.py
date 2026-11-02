import unittest
from pathlib import Path
from consolidar import parse_report,OUT

class NativeReportGuard(unittest.TestCase):
    def setUp(self):
        self.html=(OUT/'R157-interferencias-nativas.html').read_text(encoding='utf-8')
        self.project=str(OUT/'H03-R157-Revit-ESCADA17-VISUAL-NAO-EXECUTAR.rvt')
    def test_actual_native_report_identifies_five_unique_pairs(self):
        rows=parse_report(self.html,self.project)
        self.assertEqual({r['otherMark'] for r in rows},{'P4-N1','P10-N1','V13-N1','V15-N1','L6-N1'})
        self.assertEqual(len(rows),5)
    def test_wrong_project_and_truncated_report_rejected(self):
        with self.assertRaises(ValueError):parse_report(self.html,self.project.replace('R157','R155'))
        with self.assertRaises(ValueError):parse_report(self.html.replace('Fim do relatório de interferência',''),self.project)
    def test_stair_identity_change_rejected(self):
        with self.assertRaises(ValueError):parse_report(self.html.replace('ID 473597','ID 473598'),self.project)
    def test_duplicate_native_pair_rejected(self):
        changed=self.html.replace('ID 473097','ID 472933').replace('Marca P10-N1','Marca P4-N1')
        with self.assertRaises(ValueError):parse_report(changed,self.project)

if __name__=='__main__':unittest.main()
