#  Python Module for import                           Date : 2015-12-20
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
     system.endmodule()
