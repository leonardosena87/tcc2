"""Casos sintéticos: identidade, patamar adicional e unidades divergentes."""
import unittest
from auditar_ifc import by_native_tag, compare_length


class Obj:
    def __init__(self, tag, cls): self.Tag=tag; self.cls=cls
    def is_a(self): return self.cls


class IfcAuditTests(unittest.TestCase):
    def test_mm_length_correct(self):
        self.assertTrue(compare_length(178.235294117647, .001, 3.03/17)['matchesNative'])

    def test_internal_feet_value_in_mm_project_is_not_silently_repaired(self):
        r=compare_length((3.03/17)/.3048, .001, 3.03/17)
        self.assertFalse(r['matchesNative'])
        self.assertAlmostEqual(r['interpretedM'], .0005847614636405744)

    def test_extra_landing_is_not_counted_as_missing_or_duplicate_building_slab(self):
        wanted,found,extras=by_native_tag([Obj('1','IfcSlab'),Obj('2','IfcSlab')],[dict(Id=1,Kind='slab')])
        self.assertEqual(set(wanted),set(found));self.assertEqual(len(extras),1)

    def test_duplicate_tag_fails(self):
        with self.assertRaises(ValueError):by_native_tag([Obj('1','IfcSlab'),Obj('1','IfcSlab')],[dict(Id=1,Kind='slab')])

    def test_wrong_class_fails(self):
        with self.assertRaises(ValueError):by_native_tag([Obj('1','IfcBeam')],[dict(Id=1,Kind='slab')])


if __name__ == '__main__': unittest.main()
