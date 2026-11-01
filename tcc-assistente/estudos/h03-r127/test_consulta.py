import unittest
from consolidar import HERE,parse

class ApoioTest(unittest.TestCase):
    def test_real_native_readings(self):
        for branch,name in [('CAD','CAD-W17-V14-secao-UI.txt'),('BIM','BIM-W17-V2-secao-UI.txt')]:
            value=parse((HERE/name).read_text(encoding='utf-8'),branch)
            self.assertEqual((value['bwCm'],value['hCm'],value['elevationCm']),(20,16,0))
            self.assertEqual((value['extraSumDisplayedKNm'],value['wallDisplayedKNm']),(0,0))

    def test_wrong_project_and_conflicting_height_rejected(self):
        text=(HERE/'CAD-W17-V14-secao-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):parse(text,'BIM')
        with self.assertRaises(ValueError):parse(text+'\neditar (settable, string) h Value: 45 ID: 811','CAD')

if __name__=='__main__':unittest.main()
