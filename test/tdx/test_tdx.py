import os
from six import next
from unittest import TestCase
from hamcrest import assert_that, equal_to, starts_with, ends_with, close_to
from cn_stock_src.cn_stock_util import get_file_dir
from cn_stock_src.tdx import get_minute_folders, \
    get_day_folder, get_5_minutes_folder, tdx_day_2_int_day, TdxDataSource

__author__ = 'Cedric Zhuang'


class TdxTest(TestCase):
    def test_get_minute_folders(self):
        folders = list(get_minute_folders('root'))
        for folder in folders:
            assert_that(folder, starts_with('root'))
            assert_that(folder, ends_with('minline'))

    def test_get_day_folders(self):
        folders = list(get_day_folder('root'))
        for folder in folders:
            assert_that(folder, ends_with('lday'))

    def test_get_5_minutes_folder(self):
        folders = list(get_5_minutes_folder('root'))
        for folder in folders:
            assert_that(folder, ends_with('fzline'))

    def test_tdx_day_2_int_day(self):
        assert_that(tdx_day_2_int_day(23349), equal_to(20150821))
        assert_that(tdx_day_2_int_day(16714), equal_to(20120330))
        assert_that(tdx_day_2_int_day(16789), equal_to(20120405))


class TdxDataSourceTest(TestCase):
    def setUp(self):
        self.tdx = TdxDataSource(os.path.join(get_file_dir(__file__), 'data'))

    def test_read_kline(self):
        df = next(self.tdx.read_kline('sz002707'))
        assert_that(df.columns.name, equal_to('sz002707'))
        data = df.ix[20150608]
        assert_that(data.amount, close_to(457520100, 100))
        assert_that(data.volume, equal_to(3750037))
        assert_that(data.open, equal_to(126.87))
        assert_that(data.high, equal_to(130.45))
        assert_that(data.low, equal_to(117.60))
        assert_that(data.close, equal_to(119.64))

    def test_read_minutes(self):
        df = next(self.tdx.read_1_minute('sh600000'))
        assert_that(df.columns.name, equal_to('sh600000'))
        test_data = df.ix[20150522, 1018]
        assert_that(test_data.open, equal_to(17.73))
        assert_that(test_data.close, equal_to(17.74))
        assert_that(test_data.high, equal_to(17.75))
        assert_that(test_data.low, equal_to(17.72))
        assert_that(test_data.amount, equal_to(32970880))
        assert_that(test_data.volume, equal_to(1859300))

    def test_read_5_minutes(self):
        df = next(self.tdx.read_5_minute('sh600010'))
        assert_that(df.columns.name, equal_to('sh600010'))
        test_data = df.ix[20150812, 1430]
        assert_that(test_data.open, equal_to(4.77))
        assert_that(test_data.close, equal_to(4.78))
        assert_that(test_data.high, equal_to(4.79))
        assert_that(test_data.low, equal_to(4.76))
        assert_that(test_data.amount, equal_to(22869504))
        assert_that(test_data.volume, equal_to(4796300))

    def test_read_multiple_indices(self):
        ret = list(self.tdx.read_kline('sh600028', 'sz002707'))
        assert_that(len(ret), equal_to(2))
