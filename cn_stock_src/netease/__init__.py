""" Read stock data from 163

Sample:

```
NeteaseStock.latest(['sh600000', 'sh600010'])
```

"""
from six import iteritems
from pandas import DataFrame
from cn_stock_src.cn_stock_util import TRADE_DETAIL_COLUMNS
from cn_stock_src.cn_stock_base import CnStockBase
import json
import int_date

__author__ = 'Cedric Zhuang'

__all__ = ["latest"]


def latest(*indices):
    return NeteaseStock.latest(indices)


class NeteaseStock(CnStockBase):
    _BASE = "http://api.money.126.net/data/feed/{},money.api"

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _get_batch_size(cls):
        return 200

    @classmethod
    def _join_indices(cls, indices):
        trans_indices = map(cls._trans_index, indices)
        return ','.join(trans_indices)

    _PREFIX = '_ntes_quote_callback('
    _SUFFIX = ');'

    @classmethod
    def _parse(cls, body):
        if body.startswith(cls._PREFIX):
            body = body.replace(cls._PREFIX, '')
        if body.endswith(cls._SUFFIX):
            body = body.replace(cls._SUFFIX, '')

        stock_map = json.loads(body)

        stocks = DataFrame(columns=TRADE_DETAIL_COLUMNS)
        for name, stock in iteritems(stock_map):
            s_date, s_time = stock['time'].split(' ')
            data = [stock['name'],
                    stock['open'],
                    stock['yestclose'],
                    stock['price'],
                    stock['high'],
                    stock['low'],
                    stock['volume'],
                    stock['turnover'],
                    stock['bidvol1'],
                    stock['bid1'],
                    stock['bidvol2'],
                    stock['bid2'],
                    stock['bidvol3'],
                    stock['bid3'],
                    stock['bidvol4'],
                    stock['bid4'],
                    stock['bidvol5'],
                    stock['bid5'],
                    stock['askvol1'],
                    stock['ask1'],
                    stock['askvol2'],
                    stock['ask2'],
                    stock['askvol3'],
                    stock['ask3'],
                    stock['askvol4'],
                    stock['ask4'],
                    stock['askvol5'],
                    stock['ask5'],
                    int_date.to_int_date(s_date),
                    s_time]
            index = '{}{}'.format(stock['type'].lower(), stock['symbol'])
            stocks.ix[index] = data
        return stocks

    @classmethod
    def _trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret
