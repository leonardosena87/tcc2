import unittest
from decimal import Decimal as D
from auditar import resultant


class ResultantGuards(unittest.TestCase):
    def test_weighted_centroid_and_signed_origin_moments(self):
        rows=[{'xyzCm':['0','0','320'],'forceKgf':['0.0000','0.0000','-1.0000']},
              {'xyzCm':['4','8','320'],'forceKgf':['0.0000','0.0000','-3.0000']}]
        r=resultant(rows,D('-4'),(D(3),D(6)))
        self.assertEqual(r['centroidXYCm'],['3','6'])
        self.assertEqual(D(r['originMomentFromForcesKgfCm']['Mx']),D(-24))
        self.assertEqual(D(r['originMomentFromForcesKgfCm']['My']),D(12))
        self.assertTrue(r['forceExactlyEqualToNominal'])

    def test_rounding_bound_is_not_a_general_load_tolerance(self):
        row={'xyzCm':['810','195','320'],'forceKgf':['0.0000','0.0000','-217.8676']}
        rows=[row.copy() for _ in range(8)]
        r=resultant(rows)
        self.assertFalse(r['forceExactlyEqualToNominal'])
        self.assertEqual(D(r['signedForceDeltaKgf']),D('-0.0003'))
        self.assertFalse(r['roundingProvenAsCause'])
        altered=[dict(x) for x in rows]
        altered[0]['forceKgf']=['0.0000','0.0000','-217.8678']
        with self.assertRaises(ValueError):
            resultant(altered)
        with self.assertRaises(ValueError):
            resultant(rows+[row.copy()])


if __name__=='__main__':unittest.main()
