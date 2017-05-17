#  Python Module for import                           Date : 2017-05-16
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_gauss_mix.py : Gaussian mixture for fecon235

- Refactor code for structured zero-mean GM(2),
     see nb/gauss-mix-kurtosis.ipynb for details

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-05-16  Add gm2_vols_fit(), gm2_vols(), and gm2_georet()
               which fit financial volatilities using GM(2) model.
               Fix gm2_strategy() when infeasible solution occurs.
2017-05-09  First version, add doctests.
'''

from __future__ import absolute_import, print_function, division

import sympy as sym
import numpy as np
from fecon235.lib import yi_0sys as system
from . import yi_1tools as tools

'''
STRUCTURED zero-mean GM(2), nb/gauss-mix-kurtosis.ipynb

Given data set {$x$}, we can compute its variance and kurtosis.
Thus, $\sigma$ and $\rm K$ are observable.
Corollary 1.2 says that GM(2) parameters can indeed synthesize $\rm K$,
but its messiness suggests that we impose further structure for clarity.
A sensible requirement is a strict ordering,
$\sigma_1 < \sigma < \sigma_2$
in consideration of the weighted equation for $\sigma^2$.
We can impose this ordering by constrained constants $a$ and $b$.

PROPOSITION 2: Let $\sigma_1 = a\sigma$ and $b\sigma = \sigma_2$
such that $0<a<1<b$, then for zero-mean GM(2)
the following satisfies conditions for both kurtosis and variance:

$$\frac{\rm K - b^4}{a^4 - b^4} = \frac{1 - b^2}{a^2 - b^2}$$

This shows how constants $a$ and $b$ are jointly constrained
by the moments of the Gaussian mixture.

Our STRATEGY will be to choose $b>1$, then use the kurtosis $\kappa$
to compute $a$. Probability $p$ can then be computed using
Lemma 2.2, for which $q=1-p$ follows.
Since $\sigma_1 = a\sigma$ and $b\sigma = \sigma_2$
the components of our zero-mean GM(2) are fully resolved,
given specific $\sigma$.

