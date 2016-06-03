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

"""Read data from yahoo

sample

```
YahooStock.retrieve_data('sh600000')
```
"""
from six import StringIO
import logging
import int_date
import requests
import pandas as pd
from cn_stock_src.cn_stock_util import YAHOO_K_LINE_COLUMNS

__author__ = 'Cedric Zhuang'

__all__ = ["daily_k_line"]


log = logging.getLogger(__name__)


def daily_k_line(index):
    return YahooStock.daily_k_line(index)


class YahooStock(object):
    _DAILY_KL_URL = 'http://table.finance.yahoo.com/table.csv?s={}'

    def __init__(self):
        pass

    @staticmethod
    def _process_data(df):
        """change the column name and date format

        change the column name and date format

        :param df: source data frame
        :return: updated data frame
        """
        df.columns = YAHOO_K_LINE_COLUMNS
        df['date'] = df.date.apply(int_date.to_int_date)
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        return df[df.volume != 0]

    @staticmethod
    def daily_k_line(index, protocol=None, method=None):
        """get daily K line from Yahoo finance.

        :param index: stock index like sh600000
        :param protocol: 'http' or 'https'
        :param method: debug only
        :return: data frame of the daily K line
        """
        yahoo_index = YahooStock._index_converter(index)
        request_url = YahooStock._DAILY_KL_URL.format(yahoo_index)
        if protocol is not None:
            request_url = request_url.replace("http", protocol)
        log.debug("url: %s", request_url)
        if method is None:
            response = requests.get(request_url, timeout=30)
        else:
            response = method(request_url)
        df = pd.read_csv(StringIO(response.text))
        df = YahooStock._process_data(df)
        df.columns.name = index
        return df

    @staticmethod
    def _index_converter(index):
        """convert stock index into yahoo format

        for example, 'sh600000' should be '600000.ss'
        :param index: normal index
        :return: index used by yahoo
        """
        if index.startswith('sh'):
            ret = index[2:] + '.ss'
        elif index.startswith('sz'):
            ret = index[2:] + '.sz'
        else:
            ret = index
        return ret
