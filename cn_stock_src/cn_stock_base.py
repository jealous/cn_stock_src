import logging
import numpy
import requests
from cn_stock_src import CnStockHttpError

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


class CnStockBase(object):
    def __init__(self):
        pass

    @classmethod
    def get_base(cls):
        raise NotImplementedError('get_base must be implemented')

    @classmethod
    def parse(cls, body):
        raise NotImplementedError('parse not implemented.')

    @classmethod
    def join_indices(cls, indices):
        raise NotImplementedError('join_indices not implemented.')

    @classmethod
    def get_batch_size(cls):
        return 100

    @classmethod
    def latest(cls, indices, method=None):
        if method is None:
            method = requests.get
        data = cls.retrieve_data(indices, method)
        return cls.parse(data)

    @staticmethod
    def is_valid_number(number):
        from math import isnan, isinf
        valid = True
        if number is None or isinf(number) or isnan(number):
            valid = False
        return valid

    @classmethod
    def retrieve_data(cls, indices, method=None):
        if (isinstance(indices, list)
                or isinstance(indices, tuple)
                or isinstance(indices, numpy.ndarray)):
            index = cls.join_indices(indices)
        else:
            index = indices
        url = cls.get_base().format(index)
        log.debug("GET: %s", url)
        if method is None:
            response = requests.get(url, timeout=30)
        else:
            response = method(url)
        if response.status_code != 200:
            raise CnStockHttpError(url, response.status_code)
        return response.text.encode('UTF-8')
