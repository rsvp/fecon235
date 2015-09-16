#  Python Module for import                           Date : 2015-09-14
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  fecon : gathers yi_* modules for fecon235 project.

- Designed to be dropped into an IPython notebook for CONVENIENT commands. 
- User can always foo?? to access foo's orgin.
- This is meant to unify modules in one place.
- Frequently used commands can thus be generalized with shorter names.
- Detailed code development does not belong here.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-09-14  Add getstock and second argument maxi to get().
2015-09-03  Exception handling.
2015-08-31  First version unifies some commands.

TODO
[ ] - adopt Bloomberg Open Symbology for obscure financial instruments, 
         see http://bsym.bloomberg.com/sym/
         Bloomberg Global ID is a random 12-character alpha-numeric.
'''

#    Very lenient import style designed for notebooks.
#    We access modules which are primary, and 
#    catch collisions in namespace:
from yi_1tools import *
from yi_fred import *
from yi_plot import *
from yi_simulation import *
from yi_stocks import *
from yi_timeseries import *
from yi_quandl import *
#    yi_quandl_api should NOT be imported.


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



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
