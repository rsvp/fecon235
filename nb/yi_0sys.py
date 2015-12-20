#  Python Module for import                           Date : 2015-12-19
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_0sys.py : system and date functions including specs.

Code in this module must be compatible with both Python 2 and 3.
It is a bridge and a guardian between the two Pythons.

For example, it is used in the preamble of fecon235 Jupyter notebooks.


REFERENCES:
- Compatible IDIOMS: http://python-future.org/compatible_idioms.html
                     Nice presentation.

- SIX module is exhaustive: https://pythonhosted.org/six/
        Single file source: https://bitbucket.org/gutworth/six


CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-12-19  python3 compatible: absolute_import
2015-12-03  First version.
'''

from __future__ import absolute_import, print_function
#    __future__ for Python 2 and 3 compatibility; must be first in file.
import sys
import os
import time

minimumPython = ( 2, 7, 0 )
#             ... else a warning is generated in specs().


def getpwd():
    '''Get present working directory (Linux command is pwd).
       Works cross-platform, giving absolute path.
    '''
    return os.getcwd()


def program():
    '''Get name of present script; works cross-platform.'''
    #  Note: __file__ can get only the name of this module.
    return os.path.basename(sys.argv[0])


def warn( message, stub="WARNING:", prefix=" !. "):
    '''Write warning solely to standard error.'''
    print(prefix, stub, program(), message, sep=' ', file=sys.stderr)


def die( message, errcode=1, prefix=" !! "):
    '''Gracefully KILL script, optionally specifying error code.'''
    stub = "FATAL " + str(errcode) + ":"
    warn( message, stub, prefix )
    sys.exit( errcode )
    #         ^interpretation is system dependent;
    #          generally non-zero is considered as some error.
    #  Note: "os._exit" exits without calling cleanup handlers, 
    #  flushing stdio buffers, etc. Thus, it is not a standard way.


def date( hour=True, utc=True, localstr=' Local' ):
    '''Get date, and optionally time, as ISO string representation.
       Boolean hour variable also gives minutes and seconds.
       Setting utc to False will give local time instead of UTC,
       then localstr can be used to indicate location.
    '''
    if hour:
        form = "%Y-%m-%d, %H:%M:%S"
    else:
        form = "%Y-%m-%d"
    if utc:
        form += ' UTC'
        tup = time.gmtime()
    else:
        form += localstr
        tup = time.localtime()
    return time.strftime( form, tup ) 


def pythontup():
    '''Represent invoked Python version as an integer 3-tuple.'''
    #  Using sys.version is overly verbose.
    #  Here we get something like (2, 7, 10) which can be compared.
    return sys.version_info[:3]


def versionstr( module="IPython" ):
    '''Represent version as a string, or None if not installed.'''
    #  Unfortunately must treat Python vs its modules differently...
    if module=="Python" or module=="python":
        ver = pythontup()
        return str(ver[0]) + '.' + str(ver[1]) + '.' + str(ver[2])   
    else: 
        try:
            exec( "import " + module )
            exec( "vermod = " + module + ".__version__" )
            return vermod
        except:
            return None


def versiontup( module="IPython" ):
    '''Parse version string into some integer 3-tuple.'''
    s = versionstr(module)
    try:
        v = [ int(k) for k in s.split('.') ]
        return tuple(v)
    except:
        #  e.g. if not installed or not convertible to integers...
        if s == None:
            return ( 0,  0,  0)
        else:
            return (-9, -9, -9)


def version( module="IPython" ):
    '''Pretty print Python or module version info.'''
    print(" :: ", module, versionstr(module))


def specs():
    '''Show ecosystem specifications, including execution date.'''
    print(" ::  Timestamp:", date(hour=True, utc=True))
    #  APIs are subject to change, so versions are critical for debugging:
    version("Python")
    if pythontup() < minimumPython:
        warn("may need newer Python version.")
    version("IPython")
    version("notebook")
    #       ^worked for Jupyter notebook 4.0.6
    version("matplotlib")
    version("numpy")
    #       ^dependency for pandas
    version("pandas")
    version("pandas_datareader")
    #       ^but package is "pandas-datareader" esp. for financial quotes. 


if pythontup() < (3, 0, 0):
    '''ROSETTA STONE FUNCTIONS approximately bridging Python 2 and 3.
    e.g.       answer = get_input("Favorite animal? ")
               print(answer)
    '''
    get_input = raw_input
else:
    get_input = input
    #           ^beware of untrustworthy arguments!


def endmodule():
    '''Procedure after __main__ conditional in modules.'''
    die("is a MODULE for import, not for direct execution.", 113)


if __name__ == "__main__":
    endmodule()



'''
_______________ Appendix 1: PREAMBLE for Jupyter NOTEBOOKS
                            First input cell for settings and system details:


#  NOTEBOOK v4 SETTINGS and system details:      [00-tpl v5.15.1203]
from __future__ import print_function
#    Strive for compatibility between Python 2, 3, Jupyter, 
#    and being cross-platform (our backend is LINUX running bash shell). 
import yi_0sys      ; yi_0sys.specs()
import pandas as pd
#  If a module is modified, automatically reload it:
%load_ext autoreload
%autoreload 2
#       Use 0 to disable this feature.
pwd = yi_0sys.getpwd()    # present working directory as variable.
print(" ::  $pwd:", pwd)

#  Notebook DISPLAY options:
#      Represent pandas DataFrames as text; not HTML representation:
pd.set_option( 'display.notebook_repr_html', False )
#  Beware, for MATH display, use %%latex, NOT the following:
#                   from IPython.display import Math
#                   from IPython.display import Latex
from IPython.display import HTML # useful for snippets
#  e.g. HTML('<iframe src=http://en.mobile.wikipedia.org/?useformat=mobile width=700 height=350></iframe>')
from IPython.display import Image 
#  e.g. Image(filename='holt-winters-equations.png', embed=True) # url= also works
from IPython.display import YouTubeVideo
#  e.g. YouTubeVideo('1j_HxD4iLn8', start='43', width=600, height=400)
from IPython.core import page
get_ipython().set_hook('show_in_pager', page.as_hook(page.display_page), 0)
#  Or equivalently in config file: "InteractiveShell.display_page = True", 
#  which will display results in secondary notebook pager frame in a cell.

#  Generate PLOTS inside notebook, "inline" generates static png:
%matplotlib inline   
#          "notebook" argument allows interactive zoom and resize.


'''

