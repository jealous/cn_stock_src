"""Read data from yahoo

sample

```
YahooStock.retrieve_data('sh600000')
```
"""
from six import StringIO
import logging
import int_date
import requests
import pandas as pd
from cn_stock_src.cn_stock_util import YAHOO_K_LINE_COLUMNS

__author__ = 'Cedric Zhuang'

__all__ = ["daily_k_line"]


log = logging.getLogger(__name__)


def daily_k_line(index):
    return YahooStock.daily_k_line(index)


class YahooStock(object):
    _DAILY_KL_URL = 'http://table.finance.yahoo.com/table.csv?s={}'

    def __init__(self):
        pass

    @staticmethod
    def _process_data(df):
        """change the column name and date format

        change the column name and date format

        :param df: source data frame
        :return: updated data frame
        """
        df.columns = YAHOO_K_LINE_COLUMNS
        df['date'] = df.date.apply(int_date.to_int_date)
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        return df[df.volume != 0]

    @staticmethod
    def daily_k_line(index, protocol=None, method=None):
        """get daily K line from Yahoo finance.

        :param index: stock index like sh600000
        :param protocol: 'http' or 'https'
        :param method: debug only
        :return: data frame of the daily K line
        """
        yahoo_index = YahooStock._index_converter(index)
        request_url = YahooStock._DAILY_KL_URL.format(yahoo_index)
        if protocol is not None:
            request_url = request_url.replace("http", protocol)
        log.debug("url: %s", request_url)
        if method is None:
            response = requests.get(request_url, timeout=30)
        else:
            response = method(request_url)
        df = pd.read_csv(StringIO(response.text))
        df = YahooStock._process_data(df)
        df.columns.name = index
        return df

    @staticmethod
    def _index_converter(index):
        """convert stock index into yahoo format

        for example, 'sh600000' should be '600000.ss'
        :param index: normal index
        :return: index used by yahoo
        """
        if index.startswith('sh'):
            ret = index[2:] + '.ss'
        elif index.startswith('sz'):
            ret = index[2:] + '.sz'
        else:
            ret = index
        return ret
