import unittest
from comparar_etapas_vigas import compare_three


class StageAttributionTests(unittest.TestCase):
    def test_existing_export_difference_not_counted_again_as_receiver_difference(self):
        box={'minM':[0,0,2.75],'maxM':[4,.2,3.06]}
        r=compare_three(dict(topM=3.2,heightM=.45),box,box)
        self.assertTrue(r['rawTopDiffersFromNominal'])
        self.assertTrue(r['rawHeightDiffersFromNominal'])
        self.assertFalse(r['receiverTopDiffersFromRaw'])
        self.assertFalse(r['receiverHeightDiffersFromRaw'])

    def test_additional_height_change_is_separated(self):
        raw={'minM':[0,0,3.04],'maxM':[4,.2,3.06]}
        receiver={'minM':[0,0,3.01],'maxM':[4,.2,3.06]}
        r=compare_three(dict(topM=3.2,heightM=.16),raw,receiver)
        self.assertTrue(r['receiverHeightDiffersFromRaw'])
        self.assertAlmostEqual(r['receiverMinusRaw']['heightM'],.03)
        self.assertFalse(r['receiverTopDiffersFromRaw'])

    def test_small_rounding_does_not_become_new_receiver_error(self):
        raw={'minM':[0,0,1.474117647],'maxM':[4,.2,1.774117647]}
        receiver={'minM':[0,0,1.474117650],'maxM':[4,.2,1.774117650]}
        r=compare_three(dict(topM=1.774117647,heightM=.3),raw,receiver)
        self.assertFalse(r['receiverTopDiffersFromRaw'])
        self.assertFalse(r['receiverHeightDiffersFromRaw'])


if __name__=='__main__':unittest.main()
