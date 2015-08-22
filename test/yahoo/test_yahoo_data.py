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
