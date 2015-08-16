from pandas import DataFrame
import cn_stock_src
from cn_stock_src.cn_stock_base import CnStockBase
import json
import int_date

__author__ = 'Cedric Zhuang'


class NeteaseStock(CnStockBase):
    BASE = "http://api.money.126.net/data/feed/{},money.api"

    @classmethod
    def get_base(cls):
        return cls.BASE

    @classmethod
    def get_batch_size(cls):
        return 200

    @classmethod
    def join_indices(cls, indices):
        trans_indices = map(cls.trans_index, indices)
        return ','.join(trans_indices)

    PREFIX = '_ntes_quote_callback('
    SUFFIX = ');'

    @classmethod
    def parse(cls, body):
        if body.startswith(cls.PREFIX):
            body = body.replace(cls.PREFIX, '')
        if body.endswith(cls.SUFFIX):
            body = body.replace(cls.SUFFIX, '')

        stock_map = json.loads(body)

        stocks = DataFrame(columns=cn_stock_src.TRADE_DETAIL_COLUMNS)
        for name, stock in stock_map.iteritems():
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
    def trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret


if __name__ == '__main__':
    print NeteaseStock.retrieve_data(['sh600000'])
