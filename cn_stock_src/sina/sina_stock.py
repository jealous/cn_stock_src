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

""" Read stock data from sina

Sample:

```
SinaStock.retrieve_data('sh600000')
```

"""
import logging
import re
import int_date
from pandas import DataFrame
from cn_stock_src.cn_stock_util import TRADE_DETAIL_COLUMNS
from cn_stock_src.cn_stock_base import CnStockBase

__author__ = 'Cedric Zhuang'

__all__ = []

log = logging.getLogger(__name__)


class SinaStock(CnStockBase):
    _BASE = "http://hq.sinajs.cn/list={}"

    def __init__(self):
        super(SinaStock, self).__init__()

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _parse(cls, body):
        stocks = body.split(';')
        ret = DataFrame(columns=TRADE_DETAIL_COLUMNS)
        for stock in stocks:
            stock = stock.strip()
            if len(stock) == 0:
                continue
            m = re.match('var hq_str_(.*)="(.*)"', stock)
            if m is None:
                raise ValueError("response text is not valid: {}"
                                 .format(stock))
            index, data = m.group(1, 2)
            if len(data) == 0:
                log.info("data for stock %s is empty, skip.", index)
                continue
            data_array = data.split(',')[:32]
            result = [data_array[0]]
            result.extend(map(float, data_array[1:6]))
            result.extend(map(float, data_array[8:30]))
            result.extend([int_date.to_int_date(data_array[30]),
                           data_array[31]])
            ret.ix[index] = result
        return ret

    @classmethod
    def _join_indices(cls, indices):
        return ','.join(indices)
