import pandas as pd

import numpy as np

import pandas_datareader as pdr

import matplotlib.pyplot as plt
import mplfinance as mpl

import yfinance as yf



# data
_var_stock = "AAPL"
_var_period = "1y"
_var_interval = "1d"


_check_movavg = "Yes"
if _check_movavg=="Yes":
    movavg = (4, 20, 50)
else:
    movavg = False

_check_vol = "Yes"
if _check_vol == "Yes":
    vol = True
else:
    vol = False

data = yf.download([_var_stock, "SPY"], period=_var_period, interval=_var_interval, group_by='ticker', auto_adjust=True)


mpl.plot(data[_var_stock], type='candle', mav=movavg, volume=vol, title=_var_stock)

data.head()
