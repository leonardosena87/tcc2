import copy
import unittest
from auditar import time_check,validate_fine,r136,HERE

class Guards(unittest.TestCase):
    def test_processing_cannot_be_added_outside_session(self):
        session={'inicio_utc':'2026-11-01T10:00:00Z','fim_utc':'2026-11-01T10:00:10Z','duracao_ms':10000}
        process={'inicio_utc':'2026-11-01T10:00:01Z','fim_primeira_observacao_utc':'2026-11-01T10:00:11Z','duracao_ms':10000}
        with self.assertRaisesRegex(ValueError,'fora'):time_check(session,process)
        process.update(fim_primeira_observacao_utc='2026-11-01T10:00:05Z',duracao_ms=1)
        with self.assertRaisesRegex(ValueError,'inconsistente'):time_check(session,process)

    def test_reversed_portico_endpoints_are_rejected(self):
        before=r136.models(HERE.parent/'h03-r136/SAP-CAD')
        after=r136.models(HERE/'SAP-CAD')
        after=copy.deepcopy(after)
        key=next(iter(after['portico']['data']['frames']))
        after['portico']['data']['frames'][key]=list(reversed(after['portico']['data']['frames'][key]))
        with self.assertRaisesRegex(ValueError,'ordenada'):validate_fine(before,after)

    def test_other_floor_change_is_rejected(self):
        before=r136.models(HERE.parent/'h03-r136/SAP-CAD')
        after=r136.models(HERE/'SAP-CAD')
        after=copy.deepcopy(after)
        after['N2']['data']['tables']['UNEXPECTED']=[{'Value':'1'}]
        with self.assertRaisesRegex(ValueError,'N2'):validate_fine(before,after)

if __name__=='__main__':unittest.main()
