import logging

import paho.mqtt.client as mqtt
from src.log import Log
from src.mqtt_url import MqttUrl
from src.mqtt_message import Message

HANDLER_ON_MESSAGE = 'on_message'
HANDLER_ON_DISCONNECT = 'on_disconnect'
HANDLER_ON_CONNECT = 'on_connect'
HANDLER_ON_CONNECT_FAIL = 'on_connect_fail'
#HANDLER_ON_BIRTH = 'on_birth'
#HANDLER_ON_LAST_WILL = 'on_last_will'

# from paho
# on_connect, on_connect_fail, on_disconnect, on_message, on_publish,
# on_subscribe, on_unsubscribe, on_log, on_socket_open, on_socket_close,
# on_socket_register_write, on_socket_unregister_write

class Mqtt():

    def __init__(self, url, topic = None):
        self._log = Log(__name__, logging.DEBUG, 'var/log/')
        self._url = MqttUrl(url)
        self._topic = self._url.get_topic() if None is topic else topic
        self._client = _get_client(self._url)
        self._birth_msg = None
        self._last_msg = None

    def publish(self, msg):
        self._client.publish(msg.get_topic(), msg.get_payload())

    def set_handler(self, handler, function):
        setattr(self._client, handler, function)

    def set_birth(self, topic, payload):
        # todo; throw an exception if the client is already connected
        self._birth_msg = Message(topic, payload)

    def set_last_will(self, topic, payload):
        # todo; throw an exception if the client is already connected
        self._last_msg = Message(topic, payload)

    def _client_will(self, msg = None):
        try:
            self._client.will_set(msg.get_topic(), msg.get_payload())
        except AttributeError:
            self._log.debug("No \"last will\" for message is empty.")
        except ValueError:
            self._log.error(f"Last will message has invalid topic: \"{msg.get_topic()}\"")

    def _client_birth(self, msg = None):
        try:
            self.publish(msg)
        except AttributeError:
            self._log.debug("No \"birth\" for message is empty.")
        except ValueError:
            self._log.error(f"Failed to publish birth msg: \"{msg.get_topic()}\" \"{msg.get_payload()}\"")

    def _client_connect(self, url):
        self._client.connect(host=url.get_hostname(), port=url.get_port())

    def _client_subscribe(self, topic):
        try:
            self._client.subscribe(topic)
        except ValueError:
            self._log.error(f"Failed to subscribe to topic: \"{topic}\"")

    def connect(self):
        self._validate()
        self._client_will(self._last_msg)
        self._client_connect(self._url)
        self._client_birth(self._birth_msg)
        self._client_subscribe(self._topic)

    def start(self):
        self.connect()
        self._client.loop_start()

    def _validate(self):
        if None is self._topic:
            raise AttributeError("No input topic was set.")
        if None is self._last_msg:
            self._log.error("No \"last will\" message was set.")
        if None is self._birth_msg:
            self._log.error("No \"birth\" message was set.")
        if None is self._url:
            self._log.error("No \"url\" object was set.")

def _get_client(url):
    client = mqtt.Client()
    client.username_pw_set(username=url.get_username(), password=url.get_password())
    return client
