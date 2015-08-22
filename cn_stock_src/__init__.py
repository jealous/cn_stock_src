# coding=utf-8
from cn_stock_util import CnStockHttpError as CnStockHttpError
from cn_stock_src import sina, yahoo
from cn_stock_src.tdx import TdxDataSource

__author__ = 'Cedric Zhuang'

__version__ = '0.1.0'

__all__ = [
    'latest',
    'latest_company_info',
    'CnStockHttpError']


def latest(*indices):
    """ Get the latest stock data

    Check readme for sample and output.
    :param indices: stock indices
    :return: data frame containing the latest stock data
    """
    return sina.latest(*indices)


def latest_company_info(*indices):
    """ Get the basic company information for indices

    Check readme for sample output.
    :param indices: stock indices
    :return: data frame containing the basic information
    """
    return sina.latest_company_info(*indices)


def daily_k_line(*indices):
    """ Get the k line for stock indices

    Check readme for sample output.
    :param indices: stock indices
    :return: generator of the DataFrame
    """
    for index in indices:
        yield yahoo.daily_k_line(index)


def tdx(install_root_folder):
    return TdxDataSource(install_root_folder)
