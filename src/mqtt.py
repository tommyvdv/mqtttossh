import logging

import paho.mqtt.client as mqtt
from src.log import Log
from src.mqtt_url import MqttUrl

HANDLER_ON_MESSAGE = 'on_message'
HANDLER_ON_DISCONNECT = 'on_disconnect'
HANDLER_ON_CONNECT = 'on_connect'
HANDLER_ON_CONNECT_FAIL = 'on_connect_fail'

class Mqtt():

    def __init__(self, url):
        self._log = Log(__name__, logging.DEBUG, 'var/log/')
        self._url = MqttUrl(url)
        self._client = _get_client(self._url)
        self._subscribe(self._url)

    def set_handler(self, handler, function):
        setattr(self._client, handler, function)

    def _subscribe(self, url):
        self._log.debug(f"subscribing to \"{self._url.get_topic()}\"")
        self._client.subscribe(url.get_topic())

    def start(self):
        self._client.loop_start()

def _get_client(url):
    client = mqtt.Client()
    client.connect(host=url.get_hostname(), port=url.get_port())
    client.username_pw_set(username=url.get_username(), password=url.get_password())
    return client
