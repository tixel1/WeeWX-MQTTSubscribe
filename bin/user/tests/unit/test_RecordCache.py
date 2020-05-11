# pylint: disable=wrong-import-order
# pylint: disable=missing-docstring
# pylint: disable=invalid-name

import time

import unittest
import mock

import test_weewx_stubs # used to set up stubs - pylint: disable=unused-import
from user.MQTTSubscribe import RecordCache

class Test_clear_cache(unittest.TestCase):
    def test_cache_is_cleared(self):
        SUT = RecordCache()

        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        timestamp = time.time()
        SUT.update_value(key, record, timestamp)

        SUT.clear_cache()
        self.assertEqual(SUT.cached_values, {})

class Test_update_value(unittest.TestCase):
    def test_value_is_updated(self):
        SUT = RecordCache()

        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        timestamp = time.time()
        SUT.update_value(key, record, timestamp)
        self.assertIn(key, SUT.cached_values)
        # ToDo - more asserts

class Test_get_value(unittest.TestCase):
    def create_record(self):
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        return record

    def test_update_value(self):
        SUT = RecordCache()

        key = 'key'
        record = self.create_record()
        timestamp = time.time()
        SUT.update_value(key, record, timestamp)
        self.assertIn(key, SUT.cached_values)
        # ToDo - more asserts

    def test_key_not_in_cache(self):
        SUT = RecordCache()

        record = SUT.get_value('foo', 1, 0, None)

        self.assertIsNone(record)

    def test_get_data_unit_system_set(self):

        with mock.patch('user.MQTTSubscribe.weewx.units.to_std_system') as mock_to_std_system:
            SUT = RecordCache()
            key = 'key'

            converted_record = self.create_record()
            mock_to_std_system.return_value = converted_record

            record = self.create_record()
            SUT.update_value(key, record, time.time())

            cached_record = SUT.get_value(key, 1, 0, None)

            self.assertEqual(cached_record, converted_record)

    def test_get_data_unit_system_not_set(self):
        SUT = RecordCache()

        key = 'key'
        record = self.create_record()
        SUT.update_value(key, record, time.time())

        cached_record = SUT.get_value(key, None, 0, None)
        self.assertEqual(cached_record, record)

    def test_get_data_expiration_is_none(self):
        SUT = RecordCache()

        key = 'key'
        record = self.create_record()
        SUT.update_value(key, record, time.time())

        cached_record = SUT.get_value(key, None, None, None)
        self.assertEqual(cached_record, record)

    def test_get_data_is_not_expired(self):
        SUT = RecordCache()
        key = 'key'
        record = self.create_record()
        timestamp = time.time()
        SUT.update_value(key, record, timestamp)

        cached_record = SUT.get_value(key, None, timestamp, 1)
        self.assertEqual(cached_record, record)

    def test_get_data_is_expired(self):
        SUT = RecordCache()
        key = 'key'
        record = self.create_record()
        timestamp = time.time()
        SUT.update_value(key, record, timestamp)

        cached_record = SUT.get_value(key, None, timestamp + 1, 0)
        self.assertIsNone(cached_record)

class Test_update_timestamp(unittest.TestCase):
    def test_key_does_not_exist(self):
        # somewhat silly test
        SUT = RecordCache()
        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        SUT.update_value(key, record, time.time())

        nonexisting_key = 'key2'
        SUT.update_timestamp(nonexisting_key, time.time())
        self.assertNotIn(nonexisting_key, SUT.cached_values)

    def test_key_exists(self):
        SUT = RecordCache()
        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        SUT.update_value(key, record, 0)

        new_time = time.time()
        SUT.update_timestamp(key, new_time)
        self.assertEqual(SUT.cached_values['key']['timestamp'], new_time)

class Test_remove_value(unittest.TestCase):
    def test_key_does_not_exist(self):
        # somewhat silly test
        SUT = RecordCache()
        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        SUT.update_value(key, record, time.time())

        nonexisting_key = 'key2'
        SUT.remove_value(nonexisting_key)
        self.assertNotIn(nonexisting_key, SUT.cached_values)

    def test_key_exists(self):
        SUT = RecordCache()
        key = 'key'
        record = {}
        record['field1'] = "foo"
        record['field2'] = "bar"
        SUT.update_value(key, record, time.time())

        SUT.remove_value(key)
        self.assertNotIn(key, SUT.cached_values)

if __name__ == '__main__':
    unittest.main(exit=False)
