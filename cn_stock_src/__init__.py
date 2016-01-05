# coding=utf-8
from cn_stock_util import CnStockHttpError as CnStockHttpError

__author__ = 'Cedric Zhuang'

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
    from cn_stock_src import sina
    return sina.latest(*indices)


def latest_company_info(*indices):
    """ Get the basic company information for indices

    Check readme for sample output.
    :param indices: stock indices
    :return: data frame containing the basic information
    """
    from cn_stock_src import sina
    return sina.latest_company_info(*indices)


def financial_info(index):
    """ get the company financial info for index

    :param index: stock index
    :return: data frame containing financial data by season
    """
    from cn_stock_src import netease
    return netease.NeteaseStockInfo.latest(index)


def daily_k_line(*indices):
    """ Get the k line for stock indices

    Check readme for sample output.
    :param indices: stock indices
    :return: generator of the DataFrame
    """
    from cn_stock_src import yahoo
    for index in indices:
        yield yahoo.daily_k_line(index)


def tdx(install_root_folder):
    from cn_stock_src.tdx import TdxDataSource
    return TdxDataSource(install_root_folder)
