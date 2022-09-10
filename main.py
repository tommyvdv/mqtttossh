"""mqtttossh

Usage:
    main.py [-v|--version]
            [-h|--help]
            [-d|--debug]
            [--config main.conf]
            [--mqtt protocol://username:password@host:port/topic]
            [--mqtt-topic-in topic]
            [--mqtt-topic-out topic]

Options:
    -h --help                               Show this messsage and exit
    -v --version                            Show version info and exit
    -d --debug                              Print debug information
                                            [default: False]
    -q HOST --mqtt HOST                     MQTT connection string
                                            [default: mqtt://192.168.1.47:1883/python/mqtttossh/in]
    -i TOPIC_IN --mqtt-topic-in TOPIC_IN    MQTT topic for incoming messages
                                            [default: python/mqtttossh/in]
    -o TOPIC_OUT --mqtt-topic-out TOPIC_OUT MQTT topic for incoming messages
                                            [default: python/mqtttossh/out]
    -c CONFIG --config CONFIG               Configuration file [default: main.conf]

"""
import asyncio
import logging
import sys

from docopt import docopt
from src.config import Config
from src.log import Log
from src.mqtt import HANDLER_ON_CONNECT
from src.mqtt import HANDLER_ON_CONNECT_FAIL
from src.mqtt import HANDLER_ON_DISCONNECT
from src.mqtt import HANDLER_ON_MESSAGE
from src.mqtt import Mqtt
from src.mqtt_message import CommandFactory

option = docopt(__doc__, version='mqtttossh version 0.1')
opt_version = option['--version']
opt_config = option['--config']
log = Log(__name__, logging.DEBUG, stdout=True)

try:
    config = Config(opt_config)
except Exception as e: # pylint: disable=broad-except
    log.error(f"Cannot load configuration from file {opt_config}: {e}")
    sys.exit(2)

opt_debug = option['--debug']
opt_debug = config.get('debug', opt_debug)
opt_mqtt = option['--mqtt']
opt_mqtt = config.get('mqtt', opt_mqtt)
opt_mqtt_topic_in = option['--mqtt-topic-in']
opt_mqtt_topic_in = config.get('mqtt_topic_in', opt_mqtt_topic_in)
opt_mqtt_topic_out = option['--mqtt-topic-out']
opt_mqtt_topic_out = config.get('mqtt_topic_out', opt_mqtt_topic_out)
opt_mqtt_payload_birth = config.get('mqtt_payload_birth')
opt_mqtt_payload_last_will = config.get('mqtt_payload_last_will')

if opt_debug:
    log.debug(f"opt_version: {opt_version}")
    log.debug(f"opt_config: {opt_config}")
    log.debug(f"opt_debug: {opt_debug}")
    log.debug(f"opt_mqtt: {opt_mqtt}")
    log.debug(f"opt_mqtt_topic_in: {opt_mqtt_topic_in}")
    log.debug(f"opt_mqtt_topic_out: {opt_mqtt_topic_out}")
    log.debug(f"opt_mqtt_payload_birth: {opt_mqtt_payload_birth}")
    log.debug(f"opt_mqtt_payload_last_will: {opt_mqtt_payload_last_will}")
    log.debug(f"config: {config}")

mqtt = Mqtt(opt_mqtt, opt_mqtt_topic_in)
factory = CommandFactory(project_dir=config.get('ansible_project_dir'), inventory=config.get('ansible_inventory'))

def on_message(client, userdata, message):
    if message.topic in [
        opt_mqtt_topic_in,
    ]:
        log.debug(f'message {userdata} {client} {message.topic} (qos:{message.qos}) (retain:{message.retain}) {message.payload}')
        command = factory.create(message)
        command.publish(mqtt, opt_mqtt_topic_out, debug=True)

def on_disconnect(client, userdata, return_code):
    log.error(f'{return_code} disconnected {userdata} {client}')

def on_connect_fail(client, userdata, return_code):
    log.error(f'{return_code} failed to connect {userdata} {client}')

def on_connect(client, userdata, flags, return_code):
    log.error(f'{return_code} connection established {userdata} {flags} {client}')

TIMEOUT = 1
async def do_log():
    log.debug('tick')
    await asyncio.sleep(TIMEOUT)

async def main():
    mqtt.set_birth(opt_mqtt_topic_out, opt_mqtt_payload_birth)
    mqtt.set_last_will(opt_mqtt_topic_out, opt_mqtt_payload_last_will)
    mqtt.set_handler(HANDLER_ON_MESSAGE, on_message)
    mqtt.set_handler(HANDLER_ON_DISCONNECT, on_disconnect)
    mqtt.set_handler(HANDLER_ON_CONNECT, on_connect)
    mqtt.set_handler(HANDLER_ON_CONNECT_FAIL, on_connect_fail)
    mqtt.start()
    while True:
        pass
        #await asyncio.wait([
        #    loop.create_task(do_log()),
        #])

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
