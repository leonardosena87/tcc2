import unittest
from comparar_escada import model_kind


class ExportIdentityTests(unittest.TestCase):
    def test_stair_and_floor_at_same_level_are_distinct(self):
        self.assertEqual(model_kind('grelha_SAP2000_escada_N1.$2k'),'escada')
        self.assertEqual(model_kind('grelha_SAP2000_laje_N1.$2k'),'N1')
        self.assertEqual(model_kind('grelha_SAP2000_laje_TCC-7a6267fd-N2.$2k'),'N2')
        self.assertEqual(model_kind('portico_SAP2000_elastico.$2k'),'portico')

    def test_unknown_level_is_not_silently_assumed_to_be_n2(self):
        with self.assertRaises(ValueError): model_kind('grelha_SAP2000_laje_N3.$2k')


if __name__=='__main__': unittest.main()
