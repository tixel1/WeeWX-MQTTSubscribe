# pylint: disable=wrong-import-order
# pylint: disable=missing-docstring
# pylint: disable=invalid-name

import random
import string
import time

import unittest
import mock

import test_weewx_stubs # used to set up stubs - pylint: disable=unused-import
from user.MQTTSubscribe import FieldCache

class Test_clear_cache(unittest.TestCase):
    def test_cache_is_cleared(self):
        SUT = FieldCache()

        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        timestamp = time.time()
        SUT.update_value(key, value, units, timestamp)

        SUT.clear_cache()
        self.assertEqual(SUT.cached_values, {})

class Test_update_value(unittest.TestCase):
    def test_value_is_updated(self):
        SUT = FieldCache()

        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        timestamp = time.time()

        SUT.update_value(key, value, units, timestamp)
        self.assertIn(key, SUT.cached_values)
        self.assertEqual(SUT.cached_values[key]['value'], value)
        self.assertEqual(SUT.cached_values[key]['units'], units)
        self.assertEqual(SUT.cached_values[key]['timestamp'], timestamp)

class Test_get_value(unittest.TestCase):
    def test_key_not_in_cache(self):
        SUT = FieldCache()

        value = SUT.get_value('foo', 1, 0, None)

        self.assertIsNone(value)

    def test_get_data_unit_system_set(self):

        with mock.patch('user.MQTTSubscribe.weewx.units.getStandardUnitType')as mock_getStandardUnitType:
            with mock.patch('user.MQTTSubscribe.weewx.units.convert') as mock_convert:
                SUT = FieldCache()
                key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
                value = round(random.uniform(1, 100), 2)
                units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

                mock_getStandardUnitType.return_value = \
                    (''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]),
                     ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]))

                converted_value = round(random.uniform(1, 100), 2)
                mock_convert.return_value = \
                    (converted_value, random.randint(1, 10), ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]))

                SUT.update_value(key, value, units, time.time())

                cached_value = SUT.get_value(key, 1, 0, None)

                self.assertEqual(cached_value, converted_value)

    def test_get_data_unit_system_not_set(self):
        SUT = FieldCache()

        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, time.time())

        cached_value = SUT.get_value(key, None, 0, None)
        self.assertEqual(cached_value, value)

    def test_get_data_expiration_is_none(self):
        SUT = FieldCache()

        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, time.time())

        cached_value = SUT.get_value(key, None, None, None)
        self.assertEqual(cached_value, value)

    def test_get_data_is_not_expired(self):
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        timestamp = time.time()
        SUT.update_value(key, value, units, timestamp)

        cached_value = SUT.get_value(key, None, timestamp, 1)
        self.assertEqual(cached_value, value)

    def test_get_data_is_expired(self):
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        timestamp = time.time()
        SUT.update_value(key, value, units, timestamp)

        cached_value = SUT.get_value(key, None, timestamp + 1, 0)
        self.assertIsNone(cached_value)

class Test_update_timestamp(unittest.TestCase):
    def test_key_does_not_exist(self):
        # somewhat silly test
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, time.time())

        nonexisting_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_timestamp(nonexisting_key, time.time())
        self.assertNotIn(nonexisting_key, SUT.cached_values)

    def test_key_exists(self):
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, 0)

        new_time = time.time()
        SUT.update_timestamp(key, new_time)
        self.assertEqual(SUT.cached_values[key]['timestamp'], new_time)

class Test_remove_value(unittest.TestCase):
    def test_key_does_not_exist(self):
        # somewhat silly test
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, time.time())

        nonexisting_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.remove_value(nonexisting_key)
        self.assertNotIn(nonexisting_key, SUT.cached_values)

    def test_key_exists(self):
        SUT = FieldCache()
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        value = round(random.uniform(1, 100), 2)
        units = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT.update_value(key, value, units, time.time())

        SUT.remove_value(key)
        self.assertNotIn(key, SUT.cached_values)

if __name__ == '__main__':
    unittest.main(exit=False)
