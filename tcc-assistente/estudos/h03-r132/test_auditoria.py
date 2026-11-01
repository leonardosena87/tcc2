import unittest
from auditar import resultant,nodal

def row(x,y,f):
    return {'xyzCm':[str(x),str(y),'320'],'forceKgf':['0','0',str(f)],'momentKgfCm':['0','0','0']}

class AuditTests(unittest.TestCase):
    def test_same_total_does_not_imply_same_application_center(self):
        data=resultant([row('463.86','468.75','-223.0125'),row('511.59','468.75','-223.0125')])
        self.assertEqual(data['signedFzKgf'],'-446.0250')
        self.assertEqual(data['centroidDeltaXYCm'],['-9.775','-26.25'])
        self.assertNotEqual(data['originMomentDifferenceKgfCm']['Mx'],'0')

    def test_ideal_symmetric_forces_preserve_center(self):
        data=resultant([row(450,495,-1),row(545,495,-1)])
        self.assertEqual([float(v) for v in data['centroidDeltaXYCm']],[0,0])

    def test_local_axes_are_rejected(self):
        model={'tables':{'JOINT LOADS - FORCE':[{'LoadPat':'G2','CoordSys':'LOCAL'}]}}
        with self.assertRaisesRegex(ValueError,'global'):nodal(model)

if __name__=='__main__':unittest.main()
