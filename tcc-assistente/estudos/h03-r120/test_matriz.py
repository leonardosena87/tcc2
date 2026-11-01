import copy
import json
import unittest
from preparar_matriz import INPUTS, prepare


def sources():
    return {k: json.loads(p.read_text(encoding='utf-8-sig')) for k,p in INPUTS.items()}


class MatrizTest(unittest.TestCase):
    def test_actual_correction_and_paths(self):
        s = sources()
        r = prepare(s['walls']['walls'], s['segments']['segments'], s['geometry'], s['openings'], s['doorCorrection'])
        self.assertEqual(r['unknownWallIds'], ['W08'])
        self.assertEqual(r['ambiguousCrossingsGeometricallyResolved'], 4)
        self.assertEqual([w['wallId'] for w in r['priorityUnopenedParallelBeamWalls']], ['W03','W05','W07','W11','W14','W17'])
        w18 = next(w for w in r['walls'] if w['wallId'] == 'W18')
        self.assertAlmostEqual(w18['conditionalNetMasonryAreaM2'], 6.8625)
        self.assertAlmostEqual(w18['deltaConditionalAreaFromR67M2'], -0.21)
        self.assertAlmostEqual(w18['conditionalWeightMagnitudeKN'], 10.7398125)
        self.assertTrue(all(not r['readyForNativeApplication'] for r in r['segments']))
        for w in r['walls']:
            if w['wallId'] not in {'W08','W18'}:
                self.assertAlmostEqual(w['deltaConditionalAreaFromR67M2'], 0)

    def test_duplicate_opening_and_mismatched_support_rejected(self):
        s = sources()
        bad = copy.deepcopy(s['openings'])
        bad['openings'].append(dict(bad['openings'][0]))
        with self.assertRaises(ValueError):
            prepare(s['walls']['walls'], s['segments']['segments'], s['geometry'], bad, s['doorCorrection'])
        bad_geometry = copy.deepcopy(s['geometry'])
        for row in bad_geometry['BIM']:
            if row['type'] == 'IfcBeam' and row['name'] == 'V1' and row['min'] == [0.1, 6.95, 2.75]:
                row['max'][1] += 0.01
        with self.assertRaises(ValueError):
            prepare(s['walls']['walls'], s['segments']['segments'], bad_geometry, s['openings'], s['doorCorrection'])


if __name__ == '__main__': unittest.main()
