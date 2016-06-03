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

from __future__ import unicode_literals
import logging.config
import os
from multiprocessing import Pool, cpu_count

__author__ = 'Cedric Zhuang'

__all__ = ['CnStockHttpError']


def get_thread_count():
    return cpu_count() + 2


def multi_thread(func, items, call_back=None, thread_count=None):
    if thread_count is None:
        thread_count = get_thread_count()

    executor = Pool(thread_count)
    results = executor.map(func, items)
    if call_back is not None:
        results = executor.map(call_back, results)
    return results


def get_file_dir(f):
    return os.path.dirname(os.path.realpath(f))


def read_file_in_same_dir(source_file, filename):
    folder = get_file_dir(source_file)
    the_file = os.path.join(folder, filename)
    with open(the_file, 'r') as f:
        ret = f.read()
    return ret


def config_logger():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            }
        }
    })


class CnStockHttpError(Exception):
    def __init__(self, url, status_code):
        msg = ('request failed.  url: {}, response status code: {}'
               .format(url, status_code))
        super(CnStockHttpError, self).__init__(msg)


TRADE_DETAIL_COLUMNS = ['name', 'open', 'close', 'price',
                        'high', 'low', 'volume', 'amount',
                        'buy1_volume', 'buy1_price',
                        'buy2_volume', 'buy2_price',
                        'buy3_volume', 'buy3_price',
                        'buy4_volume', 'buy4_price',
                        'buy5_volume', 'buy5_price',
                        'sell1_volume', 'sell1_price',
                        'sell2_volume', 'sell2_price',
                        'sell3_volume', 'sell3_price',
                        'sell4_volume', 'sell4_price',
                        'sell5_volume', 'sell5_price',
                        'date', 'time']

K_LINE_COLUMNS = ['date', 'open', 'high', 'low',
                  'close', 'volume', 'amount']

YAHOO_K_LINE_COLUMNS = ['date', 'open', 'high', 'low',
                        'close', 'volume', 'adjClose']

SINA_STOCK_INFO_COLUMNS = ['type',
                           'pinyin',
                           'per-share earnings(year)',
                           'per-share earnings(four quarters)',
                           'per-share earnings(quarter)',
                           'net assets per share',
                           'unknown',
                           'general capital(10,000Y)',
                           'floating stock(10,000Y)',
                           'floating A stock(10,000Y)',
                           'floating B stock(10,000Y)',
                           'currency',
                           'annual net profit(10**8Y)',
                           'four quarters net profit(10**8Y)',
                           'issue price',
                           'unknown',
                           'return on equity',
                           'quarter main business income(10**8Y)',
                           'quarter net profit(10**8Y)']

NETEASE_STOCK_INFO_COLUMNS = [
    # 股票中文名
    'name',
    # 日期(季度或年)
    'date',
    # 基本每股收益(元)
    'per-share earnings',
    # 每股净资产(元)
    'net assets per share',
    # 每股经营活动产生的现金流量净额(元)
    'Net cash flow from operating activities per share',
    # 主营业务收入(万元)
    'main business income(10**5)',
    # 主营业务利润(万元)
    'main business profit(10**5)',
    # 营业利润(万元)
    'operating profit(10**5)',
    # 投资收益(万元)
    'equity earnings(10**5)',
    # 营业外收支净额(万元)
    'net non-operating income(10**5)',
    # 利润总额(万元)
    'total profit(10**5)',
    # 净利润(万元)
    'net margin(10**5)',
    # 净利润(扣除非经常性损益后)(万元)
    'Net profit (ex. non recurring gains and losses)(10**5)',
    # 经营活动产生的现金流量净额(万元)
    'Net cash flow from operating activities(10**5)',
    # 现金及现金等价物净增加额(万元)
    'Net increase in cash and cash equivalents(10**5)',
    # 总资产(万元)
    'total assets(10**5)',
    # 流动资产(万元)
    'floating assets(10**5)',
    # 总负债(万元)
    'gross liabilities(10**5)',
    # 流动负债(万元)
    'floating liabilities(10**5)',
    # 股东权益不含少数股东权益(万元)
    'shareholders interests(10**5)',
    # 净资产收益率加权(%)
    'net assets yield weighted (%)'
]
