from functools import partial
from unittest import TestCase
import operator
from hamcrest import assert_that, equal_to
from cn_stock_src.cn_stock_util import multi_thread

__author__ = 'stack'


class CnStockUtilTest(TestCase):
    def test_multi_thread_callback(self):
        double = partial(operator.mul, 2)
        result = multi_thread(int, ['3', '5', '9'], double, 3)
        assert_that(result, equal_to([6, 10, 18]))

    def test_multi_thread(self):
        triple = partial(operator.mul, 3)
        result = multi_thread(triple, [2, 5, 7])
        assert_that(result, equal_to([6, 15, 21]))
