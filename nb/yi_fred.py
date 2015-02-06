#  Python Module for import                           Date : 2015-02-05
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_fred.py : Access FRED with pandas for plots, etc.

We define procedures to access data from the St. Louis Federal Reserve Bank. 
Each economic time series and its frequency has its own "fredcode" which 
is freely available at their site: http://research.stlouisfed.org/fred2/

          Usage:  df = getfred( fredcode )
                  #             ^Favorites are named d4*, m4*, q4*.

                  plotfred( dataframe or fredcode )

                  holtfred( dataframe or fredcode )
                  #  Holt-Winters forecast for FRED.

References:
- Computational tools for pandas
       http://pandas.pydata.org/pandas-docs/stable/computation.html

- Wes McKinney, 2013, _Python for Data Analysis_.

- Mico Loretan, Federal Reserve Bulletin, Winter 2005,
       "Indexes of the Foreign Exchange Value of the Dollar", 
       http://www.federalreserve.gov/pubs/bulletin/2005/winter05_index.pdf


CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-02-05  Add m4unempfr for France unemployment.
2014-10-17  Remedy wild import of functions from our modules.
2014-10-15  Add d4gas via weekly DoE gasoline survey, $/gal w/tax NSA.
2014-10-08  Add synthetic d4oil by averaging d4wti and d4brent.
2014-09-28  Save plotdf file only if title is actually given.
2014-09-21  Modify m4gdpusr from 2009 to current dollars.
               Add stats from Eurozone (FRED key phrase "Euro Area"):
               m4infleu, m4defleu, q4gdpeu, m4gdpeur.
2014-09-15  Change alpha and beta defaults for holtfred, see yi_timeseries.
2014-09-11  Add m4housing for starts and m4homepx for Case-Shiller 20-city.
2014-09-03  Add m4baseus for US Adjusted Monetary Base.
2014-08-28  Change symbols uniformly from "gold"  to "xau",
                                     from "sp500" to "spx".
               New series: m4xaueur, m4xaujpy, d4zero10, m4zero10.
2014-08-24  Add getm4eurusd which will combine synthetic EURUSD
               from 1971-2002 obtained by averaging DEM and FRF.
               Series m4usdjpy and synthetic m4eurjpy derived. 
               Add writefile for converting to CSV file. [moved yi_1tools]
2014-08-19  Add m4inflbei to average inflation with BEI.
               Add m4usdrtb, m4xaurtb, m4spxrtb as indexes.
               Use syntax from holtfred to broaden plotfred.
2014-08-16  Add m4pop, m4emppop, m4workers for population studies. 
               m4defl is effectively the inverse of aggregrated m4infl.
               Improve holtfred to handle both fredcode and dataframe arg.
2014-08-14  Add interpolate() for upsampling: daily, monthly, quarterly.
               Add holtfred for quick Holt-Winters forecast.
               Add getinflations to average inflation measures.
               Sort fredcodes and getfred subroutines.
2014-08-13  Add d4vix, synthetics: d4eurjpy, d4curve and d4bei.
2014-08-11  Rename getdataframe to getdata_fred, so getfred() is governing.
               Add synthetic m4defl as deflator dataframe.
2014-08-10  Add some fredcodes, mostly rates and forex. Revise list names.
               Add quarterly() to conform with FRED-style indexing.
