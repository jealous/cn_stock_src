__author__ = 'Cedric Zhuang'

__version__ = '0.0.1'

TRADE_DETAIL_COLUMNS = ['name', 'open', 'close', 'price',
                        'high', 'low', 'volume', 'amount',
                        'buy1_volume', 'buy1_price',
                        'buy2_volume', 'buy2_price',
                        'buy3_volume', 'buy3_price',
                        'buy4_volume', 'buy4_price',
                        'buy5_volume', 'buy5_price',
                        'sell1_volume', 'sell1_price',
                        'sell2_volume', 'sell2_price',
                        'sell3_volume', 'sell3_price',
                        'sell4_volume', 'sell4_price',
                        'sell5_volume', 'sell5_price',
                        'date', 'time']

K_LINE_COLUMNS = ['date', 'open', 'high', 'low',
                  'close', 'volume', 'amount']

YAHOO_K_LINE_COLUMNS = ['date', 'open', 'high', 'low',
                        'close', 'volume', 'adjClose']

SINA_STOCK_INFO_COLUMNS = ['type',
                           'pinyin',
                           'per-share earnings(year)',
                           'per-share earnings(four quarters)',
                           'per-share earnings(quarter)',
                           'net assets per share',
                           'unknown',
                           'general capital(10,000Y)',
                           'floating stock(10,000Y)',
                           'floating A stock(10,000Y)',
                           'floating B stock(10,000Y)',
                           'currency',
                           'annual net profit(10**8Y)',
                           'four quarters net profit(10**8Y)',
                           'issue price',
                           'unknown',
                           'return on equity',
                           'quarter main business income(10**8Y)',
                           'quarter net profit(10**8Y)']


class CnStockHttpError(Exception):
    def __init__(self, url, status_code):
        msg = ('request failed.  url: {}, response status code: {}'
               .format(url, status_code))
        super(self, CnStockHttpError).__init__(msg)
