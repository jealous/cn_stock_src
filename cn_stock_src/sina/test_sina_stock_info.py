from unittest import TestCase
from cn_stock_src.sina.sina_stock_info import SinaStockInfo

__author__ = 'Cedric Zhuang'


class StockTest(TestCase):
    def setUp(self):
        SinaStockInfo.debug = True

    def tearDown(self):
        SinaStockInfo.debug = False
