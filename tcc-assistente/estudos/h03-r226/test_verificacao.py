import importlib.util
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from verificar import capacity, FCD, FYD, AREA, CENTRE, evaluate


def independent(near,far,normal):
    d=300-CENTRE
    def integrate(x):
        slope=min(.0035/x,.010/(d-x))
        def sigma(y):
            eps=max(0,min(.002,slope*(x-y)))
            return .85*FCD*(1-(1-eps/.002)**2)
        force=300*quad(sigma,0,x,points=[max(0,x-.002/slope)])[0]
        moment=300*quad(lambda y:sigma(y)*(150-y),0,x,points=[max(0,x-.002/slope)])[0]
        for y,count in [(CENTRE,near),(d,far)]:
            f=count*AREA*(max(-FYD,min(FYD,210000*slope*(x-y)))-sigma(y))
            force+=f;moment+=f*(150-y)
        return force/1000,moment/1e6
    root=brentq(lambda x:integrate(x)[0]-normal,.001,d-1e-5)
    return integrate(root)[1]


class Resistance(unittest.TestCase):
    def test_independent_numerical_integration_both_asymmetric_directions(self):
        for near,far in [(3,4),(4,3),(2,2)]:
            for n in [-.25,0,22]:
                self.assertAlmostEqual(capacity(near,far,n),independent(near,far,n),places=7)

    def test_same_four_corner_model_as_previous_revision(self):
        path=Path(__file__).resolve().parents[1]/'h03-r217/verificar.py'
        import sys
        sys.path.insert(0,str(path.parent))
        spec=importlib.util.spec_from_file_location('old_resistance_for_r226',path)
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        for n in [-.25,0,22]:self.assertAlmostEqual(capacity(2,2,n),old.capacity(300,300,n),places=8)

    def test_reversing_bending_direction_is_not_ignored(self):
        self.assertGreater(capacity(3,4,0),capacity(4,3,0))

    def test_minimum12_exposes_old_four_bar_limit_without_claiming_failure_of_actual_steel(self):
        row=dict(combination='controle',n_interval=[-.213,21.183],mv_bound=1.955,mh_bound=1.474)
        data={b:dict(checks=[row]) for b in ('CAD','BIM')}
        out=evaluate(data)
        self.assertGreater(out['CAD']['maxOldFourBarIndexWith12KNm'],1)
        self.assertLess(out['CAD']['governing']['additionalConservativeLinearIndex'],1)
        self.assertFalse(out['fullVerificationComplete'])
        self.assertFalse(out['anchorageApproved'])


if __name__=='__main__':unittest.main()
