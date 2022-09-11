import pytest
from src.mqtt import Mqtt

def test_without_topic_in():
    opt_mqtt = 'mqtt://222.0.0.1:1883'
    mqtt = Mqtt(opt_mqtt)
    with pytest.raises(AttributeError):
        mqtt._validate() # pylint: disable=protected-access


def test_with_topic_in_url():
    opt_mqtt = 'mqtt://127.0.0.1:1883/mqtttossh/in'
    mqtt = Mqtt(opt_mqtt)
    mqtt._validate() # pylint: disable=protected-access

def test_with_topic_in():
    opt_mqtt = 'mqtt://127.0.0.1:1883'
    mqtt = Mqtt(opt_mqtt, 'mqtttossh/in')
    mqtt._validate() # pylint: disable=protected-access

def test_without_protocol():
    with pytest.raises(AssertionError):
        Mqtt('127.0.0.1')
