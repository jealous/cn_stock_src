from unittest import TestCase
from hamcrest import assert_that, equal_to
from cn_stock_src.yahoo.yahoo_stock import YahooStock

__author__ = 'Cedric Zhuang'


class MockResponse(object):
    def __init__(self):
        self.status_code = 200
        self.text = ''


class YahooStockTest(TestCase):
    def get_mock_input(self, _):
        response = MockResponse
        response.status_code = 200
        response.text = """Date,Open,High,Low,Close,Volume,Adj Close
2015-02-06,4.94,5.04,4.59,4.74,614978500,4.74
2015-02-05,5.37,5.41,4.90,4.98,521587000,4.98
2015-02-04,5.34,5.55,5.32,5.33,485601600,5.33
2015-02-03,5.32,5.45,5.25,5.31,400091100,5.31
2015-02-02,4.89,5.47,4.86,5.33,778374600,5.33"""
        return response

    def test_index_converter_sh(self):
        yahoo_index = YahooStock.index_converter('sh600010')
        assert_that(yahoo_index, equal_to('600010.ss'))

    def test_index_converter_sz(self):
        yahoo_index = YahooStock.index_converter('sz000010')
        assert_that(yahoo_index, equal_to('000010.sz'))

    def test_retrieve_data(self):
        df = YahooStock.retrieve_data('sh600010', self.get_mock_input)
        assert_that(len(df), equal_to(5))
        record = df.ix[20150206]
        assert_that(record.ix['open'], equal_to(4.94))
        assert_that(record.ix['adjClose'], equal_to(4.74))
