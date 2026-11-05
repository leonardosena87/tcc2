import unittest
from ancoragem import anchorage, force_bound


class Regression(unittest.TestCase):
    def test_moment_cannot_be_omitted(self):
        row=dict(mv_bound=.9*.2597*10,mh_bound=.9*.1597*5,
                 vv_bound=3,vh_bound=2,n_interval=[-1,0])
        self.assertAlmostEqual(force_bound(row),21.)

    def test_compression_is_not_added_as_tension(self):
        row=dict(mv_bound=0,mh_bound=0,vv_bound=3,vh_bound=2,n_interval=[1,8])
        self.assertEqual(force_bound(row),5.)

    def test_three_bars_do_not_fit_anchorage_screen(self):
        trial=anchorage(56.974,3)
        self.assertFalse(trial['projected_length_screen_pass'])
        self.assertGreater(trial['required_mm'],180)

    def test_four_bars_have_only_screening_success(self):
        trial=anchorage(56.974,4)
        self.assertTrue(trial['projected_length_screen_pass'])
        self.assertAlmostEqual(trial['clear_spacing_mm'],31.8)
        self.assertFalse(trial['anchorage_approved'])

    def test_hook_requires_normal_cover(self):
        self.assertEqual(anchorage(56.974,4,normal_cover=23.9)['hook_factor'],1.)
        self.assertEqual(anchorage(56.974,4,normal_cover=24.)['hook_factor'],.7)

    def test_CA50_pin_and_tail(self):
        trial=anchorage(0,2)
        self.assertEqual(trial['CA50_minimum_bend_pin_mm'],40.)
        self.assertEqual(trial['minimum_90deg_straight_tail_mm'],64.)
        self.assertEqual(trial['required_mm'],100.)

    def test_five_bars_do_not_fit_aggregate_spacing(self):
        self.assertFalse(anchorage(56.974,5)['clear_spacing_pass'])


if __name__=='__main__': unittest.main()
