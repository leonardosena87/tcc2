import copy
import unittest
from decimal import Decimal as D
from auditar import isolated,HERE,r136

class IsolationGuards(unittest.TestCase):
    def models(self):
        return r136.models(HERE/'SAP-CAD'),r136.models(HERE.parent/'h03-r137/SAP-CAD')

    def test_control_contamination_is_rejected(self):
        control,wall=self.models()
        control=copy.deepcopy(control)
        control['N1']['data']['tables']['JOINT LOADS - FORCE']=[copy.deepcopy(wall['N1']['data']['tables']['JOINT LOADS - FORCE'][0])]
        with self.assertRaisesRegex(ValueError,'Controle contém'):isolated(control,wall)

    def test_other_load_pattern_is_rejected(self):
        control,wall=self.models()
        wall=copy.deepcopy(wall)
        wall['N1']['data']['tables']['JOINT LOADS - FORCE'][0]['LoadPat']='QT'
        with self.assertRaisesRegex(ValueError,'Outra ação'):isolated(control,wall)

    def test_small_force_residual_does_not_establish_moment_equality(self):
        control,wall=self.models()
        _,_,result,portico=isolated(control,wall)
        self.assertEqual(D(result['centroidDistanceCm']),0)
        self.assertLess(abs(D(portico['differenceFromN1Forces']['FzKgf'])),D('0.001'))
        self.assertNotEqual(D(portico['differenceFromN1Forces']['MxKgfCm']),0)
        self.assertNotEqual(D(portico['differenceFromN1Forces']['MyKgfCm']),0)
        self.assertFalse(portico['EberickInternalAxesProvenEquivalent'])

if __name__=='__main__':unittest.main()
