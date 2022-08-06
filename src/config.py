# pylint: disable=too-few-public-methods
class Config():

    def __init__(self, filename='main.conf'):
        self.config = {}
        # pylint: disable=exec-used,consider-using-with
        exec(compile(open(filename, "rb").read(), filename, 'exec'), self.config)

    def get(self, key, default=None):
        return self.config.get(key, default)