2014-08-08  Add dpi for saving image files.
2014-08-06  Clarify title for plotdf.
2014-08-05  Improve plotdf to produce png file.
2014-08-02  Abstract readdataframe from getdataframe.
2014-08-01  Split off utilities to yi_1tools.py
2014-07-30  Add correlation for functional clarity.
2014-07-29  Substantial revisions based on fred-inflation.ipynb
2014-07-24  First version converted from fred-plot.ipynb
'''


import urllib2                    #  for downloading data.
import matplotlib.pyplot as plt   #  for standard plots.
import pandas as pd               #  for data munging.

import yi_1tools as tools         #  Our tools.
import yi_timeseries as ts        #  esp. Holt-Winters.

dotsperinch = 140                 #  Resolution for plot.


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


#      __________ Nearly CONSTANT:
zero10dur = 8.962                # duration of 10-y Treasury bond
#  2014-08-29 = 8.962 for 10-y due 8/15/24 c2.375 at 100.36 YTM 2.334%


#      __________ DAILY fredcode:

d4defl    = 'd4defl'             # synthetic deflator dataframe, see deflator()

d4libjpy  = 'JPY3MTD156N'        # 3-m LIBOR JPY, daily
d4libeur  = 'EUR3MTD156N'        # 3-m LIBOR EUR, daily
d4libusd  = 'USD3MTD156N'        # 3-m LIBOR USD, daily
d4bills   = 'DTB3'               # Treasury bills, daily
d4zero10  = 'd4zero10'           # Zero-coupon price of Treasury 10-y, daily
d4bond10  = 'DGS10'              # Treasury 10-y constant, daily
d4tips10  = 'DFII10'             # TIPS 10-y constant, daily
d4curve   = 'd4curve'            # Treasury 10_y-bills, getfred synthetic
d4bei     = 'd4bei'              # 10_y Break-even inflation, getfred synthetic

d4usdjpy  = 'DEXJPUS'            # USDJPY, daily
d4eurusd  = 'DEXUSEU'            # EURUSD, daily
d4eurjpy  = 'd4eurjpy'           # EURJPY, daily, getfred synthetic

d4xau     = 'GOLDPMGBD228NLBM'   # London PM Gold fix, daily
d4xauusd  =  d4xau               #  " synonym

d4vix     = 'VIXCLS'             # CBOE volatility on S&P options, daily
d4spx     = 'SP500'              # S&P 500 index a.k.a. SPX, daily
     #       ^only last ten years by April 2014 licensing,
     #        however, we have it archived since 1957:
     #             ~/ok/biz/inv/eq/data/FRED-SP500_1957-2014-ARC.csv.gz
     #        See getspx below which will read a local copy.
     #
     #  [ ] - method expires 2024, then use to_csv method to renew archive.

d4brent  = 'DCOILBRENTEU'        # Oil Brent, DoE NSA daily
d4wti    = 'DCOILWTICO'          # Oil WTI,   DoE NSA daily
d4oil    = 'd4oil'               # Oil av. Brent and WTI, synthetic daily
d4gas    = 'd4gas'               # Reg. gasoline $/gal. w/ tax, synthetic daily

dl_forex  = [d4xau, d4eurusd, d4usdjpy             ]
dl_short  = [d4bills, d4libusd, d4libeur, d4libjpy ] 
dl_long   = [d4bond10, d4tips10, d4spx             ]
dlist     = dl_forex + dl_short + dl_long



#      __________ MONTHLY fredcode:

m4gdpus   = 'm4gdpus'    # U.S. GDP in billions, SA monthly synthetic
m4gdpusr  = 'm4gdpusr'   # U.S. real GDP in current billions, SA monthly synthetic
m4housing = 'HOUST'      # U.S. Housing Starts, SA monthly
m4homepx  = 'm4homepx'   # Home price index Case-Shiller 20-city, SA monthly synthetic

m4wage    = 'AHETPI'     # Hourly earnings, all private nonfarm, SA monthly
                         #    production/nonsupervisory since 1964.
#  m4wage    = 'CES0500000003'  # Hourly earnings, all private nonfarm, SA monthly
#              ^but only starts from 2006 -- shallow data.
#               Larger than AHETPI by $24.45/$20.61 = 1.1863 as of July 2014.
m4unemp   = 'UNRATE'     # Unemployment rate, SA monthly
m4emppop  = 'EMRATIO'    # Civilian employment/population, percent SA monthly
m4pop     = 'POP'        # Total US population in thousands, NSA monthly
m4workers = 'm4workers'  # Total US working population in thousands, NSA monthly
m4debt    = 'm4debt'     # U.S. Federal debt in millions, NSA monthly synthetic

m4defl    = 'm4defl'     # synthetic deflator, see getdeflator().
m4cpi     = 'CPIAUCSL'   # Consumer Price Index, SA monthly since 1947
m4cpicore = 'CPILFESL'   # CPI core, SA monthly since 1957
                         #     core excludes food and energy.
m4pce     = 'PCEPI'      # Personal Consumption Expenditure, SA monthly
m4pcecore = 'PCEPILFE'   # PCE core, SA monthly
m4infl    = 'm4infl'     # synthetic inflation, see getinflations().
m4inflbei = 'm4inflbei'  # synthetic inflation averaged with BEI, see getfred.

m4bills   = 'TB3MS'      # Treasury bills, monthly
m4zero10  = 'm4zero10'   # Zero-coupon price of Treasury 10-y, monthly
m4bond10  = 'GS10'       # Treasury 10-y constant, monthly
m4tips10  = 'FII10'      # TIPS 10-y constant, monthly
m4bei     = 'm4bei'      # 10_y Break-even inflation, getfred synthetic

m4usdrtb  = 'TWEXBPA'    # Real trade-weighted USD index: Broad, monthly
m4xau     = 'm4xau'      # London Gold PM fix, synthetic monthly for getfred
m4xauusd  =  m4xau       #  " synonym
m4xaueur  = 'm4xaueur'   # Gold euro-denominated, synthetic monthly
m4xaujpy  = 'm4xaujpy'   # Gold  yen-denominated,           monthly
m4xaurtb  = 'm4xaurtb'   # Real trade-weighted Gold index, synthetic monthly

m4usdjpy  = 'm4usdjpy'   # USDJPY monthly, getfred synthetic
m4eurusd  = 'm4eurusd'   # EURUSD, DEM FRF synthetic 1971-2002, getfred monthly
m4eurjpy  = 'm4eurjpy'   # EURJPY monthly, getfred synthetic back to 1971

m4baseus  = 'AMBSL'      # U.S. Adjusted Monetary Base in billions, SA monthly

m4spx     = 'm4spx'      # S&P 500 index a.k.a. SPX, synthetic monthly for getfred
m4spxrtb  = 'm4spxrtb'   # Real trade-weighted SPX index, synthetic monthly

m4oil     = 'm4oil'      # Oil av. Brent and WTI, synthetic monthly

ml_econ   = [m4gdpusr, m4wage, m4unemp ]
ml_infl   = [m4cpi, m4cpicore, m4pce, m4pcecore] 
ml_short  = [m4bills]
ml_long   = [m4bond10, m4tips10, m4spx]
mlist     = ml_econ + ml_infl + ml_long



#      __________ QUARTERLY fredcode:

q4gdpus   = 'GDP'        # U.S. GDP in billions, SA quarterly
q4gdpusr  = 'GDPC1'      # U.S. real GDP in 2009 billions, SA quarterly
q4debt    = 'GFDEBTN'    # U.S. Federal debt in millions, NSA quarterly

q4spx     = 'q4spx'      # S&P 500 index, synthetic quarterly for getfred

ql_econ   = [q4gdpusr]
ql_long   = [q4spx]
qlist     = ql_econ + ql_long



#      __________ EUROZONE fredcode:
q4gdpeu   = 'EUNGDP'           # EU GDP in million euros, Eurostat SA quarterly
m4gdpeur  = 'm4gdpeur'         # EU GDP in real billions, synthetic SA monthly
m4infleu  = 'm4infleu'         # EU Consumer Prices, synthetic Eurostat monthly
m4defleu  = 'm4defleu'         # EU deflator, synthetic monthly

m4unempeu = 'LRHUTTTTEZM156S'  # EU Unemployment rate, OECD SA monthly
m4unempfr = 'LRHUTTTTFRM156S'  # FR Unemployment rate, OECD SA monthly 
#      France data is updated frequently, whereas for EU there is a severe lag.


#  ======================================== End of fredcode ===============


#  GOTCHA: pd.read_csv assumes str in what's read, thus
#          make conversions for numerical work later.

def readfile( filename, separator=',', compress=None ):
    '''Read file (CSV default) as pandas dataframe.'''
    #  If separator is space, use '\s+' since regex will work.
    #  compress will take 'gzip' or 'bzip' as value.

    dataframe = pd.read_csv( filename, sep=separator, 
                             compression=compress, 
                             index_col=0, parse_dates=True, 
                             header=0, names=['T', 'Y'] )
    #            Header on FRED's first line: DATE, VALUE
    #                             replaced by: T,   Y

    #  Numeric conversion is critical for math ops between dataframes!
    #        (Not necessary for plotting, seemingly auto-converted?)
    #  dtype is crucial, yet numeric conversion can be fragile
    #        when data is missing or mistyped, e.g.
    #             dataframe['Y'] = dataframe['Y'].astype(float)
    #        will fail if the data is not in perfect condition.
    dataframe['Y'] = dataframe['Y'].convert_objects(convert_numeric=True)
    #                              ^non-convertibles become NaN

    #  FRED uses "." to indicate missing value.
    dataframe['Y'] = dataframe['Y'].fillna(method='pad')
    #                              ^NaN replaced by fill forward, 
    #                               common practice in time series analysis.
    return dataframe
    #      ^has NO NULL VALUES because of pad above, 
    #       thus .dropna() is unnecessary.



def makeURL( fredcode ):
    '''Create http address to access FRED's CSV files.'''
    #         Validated July 2014.
    return 'http://research.stlouisfed.org/fred2/series/' \
        + fredcode + '/downloaddata/' + fredcode + '.csv'


