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

from unittest import TestCase
from hamcrest import assert_that, equal_to
from cn_stock_src.cn_stock_util import read_file_in_same_dir
from cn_stock_src.yahoo import YahooStock

__author__ = 'Cedric Zhuang'


class MockResponse(object):
    def __init__(self):
        self.status_code = 200
        self.text = ''


class YahooStockTest(TestCase):
    def get_mock_input(self, _):
        response = MockResponse
        response.status_code = 200
        response.text = read_file_in_same_dir(__file__,
                                              'yahoo_stock_kline.txt')
        return response

    def test_index_converter_sh(self):
        yahoo_index = YahooStock._index_converter('sh600010')
        assert_that(yahoo_index, equal_to('600010.ss'))

    def test_index_converter_sz(self):
        yahoo_index = YahooStock._index_converter('sz000010')
        assert_that(yahoo_index, equal_to('000010.sz'))

    def test_retrieve_data(self):
        df = YahooStock.daily_k_line('sh600010', method=self.get_mock_input)
        assert_that(df.columns.name, equal_to('sh600010'))
        assert_that(len(df), equal_to(5))
        record = df.ix[20150206]
        assert_that(record.ix['open'], equal_to(4.94))
        assert_that(record.ix['adjClose'], equal_to(4.74))
