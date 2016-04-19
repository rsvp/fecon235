#  Python Module for import                           Date : 2016-04-18
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_1tools : Test fecon235 yi_1tools module.

Using a CSV file offline, we construct and test two dataframes:
xau and foo, then paste(), and finally test lagdf().


Testing: As of fecon235 v4, we favor pytest over nosetests, so e.g. 
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
               or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-04-18  First version tests lagdf().
'''

from __future__ import absolute_import, print_function

import pandas as pd
from fecon235.lib import yi_0sys as system
from fecon235.lib import yi_fred as fred
from fecon235.lib import yi_1tools as tools
#
#  N.B. -  in this tests directory without __init__.py, 
#          we use absolute import as if outside the fecon235 package,
#          not relative import (cf. modules within lib).

#  #  Show the CSV file zdata-xau-13hj-c30.csv:
#  #                    ^created in Linux environment...
#  
#       T,XAU
#       2013-03-08,1581.75
#       2013-03-11,1579.0
#       2013-03-12,1594.0
#       2013-03-13,1589.25
#       2013-03-14,1586.0
#       2013-03-15,1595.5
#       2013-03-18,1603.75
#       2013-03-19,1610.75
#       2013-03-20,1607.5
#       2013-03-21,1613.75
#       2013-03-22,1607.75
#       2013-03-25,1599.25
#       2013-03-26,1598.0
#       2013-03-27,1603.0
#       2013-03-28,1598.25
#       2013-03-29,1598.25
#       2013-04-01,1598.25
#       2013-04-02,1583.5
#       2013-04-03,1574.75
#       2013-04-04,1546.5
#       2013-04-05,1568.0
#       2013-04-08,1575.0
#       2013-04-09,1577.25
#       2013-04-10,1575.0
#       2013-04-11,1565.0
#       2013-04-12,1535.5
#       2013-04-15,1395.0
#       2013-04-16,1380.0
#       2013-04-17,1392.0
#       2013-04-18,1393.75


def test_yi_1tools_fecon235_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [ col for col in df.columns ] == ['Y']
    assert df.shape == (30, 1)
    return df


xau = test_yi_1tools_fecon235_Read_CSV_file()
xau = tools.todf( xau, 'XAU' )
#           todf used to rename column.


def test_yi_1tools_fecon235_check_xau_DataFrame():
    '''Check xau dataframe.'''
    assert [ col for col in xau.columns ] == ['XAU']
    assert tools.tailvalue( xau ) == 1393.75


foo = tools.todf( xau + 5000.00, 'FOO' )


def test_yi_1tools_fecon235_check_foo_DataFrame():
    '''Check foo dataframe which is just xau + 5000.00 increase.'''
    assert [ col for col in foo.columns ] == ['FOO']
    assert tools.tailvalue( foo ) == 6393.75


xaufoo = tools.paste([ xau, foo ])


def test_yi_1tools_fecon235_paste_function():
    '''Test xau and foo pasted together as xaufoo dataframe.'''
    assert [ col for col in xaufoo.columns ] == ['XAU', 'FOO']
    assert xaufoo.shape == (30, 2)
    assert tools.tailvalue( xaufoo, pos=0 ) == 1393.75
    assert tools.tailvalue( xaufoo, pos=1 ) == 6393.75
    assert xaufoo.index[0]  == pd.Timestamp('2013-03-08 00:00:00')
    assert xaufoo.index[-1] == pd.Timestamp('2013-04-18 00:00:00')
    #                             Timestamp is yet another pandas type.
    #                             Default time is midnight.


xaufoolag = tools.lagdf( xaufoo, lags=3 )


def test_yi_1tools_fecon235_lagdf_function():
    '''Test xaufoolag dataframe created by lagdf on xaufoo with lags=3.'''
    assert [ col for col in xaufoolag.columns ] == [ 'XAU_0', 'FOO_0',
             'XAU_1', 'FOO_1', 'XAU_2', 'FOO_2', 'XAU_3', 'FOO_3' ]
             #  Number after underscore indicates lag.
    assert xaufoolag.shape == (27, 8)
    #                lags will introduce NaN, which are then dropped,
    #                so rows are reduced from 30 to 27.


    #  Making sure LAGGED VALUES are correctly placed...
    assert tools.tailvalue( xaufoolag, pos=0, row=1 ) == 1393.75
    assert tools.tailvalue( xaufoolag, pos=1, row=1 ) == 6393.75
    assert tools.tailvalue( xaufoolag, pos=2, row=1 ) == 1392.0
    assert tools.tailvalue( xaufoolag, pos=3, row=1 ) == 6392.0
    assert tools.tailvalue( xaufoolag, pos=4, row=1 ) == 1380.0
    assert tools.tailvalue( xaufoolag, pos=5, row=1 ) == 6380.0
    assert tools.tailvalue( xaufoolag, pos=6, row=1 ) == 1395.0
    assert tools.tailvalue( xaufoolag, pos=7, row=1 ) == 6395.0

    assert tools.tailvalue( xaufoolag, pos=0, row=2 ) == 1392.0
    assert tools.tailvalue( xaufoolag, pos=1, row=2 ) == 6392.0
    assert tools.tailvalue( xaufoolag, pos=2, row=2 ) == 1380.0
    assert tools.tailvalue( xaufoolag, pos=3, row=2 ) == 6380.0
    assert tools.tailvalue( xaufoolag, pos=4, row=2 ) == 1395.0
    assert tools.tailvalue( xaufoolag, pos=5, row=2 ) == 6395.0

    assert tools.tailvalue( xaufoolag, pos=0, row=3 ) == 1380.0
    assert tools.tailvalue( xaufoolag, pos=1, row=3 ) == 6380.0
    assert tools.tailvalue( xaufoolag, pos=2, row=3 ) == 1395.0
    assert tools.tailvalue( xaufoolag, pos=3, row=3 ) == 6395.0

    assert tools.tailvalue( xaufoolag, pos=0, row=4 ) == 1395.0
    assert tools.tailvalue( xaufoolag, pos=1, row=4 ) == 6395.0

    assert xaufoolag.index[0]  == pd.Timestamp('2013-03-13 00:00:00')
    assert xaufoolag.index[-1] == pd.Timestamp('2013-04-18 00:00:00')
    #                             Timestamp is yet another pandas type.
    #                             Default time is midnight.



if __name__ == "__main__":
     system.endmodule()
