#  Python Module for import                           Date : 2016-02-22
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_secform.py : module for SEC forms.

REFERENCES:
     - SEC form 13F, http://www.sec.gov/answers/form13f.htm

     - Jupyter notebook SEC-13F-parse.ipynb derives and debugs this module.
          For static view, see https://git.io/13F

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-02-22  Replace .sort(columns=...) with .sort_values(by=...)
               per future deprecation warning in pandas 0.17.1
2015-12-20  python3 compatible: lib import fix.
2015-12-17  python3 compatible: fix with yi_0sys
2015-08-30  First revised version for form 13F.
'''

from __future__ import absolute_import, print_function

import numpy as np                #  for numerical work.
import pandas as pd               #  for data munging.
#      ^for best results, install lxml, and as fallback: bs4 & html5lib.

from . import yi_0sys as system


#  For doctest, Stanley Druckenmiller's "Duquesne Family Office" on 2015-08-14: 
druck150814='http://www.sec.gov/Archives/edgar/data/1536411/000153641115000006/xslForm13F_X01/form13f_20150630.xml'


def parse13f( url=druck150814 ):
     '''Parse SEC form 13F into a pandas dataframe.'''
     #     url should be for so-called Information Table in html/xml format.
     url = url.replace('https://', 'http://')
     #                  https cannot be read by lxml, surprisingly!
     #
     #  Use pandas to read in the xml page...
     #  See http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_html.html
     #  It searches for <table> elements and only for <tr> and <th> rows 
     #  and <td> elements within each <tr> or <th> element in the table.
     page = pd.read_html( url )
     #  page is a list of length 4, but only the 
     #  last element of page interests us which turns out to be a dataframe!
     df = page[-1]
     #
     #  Let's rename columns for our sanity:
     df.columns = [ 'stock', 'class', 'cusip', 'usd', 'size', 'sh_prin', 
          'putcall', 'discret', 'manager', 'vote1', 'vote2', 'vote3' ] 
     #  First three ROWS are SEC labels, not data, so delete them:
     df = df[3:]
     #  reset_index to start from 0 instead of 3,
     #               drop previous 'index', default is to retain:
     df.reset_index( drop=True )
     #
     #      df is the pandas DATAFRAME fully representing a 13F view.
     #         Some columns may need numeric type conversion later.
     return df



def pcent13f( url=druck150814, top=7654321 ):
     '''Prune, then sort SEC 13F by percentage allocation, showing top N.
     >>> pcent13f( top= 7 )
                           stock      cusip     usd putcall  pcent
     27          SPDR Gold Trust  78463V907  323626     NaN  21.81
     15             Facebook Inc  30303M102  160612     NaN  10.82
     29         Wells Fargo & Co  949746101   94449     NaN   6.36
     31  LyondellBasell Ind's NV  N53745100   74219     NaN   5.00
     18           Halliburton Co  406216101   66629     NaN   4.49
     16     Freeport-McMoRan Inc  35671D857   66045     NaN   4.45
     8             Citigroup Inc  172967424   64907     NaN   4.37
     '''
     df = parse13f( url )
     #    Drop irrevelant COLUMNS:
     df.drop( df.columns[[1, 4, 5, 7, 8, 9, 10, 11]], axis=1, inplace=True )
     #                    inplace=True available after pandas 0.13
     #
     #  Convert usd to float type since it was read as string:
     df[['usd']] = df[['usd']].astype( float )
     #                 Gotcha: int as type will fail for NaN !
     #  Also we need float anyways for Python2 division later.
     #
     #  Sort holdings by dollar value:
     dfusd = df.sort_values( by=['usd'], ascending=[False] )
     #         .sort(columns=...) to be deprecated per pandas 0.17.1
     #  Sum total portfolio in USD:
     usdsum = sum( dfusd.usd )
     #
     #  NEW COLUMN 'pcent' for percentage of total portfolio:
     dfusd['pcent'] = np.round(( dfusd.usd / usdsum ) * 100, 2)
     #
     #          Selects top N positions from the portfolio:
     return dfusd.head( top )



if __name__ == "__main__":
     system.endmodule()
