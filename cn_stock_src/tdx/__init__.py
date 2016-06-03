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

import logging
import os
from struct import calcsize, unpack
from math import floor
from pandas import DataFrame

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


def _get_markets():
    return 'sh', 'sz'


def get_minute_folders(tdx_root):
    for market in _get_markets():
        yield os.path.join(tdx_root, 'vipdoc', market, 'minline')


def get_5_minutes_folder(tdx_root):
    for market in _get_markets():
        yield os.path.join(tdx_root, 'vipdoc', market, 'fzline')


def get_day_folder(tdx_root):
    for market in _get_markets():
        yield os.path.join(tdx_root, 'vipdoc', market, 'lday')


def read_kline(filename):
    """read k line data

    read k line data from a tdx formatted data file
    return a data frame with the data

    sample output:

    ```
    sz002707        amount   close    high     low    open   volume
    date
    20140123  2.814259e+07   33.62   33.62   27.78   27.78   851338
    20140124  1.935452e+07   36.98   36.98   36.98   36.98   523378
    20140127  7.379800e+06   40.68   40.68   40.68   40.68   181411
    20140128  1.446759e+07   44.75   44.75   44.75   44.75   323298
    20140207  3.425596e+07   49.23   49.23   49.23   49.23   695835
    ```

    :param filename: filename of .day file
    :return: converted data frame
    """
    data_struct = 'IIIIIfII'
    data_size = calcsize(data_struct)
    index = _get_index_from_filename(filename)
    with open(filename, 'rb') as f:
        result = []
        factor = 100.0
        try:
            while 1:
                byte = f.read(data_size)
                if byte:
                    data = unpack(data_struct, byte)
                    (date, open_pri, high_pri, low_pri,
                     close_pri, amount, volume, reserve) = data
                    value = {'date': date,
                             'high': high_pri / factor,
                             'low': low_pri / factor,
                             'close': close_pri / factor,
                             'amount': amount,
                             'open': open_pri / factor,
                             'volume': volume}
                    result.append(value)
                else:
                    break
        except RuntimeError as e:
            log.exception("exception happens while reading: {}"
                          .format(filename), e)
    df = DataFrame(result).set_index('date')
    df.columns.name = index
    return df


def tdx_day_2_int_day(tdx_day):
    year = floor(tdx_day / 2048) + 2004
    month_day = tdx_day % 2048
    return year * 10000 + month_day


def tdx_time_2_int_time(tdx_minute):
    hour = int(tdx_minute / 60)
    return hour * 100 + (tdx_minute % 60)


def _get_index_from_filename(filename):
    stock = os.path.basename(filename)
    stock = '.'.join(stock.split('.')[:-1])
    return stock


def read_minutes(filename):
    """ Read minutes data from TDX data file

    Sample output:

    ```
    sh600000           amount  close   high    low   open   volume
    day      minute
    20150515 931     67558128  16.89  16.91  16.87  16.91  4000500
             932     45972624  16.90  16.90  16.88  16.89  2721000
             933     25946010  16.96  16.96  16.90  16.90  1533100
             934     30574120  16.98  17.00  16.96  16.98  1800500
    ```

    :param filename: filename pointed to the binary
                     file with minutes data
    :return: pandas DataFrame with detail data.
    """
    lc5_struct = 'hhfffffq'
    lc5_size = calcsize(lc5_struct)
    index = _get_index_from_filename(filename)
    with open(filename, 'rb') as f:
        result = []
        count = 0
        while 1:
            byte = f.read(lc5_size)
            count += 1
            if byte:
                fz_data = unpack(lc5_struct, byte)
                (day, minute, open_pri,
                 high_pri, low_pri, close_pri,
                 amount, volume) = fz_data
                value = {'day': tdx_day_2_int_day(day),
                         'minute': tdx_time_2_int_time(minute),
                         'open': round(open_pri, 2),
                         'high': round(high_pri, 2),
                         'low': round(low_pri, 2),
                         'close': round(close_pri, 2),
                         'amount': amount,
                         'volume': volume}
                result.append(value)
            else:
                break
    df = DataFrame(result)
    df.columns.name = index
    df.set_index(['day', 'minute'], inplace=True)
    return df


class TdxDataSource(object):
    """ get stock data from known TDX installations

    A root folder of TDX installation must be supplied as
    the input for the constructor.
    The data files will be searched according to the root
    installation folder.

    Check the unit test cases for this class for detail.
    """

    def __init__(self, installation_folder):
        self._root = installation_folder

    @staticmethod
    def _get_market(index):
        market = index[:2].lower()
        markets = _get_markets()
        if market not in markets:
            raise ValueError('Stock index should be prefixed '
                             'with market {}, found: {}'
                             .format(markets, index))
        return market

    def _get_filename(self, folder, index, ext):
        market = self._get_market(index)
        filename = '{}.{}'.format(index, ext)
        filename = os.path.join(self._root,
                                'vipdoc',
                                market,
                                folder,
                                filename)
        return filename

    def read_kline(self, *indices):
        for index in indices:
            filename = self._get_filename('lday', index, 'day')
            yield read_kline(filename)

    def read_5_minute(self, *indices):
        for index in indices:
            filename = self._get_filename('fzline', index, 'lc5')
            yield read_minutes(filename)

    def read_1_minute(self, *indices):
        for index in indices:
            filename = self._get_filename('minline', index, 'lc1')
            yield read_minutes(filename)
