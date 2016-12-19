#  Python Module for import                           Date : 2016-12-18
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_timeseries : Test fecon235 yi_timeseries module.

- Include test of holt() and its workout dataframe. 
- Include test of ema() which is a special case of Holt-Winters.

Doctests display at lower precision since equality test becomes fuzzy across 
different systems if full floating point representation is used.

Testing: As of fecon235 v4, we favor pytest over nosetests, so e.g. 
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
               or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-12-18  First version to verify fix #5 which revises ema():
               https://github.com/rsvp/fecon235/issues/5
'''

from __future__ import absolute_import, print_function

from fecon235.lib import yi_0sys as system
from fecon235.lib import yi_fred as fred
from fecon235.lib import yi_1tools as tools
from fecon235.lib import yi_timeseries as ts
#
#  N.B. -  In this tests directory without __init__.py, 
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


def test_yi_timeseries_fecon235_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [ col for col in df.columns ] == ['Y']
    assert df.shape == (30, 1)
    return df


#  Establish REFERENCE dataframe for tests below:
xau = test_yi_timeseries_fecon235_Read_CSV_file()


def test_yi_timeseries_fecon235_check_xau_DataFrame():
    '''Check xau dataframe.'''
    assert tools.tailvalue( xau ) == 1393.75


def test_yi_timeseries_fecon235_check_workout_dataframe_from_holt():
    '''Get workout dataframe from holt(), then display in low precision.
       Arguments alpha and beta are explicitly set to default values.
    >>> xauholt = ts.holt( xau, alpha=0.26, beta=0.19 )
    >>> xauholt2 = xauholt.round(2)
    >>> xauholt2
                      Y    Level  Growth
    T                                   
    2013-03-08  1581.75  1581.75    0.00
    2013-03-11  1579.00  1581.04   -0.14
    2013-03-12  1594.00  1584.31    0.51
    2013-03-13  1589.25  1585.97    0.73
    2013-03-14  1586.00  1586.52    0.70
    2013-03-15  1595.50  1589.37    1.11
    2013-03-18  1603.75  1593.93    1.76
    2013-03-19  1610.75  1599.60    2.51
    2013-03-20  1607.50  1603.51    2.77
    2013-03-21  1613.75  1608.22    3.14
    2013-03-22  1607.75  1610.42    2.96
    2013-03-25  1599.25  1609.71    2.26
    2013-03-26  1598.00  1608.34    1.57
    2013-03-27  1603.00  1608.12    1.23
    2013-03-28  1598.25  1606.46    0.68
    2013-03-29  1598.25  1604.83    0.24
    2013-04-01  1598.25  1603.30   -0.09
    2013-04-02  1583.50  1598.08   -1.07
    2013-04-03  1574.75  1591.23   -2.17
    2013-04-04  1546.50  1578.00   -4.27
    2013-04-05  1568.00  1572.24   -4.55
    2013-04-08  1575.00  1569.59   -4.19
    2013-04-09  1577.25  1568.48   -3.61
    2013-04-10  1575.00  1567.51   -3.11
    2013-04-11  1565.00  1564.56   -3.08
    2013-04-12  1535.50  1554.73   -4.36
    2013-04-15  1395.00  1509.97  -12.03
    2013-04-16  1380.00  1467.27  -17.86
    2013-04-17  1392.00  1434.49  -20.70
    2013-04-18  1393.75  1408.58  -21.69
    '''
    #  This output can be used to verify the initialization 
    #  and subsequent recursive computation by hand (with precision).
    pass



def test_yi_timeseries_fecon235_check_workout_beta0_from_holt():
    '''Get workout dataframe from holt(), then display in low precision.
       Argument beta=0 esp. for ema() check, where its alpha defaults to 0.20.
    >>> xauholt_b0 = ts.holt( xau, alpha=0.20, beta=0 )
    >>> xauholt2_b0 = xauholt_b0.round(2)
    >>> xauholt2_b0
                      Y    Level  Growth
    T                                   
    2013-03-08  1581.75  1581.75     0.0
    2013-03-11  1579.00  1581.20     0.0
    2013-03-12  1594.00  1583.76     0.0
    2013-03-13  1589.25  1584.86     0.0
    2013-03-14  1586.00  1585.09     0.0
    2013-03-15  1595.50  1587.17     0.0
    2013-03-18  1603.75  1590.49     0.0
    2013-03-19  1610.75  1594.54     0.0
    2013-03-20  1607.50  1597.13     0.0
    2013-03-21  1613.75  1600.45     0.0
    2013-03-22  1607.75  1601.91     0.0
    2013-03-25  1599.25  1601.38     0.0
    2013-03-26  1598.00  1600.70     0.0
    2013-03-27  1603.00  1601.16     0.0
    2013-03-28  1598.25  1600.58     0.0
    2013-03-29  1598.25  1600.11     0.0
    2013-04-01  1598.25  1599.74     0.0
    2013-04-02  1583.50  1596.49     0.0
    2013-04-03  1574.75  1592.14     0.0
    2013-04-04  1546.50  1583.02     0.0
    2013-04-05  1568.00  1580.01     0.0
    2013-04-08  1575.00  1579.01     0.0
    2013-04-09  1577.25  1578.66     0.0
    2013-04-10  1575.00  1577.93     0.0
    2013-04-11  1565.00  1575.34     0.0
    2013-04-12  1535.50  1567.37     0.0
    2013-04-15  1395.00  1532.90     0.0
    2013-04-16  1380.00  1502.32     0.0
    2013-04-17  1392.00  1480.25     0.0
    2013-04-18  1393.75  1462.95     0.0
    '''
    #  This test helped to fix the bug described in #5:
    #  https://github.com/rsvp/fecon235/issues/5
    #  Growth column must be all zeros when beta=0.
    pass



def test_yi_timeseries_fecon235_check_ema():
    '''Function ema() reads off the Level column via holtlevel(), 
       given beta fixed at 0. Its alpha defaults to 0.20.
    >>> xauema = ts.ema( xau, alpha=0.20 )
    >>> xauema2 = xauema.round(2)
    >>> xauema2
                      Y
    T                  
    2013-03-08  1581.75
    2013-03-11  1581.20
    2013-03-12  1583.76
    2013-03-13  1584.86
    2013-03-14  1585.09
    2013-03-15  1587.17
    2013-03-18  1590.49
    2013-03-19  1594.54
    2013-03-20  1597.13
    2013-03-21  1600.45
    2013-03-22  1601.91
    2013-03-25  1601.38
    2013-03-26  1600.70
    2013-03-27  1601.16
    2013-03-28  1600.58
    2013-03-29  1600.11
    2013-04-01  1599.74
    2013-04-02  1596.49
    2013-04-03  1592.14
    2013-04-04  1583.02
    2013-04-05  1580.01
    2013-04-08  1579.01
    2013-04-09  1578.66
    2013-04-10  1577.93
    2013-04-11  1575.34
    2013-04-12  1567.37
    2013-04-15  1532.90
    2013-04-16  1502.32
    2013-04-17  1480.25
    2013-04-18  1462.95
    '''
    #  Our revised exponential moving average function was recently 
    #  written as a special case of our Holt-Winters routines, 
    #  instead of the rolling average function offered by pandas.
    pass



if __name__ == "__main__":
     system.endmodule()