#  N.B. -  getdata_fred is a vital helper for MORE GENERAL getfred BELOW.
#          It's the best primitive to get raw FRED data.

def getdata_fred( fredcode ):
    '''Download CSV file from FRED and read it as pandas DATAFRAME.'''
    #  2014-08-11 former name "getdataframe".
    fredcsv = urllib2.urlopen( makeURL(fredcode) )
    return readfile( fredcsv )



#  The function to plot data looks routine, but in actuality specifying the
#  details can be such a hassle involving lots of trial and error.

def plotdf( dataframe, title='tmp' ):
    '''Plot dataframe where its index are dates.'''
    dataframe = dataframe.dropna()
    #           ^esp. if it resulted from synthetic operations, 
    #                 else timestamp of last point plotted may be wrong.
    fig, ax = plt.subplots()
    ax.xaxis_date()
    #  ^interpret x-axis values as dates.
    plt.xticks( rotation='vertical' )
    #       show x labels vertically.

    ax.plot( dataframe.index, dataframe, 'b-' )
    #        ^x               ^y          blue line
    #                                     k is black.
    ax.set_title( title + ' / last ' + str(dataframe.index[-1]) )  
    #                                  ^timestamp of last data point
    plt.grid(True)
    plt.show()

    #  Now prepare the image FILE to save, 
    #  but ONLY if the title is not the default
    #  (since this operation can be very slow):
    if title != 'tmp':
         title = title.replace( ' ', '_' )
         imgf = 'plotdf-' + title + '.png' 
         fig.set_size_inches(11.5, 8.5)
         fig.savefig( imgf, dpi=dotsperinch )
         print " ::  Finished: " + imgf
    return



#  For details on frequency conversion, see McKinney 2103, 
#       Chp. 10 Resampling, esp. Table 10-5 on downsampling.
#       pandas defaults are:
#            how='mean', closed='right', label='right'
#
#  2014-08-10  closed and label to the 'left' conform to FRED practices.
#              how='median' since it is more robust than 'mean'. 
#  2014-08-14  If upsampling, interpolate() does linear evenly, 
#              disregarding uneven time intervals.


def daily( dataframe ):
     '''Resample data to daily using only business days.'''
     #                         'D' is used calendar daily
     #                          B  for business daily
     df =   dataframe.resample('B', how='median', 
                                    closed='left', label='left', 
                                    fill_method=None)
     #       how= for downsampling, fill_method= for upsampling.
     return df.interpolate(method='linear')
     #         ^applies to nulls, if upsampling.


def monthly( dataframe ):
     '''Resample data to FRED's month start frequency.'''
     #  FRED uses the start of the month to index its monthly data.
     #                         'M' is used for end of month.
     #                          MS for start of month.
     df =   dataframe.resample('MS', how='median', 
                                     closed='left', label='left', 
                                     fill_method=None)
     #        how= for downsampling, fill_method= for upsampling.
     return df.interpolate(method='linear')
     #         ^applies to nulls, if upsampling.


def quarterly( dataframe ):
     '''Resample data to FRED's quarterly start frequency.'''
     #  FRED uses the start of the month to index its monthly data.
     #  Then for quarterly data: 1-01, 4-01, 7-01, 10-01.
     #                            Q1    Q2    Q3     Q4
     #
     #                          ______Start at first of months,
     #                          ______for year ending in indicated month.
     df =   dataframe.resample('QS-OCT', how='median', 
                                         closed='left', label='left', 
                                         fill_method=None)
     #            how= for downsampling, fill_method= for upsampling.
     return df.interpolate(method='linear')
     #         ^applies to nulls, if upsampling.



def getm4eurusd( fredcode=d4eurusd ):
     '''Make monthly EURUSD, and try to prepend 1971-2002 archive.'''
     #  Synthetic euro is the average between 
     #                 DEM fixed at 1.95583 and 
     #                 FRF fixed at 6.55957.
     eurnow = monthly( getdata_fred( fredcode ) )
     try:
          eurold = readfile( 'FRED-EURUSD_1971-2002-ARC.csv.gz', compress='gzip' )
          eurall = eurold.combine_first( eurnow )
          #               ^appends dataframe
          print ' ::  EURUSD synthetically goes back monthly to 1971.'
     except:
          eurall = eurnow
          print ' ::  EURUSD monthly without synthetic 1971-2002 archive.'
     return eurall



def getspx( fredcode=d4spx ):
     '''Make daily S&P 500 series, and try to prepend 1957-archive.'''
     #  Fred is currently licensed for only 10 years worth, 
     #  however, we have a local copy of 1957-2014 daily data.
     spnow = getdata_fred( fredcode )
     try:
          spold = readfile( 'FRED-SP500_1957-2014-ARC.csv.gz', compress='gzip' )
          spall = spold.combine_first( spnow )
          #             ^appends dataframe
          print ' ::  S&P 500 prepend successfully goes back to 1957.'
     except:
          spall = spnow
          print ' ::  S&P 500 for last 10 years (1957-archive not found).'
     return spall



def gethomepx( fredcode=m4homepx ):
     '''Make Case-Shiller 20-city, and try to prepend 1987-2000 10-city.'''
     #  Fred's licensing may change since source is S&P, 
     #  however, we have a local copy of 1987-2013 monthly SA data.
     hpnow = getdata_fred( 'SPCS20RSA' )
     #                          20-city home price index back to 2000-01-01.
     try:
          hpold = readfile( 'FRED-home-Case-Shiller_1987-2013.csv.gz', compress='gzip' )
          #                 ^includes 10-city index from 1987-2000.
          #                  Current correlation with 20-city: 0.998
          #                  Thus the mashup is justified.
          hpall = hpold.combine_first( hpnow )
          #             ^appends dataframe
          print ' ::  Case-Shiller prepend successfully goes back to 1987.'
     except:
          hpall = hpnow
          print ' ::  Case-Shiller since 2000 (1987-archive not found).'
     #  Case-Shiller is not dollar based, so we use:
     #  Median Sales Price of Existing Homes
     #  from the National Association of Realtors, fredcode: HOSMEDUSM052N
     dollarindex = 183700.57 / 153.843
     #     means:  ^Realtor$   ^C-S 20-city from 2000-01-01 to 2014-06-01.
     return hpall * dollarindex



def getinflations( inflations=ml_infl ):
     '''Normalize and average all inflation measures.'''
     #  We will take the average of indexes after their 
     #  current value is set to 1 for equal weighting. 
     inflsum = getdata_fred( inflations[0] )
     inflsum = inflsum / float(tools.tailvalue( inflsum ))
     for i in inflations[1:]:
          infl = getdata_fred( i )
          infl = infl / float(tools.tailvalue( infl ))
          inflsum += infl
     return inflsum / len(inflations)



def getdeflator( inflation=m4infl ):
     '''Construct a de-inflation dataframe suitable as multiplier.'''
     #  Usually we encounter numbers which have been deflated to dollars 
     #  of some arbitrary year (where the value is probably 100).
     #  Here we set the present to 1, while past values have increasing  
     #     multiplicative "returns" which will yield current dollars. 
     infl = getfred( inflation )
     lastin = tools.tailvalue( infl )
     return float( lastin ) / infl
     #           Think inverted inflation :-)



def getm4infleu( ):
     '''Normalize and average Eurozone Consumer Prices.'''
     #  FRED carries only NSA data from Eurostat,
     #  so we shall use Holt-Winters levels.
     cpiall   = getdata_fred( 'CP0000EZ17M086NEST' )
     #                        ^for 17 countries.
     holtall  = ts.holtlevel( cpiall )
     normall  = holtall  / float(tools.tailvalue( holtall  ))
     return normall
     #  #   SUSPENDED since last is 2013-12-01.
     #  cpicore  = getdata_fred( 'CPHPLA01EZM661N'    )
     #  holtcore = ts.holtlevel( cpicore )
     #  normcore = holtcore / float(tools.tailvalue( holtcore ))
     #  #  We will take the average of indexes after their 
     #  #  current value is set to 1 for equal weighting. 
     #  return (normall + normcore) / 2.0



def getfred( fredcode ):
     '''Retrieve from FRED in dataframe format, INCL. SPECIAL CASES.'''
     #    We can SYNTHESIZE a FREDCODE by use of string equivalent arg:
     if   fredcode == m4gdpus:
          df = monthly( getdata_fred( q4gdpus  ) )
     elif fredcode == m4gdpusr:
          df = getfred( m4defl ) * getfred( m4gdpus )
     elif fredcode == m4debt:
          df = monthly( getdata_fred( q4debt   ) )
     elif fredcode == m4workers:
          workfrac = getdata_fred( m4emppop ) / float(100)
          pop      = getdata_fred( m4pop    )
          df = workfrac * pop
     elif fredcode == m4homepx:
          df = gethomepx()

     elif fredcode == d4defl:
          df = daily( getdeflator() )
     elif fredcode == m4defl:
          df = getdeflator()
     elif fredcode == m4infl:
          df = getinflations()

     elif fredcode == m4gdpeur:
          mgdpeu = monthly( getdata_fred( q4gdpeu )) / float(1000)
          df = getfred( m4defleu ) * mgdpeu
     elif fredcode == m4infleu:
          df = getm4infleu()
     elif fredcode == m4defleu:
          df = getdeflator( m4infleu )

     elif fredcode == d4eurjpy:
          eurusd = getdata_fred( d4eurusd )
          usdjpy = getdata_fred( d4usdjpy )
          df = eurusd * usdjpy
     elif fredcode == m4usdjpy:
          df = monthly( getdata_fred( d4usdjpy ) )
     elif fredcode == m4eurusd:
          df = getm4eurusd()
     elif fredcode == m4eurjpy:
          eurusd = getfred( m4eurusd )
          usdjpy = getfred( m4usdjpy )
          df = eurusd * usdjpy
     elif fredcode == m4xau:
          df = monthly( getdata_fred( d4xau ) )
     elif fredcode == m4xaueur:
          xauusd = getfred( m4xau )
          eurusd = getfred( m4eurusd )
          df = xauusd / eurusd
     elif fredcode == m4xaujpy:
          xauusd = getfred( m4xau )
          usdjpy = getfred( m4usdjpy )
          df = xauusd * usdjpy
     elif fredcode == m4xaurtb:
          usdrtb = getdata_fred( m4usdrtb )
          xauusd = getfred( m4xau ) / float(1000)
          df = usdrtb * xauusd

     elif fredcode == d4zero10:
          bond10 = getdata_fred( d4bond10 )
          df = tools.zeroprice( bond10, zero10dur )
     elif fredcode == m4zero10:
          df = monthly( getfred( d4zero10 ))
     elif fredcode == d4curve:
          bond10 = getdata_fred( d4bond10 )
          bills  = getdata_fred( d4bills )
          df = bond10 - bills
     elif fredcode == d4bei:
          bond10 = getdata_fred( d4bond10 )
          tips10 = getdata_fred( d4tips10 )
          df = bond10 - tips10
     elif fredcode == m4bei:
          bond10 = getdata_fred( m4bond10 )
          tips10 = getdata_fred( m4tips10 )
          df = bond10 - tips10
     elif fredcode == m4inflbei:
          inflpc = tools.pcent( getfred(m4infl), 12 )  #  YoY% form 
          df = (inflpc + getfred(m4bei)) / float(2)
          #  ^average of backward and forward looking inflation!

     elif fredcode == d4spx:
          df = getspx()
     elif fredcode == m4spx:
          df = monthly( getspx() )
     elif fredcode == m4spxrtb:
          usdrtb = getdata_fred( m4usdrtb )
          spxusd = getfred( m4spx ) / float(1000)
          df = usdrtb * spxusd
     elif fredcode == q4spx:
          df = quarterly( getspx() )

     elif fredcode == d4oil:
          brent = getdata_fred( d4brent )
          wti   = getdata_fred( d4wti   )
          df = ( brent + wti ) / float(2) 
     elif fredcode == m4oil:
          df = monthly( getfred( d4oil ) )
     elif fredcode == d4gas:
          df = daily( getdata_fred( 'GASREGW' ) )
          #           ^weekly DoE survey, USD/gallon + tax, NSA 

     else:
          df = getdata_fred( fredcode )
     return df.dropna()
     #        ^NO NULLS finally, esp. for synthetics derived from 
     #         overlapping indexes, noting that in general: 
     #         readfile does fillna with pad beforehand.



def plotfred( data, title='tmp', maxi=87654321 ):
     '''Plot data should be it given as dataframe or fredcode.'''
     #  maxi is an arbitrary maximum number of points to be plotted.
     if isinstance( data, pd.DataFrame ):
          plotdf( tools.tail( data, maxi ), title )
     else:
          fredcode = data
          df = getfred( fredcode )
          plotdf( tools.tail( df,   maxi ), title )
     return



def holtfred( data, h=24, alpha=ts.hw_alpha, beta=ts.hw_beta ):
     '''Holt-Winters forecast h-periods ahead (fredcode aware).'''
     #  "data" can be a fredcode, or a dataframe to be detected:
     if isinstance( data, pd.DataFrame ):
          holtdf = ts.holt( data             , alpha, beta )
     else:
          fredcode = data
          holtdf = ts.holt( getfred(fredcode), alpha, beta )
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



# ## Footnotes
# 
# - *"Two different price indexes are popular for measuring inflation: the
# consumer price index (CPI) from the Bureau of Labor Statistics and the
# personal consumption expenditures price index (PCE) from the Bureau of
# Economic Analysis. [A]n accurate measure of inflation is important for both
# the U.S. federal government and the Federal Reserve's Federal Open Market
# Committee (FOMC), but they focus on different measures. For example, the
# federal government uses the CPI to make inflation adjustments to certain
# kinds of benefits, such as Social Security. In contrast, the FOMC focuses on
# PCE inflation in its quarterly economic projections and also states its
# longer-run inflation goal in terms of headline PCE. The FOMC focused on CPI
# inflation prior to 2000 but, after extensive analysis, changed to PCE
# inflation for three main reasons: The expenditure weights in the PCE can
# change as people substitute away from some goods and services toward others,
# the PCE includes more comprehensive coverage of goods and services, and
# historical PCE data can be revised (more than for seasonal factors only)."*
# --James Bullard, president of the Federal Reserve Bank of St. Louis. 



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
