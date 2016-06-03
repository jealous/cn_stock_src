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
from unittest import TestCase
from hamcrest import assert_that, equal_to, close_to, greater_than
from cn_stock_src.cn_stock_util import read_file_in_same_dir
from cn_stock_src.netease import NeteaseStock, NeteaseStockInfo

__author__ = 'Cedric Zhuang'


class NeteaseStockTest(TestCase):
    def test_join_indices(self):
        result = NeteaseStock._join_indices(['sh600000', 'sh600010'])
        assert_that(result, equal_to('0600000,0600010'))

    def test_parse(self):
        body = read_file_in_same_dir(__file__, 'daily_detail.json')
        result = NeteaseStock._parse(body)
        sh60 = result.ix['sh600000']
        assert_that(sh60.name, equal_to('sh600000'))
        assert_that(sh60['name'], equal_to(u'浦发银行'))
        assert_that(sh60.open, equal_to(18.28))
        assert_that(sh60.close, equal_to(18.53))
        assert_that(sh60.high, equal_to(18.46))
        assert_that(sh60.low, equal_to(18.05))
        assert_that(sh60.volume, equal_to(412760522))
        assert_that(sh60.amount, equal_to(7523663257))
        assert_that(sh60.buy1_price, equal_to(18.07))
        assert_that(sh60.buy1_volume, close_to(300, 50))
        assert_that(sh60.buy2_price, equal_to(18.06))
        assert_that(sh60.buy2_volume, close_to(532800, 50))
        assert_that(sh60.buy3_price, equal_to(18.05))
        assert_that(sh60.buy3_volume, close_to(1053500, 50))
        assert_that(sh60.buy4_price, equal_to(18.04))
        assert_that(sh60.buy4_volume, close_to(153000, 50))
        assert_that(sh60.buy5_price, equal_to(18.03))
        assert_that(sh60.buy5_volume, close_to(312200, 50))
        assert_that(sh60.sell1_price, equal_to(18.08))
        assert_that(sh60.sell1_volume, close_to(205900, 50))
        assert_that(sh60.sell2_price, equal_to(18.09))
        assert_that(sh60.sell2_volume, close_to(466000, 50))
        assert_that(sh60.sell3_price, equal_to(18.10))
        assert_that(sh60.sell3_volume, close_to(333500, 50))
        assert_that(sh60.sell4_price, equal_to(18.11))
        assert_that(sh60.sell4_volume, close_to(253600, 50))
        assert_that(sh60.sell5_price, equal_to(18.12))
        assert_that(sh60.sell5_volume, close_to(155400, 50))
        assert_that(sh60.date, equal_to(20150430))
        assert_that(sh60.time, equal_to('15:03:02'))


class NeteaseStockInfoTest(TestCase):
    def test_join_indices_error(self):
        self.assertRaises(ValueError,
                          NeteaseStockInfo._join_indices,
                          ['sh600000', 'sz000001'])

    def test_join_indices(self):
        index = NeteaseStockInfo._join_indices(['sh600000'])
        assert_that(index, equal_to('600000'))

    def test_parse(self):
        body = read_file_in_same_dir(__file__, 'zycwzb_600000,season.html')
        result = NeteaseStockInfo._parse(body)
        test_season = result.ix[20141231]
        assert_that(len(test_season['name']), greater_than(3))
        assert_that(test_season['per-share earnings'], equal_to(2.52))
        assert_that(test_season['net assets per share'], equal_to(13.15))
        assert_that(
            test_season['Net cash flow from operating activities per share'],
            equal_to(10.25))
        assert_that(test_season['main business income(10**5)'],
                    equal_to(3340800))
        assert_that(test_season['main business profit(10**5)'],
                    equal_to(1601700))
        assert_that(test_season['operating profit(10**5)'], equal_to(1601700))
        assert_that(test_season['equity earnings(10**5)'], equal_to(-2200))
        assert_that(test_season['net non-operating income(10**5)'],
                    equal_to(None))
        assert_that(test_season['total profit(10**5)'], equal_to(1617100))
        assert_that(test_season['net margin(10**5)'], equal_to(1222700))
        assert_that(
            test_season[
                'Net profit (ex. non recurring gains and losses)(10**5)'],
            equal_to(None))
        assert_that(
            test_season['Net cash flow from operating activities(10**5)'],
            equal_to(19115800))
        assert_that(
            test_season['Net increase in cash and cash equivalents(10**5)'],
            equal_to(-7733200))
        assert_that(test_season['total assets(10**5)'], equal_to(419592400))
        assert_that(test_season['floating assets(10**5)'], equal_to(None))
        assert_that(test_season['gross liabilities(10**5)'],
                    equal_to(393263900))
        assert_that(test_season['floating liabilities(10**5)'], equal_to(None))
        assert_that(test_season['shareholders interests(10**5)'],
                    equal_to(26016900))
        assert_that(test_season['net assets yield weighted (%)'],
                    equal_to(21.02))

    def test_parse_no_data(self):
        body = read_file_in_same_dir(__file__, '001979,season.html')
        result = NeteaseStockInfo._parse(body)
        assert_that(len(result), equal_to(0))
