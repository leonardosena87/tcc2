import math
import unittest
from verificar import anchor, force_bound, transverse, previous
from scipy.integrate import quad
from scipy.optimize import brentq


class Screening(unittest.TestCase):
    def test_square_capacity_independent_integration(self):
        # Quadratura adaptativa independente da integracao polinomial/Gauss.
        def response(x,n):
            slope=min(.0035/x,.010/(259.7-x))
            def concrete(y):
                strain=max(0,min(.002,slope*(x-y)))
                return .85*(25/1.4)*(1-(1-strain/.002)**2)
            points=sorted(set([0,max(0,x-.002/slope),x,300]))
            axial=quad(lambda y:300*concrete(y),0,300,points=points)[0]
            moment=quad(lambda y:300*concrete(y)*(150-y),0,300,points=points)[0]
            for y in (40.3,259.7):
                stress=max(-500/1.15,min(500/1.15,210000*slope*(x-y)))
                f=2*math.pi*16*(stress-concrete(y))
                axial+=f;moment+=f*(150-y)
            return axial/1000-n,moment/1e6
        for n in (-.5,0,10,22):
            x=brentq(lambda x:response(x,n)[0],.001,259.699)
            self.assertAlmostEqual(previous.capacity(300,300,n),response(x,n)[1],8)

    def test_moments_remain_in_anchor_bound(self):
        row=dict(mv_bound=.9*.2597*10,mh_bound=.9*.2597*5,vv_bound=3,vh_bound=2,n_interval=[-1,0])
        self.assertAlmostEqual(force_bound(row),21)
        self.assertAlmostEqual(force_bound(row,True),8)

    def test_spacing_fails_even_if_small_forces(self):
        # Current square passes; its margin is explicitly small, 5.82 mm.
        t=transverse([dict(vv_bound=19,vh_bound=16)])
        self.assertAlmostEqual(t['spacing_limit_mm']-150,5.82)
        self.assertTrue(t['screening_pass'])

    def test_reject_shear_regime_outside_screen(self):
        with self.assertRaises(ValueError):
            transverse([dict(vv_bound=70,vh_bound=16)])

    def test_two_top_bars_fail_force_screen(self):
        self.assertFalse(anchor(49.674,2)['screening_pass'])
        self.assertTrue(anchor(49.674,3)['screening_pass'])
        self.assertTrue(anchor(49.674,4)['screening_pass'])

    def test_anchor_curve_and_tail(self):
        t=anchor(49.674,3)
        self.assertAlmostEqual(t['available_before_bend_mm'],235.7)
        self.assertEqual(t['bend_pin_mm'],40)
        self.assertEqual(t['proposed_straight_tail_mm'],71)
        self.assertGreaterEqual(t['proposed_straight_tail_mm'],t['straight_tail_min_mm'])
        self.assertGreaterEqual(t['opposite_hook_tip_clearance_mm'],t['opposite_hook_tip_clearance_limit_mm'])
        self.assertGreater(t['one_stirrup_leg_yield_kN'],t['anchorage_transverse_force_per_bar_kN'])
        self.assertFalse(t['anchorage_approved'])

    def test_poor_bond_never_shortens_anchor(self):
        self.assertGreater(anchor(49.674,3,False)['hooked_required_mm'],anchor(49.674,3)['hooked_required_mm'])


if __name__ == '__main__': unittest.main()