From two observable statistics $\sigma$ and $\kappa$,
we have deduced, not fitted, the parameters of a zero-mean GM(2).
An observable mean $\mu$ which is non-zero can be added to
our model to obtain a zero-skew GM(2).
'''


def gm2_strategy(kurtosis, b=2):
    '''Use sympy to solve for "a" in Proposition 2 numerically.
    >>> round( gm2_strategy(7, 2), 4 )
    0.7454
    '''
    #  sym.init_printing(use_unicode=True)
    #  #        ^required if symbolic output is desired.
    a = sym.symbols('a')
    K = kurtosis / 3.0
    #  Use equation from Prop. 2
    LHS = (K - (b**4)) / ((a**4) - (b**4))
    RHS = (1 - (b**2)) / ((a**2) - (b**2))
    a_solved = sym.solveset( sym.Eq(LHS, RHS), a, domain=sym.S.Reals )
    #  ... expect negative and positve real solutions
    #      provided in sympy's FiniteSet format.
    if a_solved == sym.S.EmptySet:
        #               ^when no feasible solution was found in domain.
        #                Do not accept imaginary solutions :-)
        system.die("Argument b could not treat kurtosis; INCREASE b.")
        #     ^dies when kurtosis > 12 and b=2, for example.
        #           SPX returns since 1957 have kurtosis around 31.6
        #           which is very high, requiring b>3.4 for feasiblity.
    else:
        #  But a>0 by construction, so extract the positive real number:
        a_positive = max(list(a_solved))
    return a_positive


def gm2_main(kurtosis, sigma, b=2):
    '''Compute specs for GM(2) given observable statistics and b.'''
    a = gm2_strategy(kurtosis, b)
    #  Probability p as given in Lemma 2.2:
    p = (1 - (b**2)) / ((a**2) - (b**2))
    #   The returned parameters can then be used in simulations, 
    #   e.g. simug_mix() in lib/yi_simulation.py module,
    #   or for synthetic assets in risk management:
    return [[a, b], [p, a*sigma], [1-p, b*sigma]]


def gm2_print(kurtosis, sigma, b=2):
    '''Print specs for GM(2) given observable statistics and b.'''
    specs = gm2_main(kurtosis, sigma, b)
    print("Constants a, b:", specs[0])
    print("GM(2), p: ", specs[1][0])
    print("GM(2), sigma1:", specs[1][1])
    print("GM(2), q: ", specs[2][0])
    print("GM(2), sigma2:", specs[2][1])


#======================================================== APPLICATIONS ========


def gm2_vols_fit(data, b=2.5):
    '''Estimate GM(2) VOLATILITY parameters including mu, given b.'''
    #  Our data is presumed to be prices of some financial asset.
    ret = tools.diflog( data, lags=1 )
    #          ^First difference of log(data).
    arr = tools.df2a( ret )

    #  Routine stat calculations on our array:
    N = len(arr)
    mu = np.mean(arr)
    sigma = np.std(arr)
    k_Pearson = (sum((arr - mu)**4)/N) / sigma**4
    #  For kurtosis details, see our kurtfun().

    specs = gm2_main( k_Pearson, sigma, b )
    #       [[a, b], [p, a*sigma], [1-p, b*sigma]]
    sigma1 = specs[1][1]
    sigma2 = specs[2][1]
    q = specs[2][0]
    return [ mu, sigma1, sigma2, q, k_Pearson, sigma, b, N ]


def gm2_vols(data, b=2.5, yearly=256):
    '''Compute GM(2) ANNUALIZED VOLATILITY in percentage form, given b.'''
    #  Our data is presumed to be prices of some financial asset.
    #  Argument yearly expresses frequency of data, default is business daily.
    mu, sigma1, sigma2, q, k_Pearson, sigma, b, N = gm2_vols_fit( data, b )
    #  ANNUALIZE appropriately in "percentage" form...
    yc  = 100 * yearly
    ysr = 100 * np.sqrt(yearly)
    #  ... the mean return mu is still arithmetic, not geometric:
    return [ mu*yc, sigma1*ysr, sigma2*ysr, q, 
             k_Pearson, sigma*ysr, b, yearly, N ]

    #  2017-05-16  Outputs given SPX, informally minimizing b until fatal:
    #
    #  >>> gm2_vols(spx['1957':], b=3.4)
    #  [6.4231, 4.878, 52.8776, 0.07866443, 31.5634, 15.5522, 3.4, 256, 15748]
    #
    #  >>> gm2_vols(spx['1997':], b=2.0)
    #  [5.6690, 5.8802435, 38.5585, 0.23214208, 11.1628, 19.2793, 2.0, 256, 5313]
    #  
    #  >>> gm2_vols(spx['2007':], b=2.2)
    #  [4.9873, 5.1699, 44.8882, 0.195946, 13.7804, 20.4037, 2.2, 256, 2705]
    #
    #  So one might suppose a typical set of outputs would look like:
    #      Annualized mean return:  5.69% 
    #           Annualized sigma1:  5.30938 
    #           Annualized sigma2: 45.44142
    #          Probability sigma2:  0.1689 
    #                    kurtosis: 18.8355 
    #            Annualized sigma: 18.411734
    #                where b around 2.533 might work, but not always.
    #
    #  Our sigma2 guess is interesting since "double or nothing"
    #  is just 2.2 standard deviations away. The probability of
    #  drawing from the second Gaussian with the higher volatility 
    #  of 45% is about 0.17. The compensation for such risks taken
    #  is the annual mean return of 5.7%, plus dividends collected.


def gm2_georet(data, b=2.5, yearly=256):
    '''Compute annualized GEOMETRIC mean return from GM(2) volatility fit.'''
    #  Our data is presumed to be prices of some financial asset.
    #  Argument yearly expresses frequency of data, default is business daily.
    mu, sigma1, sigma2, q, k_Pearson, sigma, b, N = gm2_vols_fit( data, b )
    var1 = sigma1 * sigma1 * yearly
    var2 = sigma2 * sigma2 * yearly
    geor1 = (mu*yearly) - (var1 / 2.0)
    geor2 = (mu*yearly) - (var2 / 2.0)
    #       Note that geor2 can be negative if var2 is large.
    geor  = ((1-q)*geor1) + (q*geor2)
    #     ^[ ] - TODO: prove this equality.
    #  ANNUALIZE appropriately in "percentage" form...
    ysr = 100 * np.sqrt(yearly)
    geor = 100 * geor
    return [ geor, sigma1*ysr, sigma2*ysr, q, 
             k_Pearson, sigma*ysr, b, yearly, N ]


if __name__ == "__main__":
     system.endmodule()
