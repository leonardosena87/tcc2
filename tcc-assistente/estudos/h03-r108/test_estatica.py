import unittest
from preparar_varanda import transferred_load, total_effect


class StaticControls(unittest.TestCase):
    def test_transport_preserves_force_and_both_global_moments(self):
        load = 0.25
        nodes = transferred_load(load)
        total = load*3.15
        effect = total_effect(nodes)
        self.assertAlmostEqual(effect['FzKN'], -total)
        self.assertAlmostEqual(effect['MxKNm'], -5.475*total)
        self.assertAlmostEqual(effect['MyKNm'], 10.15*total)
        self.assertTrue(all(n['MyKNm'] > 0 for n in nodes))
        without_moment = [{**n, 'MyKNm': 0} for n in nodes]
        self.assertNotAlmostEqual(total_effect(without_moment)['MyKNm'], effect['MyKNm'])

    def test_invalid_geometry_or_nonfinite_load_rejected(self):
        for kwargs in [{'load_per_area': 0}, {'load_per_area': float('nan')},
                       {'load_per_area': .25, 'x1': 9}, {'load_per_area': .25, 'y1': 2}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                transferred_load(**kwargs)


if __name__ == '__main__':
    unittest.main()
