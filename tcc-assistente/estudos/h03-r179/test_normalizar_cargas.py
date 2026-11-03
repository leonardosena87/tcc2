import unittest
from normalizar_cargas import local_axes, canonical_load, aggregate, compare_rows


def model(i=(0,0,0),j=(10,0,0),angle=None):
    return dict(frames={'1':(i,j)},tables={
        'FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL':[] if angle is None else [{'Frame':'1','Angle':str(angle)}]})


def point(force='5',station='0.25',direction='1'):
    return dict(Frame='1',LoadPat='G',CoordSys='LOCAL',Type='Force',Dir=direction,
                DistType='RelDist',RelDist=station,Force=force)


class NormalizeLoadsTest(unittest.TestCase):
    def assertVector(self,a,b):
        for x,y in zip(a,b): self.assertAlmostEqual(x,y,places=10)

    def test_horizontal_local2_is_upward(self):
        self.assertVector(local_axes((0,0,0),(10,0,0))[1],(0,0,1))

    def test_vertical_reference_and_right_hand_rotation(self):
        axes=local_axes((0,0,0),(0,0,10),90)
        self.assertVector(axes[0],(0,0,1))
        self.assertVector(axes[1],(0,1,0))
        self.assertVector(axes[2],(-1,0,0))

    def test_downward_column_has_consistent_handedness(self):
        self.assertVector(local_axes((0,0,10),(0,0,0))[2],(0,-1,0))

    def test_angle_rotation_horizontal(self):
        self.assertVector(local_axes((0,0,0),(10,0,0),90)[1],(0,-1,0))

    def test_reversed_point_changes_station_and_local1_sign(self):
        a=canonical_load(model(),point(),'FRAME LOADS - POINT')
        b=canonical_load(model((10,0,0),(0,0,0)),point('-5','0.75'),'FRAME LOADS - POINT')
        self.assertEqual(a,b)

    def test_reversed_trapezoid_swaps_end_values(self):
        row=dict(Frame='1',LoadPat='G',CoordSys='LOCAL',Type='Force',Dir='1',
                 DistType='RelDist',RelDistA='.1',RelDistB='.6',FOverLA='2',FOverLB='4')
        other=dict(row,RelDistA='.4',RelDistB='.9',FOverLA='-4',FOverLB='-2')
        self.assertEqual(canonical_load(model(),row,'FRAME LOADS - DISTRIBUTED'),
                         canonical_load(model((10,0,0),(0,0,0)),other,'FRAME LOADS - DISTRIBUTED'))

    def test_component_aggregation_preserves_duplicate_load_magnitude(self):
        m=model();m['tables']['FRAME LOADS - POINT']=[point(),point()]
        values,counts=aggregate(m,'FRAME LOADS - POINT')
        self.assertEqual(list(values.values()),[[10,0,0]])
        self.assertEqual(list(counts.values()),[2])

    def test_small_export_residual_is_not_removed(self):
        self.assertFalse(compare_rows({'x':[1,0,0]},{'x':[1.0001,0,0]})['equalAtDeclaredRounding'])

    def test_unsupported_or_invalid_loads_fail_explicitly(self):
        for changes in ({'CoordSys':'GLOBAL'},{'Type':'Moment'}, {'RelDist':'1.1'}, {'Dir':'7'}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):
                canonical_load(model(),dict(point(),**changes),'FRAME LOADS - POINT')
        with self.assertRaises(ValueError): local_axes((0,0,0),(0,0,0))


if __name__=='__main__': unittest.main()
