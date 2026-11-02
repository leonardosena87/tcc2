import copy
import unittest
from pathlib import Path
from auditar import distributed,r122

class NativeExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=r122.parse((Path(__file__).parent/'SAP-CAD/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))

    def test_real_export_does_not_pass_as_free_wall(self):
        result=distributed(self.model)
        self.assertFalse(result['matchesPhysicalFreeInterval'])
        self.assertEqual(result['loadedLengthCm'],'384.0')
        self.assertEqual(result['overrunAtEachEndCm'],['12.0','12.0'])
        self.assertEqual(result['signedIntegralLocal2Kgf'],'-1712.71680')

    def test_duplicate_distributed_load_is_rejected(self):
        model=copy.deepcopy(self.model)
        row=next(r for r in model['tables']['FRAME LOADS - DISTRIBUTED'] if r['LoadPat']=='G2')
        model['tables']['FRAME LOADS - DISTRIBUTED'].append(row.copy())
        with self.assertRaises(ValueError):distributed(model)

    def test_wrong_axis_cannot_be_interpreted_as_this_load(self):
        model=copy.deepcopy(self.model)
        next(r for r in model['tables']['FRAME LOADS - DISTRIBUTED'] if r['LoadPat']=='G2')['Dir']='3'
        with self.assertRaises(ValueError):distributed(model)

if __name__=='__main__':unittest.main()
