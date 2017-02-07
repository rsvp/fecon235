#  Python Module for import                           Date : 2017-02-06
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_stocks.py : Access stock quotes.

We define procedures to access stock quotes FREELY and directly from 
Yahoo Finance or Google Finance. (Quandl's free services uses 
these sources indirectly, and since we want to avoid paying their 
premium pro vendors, we shall use the convenient pandas API.) 


          Usage:  df = getstock( 's4code', 7 )
                  #                        ^one week.
                  #              ^begin with s4, 
                  #               code is SYMBOL in lower case.


   Dependencies:  pandas-datareader (Another package for pandas >= 0.17)
                  #  Our code still works for older pandas 
                  #  by importing deprecated pandas.io
                  #  instead of pandas_datareader.

REFERENCES:

- pandas Remote Data Access (also for World Bank data)
       http://pandas.pydata.org/pandas-docs/stable/remote_data.html
     
- Computational tools for pandas
       http://pandas.pydata.org/pandas-docs/stable/computation.html

- Wes McKinney, 2013, _Python for Data Analysis_.


CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-02-06  Use names() within getstocks() to standardize names.
2015-12-20  python3 compatible: lib import fix.
2015-12-17  python3 compatible: fix with yi_0sys
2015-11-22  Test on python 2.7.10, IPython 4.0.0, pandas_datareader 0.2.0
                As of pandas v0.17, pandas.io is deprecated and 
                moved to a new package "pandas-datareader", 
                       but imported as "pandas_datareader".
2015-09-13  First version based on yi_quandl module.
'''

from __future__ import absolute_import, print_function

import datetime        #  pddata necessity.
try:
    import pandas_datareader.data as pddata  
    #  for pandas 0.17 and above
except:
    import pandas.io.data as pddata
    #  For old deprecated pandas

#  In pandas 0.17.0, the sub-package pandas.io.data will be removed 
#  in favor of a separately installable pandas-datareader package. 
#  This will allow the data modules to be independently updated 
#  to your pandas installation. The API for pandas-datareader v0.1.1 
#  is the same as in pandas v0.16.1. (GH8961)

from . import yi_0sys as system
from . import yi_1tools as tools


#      __________ Convenient ABBREVIATIONS for less typing of quotes:
T      = 'T'                     #  Generic time index.
Y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.
y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.


#      __________ Favorite ABBREVIATIONS as variables:
s4spx      = 's4spy'       #  Largest S&P500 ETF.



def stock_decode( slang ):
    '''Validate and translate slang string into vendor stock code.
       Our short slang must be in all lower case starting with s4, 
       e.g. 's4spy' with SYMBOL in lower case.

       Using slang helps to avoid collision in our larger namespace.
    '''
    if slang.isupper() or slang[:2] != 's4':
        #  So if given argument is in all CAPS, 
        #  or does not begin with 's4'
        raise ValueError('Stock slang argument is invalid.')
    else:
        try:
            symbol = slang[2:].upper()
        except:
            raise ValueError('Stock slang argument is invalid.')
    return symbol


def stock_all( slang, maxi=3650 ):
     '''slang string retrieves ALL columns for single stock.

     The slang string consists of 's4' + symbol, all in lower case, 
     e.g. 's4spy' for SPY.

     maxi is set to default of ten years past data.
     '''
     #       Typical:  start = datetime.datetime(2013, 1, 20)
     #       but we just want the most current window of data.
     now   = datetime.datetime.now()
     end   = now + datetime.timedelta( days=1 )
     #           ^add just to be safe about timezones.
     start = end - datetime.timedelta( days=maxi )
     #             Date offsets are chronological days, 
     #             NOT trading days.
     symbol = stock_decode( slang )
     #
     #        MAIN: use Yahoo Finance before Google Finance:
     try:
          df = pddata.DataReader( symbol, 'yahoo',  start, end )
          print(" ::  Retrieved from Yahoo Finance: " + symbol )
     except:
          df = pddata.DataReader( symbol, 'google', start, end )
          print(" ::  Retrieved from Google Finance: " + symbol)
     return df


def stock_one( slang, maxi=3650, col='Close' ):
     '''slang string retrieves SINGLE column for said stock.
        Available col include: Open, High, Low, Close, Volume
     '''
     df = stock_all( slang, maxi )
     #      return just a single column dataframe:
     return tools.todf( df[[ col ]] )


def getstock( slang, maxi=3650 ):
     '''Retrieve stock data from Yahoo Finance or Google Finance.
     maxi is the number of chronological, not trading, days.
     We can SYNTHESIZE a s4 slang by use of string equivalent arg.
     '''
     if   False:
          pass
     elif False:
          pass
     else:
          df = stock_one( slang, maxi, 'Close' )
     #
     #         _Give default fecon235 names to column and index:
     df = tools.names( df )
     #         Finally NO NULLS, esp. for synthetics derived from 
     #         overlapping indexes (note that readfile does 
     #         fillna with pad beforehand):
     return df.dropna()


if __name__ == "__main__":
     system.endmodule()
