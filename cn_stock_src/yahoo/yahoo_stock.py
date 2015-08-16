from StringIO import StringIO
import logging
import int_date
import requests
import pandas as pd
from cn_stock_src import YAHOO_K_LINE_COLUMNS

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


class YahooStock(object):
    DAILY_KL_URL = 'http://table.finance.yahoo.com/table.csv?s={}'

    def __init__(self):
        pass

    @staticmethod
    def process_data(df):
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
    def retrieve_data(index, method=None, protocol=None):
        """get daily K line from Yahoo finance.

        :param index: stock index like sh600000
        :param method: debug only
        :return: data frame of the daily K line
        """
        index = YahooStock.index_converter(index)
        request_url = YahooStock.DAILY_KL_URL.format(index)
        if protocol is not None:
            request_url = request_url.replace("http", protocol)
        log.debug("url: %s", request_url)
        if method is None:
            response = requests.get(request_url, timeout=30)
        else:
            response = method(request_url)
        df = pd.read_csv(StringIO(response.text))
        return YahooStock.process_data(df)

    @staticmethod
    def index_converter(index):
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


if __name__ == '__main__':
    print YahooStock.retrieve_data('sh600000')
