import tempfile
import unittest
from pathlib import Path
from auditar import OUT, geometry, readback


class EvidenceGuards(unittest.TestCase):
    def test_rejects_other_revision_and_rounded_native_value(self):
        text = (OUT/'CAD-recuperado-W20-UI.txt').read_text(encoding='utf-8')
        readback(text,'CAD')
        for altered in [text.replace('4.71065','4.71'),text.replace('R135-CAD','R130-CAD')]:
            with self.assertRaises(ValueError):
                readback(altered,'CAD')

    def test_rejects_shifted_drawing_origin(self):
        raw = (OUT/'CAD-N1-W20-reaberto.dxf').read_text(encoding='utf-8-sig')
        # Translate every X of start/end/center. Load length and intensity stay equal,
        # but the model reference must fail instead of passing on length alone.
        lines = raw.splitlines()
        for i in range(0,len(lines),2):
            if int(lines[i].strip()) in [10,11]:
                lines[i+1] = str(float(lines[i+1])+1)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'shifted.dxf'
            p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                geometry(p)

    def test_rejects_duplicated_wall_entity(self):
        raw = (OUT/'BIM-N1-W20-reaberto.dxf').read_text(encoding='utf-8-sig')
        lines = raw.splitlines()
        start = next(i for i in range(0,len(lines),2)
                     if lines[i].strip()=='8' and lines[i+1].strip()=='CR-Paredes')
        while start>=2 and lines[start].strip()!='0':
            start-=2
        end = start+2
        while lines[end].strip()!='0':
            end+=2
        duplicate = lines[:end]+lines[start:end]+lines[end:]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'duplicate.dxf'
            p.write_text('\n'.join(duplicate)+'\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                geometry(p)


if __name__=='__main__':
    unittest.main()
