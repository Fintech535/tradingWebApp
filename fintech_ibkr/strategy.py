from bbgapi import bdh
from datetime import date
from datetime import timedelta

def current_acc():
    GDP = bdh('ECOXPHN Index')
    GDP_Q = GDP.rolling(window=4,axis=1).sum
    CA = bdh('ECOCPHN Index')
    CA_Q = CA.rolling(window=4,axis=1).sum
    df = CA_Q/GDP_Q
    avg_CA = df.mean()

    return avg_CA

def f_direct_inv():
    GDP = bdh('ECOXPHN Index')
    GDP_Q = GDP.rolling(window=4, axis=1).sum
    FDI = bdh('PHBOFDI Index')
    FDI_Q = FDI.rolling(window=4, axis=1).sum
    df = FDI_Q / GDP_Q
    avg_FDI = df.mean()

    return avg_FDI

def trade_GDP():
    xports = bdh('ECOYEPHN Index') #4 quarters
    mports = bdh('ECOYMPHN Index') #4 quarters
    total_trade = xports + mports
    GDP = bdh('ECOXPHN Index')
    GDP_Q = GDP.rolling(window=4, axis=1).sum
    trade_pct = total_trade/GDP_Q

    return trade_pct

#The dict and the currency here are just in case we decide to do more ccy_pairs
#The dict will contain all the tickers, elasticities and data about that pair

def CA_strategy(dict, ccy_pair):
    # Calculate all of them
    today = date.today()
    yesterday =date.today() - timedelta(days = 1)
    #Call from BBG the forecast
    forecast = bdh('ECCAPH 23 Index', 'PX_LAST', None, yesterday, yesterday)

    # #date1 andd date2 will be the dates we need to find
    # date1 = Date of last forecast
    # date2 = CA Date of last ToT
    date1 =''
    date2 =''

    #Bring all the variables needed
    tot = bdh('CTOTPHP Index', 'INTERVAL_NET_CHANGE', None, date1, date2)
    ccy_pct = bdh('PHP Curncy', 'INTERVAL_NET_CHANGE', None, date1, date2)
    trade_pct = trade_GDP()
    elasticity = -0.23
    CA = current_acc()
    FDI = f_direct_inv()

    #Adjusted current account
    adjusted_fcst = forecast + (elasticity * ccy_pct + tot * (trade_pct*0.5))

    #Current account rule
    CA_rule = 0.5*CA + 0.5*FDI

    #Currency movement
    currency_chg = (CA_rule - adjusted_fcst)/elasticity

    #Bring vol 1m
    ccy_vol = bdh('USDPHPV1M BGN Curncy', 'PX_LAST', None, today, today)

    #Return Fugacity
    fugacity = currency_chg/ccy_vol

    return fugacity
