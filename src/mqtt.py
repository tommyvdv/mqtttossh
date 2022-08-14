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

    def __init__(self, url):
        self._log = Log(__name__, logging.DEBUG, 'var/log/')
        self._url = MqttUrl(url)
        self._client = _get_client(self._url)
        self._birth_msg = None
        self._last_msg = None

    def publish(self, msg):
        self._client.publish(msg.topic, msg.payload)

    def set_handler(self, handler, function):
        setattr(self._client, handler, function)

    def set_birth(self, topic, payload):
        # todo; throw an exception if the client is already connected
        self._birth_msg = Message(topic, payload)

    def set_last_will(self, topic, payload):
        # todo; throw an exception if the client is already connected
        self._last_msg = Message(topic, payload)

    def _subscribe(self, url):
        self._log.debug(f"subscribing to \"{self._url.get_topic()}\"")
        self._client.subscribe(url.get_topic())

    def connect(self):
        msg = self._last_msg
        if msg:
            self._client.will_set(msg.topic, msg.payload)
        self._client.connect(host=self._url.get_hostname(), port=self._url.get_port())
        msg = self._birth_msg
        if msg:
            self.publish(self._birth_msg)
        self._subscribe(self._url)

    def start(self):
        self.connect()
        self._client.loop_start()

def _get_client(url):
    client = mqtt.Client()
    client.username_pw_set(username=url.get_username(), password=url.get_password())
    return client
