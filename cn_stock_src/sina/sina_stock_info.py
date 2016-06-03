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

import re
import threading
from pandas import DataFrame
from cn_stock_src.cn_stock_util import SINA_STOCK_INFO_COLUMNS
from cn_stock_src.cn_stock_util import multi_thread
from cn_stock_src.sina.sina_stock import SinaStock

__author__ = 'Cedric Zhuang'

__all__ = []


class SinaStockInfo(SinaStock):
    """Get stock info from sina.

    Get company base information from sina.
    Example output:

    Sample request:
    http://hq.sinajs.cn/list=sh600000_i

    Sample response:
    var hq_str_sh600000_i="A,pfyh,2.1940,2.4606,1.8660,12.4020,11145.9783,
    1865347.1415,1492277.7132,1492277.7132,0,CNY,409.2200,459.0300,10.0000,
    1,15.0400,897.7300,347.9900";

    Meaning of each field:

    A,				A股
    pfyh,			拼音缩写
    2.1940,			最近年度每股收益
    2.4606,			最近四个季度每股收益和
    1.8660,			季度每股收益
    12.4020,		季度每股净资产
    11145.9783,
    1865347.1415,	总股本（万元）
    1492277.7132,	流通股（万元）
    1492277.7132,	流通A股（万元）
    0,				流通B股（万元）
    CNY,			货币
    409.2200,		最近年度净利润（亿元）
    459.0300,		最近四个季度净利润（亿元）
    10.0000,		发行价格
    1,
    15.0400,		净资产收益率
    897.7300,		季度主营业务收入（亿元）
    347.9900		季度净利润（亿元）
    """

    def __init__(self):
        super(SinaStockInfo, self).__init__()
        self.stock_info = None

    @classmethod
    def _join_indices(cls, indices):
        info_names = []
        for index in indices:
            info_names.append("{}_i".format(index))
        return ",".join(info_names)

    @classmethod
    def _parse(cls, body):
        stocks = body.split(';')
        ret = DataFrame(columns=SINA_STOCK_INFO_COLUMNS)
        for stock in stocks:
            stock = stock.strip()
            if len(stock) == 0:
                continue
            m = re.match('var hq_str_(.*)_i="(.+)"', stock)
            if m is None:
                raise ValueError("response text is not valid: {}"
                                 .format(stock))
            index, data = m.group(1, 2)
            data_array = data.split(',')[:32]
            data_array[2:11] = map(float, data_array[2:11])
            data_array[12:] = map(float, data_array[12:])
            ret.ix[index] = data_array
        return ret

    @classmethod
    def _regroup(cls, l, size):
        grouped = []
        if len(l) <= size:
            grouped.append(l)
        else:
            i = 0
            while i < len(l):
                grouped.append(l[i:i + size])
                i += size
        return grouped

    def _retrieve_data_in_trunk(self, indices, trunk=None):
        if trunk is None:
            trunk = self._get_batch_size()

        grouped_indices = self._regroup(indices, trunk)

        lock = threading.Lock()
        self.stock_info = None

        def update_each_group(group):
            info = self.latest(group)
            lock.acquire()
            if self.stock_info is None:
                self.stock_info = info
            else:
                self.stock_info = self.stock_info.append(info)
            lock.release()

        multi_thread(update_each_group, grouped_indices)
        return self.stock_info
