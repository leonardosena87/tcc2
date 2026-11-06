import copy
import json
import unittest
from collections import Counter
from pathlib import Path
from preparar import candidate, rows
from formas_cad import compare_axes


class Coordination(unittest.TestCase):
    def test_plan_does_not_mutate_original_or_duplicate_existing_identities(self):
        old=json.loads((Path(__file__).resolve().parents[1]/'h03-r160/R160-candidato-comum.json').read_text(encoding='utf-8'))
        before=copy.deepcopy(old);new=candidate(old)
        self.assertEqual(old,before)
        self.assertEqual(len(rows(new)),66)
        self.assertEqual(len({e['id'] for e in rows(new)}),66)
        self.assertEqual({e['id'] for e in rows(old)}-{e['id'] for e in rows(new)},set())
        self.assertEqual(new['elementCount'],66)
        self.assertFalse(new['stairsGeometryModified'])
        self.assertFalse(new['structuralApproval'])

    def test_unexpected_reference_pillar_rejected(self):
        old=json.loads((Path(__file__).resolve().parents[1]/'h03-r160/R160-candidato-comum.json').read_text(encoding='utf-8'))
        next(e for e in rows(old) if e['id']=='P11-N1')['x']+=.01
        with self.assertRaises(ValueError):candidate(old)

    def test_axes_allow_machine_rounding_and_reversal(self):
        a=Counter({('L',(0.,0.,0.),(1.,0.,0.)):1})
        b=Counter({('L',(1.+1e-15,0.,0.),(0.,0.,0.)):1})
        self.assertLess(compare_axes(a,b),1e-9)

    def test_axes_do_not_hide_displacement(self):
        a=Counter({('L',(0.,0.,0.),(1.,0.,0.)):1})
        b=Counter({('L',(0.,0.,0.),(1.01,0.,0.)):1})
        with self.assertRaises(ValueError):compare_axes(a,b)

    def test_duplicated_axis_cannot_be_matched_twice(self):
        a=Counter({('L',(0.,0.,0.),(1.,0.,0.)):2})
        b=Counter({('L',(0.,0.,0.),(1.,0.,0.)):1})
        with self.assertRaises(ValueError):compare_axes(a,b)

    def test_additional_axis_rejected(self):
        a=Counter({('L',(0.,0.,0.),(1.,0.,0.)):1})
        b=a.copy();b[('L',(1.,0.,0.),(2.,0.,0.))]+=1
        with self.assertRaises(ValueError):compare_axes(a,b)

    def test_nonfinite_last_coordinate_rejected(self):
        a=Counter({('L',(0.,0.,0.),(1.,0.,0.)):1})
        b=Counter({('L',(0.,0.,0.),(1.,0.,float('nan'))):1})
        with self.assertRaises(ValueError):compare_axes(a,b)


if __name__=='__main__':unittest.main()
