#  Python Module for import                           Date : 2018-03-10
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_fecon235 : Test and demonstrate fecon235 module.

Jupyter notebooks are indirectly integration tests in the interactive mode. 
However, non-interactive testing is desirable for the developer.
Also, demonstration for the casual user is needed. Thus this module.

This module has code snippets to be read, and then employed as follows:

    $ nosetests --with-doctest   # Better from our tests directory: ./smell

We prefer doctest over the use of assert (with ==) in nose test functions 
due to its ease and readability of ascertaining dataframe output.

If nose is not installed, then this will work as fallback:

    $ python -m doctest fecon_DEMO.py   # exit 0 indicates tests passed.

=>  As of fecon235 v4, we also favor pytest over nosetests, so e.g. 

    $ py.test --doctest-modules [optional dir/file argument]

REFERENCE:
    nosetests: http://nose.readthedocs.org/en/latest/usage.html
    pytest:    https://pytest.org/latest/getting-started.html
                  or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2018-03-10  Add demo for foreholt(). Test forecast() with grids=25.
2015-12-21  python3 compatible: lib import fix.
               Mark very slow tests with "vSlow" suffix, so
               $ py.test -k 'not vSlow'  # Excludes such tests.
2015-12-17  python3 compatible: fix with yi_0sys
2015-09-04  Add demo for forecast().
2015-09-02  First version for get().
'''

from __future__ import absolute_import, print_function

from fecon235.fecon235 import *
#    ^in one line we get essential functions from the yi_* modules,
#     including yi_0sys as system.
#
#  N.B. -  in this tests directory without __init__.py, 
#          we use absolute import as if outside the fecon235 package,
#          not relative import (cf. modules within lib).


def demo_GET_d4xau_from_FRED_vSlow():
    '''Test get() in fecon which uses getfred() in yi_fred module.
       Here we get gold quotes from the FRED database.

    >>> xau = get( d4xau )
    >>> xau['2015-07-21':'2015-07-28']
                     Y
    T                 
    2015-07-21  1105.6
    2015-07-22  1088.6
    2015-07-23  1097.4
    2015-07-24  1080.8
    2015-07-27  1100.0
    2015-07-28  1096.2
    '''
    pass



def demo_GET_w4cotr_metals_from_QUANDL_vSlow():
    '''Test get() in fecon which uses getqdl() in yi_quandl module.
       Thus it is an indirect test of yi_quandl_api module.
       Here we get the CFTC Commitment of Traders Reports 
       for gold and silver expressed as our position indicator.

    >>> metals = get( w4cotr_metals )
    >>> metals['2015-07-21':'2015-07-28']
                       Y
    Date                
    2015-07-21  0.458814
    2015-07-28  0.461077
    '''
    pass



def demo_FORECAST_m4xau_from_FRED_vSlow():
    '''Test forecast() in fecon which uses Holt-Winters method.
       Values for alpha and beta are somewhat optimized by moderate grids:
           alpha, beta, losspc, loss: [0.9167, 0.125, 2.486, 28.45]
       We use monthly gold data, and type forecast as integers 
       to avoid doctest with floats (almost equal problem).

    >>> xau = get( m4xau )
    >>> xaufc = forecast( xau['2005-07-28':'2015-07-28'], h=6, grids=25 )
    >>> xaufc.astype('int')
       Forecast
    0      1144
    1      1135
    2      1123
    3      1112
    4      1100
    5      1089
    6      1078
    '''
    pass



def demo_foreholt_m4xau_from_FRED_vSlow():
    '''Test foreholt() in fecon235 which uses Holt-Winters method.
       Default values for alpha and beta are assumed.
       We use monthly gold data, and type forecast as integers 
       to avoid doctest with floats (almost equal problem).

    >>> xau = get( m4xau )
    >>> xaufh = foreholt( xau['2005-07-28':'2015-07-28'], h=6 )
    >>> xaufh.astype('int')
       Forecast
    0      1144
    1      1161
    2      1154
    3      1146
    4      1138
    5      1130
    6      1122
    '''
    pass



def demo_groupgeoret_test_georet_Geometric_Mean_vSlow():
    '''Test groupget, followed by groupgeoret which depends on georet.
       First create a group dictionary, then retrieve...

    >>> fxdic = { 'EURUSD' : d4eurusd, 'USDJPY' : d4usdjpy }
    >>> fxdf = groupget( fxdic )
    >>> groupgeoret( fxdf['2010':'2015'], 256 )
    [[4.19, 4.63, 9.3, 256, 1565, '2010-01-01', '2015-12-31', 'USDJPY'], [-4.54, -4.08, 9.64, 256, 1565, '2010-01-01', '2015-12-31', 'EURUSD']]
    '''
    pass



if __name__ == "__main__":
     system.endmodule()
