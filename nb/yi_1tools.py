#  Python Module for import                           Date : 2014-12-09
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_1tools.py : essential utility functions.

References:
- Data structures
  http://pandas.pydata.org/pandas-docs/dev/dsintro.html

- Computational tools for pandas
  http://pandas.pydata.org/pandas-docs/stable/computation.html

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2014-12-09  Clarify comments, esp. regressformula.
2014-10-05  Note that paste for pandas < 0.14 will fail
               if column names are not unique 
               (newer pandas append _x to non-unique names).
2014-09-23  Add trend and trendforecast as aliases; detrend, detrendpc. 
               Rename normdetrend as detrendnorm. 
               Modify some formula arguments time regressions.
2014-09-19  Add helper regressTIME, then regresstimeforecast.
2014-09-14  Add some statsmodel functions:
               regressformula, regresstime, and normdetrend.
2014-09-11  Add normalize to center mean and standardize deviation.
2014-08-28  Add zeroprice for pricing zero-coupon bonds.
               Add writefile for converting to CSV file. [from yi_fred]
2014-08-23  Yield percentage form for georet.
2014-08-21  Add georet for geometric mean return.
2014-08-12  Add nona as a reminder for method dropna().
2014-08-11  Add tailvalue to extract last scalar.
2014-08-06  Add todf for series conversion to dataframe.
2014-08-05  Tool to paste dataframes across similar index values.
2014-08-01  First version split from yi_fred.py
'''

#  import numpy as np                #  for numerical work.
import matplotlib.pyplot as plt   #  for standard plots.
import pandas as pd               #  for data munging.

import statsmodels.formula.api as smf
#      ^pandas uses some portions of this package.
#
#  ols := Ordinary Least Squares, aka Linear Regression, 
#         pandas can handle multiple dependent variables.
from pandas.stats.api import ols
#                 ^relies on other sci packages.


def nona( df ):
     '''Eliminate any row in a dataframe containing NA, NaN nulls.'''
     return df.dropna()
     #  When calculating among dataframes, sometimes null entries 
     #  are produced where the indexes are overlapping.
     #  Such nulls may choke numerical routines.


def head( dfx, n=7 ):
     '''Quick look at the INITIAL data point(s).'''
     return dfx.head( n )


def tail( dfx, n=7 ):
     '''Quick look at the LATEST data point(s).'''
     return dfx.tail( n )


def tailvalue( df, pos=0, row=1 ):
     '''Seek (last) row of dataframe, then the element at position pos.'''
     #  For pos, the index is not considered.
     return df.tail(row).values.tolist()[0][pos]
     #      values to array to list within list, then the element.
     #  Note how the name of a column is not required.


def pcent( dfx, freq=1 ):
     '''PERCENTAGE CHANGE method for pandas.'''
     return dfx.pct_change( periods=freq ) * 100


def georet( dfx, yearly=256 ):
     '''Compute geometric mean return in a summary list.'''
     #  yearly refers to frequency, e.g. 256 for daily trading days,
     #                                    12 for monthly, 
     #                                     4 for quarterly.
     #-alt  dflg = np.log( dfx )
     #-alt  dfpc = dflg.diff( periods=1 )
     dfpc = dfx.pct_change( periods=1 )
     #          ^instead of first difference of logged data,
     #           gives slightly higher arithmetic means.
     mean = dfpc.mean().values.tolist()[0] * yearly
     vari = dfpc.var().values.tolist()[0]  * yearly
     #          ^summary statistics methods, see
     #           McKinney, p.139, Table 5-10.
     geor = mean - (0.5*vari)
     #      ^arithmetic mean return penalized by risk, 
     #      optimal choice under log utility.
     lst = [ geor, mean, vari ** 0.5 ]
     #                        ^^^^^^i.e. std sigma, or volatility.
     lst = [ round(i*100, 2) for i in lst ]
     #       ^[ geor, mean, volatility ] in readable % form.
     return lst + [ yearly ]


def zeroprice( rate, duration=9, yearly=2, face=100 ):
     '''Compute price of zero-coupon bond given its duration.'''
     #  Assume rate is in percentage form, e.g. 2.5% (not 0.025).
     #         rate could be a dataframe column.
     #  2014-08-28  duration of 10-y Treasury is 9.1 approx. 
     #  yearly refers to payouts per year, so 2 means semi-annual.
     periodrate = rate / float(yearly * 100)
     periods = duration * yearly
     return float(face) / (( 1 + periodrate) ** periods )



#  SMOOTH out data using EWMA, exponential weighted moving average,
#  where alpha=2/(span+1) where alpha is weight on the most recent point. 
#  The popular jargon is "span-day EW moving average."

def ema( y, alpha=0.20 ):
     '''EXPONENTIAL MOVING AVERAGE using traditional weight arg.'''
     #  y could be a dataframe.
     s = (2/float(alpha)) - 1
     #  Thus default alpha has span of 9, i.e. "9-period EWMA."
     return pd.ewma( y, span=s )


def normalize( dfy ):
     '''Center around mean zero and standardize deviation.'''
     centered = dfy - dfy.mean().tolist()[0]
     return centered / float( dfy.std().tolist()[0] )


def correlate( dfy, dfx, type='pearson' ):
     '''CORRELATION FUNCTION between series using pandas method.'''
     #  N.B. -  must specify column(s) within dataframe(s) !
     #              Types of correlations:
     #  'pearson'   Standard correlation coefficient
     #  'kendall' 	Kendall Tau correlation coefficient
     #  'spearman' 	Spearman rank correlation coefficient
     return dfy.corr( dfx, method=type )


def cormatrix( dataframe, type='pearson' ):
     '''PAIRWISE CORRELATIONS within a dataframe using pandas method.'''
     #              Types of correlations:
     #  'pearson'   Standard correlation coefficient
     #  'kendall' 	Kendall Tau correlation coefficient
     #  'spearman' 	Spearman rank correlation coefficient
     return dataframe.corr( method=type )



def regressformula( df, formula ):
     '''Helper function for statsmodel linear regression using formula.'''
     #
     #  FORMULA is a string like "Y ~ 0 + X + Z"
     #          where column names of the df dataframe are used.
     #          Omit the 0 if you want an intercept fitted.
     #
     #  USAGE given that: result = regressformula( ... )
     #        - print result.summary()
     #        - result.params
     #        - coeff = result.params.tolist()
     #
     #  ATTN:   ols is different from default OLS in pandas! see regress.
     return smf.ols(formula=formula, data=df).fit()


def regressTIME( dfy, col='Y' ):
     '''Regression on time since such index cannot be an independent variable.'''
     #  Assuming time series is evenly-spaced...
     df = dfy.dropna()
     #        ^insures proper alignment with timer:
     timer = [ -i for i in range(df.count()) ]
     timer.reverse()
     #    ^thus current point is 0, timer future is 1, 2, 3, etc.
     #  Start creating two new columns, Timer and Fitted, to df:
     df['Timer'] = timer
     formula = col + " ~ Timer"
     result = regressformula( df, formula )
     coeff = result.params.tolist()
     fitted = [ coeff[0] + (coeff[1] * i) for i in timer ]
     df['Fitted'] = fitted
     #  Now we can return the fitted dataframe with original time index:
     dffit = todf( df['Fitted'] )
     #             ^type Series
     return [ dffit, coeff ]


def regresstime( dfy, col='Y' ):
     '''Regression on time since such index cannot be an independent variable.'''
     #  Return just the fitted dataframe with original time intact.
     results = regressTIME( dfy, col )
     c, slope = results[1]
     print " ::  regresstime slope = " + str(slope)
     return results[0]


def regresstimeforecast( dfy, h=24, col='Y' ):
     '''Forecast h-periods ahead based on linear regression on time.'''
     c, slope = regressTIME( dfy, col )[1]
     forecast = [ c + (slope * i) for i in range(h+1) ]
     #  h=0 corresponds to the latest fitted point by design, 
     #      so h=1 corresponds one-period ahead forecast.
     print " ::  regresstime slope = " + str(slope)
     return todf( forecast, 'Forecast' )


#     Alias for regression on time functions:
trend         = regresstime
trendforecast = regresstimeforecast


def detrend( dfy, col='Y' ):
     '''Detread using linear regression on time.'''
     trend = regresstime( dfy, col )
     return dfy - trend


def detrendpc( dfy, col='Y' ):
     '''Detread using linear regression on time; percent deviation.'''
     trend = regresstime( dfy, col )
     return ((dfy - trend) * 100.00) / trend


def detrendnorm( dfy, col='Y' ):
     '''Detread using linear regression on time, then normalize.'''
     trend = regresstime( dfy, col )
     return normalize( dfy - trend )



def regress( dfy, dfx ):
    '''Perform LINEAR REGRESSION, a.k.a. Ordinary Least Squares.'''
    #          pandas ols can handle multiple dependent variables,
    #          but here we require only a single dependency.
    #          Other packages may not handle time index alignment.
    #  Returns summary printout,  
    #  (cf. more detailed regressformula which requires column names):
    return ols( y=dfy, x=dfx )


def stat2( dfy, dfx ):
     '''Quick STATISTICAL SUMMARY and regression on two variables'''
     print " ::  FIRST variable:"
     now = dfy.describe()
     print now
     print 
     print " ::  SECOND variable:"
     now = dfx.describe()
     print now
     print 
     print " ::  CORRELATION"
     now = correlate( dfy, dfx )
     print now
     now = regress( dfy, dfx )
     print now
     return


def stats( dataframe ):
     '''Statistics on given dataframe; correlations without regression.'''
     print dataframe.describe()
     print
     print " ::  Index on min:"
     print dataframe.idxmin()
     print
     print " ::  Index on max:"
     print dataframe.idxmax()
     print
     print " ::  Head:"
     print head( dataframe )
     print
     print " ::  Tail:"
     print tail( dataframe )
     print
     print " ::  Correlation matrix:"
     print cormatrix( dataframe )
     return


#  TIP:  After operating between dataframes, USE todf FOR CLARITY:

def todf( data, col='Y' ):
     '''CONVERT (list, Series, or DataFrame) TO DataFrame, NAMING single column.'''
     #
     #  Operating among dataframes often produces a SERIES.
     #  We need CONVERSION for possible "paste" later, 
     #     without the hassle of type() testing beforehand.
     #
     if isinstance( data, pd.DataFrame ):
          #  Oooops, easy to mistaken a dataframe for a series. 
          #  Move on, and just name that single column:
          target = data
          target.columns = [ col ]
     else:
          #  Do the conversion as intended:
          #  target = pd.DataFrame( data, columns=[ col ] )
          #                               ^fails if col pre-exists in data.
          target = pd.DataFrame( data )
          target.columns = [ col ]
     #             ________ Explicitly drop NA values. Very helpful routinely!
     return target.dropna() 


def paste( df_list ):
     '''Merge dataframes (not Series) across their common index values.'''
     #  N.B. -  paste for pandas < 0.14 will fail
     #          if column names are not unique 
     #          (newer pandas append _x to non-unique names).
     for i in df_list:
          if not isinstance( i, pd.DataFrame ):
               raise TypeError, ' !!  paste requires DataFrame args; use todf.'
               #  paste will choke on a Series type, so use todf beforehand.
     combo = df_list[0]
     for df in df_list[1:]:
          temp = combo.merge(df, left_index=True, 
                                 right_index=True, how='inner')
          #  'inner' takes intersection of index values, 
          #  whereas 'outer' takes their union.
          combo = temp.dropna()
          #            ^so row values will be comparable.
     return combo


def writefile( dataframe, filename='tmp-yi_1tools.csv', separator=',' ):
    '''Write dataframe to disk file using UTF-8 encoding.'''
    #  For tab delimited, use '\t' as separator.
    dataframe.to_csv( filename, sep=separator, encoding='utf-8' )
    print ' ::  Dataframe written to file: ' + filename
    return


if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
