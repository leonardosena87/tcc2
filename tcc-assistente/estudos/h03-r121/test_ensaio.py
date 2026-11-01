import unittest
from pathlib import Path
from consolidar import r116, unique_field, load_extent_diagnostic


class EnsaioTest(unittest.TestCase):
    def test_actual_evidence_retains_difference(self):
        summaries = {}
        for branch,name in [('CAD','V3'),('BIM','V1')]:
            text = (Path(__file__).parent / f'{branch}-resumo-analise-UI.txt').read_text(encoding='utf-8')
            summaries[branch] = r116.extract(text)
            self.assertEqual(summaries[branch]['verticalLoadsDisplayedTf']['Total'],107.09)
            self.assertEqual(summaries[branch]['verticalLoadsDisplayedTf']['Adicional'],12.51)
            after = (Path(__file__).parent / f'{branch}-{name}-reaberto-UI.txt').read_text(encoding='utf-8')
            self.assertEqual(unique_field(after,'Nome'),name)
            self.assertEqual(unique_field(after,'Carga extra',True),'4.44')
        self.assertFalse(r116.r111.r106.comparison(summaries['CAD'],summaries['BIM'])['relativeCriticalDirectionEqual'])

    def test_extent_hypotheses_do_not_claim_calibration(self):
        r = load_extent_diagnostic(10.56,12.51)
        self.assertEqual(r['differenceIntervalTfAssumingNearestHundredthRounding'],[1.94,1.96])
        self.assertFalse(r['effectiveLengthVerified'])
        self.assertFalse(r['unitConversionCalibrated'])
        self.assertTrue(any(x['lengthM']==4.4 and x['kNPerTfHypothetical']==10 and x['fallsInDisplayedDifferenceInterval'] for x in r['hypotheses']))
        self.assertFalse(any(x['lengthM']==4.2 and x['fallsInDisplayedDifferenceInterval'] for x in r['hypotheses']))


if __name__=='__main__':unittest.main()
