#  Python Module for import                           Date : 2018-03-12
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  fecon235.py : unifies lib modules for fecon235 project.

- Designed to be invoked by an IPython console or Jupyter notebook
     for convenient command access.
     CASUAL usage:
         from fecon235.fecon235 import *
- User can always foo?? to access foo's origin.
- Unifies essential lib modules in one place, thus
     frequently used commands can be generalized with shorter names.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2018-03-11  Add foreinfl() to forecast Unified Inflation 1-year ahead.
2018-03-11  Add foreholt() function, generalizing yi_fred.holtfred(),
               but retain holtfred() here for backward compatibility.
2017-06-27  Include module ys_prtf_boltzmann.py and group world4d.
2017-06-18  Add groupgemrat(), groupdiflog(), and covdiflog().
               Include module ys_matrix.py.
2017-06-06  Include our module ys_mlearn.py
2017-05-16  Include our module ys_gauss_mix.py
2016-12-29  Modify forecast() to include optimize_holtforecast().
2016-12-19  Import lib.ys_opt_holt to optimize Holt-Winters alpha and beta.
2016-01-22  Include plotdf() in plot() as first candidate.
               Rename cotr() to groupcotr(), then include smoothing.
2016-01-19  Add groupfun() to apply some function to group columns.
               This was derived by generalizing grouppc.
               Add cotr() for normalized COTR position indicators.
2016-01-11  Add forefunds() to forecast Fed Funds rate.
2016-01-08  For groupgeoret, sort results in a list, yearly default.
               For grouppc, freq default as in pcent.
2016-01-05  Add groupget, grouppc, groupgeoret, groupholtf functions.
2015-12-20  python3 compatible: lib import fix.
2015-12-17  python3 compatible: fix with yi_0sys
2015-09-14  Add getstock and second argument maxi to get().
2015-09-03  Exception handling.
2015-08-31  First version unifies some commands.

TODO
[ ] - adopt Bloomberg Open Symbology for obscure financial instruments, 
         see http://bsym.bloomberg.com/sym/
         Bloomberg Global ID is a random 12-character alpha-numeric.
