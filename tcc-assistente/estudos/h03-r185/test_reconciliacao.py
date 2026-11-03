import unittest
from reconciliar_vigas import reconcile, normalize_level


def row(guid, name, x, level='N1', valid=True):
    return dict(guid=guid, name=name, level=level,
        signature=(x, 0., 3., x + 1., .2, 3.2), closedPrismValidated=valid)


class ReconciliationTests(unittest.TestCase):
    def test_same_solids_different_groups_are_not_missing_beams(self):
        r = reconcile([row('a', 'V1', 0.), row('b', 'V2', 1.)],
            [row('c', 'V1', 0.), row('d', 'V1', 1.)])
        self.assertTrue(r['allExportedBeamPrismsMatched'])
        self.assertEqual(len(r['pairs']), 2)
        self.assertEqual(r['components'][0]['groupingRelation'], 'multiple_CAD_to_one_BIM')

    def test_duplicate_geometry_is_rejected_instead_of_arbitrary_pairing(self):
        with self.assertRaisesRegex(ValueError, 'ambigua'):
            reconcile([row('a', 'V1', 0.), row('b', 'V2', 0.)], [row('c', 'V1', 0.)])

    def test_duplicate_guid_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ambigua'):
            reconcile([row('a', 'V1', 0.), row('a', 'V2', 1.)], [])

    def test_bbox_only_is_not_proof_of_closed_prism(self):
        with self.assertRaisesRegex(ValueError, 'sem validacao'):
            reconcile([row('a', 'V1', 0., valid=False)], [row('b', 'V1', 0.)])

    def test_unmatched_piece_is_explicit(self):
        r = reconcile([row('a', 'V1', 0.), row('b', 'V2', 2.)], [row('c', 'V1', 0.)])
        self.assertFalse(r['allExportedBeamPrismsMatched'])
        self.assertEqual(r['unmatchedCAD'][0]['guid'], 'b')
        self.assertEqual(r['unmatchedBIM'], [])

    def test_level_assignment_difference_is_not_hidden(self):
        r = reconcile([row('a', 'V1', 0., 'N1')], [row('b', 'V1', 0., 'N2')])
        self.assertFalse(r['allMatchedLevelsAgree'])
        self.assertTrue(r['allExportedBeamPrismsMatched'])

    def test_same_names_on_distinct_levels_do_not_collapse_groups(self):
        r = reconcile([row('a', 'V1', 0., 'N1'), row('b', 'V1', 3., 'N2')],
            [row('c', 'V1', 0., 'N1'), row('d', 'V1', 3., 'N2')])
        self.assertEqual(len(r['components']), 2)

    def test_many_to_many_component_preserves_all_relationships(self):
        r = reconcile([row('a', 'V1', 0.), row('b', 'V1', 1.), row('c', 'V2', 2.)],
            [row('d', 'V1', 0.), row('e', 'V2', 1.), row('f', 'V2', 2.)])
        self.assertEqual(len(r['components']), 1)
        self.assertEqual(r['components'][0]['groupingRelation'], 'many_to_many')
        self.assertEqual(r['components'][0]['matchedPhysicalPieces'], 3)

    def test_unknown_level_is_not_assigned_by_default(self):
        self.assertEqual(normalize_level('TCC-7a6267fd-N1'), 'N1')
        with self.assertRaises(ValueError):
            normalize_level('Cobertura')


if __name__ == '__main__':
    unittest.main()
