"""Controles negativos do validador; não simulam sucesso dentro do Revit."""
import copy
import unittest
from consolidar import validate

class ReadbackGuard(unittest.TestCase):
    def setUp(self):self.row=dict(TotalRisers=17,Runs=[dict(Risers=9),dict(Risers=8)],Landings=[dict(FinishedM=.22+9*3.03/17)],BaseM=.22,TopM=3.25,RiserM=3.03/17,TreadM=.28,StructuralApproval=False,SupportAndGuardDesignCompleted=False)
    def test_uniform_boundary_fixture_accepted(self):validate(self.row)
    def test_eight_plus_nine_or_nonseventeen_rejected(self):
        for counts in ([8,9],[9,9]):
            row=copy.deepcopy(self.row);row['Runs']=[dict(Risers=r) for r in counts]
            with self.assertRaises(ValueError):validate(row)
    def test_small_real_geometry_error_rejected(self):
        for key in ('BaseM','TopM','RiserM','TreadM'):
            row=copy.deepcopy(self.row);row[key]+=.001
            with self.assertRaises(ValueError):validate(row)
    def test_nonfinite_rejected(self):
        for value in (float('nan'),float('inf')):
            row=copy.deepcopy(self.row);row['RiserM']=value
            with self.assertRaises(ValueError):validate(row)
    def test_wrong_landing_and_unsupported_approval_rejected(self):
        row=copy.deepcopy(self.row);row['Landings'][0]['FinishedM']=1.646
        with self.assertRaises(ValueError):validate(row)
        self.row['StructuralApproval']=True
        with self.assertRaises(ValueError):validate(self.row)
if __name__=='__main__':unittest.main()
