import unittest
from auditar_apoios import extract,read,OUT
class ReadingTests(unittest.TestCase):
 def test_real_shared_support_rounding(self):
  row=next(r for r in read(OUT/'R174-preparacao-plano.json')['rows'] if r['id']=='RP2-04')
  text=(OUT/'R174-RP2-04-QT-reaberto.txt').read_text(encoding='utf-8')
  self.assertEqual(extract(text,'Q_TELHADO_MANUTENCAO',row['QT'])['Fz'],-1.14938)
  with self.assertRaises(ValueError):extract(text,'Adicional',row['QT'])
  expected={**row['QT'],'My':0.}
  with self.assertRaises(ValueError):extract(text,'Q_TELHADO_MANUTENCAO',expected)
 def test_wrong_project_and_sign_are_rejected(self):
  row=next(r for r in read(OUT/'R174-preparacao-plano.json')['rows'] if r['id']=='VP1-02')
  text=(OUT/'R174-VP1-02-G-reaberto.txt').read_text(encoding='utf-8')
  with self.assertRaises(ValueError):extract(text.replace('R174-BIM','R000-BIM'),'Adicional',row['G'])
  with self.assertRaises(ValueError):extract(text,'Adicional',{**row['G'],'Fz':.521164})
if __name__=='__main__':unittest.main()
