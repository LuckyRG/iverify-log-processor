from datetime import date
import unittest
from unittest.mock import patch

from utils.TimeHelper import get_current_timestamp_utc

# Unit test class
class TestTimeHelper(unittest.TestCase):
    def test_get_current_timestamp_utc_success(self):
        with (
            patch('utils.TimeHelper.datetime') as mock_datetime,
        ):
            # mock date to alwyas return set value for test
            mock_datetime.now.return_value = date(2024, 6, 11)
            mock_datetime.side_effect = lambda *args, **kw: date(*args, **kw)

            test_expected_result = '2024-06-11T00-00-00-000'

            result: str = get_current_timestamp_utc()            

            self.assertEqual(result, test_expected_result)



if __name__ == '__main__':
    unittest.main()
