import copy
import unittest
from auditar import inventory,r136,HERE

class SupportInventoryGuards(unittest.TestCase):
    def model(self):return r136.models(HERE.parent/'h03-r137/SAP-CAD')['N1']['data']

    def test_local_spring_cannot_be_silently_treated_as_global(self):
        model=copy.deepcopy(self.model())
        model['tables']['JOINT SPRING ASSIGNMENTS 1 - UNCOUPLED'][0]['CoordSys']='LOCAL'
        with self.assertRaisesRegex(ValueError,'transformação'):inventory(model)

    def test_spring_with_unknown_joint_is_rejected(self):
        model=copy.deepcopy(self.model())
        model['tables']['JOINT SPRING ASSIGNMENTS 1 - UNCOUPLED'][0]['Joint']='999999'
        with self.assertRaisesRegex(ValueError,'sem nó'):inventory(model)

if __name__=='__main__':unittest.main()
