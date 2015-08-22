from cn_stock_src.sina.sina_stock import SinaStock
from cn_stock_src.sina.sina_stock_info import SinaStockInfo

__author__ = 'Cedric Zhuang'

__all__ = ["latest", "latest_company_info"]


def latest(*indices):
    return SinaStock.latest(indices)


def latest_company_info(*indices):
    return SinaStockInfo.latest(indices)
