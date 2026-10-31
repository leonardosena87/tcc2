"""Casos IFC sinteticos em memoria; nao substituem verificacao dentro do Revit/Eberick."""
import copy
import unittest
import ifcopenshell
from auditar_intercambio import inspect_model, numeric_property


def fixture(value=25e6, unit=True, material_name='Concreto do teste'):
    model = ifcopenshell.file(schema='IFC2X3')
    pascal = model.create_entity('IfcSIUnit', UnitType='PRESSUREUNIT', Name='PASCAL')
    units = model.create_entity('IfcUnitAssignment', Units=[pascal])
    model.create_entity('IfcProject', GlobalId=ifcopenshell.guid.new(), UnitsInContext=units)
    material = model.create_entity('IfcMaterial', Name=material_name)
    obj = model.create_entity('IfcColumn', GlobalId=ifcopenshell.guid.new(), Tag='1')
    model.create_entity('IfcRelAssociatesMaterial', GlobalId=ifcopenshell.guid.new(),
                        RelatedObjects=[obj], RelatingMaterial=material)
    props = []
    if value is not None:
        prop = model.create_entity('IfcPropertySingleValue', Name='Compressão do concreto',
                                  NominalValue=model.create_entity('IfcPressureMeasure', value))
        props.append(prop)
        model.create_entity('IfcExtendedMaterialProperties', Material=material, Name='Structural', ExtendedProperties=props)
    if not unit:
        units.Units = []
    native = dict(elements=[dict(id='1', categoryId='-2001330', structuralMaterialId='10')],
                  materials=[dict(id='10', name='Concreto do teste', asset=dict(
                      concreteCompression=dict(status='read', converted=25)))])
    return model, native, props


class InterchangeTests(unittest.TestCase):
    def test_name_and_association_do_not_supply_missing_strength(self):
        model, native, _ = fixture(value=None)
        result = inspect_model(model, native)
        self.assertEqual(result['singleMaterialNameMatches'], 1)
        self.assertEqual(result['matchingPropertyCounts']['compressionMPa'], 0)
        self.assertEqual(result['rows'][0]['properties']['compressionMPa']['status'], 'absent')

    def test_pressure_pascal_is_converted_and_compared(self):
        model, native, _ = fixture()
        result = inspect_model(model, native)
        self.assertEqual(result['matchingPropertyCounts']['compressionMPa'], 1)
        self.assertEqual(result['rows'][0]['properties']['compressionMPa']['value'], 25)

    def test_explicit_megapascal_overrides_project_pascal(self):
        model, native, props = fixture(value=25)
        props[0].Unit = model.create_entity('IfcSIUnit', UnitType='PRESSUREUNIT', Prefix='MEGA', Name='PASCAL')
        self.assertEqual(inspect_model(model, native)['matchingPropertyCounts']['compressionMPa'], 1)

    def test_unit_absence_is_not_assumed_to_be_pascal(self):
        model, native, _ = fixture(unit=False)
        read = inspect_model(model, native)['rows'][0]['properties']['compressionMPa']
        self.assertEqual(read['status'], 'missing_unit')
        self.assertIsNone(read['value'])
        self.assertFalse(read['matchesNative'])

    def test_density_kg_m3_is_not_multiplied_by_thousand(self):
        model, _, _ = fixture()
        kg = model.create_entity('IfcSIUnit', UnitType='MASSUNIT', Prefix='KILO', Name='GRAM')
        metre = model.create_entity('IfcSIUnit', UnitType='LENGTHUNIT', Name='METRE')
        density = model.create_entity('IfcDerivedUnit', UnitType='MASSDENSITYUNIT', Elements=[
            model.create_entity('IfcDerivedUnitElement', Unit=kg, Exponent=1),
            model.create_entity('IfcDerivedUnitElement', Unit=metre, Exponent=-3)])
        prop = model.create_entity('IfcPropertySingleValue', Name='Densidade', Unit=density,
            NominalValue=model.create_entity('IfcMassDensityMeasure', 2407.31172))
        self.assertAlmostEqual(numeric_property(model, prop, 'densityKgM3')['value'], 2407.31172)

    def test_repeated_tag_refuses_ambiguous_mapping(self):
        model, native, _ = fixture()
        model.create_entity('IfcColumn', GlobalId=ifcopenshell.guid.new(), Tag='1')
        with self.assertRaisesRegex(ValueError, 'Tag'):
            inspect_model(model, native)

    def test_different_material_is_not_matched_by_tag_alone(self):
        model, native, _ = fixture(material_name='Outro concreto')
        result = inspect_model(model, native)
        self.assertEqual(result['singleMaterialNameMatches'], 0)
        self.assertEqual(result['matchingPropertyCounts']['compressionMPa'], 0)

    def test_changed_value_is_detected(self):
        model, native, _ = fixture(value=10e6)
        self.assertEqual(inspect_model(model, native)['matchingPropertyCounts']['compressionMPa'], 0)

    def test_missing_native_value_is_not_declared_retained(self):
        model, native, _ = fixture()
        native = copy.deepcopy(native)
        native['materials'][0]['asset']['concreteCompression'] = {'status': 'missing'}
        self.assertFalse(inspect_model(model, native)['rows'][0]['properties']['compressionMPa']['matchesNative'])


if __name__ == '__main__':
    unittest.main()
