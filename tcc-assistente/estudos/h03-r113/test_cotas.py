import unittest
from consolidar import floor, architectural_level


class LevelsControls(unittest.TestCase):
    def test_level_and_storey_height_remain_distinct(self):
        text='editar (settable, string) Nome Value: N2 ID: 103\neditar (settable, string) Altura Value: 319 ID: 104\neditar (disabled, settable, string) Nível Value: 639 ID: 106'
        r=floor(text);self.assertEqual((r['heightCm'],r['levelCm']),(319,639))
        with self.assertRaises(ValueError): floor(text+'\neditar (settable, string) Altura Value: 300 ID: 104')

    def test_pdf_y_down_is_transformed_to_height_up(self):
        self.assertEqual(architectural_level(1800,2000,3.25,50),7.25)
        self.assertEqual(architectural_level(2100,2000,3.25,50),1.25)
        with self.assertRaises(ValueError):architectural_level(1800,2000,3.25,0)


if __name__=='__main__':unittest.main()
