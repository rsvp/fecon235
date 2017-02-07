#  Python Module for import                           Date : 2017-02-07
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_quandl.py : Access Quandl with pandas for plots, etc.

We define procedures to access data from Quandl.  Each economic time series
and its frequency has its own "quandlcode" which is available at their site:
http://www.quandl.com

          Usage:  df = getqdl( quandlcode )
                  #            ^Favorites are named d4*, w4*, m4*, q4*.

                  plotqdl( dataframe or quandlcode )

                  holtqdl( dataframe or quandlcode )
                  #  Holt-Winters forecast.

                  #  Single column dot notation for quandlcode: 
                  #  e.g. 'NSE/OIL.4' grabs the 4th column of NSE/OIL.

SYNOPSIS
          _____ API Key

You will need an API Key unless you are doing fewer than 50 calls per day.

Once you have your token, simply include it with your first function call,
like this:

     mydata = qdlapi.get("NSE/OIL", authtoken="your token here")

It will then be stored in your working directory for continued use.
Authtokens are saved as pickled files in the local directory as "authtoken.p"
so it is unnecessary to enter them more than once, unless you change your
working directory. 

After creating an account at quandl.com, set your authentication token with
the [Deprecated: Quandl.auth() function] setQuandlToken function below.


          _____ Usage Rules

API usage is free for registered users. Registered users have a limit of 2,000
calls per 10 minutes, and a limit of 50,000 calls per day. Premium data
subscribers have a limit of 5,000 calls per 10 minutes, and a limit of 720,000
calls per day.  Dataset calls are rate-limited to 2,000 calls per 10 minutes.

All API requests must be made using HTTPS. Requests made over HTTP will fail.


          _____ Quandl Codes

To use the API to download a dataset, you will need to know the dataset's
"quandlcode".  Each dataset on Quandl has a unique Quandl code, comprising a
database_code and a dataset_code. For instance, the dataset named GDP of the
United States has the Quandl code FRED/GDP, where FRED is the database code
and GDP is the dataset_code. All datasets from the same database will have the
same database code.

Dataset codes are not guaranteed to be unique across databases. SHFE/CUG2014
is not the same as MCX/CUG2014. You need both the database_code and the
dataset_code to fully identify a dataset.


          _____ Pre-calculations

In general, we suggest downloading the data in raw format in the highest
frequency possible and preforming any data manipulation in pandas itself.

Quandl allows you to perform certain elementary calculations on your data
prior to downloading. The transformations currently availabe are row-on-row
change, percentage change, cumulative sum, and normalize (set starting value
at 100).  If a datapoint for time t is denoted as y[t] and the transformed
data as y'[t], the available transformations are defined as below:

Transformation      Parameter     Effect
Row-on-row change   diff          y'[t] = y[t] - y[t-1]
Row-on-row % change rdiff         y'[t] = (y[t] - y[t-1])/y[t-1]
Cumulative sum      cumul         y'[t] = y[t] +y[t-1] + ... + y[0]
Start at 100        normalize     y'[t] = (y[t]/y[0]) * 100

Note that y[0] in the above table refers to the starting date for the API
call, i.e., the date specified by trim_start= or rows=, NOT the starting date
of the entire dataset.


          _____ Specific API Guides

Economics: https://www.quandl.com/resources/api-for-economic-data
Stocks:    https://www.quandl.com/resources/api-for-stock-data
Earnings:  https://www.quandl.com/resources/api-for-earnings-data
Futures:   https://www.quandl.com/resources/api-for-futures-data
Currencies:  https://www.quandl.com/resources/api-for-currency-data
Bitcoin:     https://www.quandl.com/resources/api-for-bitcoin-data
Commodities: https://www.quandl.com/resources/api-for-commodity-data
Housing:     https://www.quandl.com/resources/api-for-housing-data
Cross-Country Stats: https://www.quandl.com/resources/api-for-country-data


          _____ Contact

Reach out to Quandl for direct support at connect@quandl.com
Inquires about the Python API package to    Chris@quandl.com


     __________ Using Quandl's Python module

