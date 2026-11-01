import copy
import unittest
from comparar import SOURCE, r122, canonical, compare, normalize_value
from orientacao import diagnose


def load(branch):
    return r122.parse((SOURCE / f'SAP-{branch}/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252'))


class ComparacaoTest(unittest.TestCase):
    def test_real_exports_keep_orientation_differences(self):
        a, b = load('CAD'), load('BIM')
        result = compare(a, b)
        self.assertFalse(result['allTableRecordsEqualAfterRenumbering'])
        self.assertTrue(result['perTable']['COMBINATION DEFINITIONS']['equal'])
        self.assertTrue(result['perTable']['JOINT LOADS - FORCE']['equal'])
        self.assertEqual(diagnose(a, b)['counts']['reversedOrder'], 68)
        self.assertEqual(diagnose(a, b)['counts']['ambiguousParallelGroups'], 1)

    def test_no_tolerance_or_loss_of_multiplicity(self):
        a = load('CAD')
        b = copy.deepcopy(a)
        b['tables']['FRAME LOADS - DISTRIBUTED'][0]['FOverLA'] = '-1,5001'
        self.assertFalse(compare(a, b)['frameAssociationsEqualAfterRenumbering'])
        b = copy.deepcopy(a)
        b['tables']['FRAME LOADS - DISTRIBUTED'].append(copy.deepcopy(b['tables']['FRAME LOADS - DISTRIBUTED'][0]))
        self.assertFalse(compare(a, b)['frameAssociationsEqualAfterRenumbering'])
        self.assertEqual(normalize_value('-0,0000'), '0')
        self.assertNotEqual(normalize_value('0,0001'), '0')

    def test_coincident_joint_identity_is_rejected(self):
        a = load('CAD')
        a['joints']['duplicate'] = a['joints']['1']
        with self.assertRaises(ValueError):
            canonical(a)


if __name__ == '__main__':
    unittest.main()
