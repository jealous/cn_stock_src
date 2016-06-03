# coding=utf-8
# Copyright (c) 2016, Cedric Zhuang
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of disclaimer nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import requests
from cn_stock_src import CnStockHttpError

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


class CnStockBase(object):
    def __init__(self):
        pass

    @classmethod
    def _get_base(cls):
        raise NotImplementedError('get_base must be implemented')

    @classmethod
    def _parse(cls, body):
        raise NotImplementedError('parse not implemented.')

    @classmethod
    def _join_indices(cls, indices):
        raise NotImplementedError('join_indices not implemented.')

    @classmethod
    def _get_batch_size(cls):
        return 100

    @classmethod
    def _process_index(cls, index):
        return index

    @classmethod
    def latest(cls, indices, method=None):
        if method is None:
            method = requests.get
        data = cls._retrieve_data(indices, method)
        return cls._parse(data)

    @staticmethod
    def _is_valid_number(number):
        from math import isnan, isinf
        valid = True
        if number is None or isinf(number) or isnan(number):
            valid = False
        return valid

    @classmethod
    def _retrieve_data(cls, indices, method=None):
        if hasattr(indices, '__iter__'):
            index = cls._join_indices(indices)
        else:
            index = cls._process_index(indices)
        url = cls._get_base().format(index)
        log.info("GET: %s", url)
        if method is None:
            response = requests.get(url, timeout=30)
        else:
            response = method(url)
        if response.status_code != 200:
            raise CnStockHttpError(url, response.status_code)
        return response.text.encode('UTF-8')