[We have copied the Quandl.py module to yi_quandl_api.py as qdlapi. 
 Thus their use of Quandl.get is equivalent to our quandl function here.]

The Quandl package is able to return data in 2 formats: a pandas data series
("pandas") and a numpy array ("numpy"). "pandas" is the default. Here's how
you specify the format explicitly:

     mydata = Quandl.get("WIKI/AAPL", returns="numpy")

You can get multiple datasets in one call by passing an array of Quandl codes,
like this:

     mydata = Quandl.get(["NSE/OIL.4","WIKI/AAPL.1"])

This grabs the 4th column of dataset NSE/OIL and the 1st column of dataset
WIKI/AAPL, and returns them in a single call.

Python package offers various ways to manipulate or transform the data prior
to download: 

     Specific Date Range:
     mydata = Quandl.get("NSE/OIL", trim_start="yyyy-mm-dd", 
                                    trim_end="yyyy-mm-dd")

     Frequency Change:
     mydata = Quandl.get("NSE/OIL", collapse="annual")
     #  ("daily"|weekly"|"monthly"|"quarterly"|"annual")

     Transformations:
     mydata = Quandl.get("NSE/OIL", transformation="rdiff")
     #  ("diff"|"rdiff"|"normalize"|"cumul")

     Return last n rows:
     mydata = Quandl.get("NSE/OIL", rows=5)

A request with a full list of options would look like the following:

data = Quandl.get('PRAGUESE/PX', authtoken='xxxxxx', trim_start='2001-01-01',
                  trim_end='2010-01-01', collapse='annual',
                  transformation='rdiff', rows=4, returns='numpy')


          _____ Push Example

You can now upload your own data to Quandl through the Python package. At this
time the only accepted format is a date indexed Pandas DataSeries.

Things to do before you upload:

    - Make an account and set your authentication token within the package
      with the setQuandlToken function below.
    - Get your data into a data frame with the dates in the first column.
    - Pick a code for your dataset - only capital letters, numbers and
      underscores are acceptable.

Then call the following to push the data:
     Quandl.push(data, code='TEST', name='Test', desc='test')

All parameters but desc are necessary. If you wish to override the existing
set at code TEST add override=True.


REFERENCES:

- Using Quandl's Python module: https://www.quandl.com/help/python
                   GitHub repo: https://github.com/quandl/quandl-python

- Complete Quandl API documentation: https://www.quandl.com/docs/api
  including error codes.

