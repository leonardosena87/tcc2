import tempfile
import unittest
from pathlib import Path
from ler_dxf import entities,wall_line

class DXFTests(unittest.TestCase):
    def test_only_entities_section(self):
        text='0\nSECTION\n2\nBLOCKS\n0\nLINE\n8\nCR-Paredes\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\nCR-Paredes\n0\nENDSEC\n0\nEOF\n'
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'scope.dxf';p.write_text(text,encoding='utf-8')
            self.assertEqual(len(entities(p)),1)

    def test_rejects_ambiguous_wall_lines(self):
        text='0\nSECTION\n2\nENTITIES\n0\nLINE\n8\nCR-Paredes\n0\nLINE\n8\nCR-Paredes\n0\nMTEXT\n8\nCR-Paredes\n0\nENDSEC\n0\nEOF\n'
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'duplicate.dxf';p.write_text(text,encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'única'):wall_line(p)

if __name__=='__main__':unittest.main()
