import unittest
from types import SimpleNamespace
from unittest.mock import patch
from preparar_niveis import plan_levels


class Product:
    def __init__(self,kind):self.kind=kind
    def is_a(self):return self.kind


class Model:
    def __init__(self,elevations=(0,170,200,220,1774.1176470588232,3000,3200,3250,6390)):
        self.levels=[SimpleNamespace(Elevation=e,GlobalId=str(i),Name='Level'+str(i)) for i,e in enumerate(elevations)]
        self.rels=[]
    def by_type(self,kind):return self.levels if kind=='IfcBuildingStorey' else self.rels


class LevelGuardTests(unittest.TestCase):
    def run_plan(self,model):
        with patch('preparar_niveis.calculate_unit_scale',return_value=.001):return plan_levels(model)
    def test_rejects_missing_and_duplicate_primary_levels(self):
        for value in (201,3200):
            m=Model();m.levels[2].Elevation=value
            with self.assertRaises(ValueError):self.run_plan(m)
    def test_rejects_unexpected_number_of_levels(self):
        with self.assertRaises(ValueError):self.run_plan(Model([200,3200,6390]))
    def test_remaps_only_observed_auxiliary_contents(self):
        m=Model()
        for i,kind in ((1,'IfcStair'),(4,'IfcBeam')):
            m.rels.append(SimpleNamespace(RelatingStructure=m.levels[i],RelatedElements=[Product(kind)]))
        keep,old,remap=self.run_plan(m)
        self.assertEqual(len(old),6)
        self.assertEqual([r[1] for r in remap],[keep['N0'],keep['N1']])
    def test_refuses_automatic_distribution_of_unexpected_elements(self):
        m=Model();m.rels=[SimpleNamespace(RelatingStructure=m.levels[4],RelatedElements=[Product('IfcColumn')])]
        with self.assertRaises(ValueError):self.run_plan(m)


if __name__=='__main__':unittest.main()
