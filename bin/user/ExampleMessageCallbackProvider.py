"""


Configuration:
[MQTTSubscribeService] or [MQTTSubscribeDriver]

    # The message callback provider.
    message_callback_provider = user.ExampleMessageCallbackProvider.MessageCallbackProvider

    # Configuration for the message callback.
    [[message_callback]]
        # The delimiter between fieldname and value pairs. (field1=value1, field2=value2).
        # Default is: ,
        keyword_delimiter = ,

        # The separator between fieldname and value pairs. (field1=value1, field2=value2).
        # Default is: =
        keyword_separator = =

        # Mapping to WeeWX names.
        [[[label_map]]]
            temp1 = extraTemp1
"""

from __future__ import print_function
import xml.etree.ElementTree
#from weeutil.weeutil import to_float
import user.MQTTSubscribe
#import user.MQTTSubscribe.MessageCallbackProvider

class MessageCallbackProvider(user.MQTTSubscribe.MessageCallbackProvider):
    # pylint: disable=too-few-public-methods
    """ Provide the MQTT callback. """
    def __init__(self, config, logger, topic_manager): # pylint: disable=super-init-not-called
        # ToDo call base class init when an abstract class exists
        self.logger = logger
        self.topic_manager = topic_manager
        self.keyword_delimiter = config.get('keyword_delimiter', ',')
        self.keyword_separator = config.get('keyword_separator', '=')
        self.label_map = config.get('label_map', {})

        self.fields = config.get('fields', {}) # hack, in case no fields are set

    def get_callback(self):
        """ Get the MQTT callback. """
        return self._on_message

    def get_observations(self, parent, fullname, fields, unit_system):
        """ Create the dictionary of observations. """
        observations = {}

        for child in parent:
            saved_fullname = fullname
            fullname = fullname + '/' + child.tag
            observations.update(self.get_observations(child, fullname, fields, unit_system))
            fullname = saved_fullname

        if parent.text is None:
            for (name, tvalue) in parent.items(): # need to match signature pylint: disable=unused-variable
                (fieldname, value) = self._update_data(fields, fullname[1:], tvalue, unit_system)
                observations[fieldname] = value
        elif not parent:
            (fieldname, value) = self._update_data(fields, fullname[1:], parent.text, unit_system)
            observations[fieldname] = value

        return observations

    def _on_message(self, client, userdata, msg):  # (match callback signature) pylint: disable=unused-argument
        # Wrap all the processing in a try, so it doesn't crash and burn on any error
        try:
            self.logger.debug("MessageCallbackProvider For %s received: %s" %(msg.topic, msg.payload))
            fields = self._get_fields(msg.topic)
            unit_system = self.topic_manager.get_unit_system(msg.topic) # TODO - need public method
            root = xml.etree.ElementTree.fromstring(msg.payload)
            observations = self.get_observations(root, "", fields, unit_system)

            if observations:
                self.topic_manager.append_data(msg.topic, observations)

        except Exception as exception: # (want to catch all) pylint: disable=broad-except
            self.logger.error("MessageCallbackProvider on_message_keyword failed with: %s" % exception)
            self.logger.error("**** MessageCallbackProvider Ignoring topic=%s and payload=%s" % (msg.topic, msg.payload))