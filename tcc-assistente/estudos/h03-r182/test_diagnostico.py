import unittest
from consolidar_diagnostico import parse_report,prism_signature


def report(body):
    return ('DIMENSIONAMENTO DOS ELEMENTOS\n'+body+
            '\nTempo de dimensionamento dos elementos: 00:00:02\nTempo total de processamento: 00:00:07')


class ReportTests(unittest.TestCase):
    def test_bim_name_error_count_and_nested_time(self):
        r=parse_report(report('Pavimento TCC-7a6267fd-N1\n    Vigas: 11 Com sucesso, 1 com erro\n'))
        self.assertEqual(r['levels']['N1']['reportedCategories']['Vigas'],dict(reportedSuccess=11,reportedError=1))
        self.assertEqual(r['nativeTotalSeconds'],7)
        self.assertEqual(r['nativeDimensioningSeconds'],2)
        self.assertTrue(r['dimensioningTimeIsIncludedInTotal'])

    def test_empty_block_not_invented_zero(self):
        r=parse_report(report('Pavimento N0\n\n'))
        self.assertEqual(r['levels']['N0']['reportedCategories'],{})
        self.assertTrue(r['levels']['N0']['emptyLevelBlockIsNotAZeroCount'])

    def test_duplicate_level_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicado'):
            parse_report(report('Pavimento N1\n    Vigas: 1 Com sucesso\nPavimento N1\n    Lajes: 2 Com sucesso\n'))

    def test_unrecognized_status_not_silently_dropped(self):
        with self.assertRaisesRegex(ValueError,'nao reconhecida'):
            parse_report(report('Pavimento N1\n    Vigas: texto inesperado\n'))

    def test_summary_cannot_approve_stair(self):
        r=parse_report(report('Pavimento N1\n    Lajes: 9 Com sucesso\n'))
        self.assertTrue(r['stairPassCannotBeInferredFromReportedSlabCounts'])


V=[(0,0,0),(2,0,0),(2,1,0),(0,1,0),(0,0,1),(2,0,1),(2,1,1),(0,1,1)]
F=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
   (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]


class SolidTests(unittest.TestCase):
    def test_different_face_diagonal_same_closed_prism(self):
        other=[(0,3,1),(1,3,2)]+F[2:]
        self.assertEqual(prism_signature(V,F),prism_signature(V,other))

    def test_nonface_triangle_rejected(self):
        with self.assertRaisesRegex(ValueError,'fora da face'):
            prism_signature(V,[(0,2,6)]+F[1:])

    def test_duplicate_face_rejected(self):
        with self.assertRaises(ValueError):
            prism_signature(V,F[:-1]+[F[0]])

    def test_only_bbox_vertices_are_insufficient(self):
        with self.assertRaises(ValueError):
            prism_signature(V,[])


if __name__=='__main__':
    unittest.main()
