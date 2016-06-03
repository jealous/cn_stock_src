# coding=utf-8
# Copyright (c) 2016, Cedric Zhuang
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of disclaimer nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from cn_stock_src.cn_stock_util import CnStockHttpError as CnStockHttpError
from cn_stock_src import sina
from cn_stock_src import netease
from cn_stock_src import yahoo
from cn_stock_src.tdx import TdxDataSource

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
    return sina.latest(*indices)


def latest_company_info(*indices):
    """ Get the basic company information for indices

    Check readme for sample output.
    :param indices: stock indices
    :return: data frame containing the basic information
    """
    return sina.latest_company_info(*indices)


def financial_info(index):
    """ get the company financial info for index

    :param index: stock index
    :return: data frame containing financial data by season
    """
    return netease.NeteaseStockInfo.latest(index)


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
