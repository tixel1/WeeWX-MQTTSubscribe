# pylint: disable=wrong-import-order
# pylint: disable=missing-docstring
# pylint: disable=invalid-name

import time

import unittest
import mock
from user.MQTTSubscribe import RecordCache

class Test_get_value(unittest.TestCase):
    def test_update_value(self):
        SUT = RecordCache()

        key = "foo"
        value = "bar"
        timestamp = time.time()
        SUT.update_value(key, value, timestamp)
        self.assertIn(key, SUT.cached_values)

    def test_key_not_in_cache(self):
        SUT = RecordCache()

        record = SUT.get_value('foo', 1, 0, None)

        self.assertIsNone(record)

    def test_get_data_unit_system_set(self):
        data = {}
        with mock.patch('user.MQTTSubscribe.weewx.units.to_std_system') as mock_to_std_system:
            SUT = RecordCache()
            mock_to_std_system.return_value = data

            key = "foo"
            value = "bar"
            timestamp = time.time()
            SUT.update_value(key, value, timestamp)

            record = SUT.get_value('foo', 1, 0, None)

            print(record)

    def test_get_data_unit_system_not_set(self):
        # data = {}
        # with mock.patch('user.MQTTSubscribe.weewx.units.to_std_system') as mock_to_std_system:
        SUT = RecordCache()
        #mock_to_std_system.return_value = data

        key = "foo"
        value = "bar"
        timestamp = time.time()
        SUT.update_value(key, value, timestamp)

        record = SUT.get_value('foo', None, 0, None)

        print(record)

    # test get_data expiration is none
    # test get_data is not expired
    # test get_data expired

    # test update_timestamp, key exists
    # test update_timestamp, key does not exist

    # test remove_value, key exists
    # test remove_value, key does not exist

    # test clear cache

if __name__ == '__main__':
    unittest.main(exit=False)