- [ RESTful interface introduction:  https://www.quandl.com/help/api
            Not needed here, but it's available. ]

- CFTC Commitments of Traders Report, explanatory notes:
  http://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes

     - Traders' option positions are computed on a futures-equivalent basis
       using delta factors supplied by the exchanges.
     
- Computational tools for pandas
       http://pandas.pydata.org/pandas-docs/stable/computation.html

- Wes McKinney, 2013, _Python for Data Analysis_.


CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-02-07  Add quandlcode for Bitcoin count and USD price.
2017-02-06  Use names() within getqdl() to standardize names.
2016-11-05  Remove comments intended as code templates.
2016-03-21  Add freqM2MS for compatibility with FRED monthly format.
               Add m4spx_1871_p, m4spx_1871_e, m4spx_1871_d. 
2015-12-20  python3 compatible: lib import fix.
2015-12-17  python3 compatible: fix with yi_0sys
2015-09-11  Add getfut to quickly retrieve futures price data.
2015-08-26  Add silver futures symbol and w4cotr_metals.
2015-08-03  First version patterned after yi_fred.py
'''

from __future__ import absolute_import, print_function

import pandas as pd

from . import yi_quandl_api as qdlapi    #  a.k.a. Quandl.py module
from . import yi_0sys as system
from . import yi_1tools as tools         
from . import yi_fred as fred            #  For: plotdf, freqM2MS
from . import yi_timeseries as ts        #  esp. Holt-Winters.


#      __________ Convenient ABBREVIATIONS for less typing of quotes:
#                 pandas can use string to slice data, e.g. df[t06:]
t50    = '1950'
t60    = '1960'
t70    = '1970'
t80    = '1980'
t90    = '1990'
t98    = '1998'
t00    = '2000'
t06    = '2006'                  #  a.k.a. post Great Recession.
t10    = '2010'
t13    = '2013'

T      = 'T'                     #  Generic time index.
Y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.
y      = 'Y'                     #  GENERIC FIRST COLUMN name herein.



#      __________ FUTURES quandlcode:
#                 Related to fut_dict and fut_decode() for code slang.
#
f4fed         = 'FF'      #  CME/CBOT Fed Funds
f4libor       = 'ED'      #  CME Eurodollars
f4bond10      = 'TY'      #  CME/CBOT 10-y Treasury
f4spx         = 'SP'      #  CME S&P 500
f4spes        = 'ES'      #  CME E-minis
f4cad         = 'CD'      #  CME
f4gbp         = 'BP'      #  CME
f4eur         = 'EC'      #  CME
f4chf         = 'SF'      #  CME
f4jpy         = 'JY'      #  CME
f4xau         = 'GC'      #  CME/COMEX Gold
f4xag         = 'SI'      #  CME/COMEX Silver
f4wti         = 'CL'      #  CME/NYMEX Oil



#      __________ DAILY quandlcode: #  d7 means seven days/week 
d7xbtusd      = 'BCHAIN/MKPRU'      #  Bitcoin price in USD
d7xbtcount    = 'BCHAIN/TOTBC'      #  number of Bitcoins (~16 million)
#  d7xbtcap   = 'BCHAIN/MKTCP'      #  Market capitalization (~16 billion USD)
#                ...                   ... replicated by d7xbtusd * d7xbtcount


#      __________ WEEKLY quandlcode:
w4cotr_xau      = 'w4cotr_xau'      #  CFTC COTR Manager position: Gold
w4cotr_metals   = 'w4cotr_metals'   #  CFTC COTR Manager position: Gold, Silver
w4cotr_usd      = 'w4cotr_usd'      #  CFTC COTR Manager position: US Dollar
w4cotr_bonds    = 'w4cotr_bonds'    #  CFTC COTR Manager position: Bonds
w4cotr_equities = 'w4cotr_equities' #  CFTC COTR Manager position: Equities



#      __________ MONTHLY quandlcode:
m4spx_1871_p    = 'm4spx_1871_p'    #  Shiller S&P500 nominal price
m4spx_1871_e    = 'm4spx_1871_e'    #  Shiller S&P500 nominal earnings 12-month
m4spx_1871_d    = 'm4spx_1871_d'    #  Shiller S&P500 nominal dividends 12-month



#       __________ ALIASES

quandl = qdlapi.get
#              ^MAIN workhorse to RETREIVE data using QUANDL API.  <= !!
#                    Note: getqdl is our convenience wrapper.



def setQuandlToken( API_key ):
     '''Generate authtoken.p in the local directory for API access.'''
     #  Must have API key which is free by creating a Quandl account, 
     #  however, this is not necessary for very limited usage.
     dummy = qdlapi.get("NSE/OIL", authtoken=API_key, rows=1)
     #  The first request is all that matters for getting initiated.
     print(' ::  Generated authtoken.p in local directory for API access.')
     #
     #  For security, authtoken.p shall not be committed via .gitignore


def cotr_get( futures='GC', type='FO' ):
     '''Get CFTC Commitment of Traders Report COTR.'''
     #  Report for futures only requested by type "F".
     #  Report for both futures and options requested by type "FO".
     #  e.g. 'CFTC/GC_FO_ALL' for CFTC COTR: Gold futures and options.
     #
     #  Traders' option positions are computed on a futures-equivalent basis
     #  using delta factors supplied by the exchanges.
     quandlcode = 'CFTC/' + futures + '_' + type + '_ALL'
     return quandl( quandlcode )


def cotr_position( futures='GC' ):
     '''Extract market position from CFTC Commitment of Traders Report.'''
     cotr = cotr_get( futures )
     #  Report for both futures and options requested by implicit "FO".
     #
     #  For directionality we use these categories:
     try:
          longs  = cotr['Asset Manager Longs']
          shorts = cotr['Asset Manager Shorts']
          #  "Leveraged Funds" for FINANCIALS appear short-term, whereas 
          #  "Asset Manager" takes longer term perspective.
     except:
          longs  = cotr['Money Manager Longs']
          shorts = cotr['Money Manager Shorts']
          #  "Money Manager" for COMMODITIES. 
          #  The report is structured differently than financials.
          #
     #                _Scale-free between 0 and 1 indicating bullishness.
     return tools.todf( longs / (longs + shorts ))


def cotr_position_usd():
     '''Market position for USD from COTR of JY and EC.'''
     #  We ignore USD index DX from ICE.
     pos1 = cotr_position( 'JY' )
     #                      JPY futures.
     pos2 = cotr_position( 'EC' )
     #                      EUR futures.
     #
     #                  _Inverts position relative to quotation styles.
     #                      _Average reading between two contracts.
     return tools.todf( 1 - ((pos1 + pos2) / 2.0) )


def cotr_position_metals():
     '''Market position for precious metals from COTR of GC and SI.'''
     pos1 = cotr_position( 'GC' )
     #                      Gold Comex
     pos2 = cotr_position( 'SI' )
     #                      Silver Comex
     #
     #                  _Average reading between two contracts.
     return tools.todf( (pos1 + pos2) / 2.0 )


def cotr_position_bonds():
     '''Market position for bonds from COTR of TY and ED.'''
     pos1 = cotr_position( 'TY' )
     #                      TY is 10-years.
     pos2 = cotr_position( 'ED' )
     #                      Eurodollar strips.
     #
     #                  _Average reading between two contracts.
     return tools.todf( (pos1 + pos2) / 2.0 )


def cotr_position_equities():
     '''Market position for equities from COTR of both SP and ES.'''
     pos1 = cotr_position( 'SP' )
     #                      SP better for options reading.
     pos2 = cotr_position( 'ES' )
     #                      Minis better for reading futures.
     #
     #                  _Average reading between two contracts.
     return tools.todf( (pos1 + pos2) / 2.0 )



#   DICTIONARY to translate our futures slang to vendor code:
fut_dict = {
    'f4fed':      'CME/FF',
    'f4libor':    'CME/ED',
    'f4bond10':   'CME/TY',
    'f4spx':      'CME/SP',
    'f4spes':     'CME/ES',
    'f4cad':      'CME/CD',
    'f4gbp':      'CME/BP',
    'f4chf':      'CME/SF',
    'f4eur':      'CME/EC',
    'f4jpy':      'CME/JY',
    'f4xau':      'CME/GC',
    'f4xag':      'CME/SI',
    'f4wti':      'CME/CL'}

#  Gotcha: dataframe columns are not consistent across exchanges.
#
#          Chicago Mercantile Exchange     CME    [for NYMEX and COMEX]
#          Intercontinental Exchange       ICE
#          Eurex                           EUREX
#          London                          LIFFE
#          Singapore Exchange              SGX
#          Shanghai Futures Exchange       SHFE
#          Tokyo Futures Exchange          TFX


def fut_decode( slang ):
    '''Validate and translate slang string into vendor futures code.

    Quandl uses format: {EXCHANGE}/{CODE}{MONTH}{YEAR}
         {EXCHANGE} is the acronym for the futures exchange
         {CODE} is the futures ticker code
         {MONTH} is the single-letter month code
         {YEAR} is a 4-digit year
    So for COMEX Gold Dec 2015: 'CME/GCZ2015' [note: CAPITALIZATION]

    !!  Our short slang must be in all lower case, e.g. 

    >>> print(fut_decode( 'f4xau15z' ))
    CME/GCZ2015
    '''
    if slang.isupper():
        #  So if given argument is in all CAPS...
        raise ValueError('Futures slang argument is invalid.')
        #  The official code should yield all dataframe columns, 
        #  whereas slang is intended for selecting just one column.
        #  Thus NOT:  symbol = slang
    else:
        try:
            #  Parse slang, lookup in dict, translate into symbol:
            asset = slang[:-3].lower()
            #                 ^if f4* variables are possibly involved.
            year  = '20' + slang[-3:-1]
            month = slang[-1].upper()
            symbol = fut_dict[ asset ] + month + year
        except:
            raise ValueError('Futures slang argument is invalid.')
    return symbol


def getfut( slang, maxi=512, col='Settle' ):
     '''slang string retrieves single column for one futures contract.

     The string consists of a key from fut_dict concatenated with 
     'yym' where yy is shorthand for year and m is the month symbol 
     all in lower case, e.g. 'f4xau15z' for December 2015 Comex Gold.

     Available col are: Open, High, Low, Last, Change, Settle,
                        Volume, 'Open Interest'
     '''
     #  Other than Eurodollars, we should not need more than 512 days 
     #  of data due to finite life of a futures contract.
     #  2015-09-11  quandl default seems to be maxi around 380.
     #
     fut = quandl( fut_decode( slang ), rows=maxi )
     #      return just a single column dataframe:
     return tools.todf( fut[[ col ]] )


#  CONTINUOUS FUTURES CONTRACTS are also available:
#  
#  Quandl proides continuous (aka concatenated or chained) futures contracts from
#  two sources: a free inhouse source CHRIS and a paid premium source Stevens SCF. 
#  Quality of SCF is substantially higher than that of CHRIS; the latter has
#  spikes, nulls, missing rows, jumps in the data, and inconsistent OHLC values;
#  the former is audited to be accurate, consistent and error-free.
#  
#  The format for continuous contracts from source CHRIS is
#       CHRIS/{EXCHANGE}_{CODE}{NUMBER}
#  where {NUMBER} is the "depth" associated with the chained contract. For
#  instance, the front month contract has depth 1, the second month contract has
#  depth 2, and so on.
#  
#  The format for continuous contracts from source Stevens SCF is
#       SCF/{EXCHANGE}_{CODE}{NUMBER}_{RULE}
#  where {NUMBER} is the "depth" associated with the chained contract, and {RULE}
#  specifies the roll-date rule and price adjustment if any. SCF offers 14
#  different combinations of roll date and price adjustment.


def freqM2MS( dataframe ):
     '''Change Monthly dates to (FRED-compatible) Month Start frequency.'''
     #  FRED uses first day of month 'MS' to index that month's data,
     #  whereas Quandl data *may* use varying end of month dates.
     df = dataframe.set_index(pd.DatetimeIndex(
                    [i.replace(day=1) for i in dataframe.index]))
     df.index = df.index.normalize()
     #  Thus converted to midnight (normalize) first day of month.
     df.index.name = 'T'
     #             ... but rename your columns elsewhere.
     #  Quandl *may* not infer frequency in its transmitted dataframes.
     #  So lastly, resampling converts index freq from None to 'MS'
     #  which may be necessary to align operations between dataframes:
     return fred.monthly( df )


#  For details on Shiller m4spx_1871_*, see notebook qdl-spx-earn-div.ipynb
#  esp. for underlying sources of reconstructed data.


def getm4spx_1871_p():
     '''Retrieve nominal monthly Shiller S&P500 price, starting 1871.'''
     price  = freqM2MS(quandl( 'MULTPL/SP500_REAL_PRICE_MONTH' ))
     #                           ^But they meant NOMINAL!
     #  Their inflation-adjusted monthly series is called
     #        MULTPL/SP500_INFLADJ_MONTH
     #  Alternative: official YALE/SPCOMP, but 9 months latency!
     return tools.todf( price )


def getm4spx_1871_e():
     '''Retrieve nominal monthly Shiller S&P500 earnings, starting 1871.'''
     ratio = freqM2MS(quandl( 'MULTPL/SP500_PE_RATIO_MONTH' ))
     #  Gets price/earnings ratio, so solve for 12-month earnings.
     #  Alternative: official YALE/SPCOMP, but 9 months latency!
     price = getm4spx_1871_p()
     earn  = tools.div( price, ratio )
     return tools.todf( earn )


def getm4spx_1871_d():
     '''Retrieve nominal monthly Shiller S&P500 dividends, starting 1871.'''
     dyield = freqM2MS(quandl( 'MULTPL/SP500_DIV_YIELD_MONTH' ))
     #  Gets dividend yield in percentage form, 
     #  but we want just plain dividends over previous 12 months.
     #  Alternative: official YALE/SPCOMP, but 9 months latency!
     dyield = tools.todf(tools.div( dyield, 100 ))
     price  = getm4spx_1871_p()
     return tools.todf( dyield * price )


def getqdl( quandlcode, maxi=87654321 ):
     '''Retrieve from Quandl in dataframe format, INCL. SPECIAL CASES.
            maxi is just arbitrarily large as default, 
                 useful to limit data to last maxi rows, 
                 e.g. maxi=1 for most recent row only,
                 but NOT used in all cases below.
     We can SYNTHESIZE a quandlcode by use of string equivalent arg.
     '''
     if   quandlcode == w4cotr_xau:
          df = cotr_position( f4xau )
     elif quandlcode == w4cotr_metals:
          df = cotr_position_metals()
     elif quandlcode == w4cotr_usd:
          df = cotr_position_usd()
     elif quandlcode == w4cotr_bonds:
          df = cotr_position_bonds()
     elif quandlcode == w4cotr_equities:
          df = cotr_position_equities()

     elif quandlcode == m4spx_1871_p:
          df = getm4spx_1871_p()
     elif quandlcode == m4spx_1871_e:
          df = getm4spx_1871_e()
     elif quandlcode == m4spx_1871_d:
          df = getm4spx_1871_d()

     elif quandlcode[:2] == 'f4':
          df = getfut( quandlcode )

     else:
          df = quandl( quandlcode, rows=maxi )
     #                 ^just the vanilla series... so
     #                  for "transformation" and "collapse" (resampling), 
     #                  call quandl() directly.
     #
     #         _Give default fecon235 names to column and index:
     df = tools.names( df )
     #         Finally NO NULLS, esp. for synthetics derived from 
     #         overlapping indexes (note that readfile does 
     #         fillna with pad beforehand):
     return df.dropna()



def plotqdl( data, title='tmp', maxi=87654321 ):
     '''Plot data should be it given as dataframe or quandlcode.'''
     #  maxi is an arbitrary maximum number of points to be plotted.
     #  Single column dot notation: e.g. 'NSE/OIL.4'
     #                              grabs the 4th column of NSE/OIL.
     if isinstance( data, pd.DataFrame ):
          fred.plotdf( tools.tail( data, maxi ), title )
     else:
          quandlcode = data
          df = getqdl( quandlcode )
          fred.plotdf( tools.tail( df,   maxi ), title )
     return


def holtqdl( data, h=24, alpha=ts.hw_alpha, beta=ts.hw_beta ):
     '''Holt-Winters forecast h-periods ahead (quandlcode aware).'''
     #  "data" can be a quandlcode, or a dataframe to be detected:
     if isinstance( data, pd.DataFrame ):
          holtdf = ts.holt(  data             , alpha, beta )
     else:
          quandlcode = data
          holtdf = ts.holt( getqdl(quandlcode), alpha, beta )
          #              ^No interim results retained.
     #    holtdf is expensive to compute, but also not retained.
     #    For details, see module yi_timeseries.
     return ts.holtforecast( holtdf, h )




#  #      __________ save and load dataframe by pickle. 
#                    ^^^^     ^^^^ renamed recently.
#  
#  The easiest way is to pickle it using save:
#  
#       df.to_pickle(file_name)  # where to save it, usually as a .pkl
#  
#  Then you can load it back using:
#  
#       df = pd.read_pickle(file_name)
#
#  However, PICKLE FORMAT IS NOT GUARANTEED, and takes up 4x relative to gz.



if __name__ == "__main__":
     system.endmodule()
