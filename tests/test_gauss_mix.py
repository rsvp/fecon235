#  Python Module for import                           Date : 2017-06-05
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_gauss_mix : Test fecon235 ys_gauss_mix module.

Assuming testing will occur in tests directory, to locate small data file.

Doctests display at lower precision since equality test becomes fuzzy across 
different systems if full floating point representation is used.

Testing: As of fecon235 v4, we favor pytest over nosetests, so e.g. 
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
               or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-05  Add test for gm2gem().
2017-05-21  Add tests for gemrate() and gemrat(). Note the deprecation of
               gm2_georet() and georet_gm2() due to math proof.
2017-05-19  First version.
'''

from __future__ import absolute_import, print_function

from fecon235.lib import yi_0sys as system
from fecon235.lib import yi_fred as fred
from fecon235.lib import yi_1tools as tools
from fecon235.lib import ys_gauss_mix as gmix
#
#  N.B. -  In this tests directory without __init__.py, 
#          we use absolute import as if outside the fecon235 package,
#          not relative import (cf. modules within lib).


#  #  Show the CSV file zdata-xau-13hj-c30.csv:
#  #                    ^created in Linux environment...
#  #  Warning: last four points may look like outliers, but they are actual.
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


def test_ys_gauss_mix_fecon235_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [ col for col in df.columns ] == ['Y']
    assert df.shape == (30, 1)
    return df


#  Establish REFERENCE dataframe for tests below:
xau = test_ys_gauss_mix_fecon235_Read_CSV_file()


def test_ys_gauss_mix_fecon235_check_xau_DataFrame():
    '''Check xau dataframe.'''
    assert tools.tailvalue( xau ) == 1393.75


def test_ys_gauss_mix_fecon235_check_gm2_strategy_feasible():
    '''Test sympy solving for "a" in Proposition 2 numerically.'''
    a_feasible = round( gmix.gm2_strategy(kurtosis=7, b=2), 4 )
    assert a_feasible == 0.7454


def test_ys_gauss_mix_fecon235_check_gm2_strategy_infeasible():
    '''Destroy sympy solving for "a" in Proposition 2 numerically.'''
    try:
        a_feasible = round( gmix.gm2_strategy(kurtosis=13, b=2), 4 )
        #  INTENTIONAL FAIL: That b is too low for high kurtosis.
        #  Previous test shows feasible when kurtosis=7.
        #  sympy actually fails correctly, and will raise its exception.
    except:
        a_feasible = "Intentionally_FATAL_since_INFEASIBLE"
        #             Avoids reproducing the traceback to assert next:
    assert a_feasible == "Intentionally_FATAL_since_INFEASIBLE"


def test_ys_gauss_mix_fecon235_check_gm2_vols():
    '''Check the annualized version of gm2_vols_fit() on test data.'''
    xauvols = gmix.gm2_vols( xau[:'2013-04-12'], b=2.5, yearly=256 )
    #                            ^else severe drop in price for small sample.
    mu, sigma1, sigma2, q, k_Pearson, sigma, b, yearly, N = xauvols
    assert round(mu, 4) == -30.3880       # mu annualized
    assert round(sigma1, 4) == 11.1829    # sigma1 annualized
    assert round(sigma2, 4) == 28.7713    # sigma2 annualized
    assert round(q, 4) == 0.0105          # q
    assert round(k_Pearson, 4) == 3.8787  # kurtosis
    assert round(sigma, 4) == 11.5085     # sigma
    assert b == 2.5                       # b
    assert yearly == 256                  # yearly
    assert N == 25                        # N, sample size


def test_ys_gauss_mix_fecon235_check_gemrate():
    '''Check on geometric mean rate gemrate() based on gemreturn_Jean().'''
    assert 0.05 - ((0.20*0.20)/2.) == 0.03
    #           ^most well-known approx. for mu=0.05 and sigma=0.20
    assert round(gmix.gemrate(0.05, 0.20, kurtosis=3, yearly=1),  7) == 0.0301066
    #      Jean (1983) adds just 1 bp for Gaussian over usual approximation.
    assert round(gmix.gemrate(0.05, 0.20, kurtosis=13, yearly=1), 7) == 0.0267223
    #      So increase in kurtosis lowered geometric mean rate by 34 bp.
    assert round(gmix.gemrate(0.05, 0.20, kurtosis=3, yearly=10), 7) == 0.3453084
    #      OK, compounding works as intended.


def test_ys_gauss_mix_fecon235_check_gemrat():
    '''Check on geometric mean rate of data, gemrat() in percentage form.'''
    xaugem = gmix.gemrat( xau[:'2013-04-12'], yearly=256 )
    #                         ^else severe drop in price for small sample.
    grate, mu, sigma, k_Pearson, yearly, N  = xaugem
    assert round(grate, 4) == -31.3826    # gemrat annualized
    assert round(mu, 4) == -30.388        # arithmetic mean annualized
    assert round(sigma, 4) == 11.5085     # sigma
    assert round(k_Pearson, 4) == 3.8787  # kurtosis
    assert yearly == 256                  # yearly
    assert N == 25                        # N, sample size


def test_ys_gauss_mix_fecon235_check_gm2gem():
    '''Check on geometric mean rate of data and GM(2) model: print gm2gemrat().
    >>> gmix.gm2gem( xau[:'2013-04-12'], yearly=256, b=2.5, pc=True, n=4 )
    Geometric  mean rate: -31.3826
    Arithmetic mean rate: -30.388
    sigma: 11.5085
    kurtosis (Pearson): 3.8787
    GM(2), sigma1: 11.1829
    GM(2), sigma2: 28.7713
    GM(2), q:  0.0105
    GM(2), b:  2.5
    yearly: 256
    N: 25
    '''
    pass


if __name__ == "__main__":
     system.endmodule()
