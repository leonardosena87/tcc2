import unittest
from consolidar import summary, comparison


def evidence(direction='Y-', floor='N1'):
    return ('editar Value: Cargas verticais: Q_TELHADO_MANUTENCAO = 1.40 tf '
            'Deslocamento horizontal máximo do centro de massa (Vento): '
            'X+ = 0.20 cm (limite 0.42) X- = 0.20 cm (limite 0.42) '
            'Y+ = 0.20 cm (limite 0.42) Y- = 0.20 cm (limite 0.42) '
            f'Deslocamento relativo máximo do centro de massa (Vento): {floor} - {direction} = 0.17 cm (limite 0.35) '
            'Gama-Z Processo P-Delta')


class EvidenceControls(unittest.TestCase):
    def test_preserves_direction_discrepancy_despite_equal_rounded_values(self):
        cad = summary(evidence())
        bim = summary(evidence('Y+', 'TCC-cdd31967-N1'))
        result = comparison(cad, bim)
        self.assertTrue(result['horizontalValuesAndDisplayedLimitsEqual'])
        self.assertTrue(result['relativeValueAndDisplayedLimitEqual'])
        self.assertFalse(result['relativeCriticalDirectionEqual'])
        self.assertFalse(result['rawSummariesEqual'])
        self.assertIsNone(result['directionDiscrepancyCause'])
        self.assertFalse(result['transferDefectDemonstrated'])
        self.assertEqual(bim['relative']['floorNative'], 'TCC-cdd31967-N1')

    def test_rejects_missing_conflicting_or_unverified_evidence(self):
        for text in ['', evidence() + '\n' + evidence('Y+'),
                     evidence().replace('Y- = 0.20 cm (limite 0.42)', ''),
                     evidence() + ' Os deslocamentos horizontais não foram verificados']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                summary(text)


if __name__ == '__main__':
    unittest.main()
