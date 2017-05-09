#  Python Module for import                           Date : 2017-05-09
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_gauss_mix.py : Gaussian mixture for fecon235

- Refactor code for structured zero-mean GM(2),
     see nb/gauss-mix-kurtosis.ipynb for details

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-05-09  First version, add doctests.
'''

from __future__ import absolute_import, print_function, division

import sympy as sym
from fecon235.lib import yi_0sys as system

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
    #  But a>0 by construction, so extract the positive real number:
    return max(list(a_solved))


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
    print("GM(2), sigma_1:", specs[1][1])
    print("GM(2), q: ", specs[2][0])
    print("GM(2), sigma_2:", specs[2][1])


if __name__ == "__main__":
     system.endmodule()
