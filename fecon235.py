#  Python Module for import                           Date : 2016-01-08
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  fecon235.py : unifies yi_* modules for fecon235 project.

- Designed to be invoked by an IPython/Jupyter console or notebook 
  for convenient command access. CASUAL usage:
        from fecon235.fecon235 import *
- User can always foo?? to access foo's origin.
- Unifies essential lib modules in one place, thus
  frequently used commands can be generalized with shorter names.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
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

from .lib import yi_0sys as system

#    CASUAL import style below intentionally for Jupyter notebooks
#    and interactive settings (lib modules follow proper import protocol).
#    We access essential modules and catch collisions in namespace:
from .lib.yi_1tools import *
from .lib.yi_fred import *
from .lib.yi_plot import *
from .lib.yi_quandl import *
#         yi_quandl_api should NOT be imported.
from .lib.yi_simulation import *
from .lib.yi_stocks import *
from .lib.yi_timeseries import *


#  We can specify our favorite series as a dictionary
#  where key is name, and corresponding value is its data code:
group4d = { 'Zero10' : d4zero10, 'SPX' : d4spx, 'XAU' : d4xau, 
            'EURUSD' : d4eurusd, 'USDJPY' : d4usdjpy }
#         For usage details, see fred-georeturns.ipynb for details,
#         in particular, functions like group*() in this module.


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
                raise ValueError('INVALID symbol string or code for fecon.get()')
    return df


def plot( data, title='tmp', maxi=87654321 ):
    '''Unifies plotfred and plotqdl for plotting data.'''
    #  "data" could also be fredcode or quandlcode, but not stock slang.
    try:
        plotfred( data, title, maxi )
    except:
        try:
            plotqdl( data, title, maxi )
        except:
            raise ValueError('INVALID argument or data for fecon.plot()')
    return


def forecast( data, h=12 ):
    '''Unifies holtfred and holtqdl for quick forecasting.'''
    #  Using the defaults: alpha=ts.hw_alpha and beta=ts.hw_beta
    #  "data" could also be fredcode or quandlcode, but not stock slang.
    try:
        df = holtfred( data, h )
    except:
        try:
            df = holtqdl( data, h )
        except:
            raise ValueError('INVALID argument or data for fecon.forecast()')
    return df


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


def grouppc( groupdf, freq=1 ):
    '''Create overlapping pcent dataframe, given a group dataframe.'''
    #  See groupget() to retrieve and create group dataframe.  
    #  Very useful to visualize as boxplot, see fred-georeturns.ipynb
    keys = list(groupdf.columns)
    #  Compute individual columns as dataframe values in a dictionary:
    pcdic = { key : todf(pcent(groupdf[key], freq))  for key in keys }
    #             ^Illustrates dictionary comprehension.
    #  Paste together dataframes into one large dataframe:
    pcdf = paste([ pcdic[key] for key in keys ])
    #  Name the columns:
    pcdf.columns = keys
    return pcdf


def groupgeoret( groupdf, yearly=256 ):
    '''Geometric mean returns, non-overlapping, for group dataframe.
       Argument "yearly" refers to annual frequency, e.g. 
       256 for daily trading days, 12 for monthly, 4 for quarterly.
    '''
    keys = list(groupdf.columns)
    #  Use list comprehension to store lists from georet():
    geo = [ georet(todf(groupdf[k]), yearly) + [k]  for k in keys ]
    #  where each georet list gets appended with a identifying key.
    geo.sort(reverse=True)
    #  Group is ordered in-place with respect to decreasing georet.
    return geo


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


if __name__ == "__main__":
     system.endmodule()
