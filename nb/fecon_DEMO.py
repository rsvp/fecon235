#  Python Module for import                           Date : 2015-09-04
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  fecon_DEMO : Test, while demonstrating, the fecon module.

IPython notebooks are indirectly integration tests in the interactive mode. 
However, non-interactive testing is desirable for the developer.
Also, demonstration for the casual user is needed. Thus this module.

This module has code snippets to be read, and then employed as follows:

    $ nosetests --with-doctest   # Better from tests directory: ./nose

We prefer doctest over the use of assert (with ==) in nose test functions 
due to its ease and readability of ascertaining dataframe output.

If nose is not installed, then this will work as fallback:

    $ python -m doctest fecon_DEMO.py   # exit 0 indicates tests passed.

Reference:
NOSETESTS: http://nose.readthedocs.org/en/latest/usage.html

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-09-04  Add demo for forecast().
2015-09-02  First version for get().
'''


from fecon import *
#    ^in one line we get essential functions from the yi_* modules.


def demo_GET_d4xau_from_FRED():
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



def demo_GET_w4cotr_metals_from_QUANDL():
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



def demo_FORECAST_m4xau_from_FRED():
    '''Test forecast() in fecon which uses Holt-Winters method.
       We use monthly gold data, and type forecast as integers 
       to avoid doctest with floats (almost equal problem).

    >>> xau = get( m4xau )
    >>> xaufc = forecast( xau['2005-07-28':'2015-07-28'], h=6 )
    >>> xaufc.astype('int')
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



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
