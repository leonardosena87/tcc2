import copy
import json
import unittest
from preparar import build,bounds,volume_overlap,PLAN,PROPOSAL,REF

class CandidateGuard(unittest.TestCase):
    def setUp(self):
        self.p=json.loads(PROPOSAL.read_text(encoding='utf-8'));self.g=json.loads(PLAN.read_text(encoding='utf-8'));self.r=json.loads(REF.read_text(encoding='utf-8'))
        self.c=build(self.p,self.g,self.r)
    def test_finished_geometry_is_preserved_but_concrete_has_explicit_offset(self):
        self.assertEqual(self.c['finishedGeometry']['totalRisers'],17)
        self.assertAlmostEqual(self.c['virtualConcreteStartM'],.17)
        self.assertTrue(self.c['lowerSupportInterfaceUnresolved'])
        self.assertAlmostEqual(self.c['concreteLandingM']+.05,self.c['finishedGeometry']['proposedFinishedLandingM'])
    def test_supports_do_not_intercept_window_or_catalogued_openings(self):
        self.assertTrue(volume_overlap(bounds(self.c['rejectedFacadeBeam']),self.c['windowJ4BoxInterpretedM']))
        self.assertTrue(all(not volume_overlap(bounds(e),self.c['windowJ4BoxInterpretedM']) for e in self.c['addedElements']))
        self.assertEqual(self.c['newColumnDoorPlanIntersections'],[])
    def test_only_two_existing_elements_are_changed_and_no_original_is_mutated(self):
        before=copy.deepcopy(self.p);build(self.p,self.g,self.r)
        self.assertEqual(before,self.p)
        self.assertEqual({e['id'] for e in self.c['changedExistingElements']},{'V15-N1','L6-N1'})
        self.assertEqual(self.c['countsByKind'],dict(column=24,beam=30,slab=11))
    def test_nominal_clearance_is_not_promoted_to_structural_or_native_success(self):
        self.assertEqual(self.c['nominalHorizontalSurfaceOverlaps'],[])
        self.assertTrue(self.c['zeroNominalSurfaceOverlapsIsNotSolidClashClearance'])
        self.assertFalse(self.c['structuralCapacityVerified'])
        self.assertFalse(self.c['nativeAuthoringApplied'])
        self.assertAlmostEqual(self.c['centralGapM'],.15)

if __name__=='__main__':unittest.main()
