import copy
import unittest
from consolidar import time_check

class TimeIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.session = {'startUtc': '2026-11-01T10:00:00Z', 'endUtc': '2026-11-01T10:03:00Z', 'wallMs': 180000}
        self.process = {'utc': '2026-11-01T10:00:30Z', 'endUtc': '2026-11-01T10:01:00Z', 'elapsedSeconds': 30}

    def test_processing_interval_is_contained(self):
        time_check(self.session, self.process)
        outside = copy.deepcopy(self.process)
        outside['endUtc'] = '2026-11-01T10:04:00Z'
        with self.assertRaisesRegex(ValueError, 'fora da sessão'):
            time_check(self.session, outside)

    def test_unknown_duration_cannot_become_zero_or_nan_time(self):
        for duration in [0, -1, float('nan'), float('inf')]:
            with self.subTest(duration=duration):
                invalid = {**self.process, 'elapsedSeconds': duration}
                with self.assertRaisesRegex(ValueError, 'Duração inválida'):
                    time_check(self.session, invalid)

if __name__ == '__main__':
    unittest.main()
