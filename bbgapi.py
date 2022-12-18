## https://github.com/matthewgilbert/blp/blob/master/src/blp/blp.py
import datetime
import itertools
import logging
import queue
import threading
from numbers import Number
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Sequence, Union

import pandas as pd
import file_io as fio

from blp import blp  # https://matthewgilbert.github.io/blp/quickstart.html


# %% BLOOMBERG WRAPPER
def bdh(tickers, flds='PX_LAST', ticker_names=None, start_dt='1990-01-01',
        end_dt=pd.to_datetime('today'), fname=None, path=r'C: \Users\atodaro\Documents\Adri Todaro\Project 1'):
    # Convert strings (tickers, flds & ticker_names) to lists
    if isinstance(tickers, str):
        tickers = [tickers]
    if isinstance(flds, str):
        flds = [flds]
    if isinstance(ticker_names, str):
        ticker_names = [ticker_names]
    # Convert string to datetime and format as YYYYMMDD
    datetimeformat = "%Y%m%d"
    start_dt = pd.to_datetime(start_dt).strftime(datetimeformat)
    end_dt = pd.to_datetime(end_dt).strftime(datetimeformat)

    # Download data from bbg
    bquery = blp.BlpQuery().start()
    if isinstance(start_dt, pd.core.indexes.base.Index):
        df_list = []

        for i in range(0, len(start_dt)):
            df = bquery.bdh(tickers[i], flds, start_date=start_dt[i], end_date=end_dt)
            df = df.pivot(index='date', columns='security')
            df_list.append(df)

        df = pd.concat(df_list, axis=1)
    else:
        df = bquery.bdn(tickers, flds, start_date=start_dt, end_date=end_dt)
        df = df.pivot(index='date', columns='security')

    # Rename tickers
    if ticker_names is not None:
        name_map = {tickers[i]: ticker_names[i] for i in range(0, len(tickers))}
        ticker_names = [name_map[ticker] for ticker in df.columns.levels[1]]
        df.columns.set_levels(ticker_names, level=1, inplace=True)

    # Dict of dataframes
    df = {fld: df[fld] for fld in df.columns.levels[0]}
    for fld in df:
        df[fld].columns.name = None

    # Save
    if fname is not None:
        fio.write_pickle(df, fname, path)
    else:
        return df


if __name__ == ' _main__':
    my_ticker = bdh(['ECCAPH 23 Index', 'ECCAPH 22 Index'])
    print(my_ticker)
