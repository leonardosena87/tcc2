import unittest
from consolidar import HERE,beam,system_units

class UnidadesTest(unittest.TestCase):
    def test_real_unit_switch_and_restoration(self):
        read=lambda p:(HERE/p).read_text(encoding='utf-8')
        a=system_units(read('Sistema-SI-retomada-UI.txt'))
        b=system_units(read('Sistema-linear-kgfm-UI.txt'))
        c=system_units(read('Sistema-SI-restaurar-UI.txt'))
        self.assertEqual(a,c)
        self.assertEqual(b,{**a,'102':'kgf/m'})
        kgf=beam(read('BIM-primeiro-V1-carga-kgfm-UI.txt'),'kgf/m')
        kn=beam(read('BIM-primeiro-V1-carga-SI-restaurada-UI.txt'),'kN/m')
        self.assertAlmostEqual(kgf['extraDisplayed']/kn['extraDisplayed'],100)

    def test_wrong_unit_or_identity_rejected(self):
        text=(HERE/'BIM-primeiro-V1-carga-kgfm-UI.txt').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):beam(text,'kN/m')
        with self.assertRaises(ValueError):beam(text.replace('39-H03-R122-BIM','outro-projeto'),'kgf/m')

if __name__=='__main__':unittest.main()
