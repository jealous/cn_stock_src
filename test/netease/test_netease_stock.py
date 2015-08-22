# coding=utf-8
from unittest import TestCase
from hamcrest import assert_that, equal_to, close_to
from cn_stock_src.cn_stock_util import read_file_in_same_dir
from cn_stock_src.netease import NeteaseStock

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
