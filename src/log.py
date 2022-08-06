import datetime
import logging
import time
import os

class Log:

    # pylint: disable=too-many-arguments
    def __init__(self, topic='none', level=logging.NOTSET, path=None, indent_level=7, indent_name=11, stdout=False):
        self.time_start = None
        self.log = None
        self.topic = None
        self.level = None
        self.indent_level = 7
        self.indent_name = 11

        self.topic = topic
        self.set_indent(indent_level=indent_level, indent_name=indent_name)
        self.set_log_level(level)
        self.log = logging.getLogger(topic)
        if stdout:
            self.log.addHandler(self.get_handler())
        if path:
            self.log.addHandler(self.get_file_handler(path))
        self.log.setLevel(self.level)

    def set_indent(self, indent_level, indent_name):
        self.indent_level = indent_level
        self.indent_name = indent_name

    def set_log_level(self, level):
        if isinstance(level, str) and getattr(logging, level):
            self.level = getattr(logging, level)
        else:
            self.level = level

    def get_handler(self):
        handler = logging.StreamHandler()
        handler.setFormatter(self.get_formatter())
        return handler

    def get_file_handler(self, path):
        os.makedirs(path, exist_ok=True)
        handler = logging.FileHandler(f'{path}/{self.topic}.log')
        handler.setLevel(self.level)
        handler.setFormatter(self.get_formatter())
        return handler

    def get_formatter(self):
        name = self.indent_name
        level = self.indent_level
        result = Formatter(fmt=f'%(asctime)s %(levelname){level}s - %(name)-{name}s - %(message)s', datefmt='%H:%M')
        return result

    def debug(self, string):
        self.log.debug(string)

    def info(self, string):
        self.log.info(string)

    def warning(self, string):
        self.log.warning(string)

    def error(self, string):
        self.log.error(string)

    def critical(self, string):
        self.log.critical(string)

    def exception(self, string):
        self.log.exception(string)

    def get_time(self):
        if self.time_start is None:
            self.time_start = time.time()
        current_time = time.strftime('%H:%M')
        seconds = time.time() - self.time_start
        uptime = str(datetime.timedelta(seconds=seconds))
        uptime = uptime.split('.', maxsplit=1)[0]
        return f'{uptime} {current_time}'

class Formatter(logging.Formatter):
    time_start = None
    def formatTime(self, record, datefmt='%H:%M'):
        if self.time_start is None:
            self.time_start = time.time()
        current_time = time.strftime(datefmt)
        seconds = time.time() - self.time_start
        uptime = str(datetime.timedelta(seconds=seconds))
        uptime = uptime.split('.', maxsplit=1)[0]
        return f'{uptime} {current_time}'
