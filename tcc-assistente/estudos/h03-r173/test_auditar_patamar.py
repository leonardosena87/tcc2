import copy
import unittest
from pathlib import Path
from auditar_patamar import compare, sap, OUT

class AnalyticalCorrectionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.before=sap.parse((OUT/'analitico-antes/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))
  cls.after=sap.parse((OUT/'analitico-depois/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))
 def test_real_correction_and_continuous_columns(self):
  r=compare(self.before,self.after)
  self.assertEqual(r['verticalColumnPositions'],11)
  self.assertTrue(r['beamConnectedThroughRigidLinksToContinuousColumns'])
  self.assertFalse(r['jointForcesAtGlobalPositionsEqual'])
 def test_unchanged_model_is_rejected(self):
  with self.assertRaises(ValueError):compare(self.before,self.before)
 def test_disconnected_joint_is_rejected(self):
  changed=copy.deepcopy(self.after)
  row=next(r for r in changed['tables']['CONNECTIVITY - FRAME'] if r['Frame']=='23')
  row['JointI']='1'
  with self.assertRaises(ValueError):compare(self.before,changed)
 def test_unrequested_column_position_is_rejected(self):
  changed=copy.deepcopy(self.after)
  changed['frames']['extra']=((100.,100.,20.),(100.,100.,320.))
  with self.assertRaises(ValueError):compare(self.before,changed)

if __name__=='__main__':unittest.main()
