import unittest
from auditar import horizontal_point, portico_increment, differences

class AuditTests(unittest.TestCase):
    def point(self):
        return {'Frame': '1', 'CoordSys': 'LOCAL', 'Type': 'Force', 'Dir': '2',
                'DistType': 'RelDist', 'RelDist': '0.25', 'Force': '-100', 'LoadPat': 'G2'}

    def model(self):
        return {'frames': {'1': ((10, 20, 320), (110, 20, 320))}, 'tables': {}, 'joints': {}}

    def test_reversed_endpoints_require_complementary_station(self):
        a, r = self.model(), self.point()
        b = self.model()
        b['frames']['1'] = tuple(reversed(a['frames']['1']))
        xyz_a, f_a, _ = horizontal_point(a, r)
        xyz_b, f_b, _ = horizontal_point(b, {**r, 'RelDist': '0.75'})
        self.assertEqual((xyz_a, f_a), (xyz_b, f_b))
        self.assertNotEqual(horizontal_point(b, r)[0], xyz_a)

    def test_rotated_inclined_and_global_inputs_are_rejected(self):
        a, r = self.model(), self.point()
        a['tables']['FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL'] = [{'Frame': '1', 'Angle': '90'}]
        with self.assertRaisesRegex(ValueError, 'Rotação'):
            horizontal_point(a, r)
        a = self.model()
        a['frames']['1'] = ((10, 20, 320), (110, 20, 321))
        with self.assertRaisesRegex(ValueError, 'horizontal'):
            horizontal_point(a, r)
        with self.assertRaisesRegex(ValueError, 'eixo padrão'):
            horizontal_point(self.model(), {**r, 'CoordSys': 'GLOBAL'})

    def test_couples_are_added_to_cross_product(self):
        a = self.model()
        a['joints']['7'] = (10, 20, 320)
        row = {'Joint': '7', 'LoadPat': 'G2', 'CoordSys': 'GLOBAL', 'F1': '0', 'F2': '0',
               'F3': '-100', 'M1': '7', 'M2': '11', 'M3': '0'}
        delta = {'JOINT LOADS - FORCE': {'added': [row], 'removed': []}}
        result = portico_increment(a, a, delta)
        self.assertEqual(result['signedTotals'], {'Fz': '-100', 'Mx': '-1993', 'My': '1011'})

    def test_identical_duplicate_loads_are_not_deduplicated(self):
        row = {'Joint': '7', 'LoadPat': 'G2'}
        before = {'tables': {'LOADS': [row]}}
        after = {'tables': {'LOADS': [row, row]}}
        self.assertEqual(differences(before, after)['LOADS'], {'added': [row], 'removed': []})

if __name__ == '__main__':
    unittest.main()
