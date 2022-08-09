import logging

import paho.mqtt.client as mqtt
from src.log import Log
from src.mqtt_url import MqttUrl

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
        self._on_birth = None

    def set_handler(self, handler, function):
        setattr(self._client, handler, function)

    def set_birth(self, function):
        self._on_birth = function

    def set_last_will(self, function):
        function(self._client)

    def _subscribe(self, url):
        self._log.debug(f"subscribing to \"{self._url.get_topic()}\"")
        self._client.subscribe(url.get_topic())

    def connect(self):
        self._client.connect(host=self._url.get_hostname(), port=self._url.get_port())
        self._on_birth(self._client)
        self._subscribe(self._url)

    def start(self):
        self.connect()
        self._client.loop_start()

def _get_client(url):
    client = mqtt.Client()
    client.username_pw_set(username=url.get_username(), password=url.get_password())
    return client
