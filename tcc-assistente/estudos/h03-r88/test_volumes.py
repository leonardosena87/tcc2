import unittest
from auditar_volumes import compare_unions, normalized, intersection_pairs, validate_box_surface


class OccupiedVolumeTest(unittest.TestCase):
    def test_nonbox_surface_is_rejected_even_if_a_scalar_volume_could_match(self):
        v=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        f=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
           (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
        validate_box_surface(v,f)
        with self.assertRaises(ValueError):validate_box_surface(v[:6]+[(.5,1,1)]+v[7:],f)
        with self.assertRaises(ValueError):validate_box_surface(v,[(0,2,6)]+f[1:])
        with self.assertRaises(ValueError):validate_box_surface(v[:-1]+[v[0]],f)

    def test_overlap_and_duplicates_do_not_increase_occupied_volume(self):
        a = [(0,2,0,1,0,1),(1,3,0,1,0,1),(0,2,0,1,0,1)]
        b = [(0,3,0,1,0,1)]
        r = compare_unions(a,b)
        self.assertAlmostEqual(r['unionAM3'],3)
        self.assertAlmostEqual(r['symmetricDifferenceM3'],0)

    def test_equal_totals_do_not_conceal_a_displaced_shape(self):
        r = compare_unions([(0,1,0,1,0,1)],[(1,2,0,1,0,1)])
        self.assertAlmostEqual(r['unionAM3'],r['unionBM3'])
        self.assertAlmostEqual(r['symmetricDifferenceM3'],2)
        self.assertFalse(r['sameOccupiedVolumeWithinDeclaredCriterion'])

    def test_partition_and_touching_faces_preserve_volume(self):
        r = compare_unions([(0,1,0,1,0,2)],[(0,1,0,1,0,1),(0,1,0,1,1,2)])
        self.assertAlmostEqual(r['intersectionM3'],2)
        self.assertAlmostEqual(r['symmetricDifferenceM3'],0)

    def test_voids_are_not_filled_by_the_outer_bounding_box(self):
        a = [(0,1,0,1,0,1),(2,3,0,1,0,1)]
        r = compare_unions(a,[(0,3,0,1,0,1)])
        self.assertAlmostEqual(r['onlyBM3'],1)
        self.assertAlmostEqual(r['unionAM3'],2)

    def test_nonfinite_or_degenerate_boxes_are_rejected(self):
        with self.assertRaises(ValueError):normalized((0,0,0,1,0,1))
        with self.assertRaises(ValueError):normalized((0,float('nan'),0,1,0,1))

    def test_pair_sums_are_not_used_as_union_overlap_with_three_coincident_objects(self):
        box=(0,1,0,1,0,1)
        objects=[dict(name=str(i),guid=str(i),box=box) for i in range(3)]
        self.assertAlmostEqual(sum(p['intersectionM3'] for p in intersection_pairs(objects)),3)
        r=compare_unions([box,box,box],[box])
        self.assertAlmostEqual(r['unionAM3'],1)
        self.assertAlmostEqual(r['symmetricDifferenceM3'],0)


if __name__ == '__main__':
    unittest.main()
