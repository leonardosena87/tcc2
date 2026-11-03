import copy, json, unittest
from pathlib import Path
import auditar_cobertura as audit

class CoverageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=audit.read(audit.OUT/'R175-preparacao-plano.json')['rows']
        cls.before=audit.sap.parse((audit.OUT/'analitico-apos-regenerar/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))
        cls.after=audit.sap.parse((audit.OUT/'analitico-cargas-final/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))

    def test_actual_export_has_26_vectors_and_explicit_other_load_differences(self):
        result=audit.audit_models(self.before,self.after,self.plan)
        self.assertEqual(result['checkedComponents'],156)
        self.assertFalse(result['otherExportedLoadRowsUnchanged'])
        self.assertEqual(len(result['rawLoadChanges']['jointRowsOutsideTargetNodes']['removed']),2)

    def test_duplicate_vector_is_rejected(self):
        model=copy.deepcopy(self.after)
        row=next(r for r in model['tables']['JOINT LOADS - FORCE'] if r['Joint']=='33' and r['LoadPat']=='QT')
        model['tables']['JOINT LOADS - FORCE'].append(copy.deepcopy(row))
        with self.assertRaises(ValueError):audit.audit_models(self.before,model,self.plan)

    def test_wrong_action_and_force_sign_are_rejected(self):
        for field,value in [('LoadPat','Q'),('F3','107,2500')]:
            with self.subTest(field=field):
                model=copy.deepcopy(self.after)
                row=next(r for r in model['tables']['JOINT LOADS - FORCE'] if r['Joint']=='33' and r['LoadPat']=='QT')
                row[field]=value
                with self.assertRaises(ValueError):audit.audit_models(self.before,model,self.plan)

    def test_stale_export_and_unrelated_section_change_are_rejected(self):
        stale=audit.sap.parse((audit.OUT/'analitico-nos-sem-cargas/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))
        with self.assertRaises(ValueError):audit.audit_models(stale,self.after,self.plan)
        model=copy.deepcopy(self.after)
        model['tables']['FRAME SECTION ASSIGNMENTS'][0]['AnalSect']='UNEXPECTED'
        with self.assertRaises(ValueError):audit.audit_models(self.before,model,self.plan)

if __name__=='__main__':unittest.main()
