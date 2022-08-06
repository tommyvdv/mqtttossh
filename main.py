"""mqtttossh

Usage:
    main.py [-v|--version]
            [-h|--help]
            [-d|--debug]
            [--config main.conf]
            [--mqtt protocol://username:password@host:port/topic]

Options:
    -h --help                       Show this messsage and exit
    -v --version                    Show version info and exit
    -d --debug                      Print debug information
    -q HOST --mqtt HOST             MQTT connection string
                                    [default: mqtt://192.168.1.47:1883/python/mqtttossh/in]
    -c CONFIG --config CONFIG       Configuration file [default: main.conf]

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

log = Log(__name__, logging.DEBUG)
option = docopt(__doc__, version='mqtttossh version 0.1')
opt_version = option['--version']
opt_config = option['--config']
opt_debug = option['--debug']
opt_mqtt = option['--mqtt']

try:
    config = Config(opt_config)
except Exception as e: # pylint: disable=broad-except
    print(f"Cannot load configuration from file {opt_config}: {e}")
    sys.exit(2)

if opt_debug:
    log.debug(f"opt_version: {opt_version}")
    log.debug(f"opt_config: {opt_config}")
    log.debug(f"opt_debug: {opt_debug}")
    log.debug(f"opt_mqtt: {opt_mqtt}")
    log.debug(f"config: {config}")

def on_message(client, userdata, message):
    if message.topic in [
        config.get('topic_in'),
    ]:
        print(f'message {userdata} {client} {message.topic} {message.payload}')

def on_disconnect(client, userdata, return_code):
    print(f'{return_code} disconnected {userdata} {client}')

def on_connect_fail(client, userdata, return_code):
    print(f'{return_code} failed to connect {userdata} {client}')

def on_connect(client, userdata, flags, return_code):
    print(f'{return_code} connection established {userdata} {flags} {client}')

TIMEOUT = 1
async def do_log():
    print('tick')
    await asyncio.sleep(TIMEOUT)

async def main():
    mqtt = Mqtt(option['--mqtt'])
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
