"""Controles de unidades e campos ausentes; requer runtime Python3.12/IfcOpenShell."""
import unittest
from auditar_ifc import cover_fields,pressure_mpa,ifcopenshell


class Information(unittest.TestCase):
    def model(self):
        m=ifcopenshell.file(schema='IFC4')
        unit=m.create_entity('IfcSIUnit',UnitType='PRESSUREUNIT',Name='PASCAL')
        assignment=m.create_entity('IfcUnitAssignment',Units=[unit])
        m.create_entity('IfcProject',GlobalId=ifcopenshell.guid.new(),UnitsInContext=assignment)
        return m

    def test_pressure_uses_project_unit_and_not_material_name(self):
        m=self.model();p=m.create_entity('IfcPropertySingleValue',Name='resistencia',NominalValue=m.create_entity('IfcPressureMeasure',25e6))
        self.assertEqual(pressure_mpa(p,m),25)

    def test_explicit_megapascals_are_not_converted_twice(self):
        m=self.model();unit=m.create_entity('IfcSIUnit',UnitType='PRESSUREUNIT',Name='PASCAL',Prefix='MEGA')
        p=m.create_entity('IfcPropertySingleValue',Name='resistencia',NominalValue=m.create_entity('IfcPressureMeasure',25),Unit=unit)
        self.assertEqual(pressure_mpa(p,m),25)

    def test_wrong_measure_not_accepted_as_strength(self):
        m=self.model();p=m.create_entity('IfcPropertySingleValue',Name='resistencia',NominalValue=m.create_entity('IfcLengthMeasure',25))
        with self.assertRaises(ValueError):pressure_mpa(p,m)

    def test_missing_cover_never_becomes_zero_or_approved(self):
        result=cover_fields({},30)
        self.assertFalse(result['allThreeMatch'])
        self.assertEqual(result['fields'],[])

    def test_same_three_field_names_do_not_conceal_wrong_value(self):
        p={'Estrutural':{'Recobrimento superior':'II. <30 mm>','Recobrimento inferior':'II. <30 mm>','Recobrimento outras':'I. <25 mm>'}}
        self.assertFalse(cover_fields(p,30)['allThreeMatch'])
        p['Estrutural']['Recobrimento outras']='II. <30 mm>'
        self.assertTrue(cover_fields(p,30)['allThreeMatch'])


if __name__=='__main__':unittest.main()
