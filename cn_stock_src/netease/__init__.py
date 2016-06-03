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

""" Read stock data from 163

Sample:

```
NeteaseStock.latest(['sh600000', 'sh600010'])
```

"""
from six import string_types
from pandas import DataFrame
from cn_stock_src.cn_stock_util import TRADE_DETAIL_COLUMNS, \
    NETEASE_STOCK_INFO_COLUMNS
from cn_stock_src.cn_stock_base import CnStockBase
import json
import int_date
import re
import numpy as np

__author__ = 'Cedric Zhuang'

__all__ = ["latest"]


def latest(*indices):
    return NeteaseStock.latest(indices)


class NeteaseStock(CnStockBase):
    _BASE = "http://api.money.126.net/data/feed/{},money.api"

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _get_batch_size(cls):
        return 200

    @classmethod
    def _join_indices(cls, indices):
        trans_indices = map(cls._trans_index, indices)
        return ','.join(trans_indices)

    _PREFIX = '_ntes_quote_callback('
    _SUFFIX = ');'

    @classmethod
    def _parse(cls, body):
        if body.startswith(cls._PREFIX):
            body = body.replace(cls._PREFIX, '')
        if body.endswith(cls._SUFFIX):
            body = body.replace(cls._SUFFIX, '')

        stock_map = json.loads(body)

        stocks = DataFrame(columns=TRADE_DETAIL_COLUMNS)
        for name, stock in stock_map.items():
            s_date, s_time = stock['time'].split(' ')
            data = [stock['name'],
                    stock['open'],
                    stock['yestclose'],
                    stock['price'],
                    stock['high'],
                    stock['low'],
                    stock['volume'],
                    stock['turnover'],
                    stock['bidvol1'],
                    stock['bid1'],
                    stock['bidvol2'],
                    stock['bid2'],
                    stock['bidvol3'],
                    stock['bid3'],
                    stock['bidvol4'],
                    stock['bid4'],
                    stock['bidvol5'],
                    stock['bid5'],
                    stock['askvol1'],
                    stock['ask1'],
                    stock['askvol2'],
                    stock['ask2'],
                    stock['askvol3'],
                    stock['ask3'],
                    stock['askvol4'],
                    stock['ask4'],
                    stock['askvol5'],
                    stock['ask5'],
                    int_date.to_int_date(s_date),
                    s_time]
            index = '{}{}'.format(stock['type'].lower(), stock['symbol'])
            stocks.ix[index] = data
        return stocks

    @classmethod
    def _trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret


class NeteaseStockInfo(CnStockBase):
    """get stock info from netease html

    sample url looks like this:
    report data
    `http://quotes.money.163.com/f10/zycwzb_600010,report.html`

    season data
    `http://quotes.money.163.com/f10/zycwzb_600010,season.html`

    year data
    `http://quotes.money.163.com/f10/zycwzb_600010,year.html`

    season is the preferred source.
    """
    _BASE = "http://quotes.money.163.com/f10/zycwzb_{},report.html"

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _get_batch_size(cls):
        return 1

    @classmethod
    def _join_indices(cls, indices):
        length = len(indices)
        if length != 1:
            raise ValueError('only accept one stock per request.')
        return cls._process_index(indices[0])

    @classmethod
    def _process_index(cls, index):
        if index.startswith(('sh', 'sz')):
            index = index[2:]
        return index

    @classmethod
    def _parse(cls, body):
        matched = re.search(r'<div class="col_r" style="">(.*?)</div>', body,
                            re.MULTILINE | re.DOTALL | re.UNICODE)
        if matched is None or len(matched.groups()) == 0:
            raise ValueError('no matched data found.')

        lines = matched.group(1).strip().split('\n')

        value_pattern = re.compile(r'>(.*?)<', re.UNICODE)
        data_array = []
        stock_name = cls._get_stock_name(body)
        for line in lines:
            if r'<tr' not in line:
                continue

            data = []
            line = line.strip()
            for value in re.findall(value_pattern, line):
                value = cls._normalize(value)
                if isinstance(value, string_types) and len(value) == 0:
                    continue
                data.append(value)
            if len(data) > 0:
                data_array.append(data)

        if data_array:
            data_array.insert(0, [stock_name] * len(data_array[0]))
            data_array = np.array(data_array).T
        df = DataFrame(data_array, columns=NETEASE_STOCK_INFO_COLUMNS)
        df.set_index('date', inplace=True)
        return df

    @classmethod
    def _get_stock_name(cls, text):
        ret = ''
        name_pattern = re.compile(r"var STOCKNAME = '(.+)';", re.UNICODE)
        for value in re.findall(name_pattern, text):
            ret = value
            break
        return ret

    @classmethod
    def _normalize(cls, value):
        value = value.strip()
        if value == '--':
            value = None
        elif '-' in value and not value.startswith('-'):
            value = int_date.to_int_date(value)
        elif len(value) > 0:
            if ',' in value:
                value = value.replace(',', '')
            value = float(value)
        return value

    @classmethod
    def _trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret
