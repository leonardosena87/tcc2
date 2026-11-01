import unittest
from consolidar import HERE, parse, span, geometry_comparison


class ExportacaoTest(unittest.TestCase):
    def test_actual_exports_target_neighbor_and_geometry(self):
        models = []
        for branch in ['CAD', 'BIM']:
            model = parse((HERE / f'SAP-{branch}/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))
            models.append(model)
            wall = span(model, (0, 705, 320), (440, 705, 320))
            self.assertEqual(wall['lengthCm'], 440)
            load = wall['G2DistributedLoads'][0]
            self.assertAlmostEqual(load['magnitudeTf'], 1.9536)
            self.assertEqual(load['loadedLengthCm'], 440)
            self.assertEqual(span(model, (440, 705, 320), (965, 705, 320))['G2DistributedLoads'], [])
        self.assertTrue(geometry_comparison(*models)['frameEndpointMultisetEqualAtExportPrecision'])

    def test_unsupported_units_missing_span_duplicate_node_rejected(self):
        text = (HERE / 'SAP-CAD/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252')
        with self.assertRaises(ValueError):
            parse(text.replace('Kgf, cm, C', 'kN, m, C'))
        model = parse(text)
        with self.assertRaises(ValueError):
            span(model, (10, 705, 320), (430, 705, 320))
        with self.assertRaises(ValueError):
            parse(text.replace('TABLE:   "JOINT RESTRAINT ASSIGNMENTS"',
                'Joint=1 CoordSys=GLOBAL CoordType=Cartesian XorR=0 Y=0 Z=20\nTABLE:   "JOINT RESTRAINT ASSIGNMENTS"'))


if __name__ == '__main__':
    unittest.main()
