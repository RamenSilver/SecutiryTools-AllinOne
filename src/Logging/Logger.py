# coding: utf-8
import configparser
import logging
from abc import ABCMeta, abstractmethod
from functools import wraps
import requests


class AbstractLogger(metaclass=ABCMeta):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = configparser.ConfigParser()
        self._config.read('config.ini', encoding='utf-8')
        self._log_output_dir = self._config['LOG']['DIR_NAME']

    @abstractmethod
    def wrap(pre,post):
        def decorate(func):
            def call(*args, **kwargs):
               """ Actual wrapping """
               pre(func)
               result = func(*args, **kwargs)
               post(func)
               return result
            return call
        return decorate

class HttpClientLogger(AbstractLogger):
    def __init__(self):
        super().__init__(self)

    def wrap(self,pre,post):
        def decorate(func):
            def call(*args, **kwargs):
               """ Actual wrapping """
               pre(func)
               self.logger.info('-'*20)
               self.logger.info()
               #self.logger.info('%s - %s - %s - %s', request.remote_addr, request.method, request.url, request.query_string)
               self.logger.info()
               result = func(*args, **kwargs)
               self.logger.info()
               self.logger.info('-'*20)
               post(func)
               return result
            return call
        return decorate
