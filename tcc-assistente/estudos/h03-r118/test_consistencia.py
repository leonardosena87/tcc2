import copy
import json
import unittest
from pathlib import Path
from consolidar import validate_table


class VisualTranscriptionControls(unittest.TestCase):
    def setUp(self):
        self.table = json.loads((Path(__file__).parent / 'transcricao-visual.json').read_text(encoding='utf-8'))['branches']['CAD']

    def test_valid_transcription_and_inactive_option_rejected(self):
        validate_table(self.table)
        changed = copy.deepcopy(self.table)
        changed['elementChoices']['vigas']['longitudinais']['selectedMm'].append(25)
        with self.assertRaises(ValueError): validate_table(changed)

    def test_missing_row_and_active_wrong_class_rejected(self):
        changed = copy.deepcopy(self.table)
        changed['bars'].pop()
        with self.assertRaises(ValueError): validate_table(changed)
        changed = copy.deepcopy(self.table)
        next(r for r in changed['bars'] if r['active'])['steel'] = 'CA60'
        with self.assertRaises(ValueError): validate_table(changed)


if __name__ == '__main__': unittest.main()
