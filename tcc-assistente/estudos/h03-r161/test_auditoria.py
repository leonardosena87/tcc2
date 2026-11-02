"""Testes de unidades, identidades e limites; nao substituem ensaio nativo."""
import math
import unittest

from auditar_exportacao import by_native_tag, require_complete_identity, compare_length, ifcopenshell
from leitor_propriedades_r94 import numeric_property, scale_to_si
from auditar_cad_eberick import check_landing_beam
from planejar_revisao_cad import unique_slab_candidate


class IdentityTests(unittest.TestCase):
    def test_duplicate_tag_rejected(self):
        m=ifcopenshell.file(schema='IFC2X3')
        native=[{'Id':1,'Kind':'beam'}]
        with self.assertRaisesRegex(ValueError,'duplicada'):
            by_native_tag([m.create_entity('IfcBeam',Tag='1'),m.create_entity('IfcBeam',Tag='1')],native)

    def test_wrong_class_rejected(self):
        m=ifcopenshell.file(schema='IFC2X3')
        with self.assertRaisesRegex(ValueError,'Classe'):
            by_native_tag([m.create_entity('IfcColumn',Tag='1')],[{'Id':1,'Kind':'beam'}])

    def test_missing_native_id_rejected(self):
        with self.assertRaisesRegex(ValueError,'ausentes'):
            require_complete_identity({'1':{}},{},[])

    def test_removed_column_rejected(self):
        m=ifcopenshell.file(schema='IFC2X3')
        with self.assertRaisesRegex(ValueError,'rejeitado'):
            require_complete_identity({'1':{}},{'1':{}},[m.create_entity('IfcColumn',Tag='473797')])


class PropertyTests(unittest.TestCase):
    def setUp(self):
        self.m=ifcopenshell.file(schema='IFC2X3')

    def pressure(self,value,prefix=None):
        unit=self.m.create_entity('IfcSIUnit',UnitType='PRESSUREUNIT',Name='PASCAL',Prefix=prefix)
        return self.m.create_entity('IfcPropertySingleValue',Name='fck',NominalValue=self.m.create_entity('IfcPressureMeasure',value),Unit=unit)

    def test_pa_and_mpa_normalize_to_same_value(self):
        a=numeric_property(self.m,self.pressure(25000000.),'compressionMPa')
        b=numeric_property(self.m,self.pressure(25.,'MEGA'),'compressionMPa')
        self.assertEqual(a['value'],25.)
        self.assertEqual(a['value'],b['value'])

    def test_absent_does_not_become_zero(self):
        result=numeric_property(self.m,None,'compressionMPa')
        self.assertEqual(result,{'status':'absent','value':None})

    def test_wrong_measure_rejected(self):
        prop=self.m.create_entity('IfcPropertySingleValue',Name='fck',NominalValue=self.m.create_entity('IfcLabel','25 MPa'))
        self.assertEqual(numeric_property(self.m,prop,'compressionMPa')['status'],'unexpected_measure_type')

    def test_kilogram_not_scaled_twice(self):
        unit=self.m.create_entity('IfcSIUnit',UnitType='MASSUNIT',Name='GRAM',Prefix='KILO')
        self.assertEqual(scale_to_si(unit),1.)

    def test_stair_attributes_and_psets_are_compared_by_unit(self):
        native=3.03/17
        self.assertFalse(compare_length(native/.3048,.001,native)['matchesNative'])
        self.assertTrue(compare_length(native*1000,.001,native)['matchesNative'])
        self.assertFalse(compare_length(None,.001,native)['matchesNative'])


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.native={'AxisM':[4.4,0,1.774117647,6.55,0,1.774117647],'BM':.2,'HM':.3}
        self.supports={'P4':[{'minM':[4.3,-.15,.2],'maxM':[4.5,.15,3.2]}],
                       'P10':[{'minM':[6.45,-.15,.2],'maxM':[6.65,.15,3.2]}]}
        self.box={'minM':[4.5,-.1,1.474],'maxM':[6.45,.1,1.774]}

    def test_clear_span_and_recorded_rounding(self):
        result=check_landing_beam(self.box,self.supports,self.native)
        self.assertTrue(result['matchesWithinDeclaredTolerance'])
        self.assertAlmostEqual(result['clearLengthM'],1.95)
        self.assertAlmostEqual(result['nominalAxisLengthM'],2.15)
        self.assertAlmostEqual(result['topDeltaM'],-.000117647)

    def test_horizontal_shift_fails_even_when_height_matches(self):
        self.box['minM'][1]+=.005; self.box['maxM'][1]+=.005
        self.assertFalse(check_landing_beam(self.box,self.supports,self.native)['matchesWithinDeclaredTolerance'])

    def test_excessive_height_difference_fails(self):
        self.box['maxM'][2]+=.002
        self.assertFalse(check_landing_beam(self.box,self.supports,self.native)['matchesWithinDeclaredTolerance'])

    def test_ambiguous_support_rejected(self):
        self.supports['P4']*=2
        with self.assertRaisesRegex(ValueError,'ambiguos'):
            check_landing_beam(self.box,self.supports,self.native)


class SlabAssociationTests(unittest.TestCase):
    def setUp(self):
        self.target={'ProfileM':[[4.4,2.935783,3.2],[6.55,3.9,3.2]],'AxisM':[3.2],'HM':.14}
        self.actual={'name':'L5','geometry':{'minM':[4.5,2.95,3.06],'maxM':[6.45,3.8,3.2]}}
        self.same_name={'name':'L6','geometry':{'minM':[9.75,3.8,3.06],'maxM':[10.725,7.1,3.2]}}

    def test_different_label_does_not_prevent_spatial_candidate(self):
        self.assertIs(unique_slab_candidate([self.same_name,self.actual],self.target),self.actual)

    def test_same_label_outside_location_is_not_associated(self):
        with self.assertRaisesRegex(ValueError,'ausente ou ambigua'):
            unique_slab_candidate([self.same_name],self.target)

    def test_ambiguous_spatial_candidates_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'ausente ou ambigua'):
            unique_slab_candidate([self.actual,self.actual],self.target)


if __name__=='__main__':unittest.main()
