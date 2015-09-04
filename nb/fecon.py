#  Python Module for import                           Date : 2015-09-03
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  fecon : gathers yi_* modules for fecon235 project.

- Designed to be dropped into a notebook for CONVENIENT commands. 
- This is meant to unify modules in one place.
- Frequently used commands can thus be generalized with shorter names.
- Detailed code development does not belong here.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-09-03  Exception handling.
2015-08-31  First version unifies some commands.
'''

#    Very lenient import style designed for notebook inputs, 
#    accesses modules which are important.
#    User can always foo?? to access foo's orgin.
#    Try to catch collisions in namespace:
from yi_1tools import *
from yi_fred import *
from yi_plot import *
from yi_simulation import *
from yi_timeseries import *
from yi_quandl import *
#    yi_quandl_api should NOT be imported.


def get( code ):
    '''Unifies getfred and getqdl for data retrieval.'''
    try:
        df = getfred( code )
    except:
        try:
            df = getqdl(  code )
        except:
            raise ValueError('INVALID symbol string or code for fecon.get()')
    return df


def plot( data, title='tmp', maxi=87654321 ):
    '''Unifies plotfred and plotqdl for plotting data.'''
    #  data could also be fredcode or quandlcode.
    try:
        plotfred( data, title, maxi )
    except:
        try:
            plotqdl(  data, title, maxi )
        except:
            raise ValueError('INVALID argument or data for fecon.plot()')
    return


def forecast( data, h=12 ):
    '''Unifies holtfred and holtqdl for forecasting.'''
    #  Using the defaults: alpha=ts.hw_alpha and beta=ts.hw_beta
    #  data could also be fredcode or quandlcode.
    try:
        df = holtfred( data, h )
    except:
        try:
            df = holtqdl(  data, h )
        except:
            raise ValueError('INVALID argument or data for fecon.forecast()')
    return df



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
