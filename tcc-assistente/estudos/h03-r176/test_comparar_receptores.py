import copy,unittest
import comparar_receptores as m

class ReceiverComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models={b:m.sap.parse((m.OUT/f'SAP-{b}/portico_SAP2000_elastico.$2k').read_text(encoding='cp1252')) for b in ['CAD','BIM']}

    def test_real_same_geometry_and_sections_preserves_load_differences(self):
        r=m.compare(self.models['CAD'],self.models['BIM'])
        self.assertTrue(r['jointCoordinateMultisetsEqual'])
        self.assertTrue(r['frameUndirectedEndpointMultisetsEqual'])
        self.assertTrue(r['sectionPropertiesByUndirectedSegmentEqual'])
        self.assertEqual(len(r['nodalLoadDifferences']),9)
        self.assertFalse(r['allExportedTablesEqualAfterSpatialNormalization'])

    def test_identifier_renaming_does_not_create_false_differences(self):
        original=self.models['CAD'];renamed=copy.deepcopy(original)
        renamed['joints']={'node_'+k:v for k,v in renamed['joints'].items()}
        renamed['frames']={'bar_'+k:v for k,v in renamed['frames'].items()}
        for rows in renamed['tables'].values():
            for row in rows:
                for key in ['Joint','JointI','JointJ']:
                    if key in row:row[key]='node_'+row[key]
                if 'Frame' in row:row['Frame']='bar_'+row['Frame']
        self.assertTrue(m.compare(original,renamed)['allExportedTablesEqualAfterSpatialNormalization'])

    def test_moved_load_detected_even_if_total_is_unchanged(self):
        original=self.models['CAD'];changed=copy.deepcopy(original)
        row=next(r for r in changed['tables']['JOINT LOADS - FORCE'] if r['LoadPat']=='QT')
        row['Joint']=next(k for k in changed['joints'] if k!=row['Joint'])
        r=m.compare(original,changed)
        self.assertFalse(r['nodalLoadPositionPatternKeysEqual'])
        self.assertFalse(r['tables']['JOINT LOADS - FORCE']['equal'])

    def test_duplicate_load_and_missing_table_are_rejected(self):
        original=self.models['CAD'];changed=copy.deepcopy(original)
        changed['tables']['JOINT LOADS - FORCE'].append(copy.deepcopy(changed['tables']['JOINT LOADS - FORCE'][0]))
        with self.assertRaises(ValueError):m.compare(original,changed)
        changed=copy.deepcopy(original);del changed['tables']['JOINT RESTRAINT ASSIGNMENTS']
        with self.assertRaises(ValueError):m.compare(original,changed)

if __name__=='__main__':unittest.main()
