from urllib.parse import ParseResult
import pytest
from src.mqtt_url import MqttUrl

def test_with_protocol_host_port_topic():
    url = MqttUrl('mqtt://127.0.0.1:1883/mqtttossh/in')
    assert 'mqtt' == url.get_protocol()
    assert '127.0.0.1' == url.get_hostname()
    assert 1883 == url.get_port()
    assert 'mqtttossh/in' == url.get_topic()
    assert isinstance(url.get_url(), ParseResult)

def test_with_protocol_host_port():
    url = MqttUrl('mqtt://127.0.0.1:1883/')
    assert 'mqtt' == url.get_protocol()
    assert '127.0.0.1' == url.get_hostname()
    assert 1883 == url.get_port()
    assert None is url.get_topic()
    assert isinstance(url.get_url(), ParseResult)

    url = MqttUrl('mqtt://127.0.0.1:1883')
    assert 'mqtt' == url.get_protocol()
    assert '127.0.0.1' == url.get_hostname()
    assert 1883 == url.get_port()
    assert None is url.get_topic()
    assert isinstance(url.get_url(), ParseResult)

def test_with_protocol_host():
    url = MqttUrl('mqtt://127.0.0.1')
    assert 'mqtt' == url.get_protocol()
    assert '127.0.0.1' == url.get_hostname()
    assert 1883 == url.get_port()
    assert None is url.get_topic()
    assert isinstance(url.get_url(), ParseResult)

def test_with_protocol_host_topic():
    url = MqttUrl('mqtt://127.0.0.1/mqtttossh/in')
    assert 'mqtt' == url.get_protocol()
    assert '127.0.0.1' == url.get_hostname()
    assert 1883 == url.get_port()
    assert 'mqtttossh/in' == url.get_topic()
    assert isinstance(url.get_url(), ParseResult)

def test_with_host():
    with pytest.raises(AssertionError):
        MqttUrl('127.0.0.1')
