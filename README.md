# Stock data source for Chinese markets

[![Build Status](https://travis-ci.org/jealous/cn_stock_src.svg?branch=master)](https://travis-ci.org/jealous/cn_stock_src)
[![Coverage Status](https://coveralls.io/repos/jealous/cn_stock_src/badge.svg?branch=master&service=github)](https://coveralls.io/github/jealous/cn_stock_src?branch=master)

## Introduction

Retrieve stock data from web interface and saved in pandas ``DataFrame``.

Tested on python 2.7

## Installation

``pip install cn_stock_src``


## Tutorial

* Get the latest trading data for stock indices.

Example:

```python
latest('sh600000', 'sh600238', 'sz000001')
```

Output:

```
          name   open  close  price   high    low     volume        amount  \
sh600000  浦发银行  13.93  14.22  12.87  13.95  12.80  334859429  4.407389e+09
sh600238  海南椰岛  12.60  12.91  11.62  12.60  11.62   12069736  1.421766e+08
sz000001  平安银行  11.10  11.50  10.35  11.17  10.35  151802968  1.601529e+09

          buy1_volume  buy1_price    ...     sell2_volume  sell2_price  \
sh600000       981800       12.87    ...            71334        12.89
sh600238            0        0.00    ...            12913        11.63
sz000001            0        0.00    ...           284420        10.36

          sell3_volume  sell3_price  sell4_volume  sell4_price  sell5_volume  \
sh600000        241900        12.90        238100        12.91         37500
sh600238          2000        11.65          2300        11.68          9200
sz000001         68739        10.37        212580        10.38         57200

          sell5_price      date      time
sh600000        12.92  20150824  15:03:04
sh600238        11.70  20150824  15:03:04
sz000001        10.39  20150824  15:05:55

[3 rows x 30 columns]
```

* Get the basic company information for stock indices.

Example:

```python
latest_company_info('sh600000', 'sh600238', 'sz000001')
```

Output:

```
             type pinyin  per-share earnings(year)  
sh600000    A   pfyh                     2.521
sh600238    A   hnyd                     0.090
sz000001    A   payh                     1.730

          per-share earnings(four quarters)  per-share earnings(quarter)  
sh600000                             2.5877                       1.2810
sh600238                             0.0038                       0.0033
sz000001                             1.7603                       0.8400

          net assets per share    unknown  general capital(10,000Y)  
sh600000               13.7120  6085.9750              1865347.1415
sh600238                1.9813   517.2827                44820.0000
sz000001               10.5400  3688.2195              1430867.6139

          floating stock(10,000Y)  floating A stock(10,000Y)  
sh600000             1492277.7132               1492277.7132
sh600238               44473.1580                 44473.1580
sz000001             1180405.4579               1180405.4579

          floating B stock(10,000Y) currency  annual net profit(10**8Y)  
sh600000                          0      CNY                   470.2600
sh600238                          0      CNY                     0.4189
sz000001                          0      CNY                   198.0200

          four quarters net profit(10**8Y)  issue price  unknown  
sh600000                          482.7300         10.0        1
sh600238                            0.0178          4.1        1
sz000001                          213.1500         40.0        1

          return on equity  quarter main business income(10**8Y)  
sh600000              9.35                                707.01
sh600238              0.17                                  1.88
sz000001              7.68                                465.75

          quarter net profit(10**8Y)
sh600000                    239.0300
sh600238                      0.0148
sz000001                    115.8500
```

* Get the daily k-line for stock indices

Example:

```python
data = daily_k_line('sh600000', 'sh600238', 'sz000001')
data.next()
```

Output:

```
sh600000      open      high       low     close     volume  adjClose
date
19991110  29.50000  29.80000  27.00001  27.74999  617827800   5.03743
19991111  27.57999  28.38001  27.52998  27.70999  104352900   5.03017
19991112  27.86001  28.30001  27.77000  28.04998   53263200   5.09189
...            ...       ...       ...       ...        ...       ...
20150819  14.87000  15.17000  14.50000  15.00000  199062100  15.00000
20150820  14.94000  14.99000  14.66000  14.68000   88124700  14.68000
20150821  14.61000  14.74000  14.20000  14.22000  123792800  14.22000
```

To file issue, please visit:

https://github.com/jealous/cn_stock_src


Contact author:

cedric.zhuang@gmail.com