'''

from __future__ import absolute_import, print_function

import pandas as pd
from .lib import yi_0sys as system

#    CASUAL import style below intentionally for Jupyter notebooks
#    and interactive settings (lib modules follow proper import protocol).
#    We access essential modules and catch collisions in namespace:
from .lib.yi_1tools import *
from .lib.yi_fred import *
from .lib.yi_matrix import *
from .lib.yi_plot import *
from .lib.yi_quandl import *
#         yi_quandl_api should NOT be imported.
from .lib.yi_simulation import *
from .lib.yi_stocks import *
from .lib.yi_timeseries import *
from .lib.ys_gauss_mix import *
from .lib.ys_mlearn import *
from .lib.ys_opt_holt import *
from .lib.ys_prtf_boltzmann import *


#  GROUPS:  specify our favorite series as a dictionary
#  where key is name, and corresponding value is its data code:

group4d = { 'Zero10' : d4zero10, 'SPX' : d4spx, 'XAU' : d4xau, 
            'EURUSD' : d4eurusd, 'USDJPY' : d4usdjpy }
#         For usage, see fred-georeturns.ipynb for details,
#         in particular, functions like group*() in this module.

cotr4w = { 'Bonds' : w4cotr_bonds, 'Equities' : w4cotr_equities, 
           'Metals' : w4cotr_metals, 'USD' : w4cotr_usd }
#         For usage, see qdl-COTR-positions.ipynb for details,
#         "Market position indicators using CFTC COTR"
#         COTR := Commitment of Traders Report.

world4d = { 'America' : 's4spy', 'Europe' : 's4ezu',
            'Japan' : 's4ewj',  'Emerging' : 's4eem', 'Gold' : 's4gld' }
#         For usage, see prtf-boltzmann-1.ipynb for details,
#         Exchange Traded Funds (ETF) of daily frequency
#         representing EQUITIES worldwide plus gold.


def get( code, maxi=0 ):
    '''Unifies getfred, getqdl, and getstock for data retrieval.
    code is fredcode, quandlcode, futures slang, or stock slang.
    maxi should be an integer to set maximum number of data points, 
         where 0 implies the default value.

    get() will accept the vendor code directly as string, e.g. 
    from FRED and Quandl, or use one of our abbreviated variables 
    documented in the appropriate module listed above.
    The notebooks provide good code examples in action.

    Futures slang is of the form 'f4spotyym' where
                  spot is the spot symbol in lower case,
                  yy   is the last two digits of the year
                  m    is the delivery month code,
            so for December 2015 COMEX Gold: 'f4xau15z'

    Stock slang can be also used for ETFs and mutual funds. 
    The general form is 's4symbol' where the symbol must be in 
    lower case, so for SPY, use 's4spy' as an argument.
    '''
    try:
        df = getfred( code )
    except:
        try:
            if maxi:
                df = getqdl( code, maxi )
            else:
                df = getqdl( code )
        except:
            try:
                if maxi:
                    df = getstock( code, maxi )
                else:
                    df = getstock( code )
            except: 
                raise ValueError('INVALID symbol string or code for fecon get()')
    return df


def plot( data, title='tmp', maxi=87654321 ):
    '''Unifies plotdf, plotfred and plotqdl for plotting data.
       The "data" argument could also be fredcode or quandlcode, 
       but not stock slang -- a Dataframe is first choice, 
       yet (as of 2016-01-20) Series type is also acceptable.
       Assumes date index; for numbered index or List, use plotn() instead.
    '''
    try:
        plotdf( tail(data, maxi), title )
        #  2016-01-20  plotdf now sports a todf pre-filter for convenience.
    except:
        try:
            plotfred( data, title, maxi )
        except:
            try:
                plotqdl( data, title, maxi )
            except:
                raise ValueError('INVALID argument or data for fecon plot()')
    return



def forecast( data, h=12, grids=0, maxi=0 ):
    '''Make h period ahead forecasts using holt* or optimize_holtforecast,
       where "data" may be a DataFrame, fredcode, quandlcode, or stock slang.
       (Supercedes: "Unifies holtfred and holtqdl for quick forecasting.")
    '''
    #  Generalization of 2016-12-29 preserves and expands former interface.
    if not isinstance( data, pd.DataFrame ):
        try:
            data = get( data, maxi )
            #           ^expecting fredcode, quandlcode, or stock slang
            #      to be retrieved as DataFrame.
        except:
            raise ValueError("fecon235.forecast(): INVALID data argument.")
    if grids > 0:
        #  Recommend grids=50 for reasonable results,
        #  but TIME-CONSUMING for search grids > 49
        #  to FIND OPTIMAL alpha and beta by minBrute():
        opt =  optimize_holtforecast( data, h, grids=grids )
        #  See optimize_holtforecast() in module ys_opt_holt for details.
        system.warn( str(opt[1]), stub="OPTIMAL alpha, beta, losspc, loss:" )
        return opt[0]
    else:
        #  QUICK forecasts when grids=0 ...
        #  by using FIXED defaults: alpha=ts.hw_alpha and beta=ts.hw_beta:
        holtdf = holt( data )
        system.warn("Holt-Winters parameters have NOT been optimized.")
        return holtforecast( holtdf, h )


def foreholt( data, h=12, alpha=hw_alpha, beta=hw_beta, maxi=0 ):
    '''Holt-Winters forecast h-periods ahead (data slang aware).'''
    #  "data" can be a fredcode, quandlcode, stock slang, 
    #         OR a DataFrame which will be detected:
    if not isinstance( data, pd.DataFrame ):
        try:
            data = get( data, maxi )
        except:
            raise ValueError("fecon235.forehalt(): INVALID data argument.")
    #  To find optimal parameter values for alpha and beta beforehand, 
    #  use optimize_holtforecast() in module ys_opt_holt.
    holtdf = holt( data, alpha, beta )
    #   Interim results will not be retained.
    return holtforecast( holtdf, h )


def holtfred( data, h=24, alpha=hw_alpha, beta=hw_beta ):
     '''Holt-Winters forecast h-periods ahead (fredcode aware).'''
     #  Retained for backward compatibility, esp. pre-2016 notebooks.
     return foreholt( data, h, alpha, beta )


def groupget( ggdic=group4d, maxi=0 ):
    '''Retrieve and create group dataframe, given group dictionary.'''
    #  Since dictionaries are unordered, create SORTED list of keys:
    keys = [ key for key in sorted(ggdic) ]
    #  Download individual dataframes as values into a dictionary:
    dfdic = { key : get(ggdic[key], maxi)  for key in keys }
    #             ^Illustrates dictionary comprehension.
    #  Paste together dataframes into one large sorted dataframe:
    groupdf = paste([ dfdic[key] for key in keys ])
    #  Name the columns:
    groupdf.columns = keys
    return groupdf


def groupfun( fun, groupdf, *pargs, **kwargs ):
    '''Use fun(ction) column-wise, then output new group dataframe.'''
    #  In math, this is known as an "operator":
    #           a function which takes another function as argument.
    #  Examples of fun: pcent, normalize, etc. See grouppc() next.
    #  See groupget() to retrieve and create group dataframe.  
    keys = list(groupdf.columns)
    #  Compute individual columns as dataframes in a list:
    out = [todf( fun(todf(groupdf[key]), *pargs, **kwargs) ) for key in keys]
    #            ^Python 2 and 3 compatible: apply() removed in Python 3.
    #  Paste together dataframes into one large dataframe:
    outdf = paste( out )
    #  Name the columns:
    outdf.columns = keys
    return outdf


def grouppc( groupdf, freq=1 ):
    '''Create overlapping pcent dataframe, given a group dataframe.'''
    #  See groupget() to retrieve and create group dataframe.  
    #  Very useful to visualize as boxplot, see fred-georeturns.ipynb
    return groupfun( pcent, groupdf, freq )


def groupdiflog( groupdf, lags=1 ):
    '''Difference between lagged log(data) for columns in group dataframe.'''
    #  See groupget() to retrieve and create group dataframe.  
    return groupfun( diflog, groupdf, lags )


def covdiflog( groupdf, lags=1 ):
    '''Covariance array for differenced log(column) from group dataframe.
       For correlation array: apply yi_matrix.cov2cor() later.
    '''
    #  See groupget() to retrieve and create group dataframe.  
    rates = groupdiflog( groupdf, lags )
    V = rates.cov()
    #        ^Type of V is still pandas DataFrame, so convert to array.
    #  AVOID the np.matrix subclass; stick with np.ndarrays instead:
    return V.values


def groupgeoret( groupdf, yearly=256, order=True ):
    '''Geometric mean returns, non-overlapping, for group dataframe.
       Argument "yearly" refers to annual frequency, e.g. 
       256 for daily trading days, 12 for monthly, 4 for quarterly.
       ___ATTN___ Use groupgemrat() instead for greater accuracy.
    '''
    keys = list(groupdf.columns)
    #  Use list comprehension to store lists from georet():
    geo = [ georet(todf(groupdf[k]), yearly) + [k]  for k in keys ]
    #  where each georet list gets appended with an identifying key.
    if order:
        geo.sort(reverse=True)
        #  Group is ordered in-place with respect to decreasing georet.
    return geo


def groupgemrat( groupdf, yearly=256, order=False, n=2 ):
    '''Geometric mean rates, non-overlapping, for group dataframe.
       Argument "yearly" refers to annual frequency, e.g. 
       256 for daily trading days, 12 for monthly, 4 for quarterly.
       Output is rounded to n-decimal places.
       Algorithm takes KURTOSIS into account for greater accuracy.
    '''
    keys = list(groupdf.columns)
    #  Use list comprehension to store lists from gemrat():
    gem = [ roundit(gemrat(todf(groupdf[k]), yearly), n, echo=False) 
            + [k]  for k in keys ]
    #       ^each gemrat list gets appended with an identifying key.
    if order:
        gem.sort(reverse=True)
        #  Group is ordered in-place with respect to decreasing gemrat.
    return gem


def groupholtf( groupdf, h=12, alpha=ts.hw_alpha, beta=ts.hw_beta ):
    '''Holt-Winters forecasts h-periods ahead from group dataframe.'''
    #  Tip: use all available (non-sliced) data for forecasting.    
    #  This is essentially a Kalman filter with optimal alpha-beta, 
    #  applied to each series individually, not jointly.
    #  cf. holtfred() which works given a single series dataframe.
    forecasts = []
    keys = list(groupdf.columns)
    for k in keys:
        kdf = todf( groupdf[k] )
        holtdf = holt( kdf, alpha, beta )
        forecastdf = holtforecast( holtdf, h )
        forecasts.append( forecastdf )
    keysdf = paste( forecasts )
    keysdf.columns = keys
    return keysdf


def groupcotr( group=cotr4w, alpha=0 ): 
    '''Compute latest normalized CFTC COTR position indicators.
       Optionally specify alpha for Exponential Moving Average
       which is a smoothing parameter: 0 < alpha < 1 (try 0.26)
       COTR is the Commitment of Traders Report from US gov agency.
    '''
    #  For detailed derivation, see qdl-COTR-positions.ipynb
    positions = groupget( group )
    norpositions = groupfun( normalize, positions )
    #  alpha default should skip SMOOTHING operation...
    if alpha:
        return groupfun( ema, norpositions, alpha )
    else:
        return norpositions


def forefunds( nearby='16m', distant='17m' ):
    '''Forecast distant Fed Funds rate using Eurodollar futures.'''
    #  Long derivation is given in qdl-libor-fed-funds.ipynb
    ffer = getfred('DFF')
    #      ^Retrieve Fed Funds effective rate, daily since 1954.
    ffer_ema = ema( ffer['1981':], 0.0645 )
    #                    ^Eurodollar futures debut.
    #          ^Exponentially Weighted Moving Average, 30-period.
    libor_nearby  = get( 'f4libor' + nearby  ) 
    libor_distant = get( 'f4libor' + distant )
    libor_spread = todf( libor_nearby - libor_distant )
    #     spread in forward style quote since futures uses 100-rate.
    return todf( ffer_ema + libor_spread )


def foreinfl( n=120, alpha=1.0, beta=0.3673 ):
    '''Forecast Unified Inflation 1-year ahead per fred-inflation.ipynb.'''
    #  Holt-Winters parameters alpha and beta are optimized
    #  from the 1960-2018 dataset, consisting of 697 monthly points.
    #  Each "way" is an orthogonal method, to be averaged as way[0].
    way = [-9, -9, -9, -9, -9]
    inflall = get( m4infl )  # synthetic Unified Inflation, monthly.
    infl = tail(inflall, n)
    #                    ^Default n=120 months, i.e. last 10 years.
    way[1] = str(infl.index[-1]).replace(" 00:00:00", "")
    #                ^Most recent month for CPI, CPIc, PCE, PCEc data.
    gm = gemrat( infl, yearly=12 )
    way[2] = gm[0]  #  Geometric Mean Rate over n months.
    hw = foreholt( infl, 12, alpha, beta )  # Holt-Winters model.
    way[3] = (tailvalue(hw) - 1) * 100   # Convert forecasted level to rate.
    bond10 = get(m4bond10)
    tips10 = get(m4tips10)
    bei = todf(bond10 - tips10)   #  10-year BEI Break-even Inflation.
    #         ^Bond market data will be more recent than m4infl.
    way[4] = tailvalue(bei)
    #        Final forecast is the AVERAGE of orthogonal ways:
    way[0] = sum(way[2:]) / len(way[2:]) 
    #     "way" in SUMMARY is thus: [Average, "infl-date", GMR, HW, BEI]
    #                e.g. [2.2528, '2018-01-01', 1.5793, 3.0791, 2.1000]
    return way


if __name__ == "__main__":
     system.endmodule()
