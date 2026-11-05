"""Controles de leitura/comparacao dos relatorios, sem simular aprovacao estrutural."""
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from conferir import records, compare, FIELDS, HEADERS


def fixture(path, wrong_element=False, duplicate=False):
    def cell(content): return '<w:tc>'+''.join('<w:p><w:r><w:t>'+s+'</w:t></w:r></w:p>' for s in content)+'</w:tc>'
    tables=[]
    for n in range(87):
        label = 'G1+Q'+str(n) if n < 68 else 'Vento X+ (V'+str(n)+')'
        if duplicate: label='G1+Q'
        header='<w:tr>'+''.join(cell([h]) for h in HEADERS)+'</w:tr>'
        rows=[]
        for segment in range(1,4):
            values=[[str(i)+',25' for i in range(k)] for k in [1,2,2,1,2,1,2,2,1]]
            rows.append('<w:tr>'+cell([('V2' if wrong_element else 'V3')+' - '+str(segment)])+
                        ''.join(cell(v) for v in values)+'</w:tr>')
        tables.append('<w:tbl><w:tr>'+cell(['CASO: '+label])+'</w:tr>'+header+''.join(rows)+'</w:tbl>')
    xml='<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+''.join(tables)+'</w:body></w:document>'
    with ZipFile(path,'w') as z: z.writestr('word/document.xml',xml)


class Conference(unittest.TestCase):
    def test_multiline_cells_keep_distinct_numbers(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.docx'; fixture(p); rows=records(p,'V3')
            self.assertEqual(len(rows),87)
            row=rows['G1+Q0'][0]
            self.assertEqual(row['n_t'],.25)
            self.assertEqual(row['n_c'],1.25)
            self.assertEqual(len(row),14)
            self.assertEqual(compare(rows, rows)['comparedValues'],3654)

    def test_wrong_element_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.docx'; fixture(p,wrong_element=True)
            with self.assertRaises(ValueError): records(p,'V3')

    def test_duplicate_case_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.docx'; fixture(p,duplicate=True)
            with self.assertRaises(ValueError): records(p,'V3')

    def test_small_difference_is_not_rounded_away(self):
        a={'G1+Q':[{k:0. for k in FIELDS} for _ in range(3)]}
        b={'G1+Q':[{k:0. for k in FIELDS} for _ in range(3)]}
        b['G1+Q'][2]['mvf']=.01
        result=compare(a,b)
        self.assertEqual(result['differingValues'],1)
        self.assertEqual(result['maxPrintedAbsoluteDifference'],.01)
        self.assertFalse(result['samePrintedValues'])

    def test_different_cases_rejected(self):
        with self.assertRaises(ValueError): compare({'G1':[]},{'G2':[]})


if __name__=='__main__': unittest.main()
