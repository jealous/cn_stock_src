# coding=utf-8
from unittest import TestCase
from hamcrest import equal_to, assert_that
from cn_stock_src.cn_stock_util import read_file_in_same_dir
from cn_stock_src.sina.sina_stock import SinaStock

__author__ = 'Cedric Zhuang'


class MockResponse(object):
    def __init__(self):
        self.status_code = 200
        self.text = ''


class SinaStockTest(TestCase):
    def test_latest(self):
        """
        this case requires network connection
        :return:
        """
        body = read_file_in_same_dir(__file__, 'sina_stock_detail.txt')
        data = SinaStock._parse(body)
        assert_that(len(data), equal_to(2))

        stock = data.ix['sh999999']
        assert_that(stock['name'], equal_to('\u6d66\u53d1\u94f6\u884c'))
        assert_that(stock.open, equal_to(14.58))
        assert_that(stock.price, equal_to(14.47))
        assert_that(stock.close, equal_to(14.42))
        assert_that(stock.high, equal_to(14.69))
        assert_that(stock.low, equal_to(14.36))
        assert_that(stock.volume, equal_to(207865327))
        assert_that(stock.amount, equal_to(3021747775))

        assert_that(stock.buy1_volume, equal_to(111100))
        assert_that(stock.buy1_price, equal_to(14.47))
        assert_that(stock.buy2_volume, equal_to(201300))
        assert_that(stock.buy2_price, equal_to(14.46))
        assert_that(stock.buy3_volume, equal_to(451773))
        assert_that(stock.buy3_price, equal_to(14.45))
        assert_that(stock.buy4_volume, equal_to(210555))
        assert_that(stock.buy4_price, equal_to(14.44))
        assert_that(stock.buy5_volume, equal_to(404000))
        assert_that(stock.buy5_price, equal_to(14.43))

        assert_that(stock.sell1_volume, equal_to(58047))
        assert_that(stock.sell1_price, equal_to(14.48))
        assert_that(stock.sell2_volume, equal_to(309031))
        assert_that(stock.sell2_price, equal_to(14.49))
        assert_that(stock.sell3_volume, equal_to(582880))
        assert_that(stock.sell3_price, equal_to(14.50))
        assert_that(stock.sell4_volume, equal_to(109444))
        assert_that(stock.sell4_price, equal_to(14.51))
        assert_that(stock.sell5_volume, equal_to(367634))
        assert_that(stock.sell5_price, equal_to(14.52))

        assert_that(stock.date, equal_to(20150130))
        assert_that(stock.time, equal_to('15:03:04'))
