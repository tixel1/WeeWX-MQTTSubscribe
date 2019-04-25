from __future__ import with_statement

import unittest
import mock

import paho.mqtt.client as mqtt
import random
import string
from user.MQTTSubscribe import MQTTSubscribe, MQTTSubscribeService

class TestInitialization(unittest.TestCase):
    def test_payload_type_json(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = 'json'
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = None
        password = None
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        self.assertEquals(mock_client.on_message, SUT.on_message_json)

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_payload_type_individual(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = 'individual'
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = None
        password = None
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        self.assertEquals(mock_client.on_message, SUT.on_message_individual)

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_payload_type_other(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = None
        password = None
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        self.assertEquals(mock_client.on_message, SUT.on_message)

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_username_None(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = None
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = None
        password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        mock_client.username_pw_set.assert_not_called()

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_password_None(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = None
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        password = None
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        mock_client.username_pw_set.assert_not_called()

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_username_and_password_None(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = None
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = None
        password = None
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        mock_client.username_pw_set.assert_not_called()

        mock_client.connect.assert_called_once_with(host, port, keepalive)

    def test_username_and_password_set(self):
        console = False
        mock_client = mock.Mock(spec=mqtt.Client)
        queue = None
        archive_queue = None
        label_map = {}
        unit_system = random.randint(1, 10)
        payload_type = None
        host = 'host'
        keepalive = random.randint(1, 10)
        port = random.randint(1, 10)
        username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        topic = None
        archive_topic = None

        SUT = MQTTSubscribe(console, mock_client, queue, archive_queue, label_map, unit_system, payload_type,
                            host, keepalive, port, username, password, topic, archive_topic
                            )

        mock_client.username_pw_set.assert_called_once_with(username, password)

        mock_client.connect.assert_called_once_with(host, port, keepalive)

class Teston_connect(unittest.TestCase):
    console = False
    queue = None
    archive_queue = None
    label_map = {}
    unit_system = random.randint(1, 10)
    payload_type = None
    host = 'host'
    keepalive = random.randint(1, 10)
    port = random.randint(1, 10)
    username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    topic = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

    def test_archive_topic_set(self):
        mock_client = mock.Mock(spec=mqtt.Client)
        archive_topic = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        SUT = MQTTSubscribe(self.console, mock_client, self.queue, self.archive_queue, self.label_map, self.unit_system, self.payload_type,
                            self.host, self.keepalive, self.port, self.username, self.password, self.topic, archive_topic
                            )

        rc = random.randint(1, 10)
        SUT.on_connect(mock_client, None, None, rc,)

        self.assertEqual(mock_client.subscribe.call_count, 2)
        mock_client.subscribe.assert_called_with(archive_topic)

    def test_archive_topic_not_set(self):
        mock_client = mock.Mock(spec=mqtt.Client)
        archive_topic = None
        SUT = MQTTSubscribe(self.console, mock_client, self.queue, self.archive_queue, self.label_map, self.unit_system, self.payload_type,
                            self.host, self.keepalive, self.port, self.username, self.password, self.topic, archive_topic
                            )

        rc = random.randint(1, 10)
        SUT.on_connect(mock_client, None, None, rc,)

        self.assertEqual(mock_client.subscribe.call_count, 1)

class TestJsonPayload(unittest.TestCase):
    pass

class TestIndividualPayload(unittest.TestCase):
    pass

class TestKeywoardPayload(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
