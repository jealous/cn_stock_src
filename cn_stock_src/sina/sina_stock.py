# coding=utf-8
import logging
import re
import int_date
from pandas import DataFrame
from error import ParamError
import cn_stock_src
from cn_stock_src.cn_stock_base import CnStockBase

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


class SinaStock(CnStockBase):
    BASE = "http://hq.sinajs.cn/list={}"

    def __init__(self):
        super(SinaStock, self).__init__()

    @classmethod
    def get_base(cls):
        return cls.BASE

    @classmethod
    def parse(cls, body):
        stocks = body.split(';')
        ret = DataFrame(columns=cn_stock_src.TRADE_DETAIL_COLUMNS)
        for stock in stocks:
            stock = stock.strip()
            if len(stock) == 0:
                continue
            m = re.match('var hq_str_(.*)="(.*)"', stock)
            if m is None:
                raise ParamError("response text is not valid: {}"
                                 .format(stock))
            index, data = m.group(1, 2)
            if len(data) == 0:
                log.info("data for stock %s is empty, skip.", index)
                continue
            data_array = data.split(',')[:32]
            result = [data_array[0]]
            result.extend(map(float, data_array[1:6]))
            result.extend(map(float, data_array[8:30]))
            result.extend([int_date.to_int_date(data_array[30]),
                           data_array[31]])
            ret.ix[index] = result
        return ret

    @classmethod
    def join_indices(cls, indices):
        return ','.join(indices)


if __name__ == '__main__':
    print SinaStock.retrieve_data('sh600000')
