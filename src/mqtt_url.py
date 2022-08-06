from urllib.parse import urlparse

class MqttUrl():

    def __init__(self, url):
        self._url = None
        self._topic = None
        self.set_url(url)

    def set_url(self, url):
        self._url = _parse_url(url)
        self._topic = _parse_topic(self.get_url())

    def get_url(self):
        return self._url

    def get_topic(self):
        return self._topic

    def get_hostname(self):
        return self.get_url().hostname

    def get_port(self):
        return self.get_url().port

    def get_protocol(self):
        # pylint: disable=no-member
        return self.get_url().protocol

    def get_username(self):
        return self.get_url().username

    def get_password(self):
        return self.get_url().password

def _parse_url(url):
    url = url.replace("#","[HASHMARK]")
    url = urlparse(url)
    return url

def _parse_topic(url):
    topic = url.path
    topic = topic.strip("/")
    topic = topic.replace("[HASHMARK]", "#")
    return topic
