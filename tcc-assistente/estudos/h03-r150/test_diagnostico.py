import unittest
from consolidar import OUT,parse
class Diagnosis(unittest.TestCase):
    def setUp(self):self.text=(OUT/'BIM-V2-No2-bitolas-UI.txt').read_text(encoding='utf-8')
    def test_native_rejections(self):
        rows=parse(self.text)
        self.assertEqual([r['diameterMm'] for r in rows],[8,10,12.5,16,20])
        self.assertEqual({r['code'] for r in rows},{'A07'})
    def test_wrong_node_rejected(self):
        with self.assertRaises(ValueError):parse(self.text.replace('(nó 2)','(nó 3)'))
    def test_incomplete_evidence_rejected(self):
        with self.assertRaises(ValueError):parse('\n'.join(l for l in self.text.splitlines() if 'ø 12.5' not in l))
if __name__=='__main__':unittest.main()
