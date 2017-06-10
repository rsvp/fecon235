#  Python Module for import                           Date : 2017-06-09
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_mlearn.py : Machine learning tools

- softmax() for cross-entropy, MLE, neural networks, Boltzmann portfolio.
  softmax_sort() for ordering and filtering info on the probabilities.


REFERENCES
- David J.C. MacKay (2008), Information theory, Inference, and Learning
     Algorithms, 7th printing from Cambridge U. Press.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-09  Revise tau dependence on arrstable mean, not second max.
2017-06-07  Add softmax_sort() with filter and renormalization.
2017-06-06  First fecon235 version.
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from operator import itemgetter
from . import yi_1tools as tools


def softmax( it, temp=55, n=4 ):
    '''Softmax probabilities for iterable where temp sets temperature tau.
       Temperature tau is set as a temp percent of ensemble mean so that
       the scaling of tau works well across many different scenarios.
       Experiment with temp around 40 to 70; higher temp (100+)
       will make it-scores more equi-probable, whereas probabilities
       can be sharpened by decreasing temp towards 1.
       Setting temp to 0 results in generic softmax without temperature.
       Results are rounded to n decimal places.
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=200, n=4 )
    [0, 16, 0.2598, 200, [0.2598, 0.2001, 0.1757, 0.1542, 0.1188, 0.0915]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=50, n=4 )
    [0, 16, 0.5733, 50, [0.5733, 0.2019, 0.1198, 0.0711, 0.0251, 0.0088]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=30, n=4 )
    [0, 16, 0.7773, 30, [0.7773, 0.1365, 0.0572, 0.024, 0.0042, 0.0007]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=1, n=4 )
    [0, 16, 1.0, 1, [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=0, n=4 )
    [0, 16, 0.9997, 0, [0.9997, 0.0003, 0.0, 0.0, 0.0, 0.0]]
    >>> softmax( [ 16, 16 ], temp=200, n=4 )
    [0, 16, 0.5, 200, [0.5, 0.5]]
    >>> softmax( [ 16, 15, -8 ], temp=50, n=4 )
    [0, 16, 0.5587, 50, [0.5587, 0.4395, 0.0018]]
    '''
    #  Reference: https://compute.quora.com/What-is-softmax
    #  Convert iterable to numpy array, then find index of its maximum value:
    arr = tools.toar( it )
    idmax = np.argmax( arr )
    hardmax = arr[idmax]
    #  Without loss of generality for mathematically defined softmax,
    #  subtracting an arbitrary constant from each it-element
    #  always helps NUMERICAL STABILITY, so let it be hardmax:
    arrstable = arr - hardmax
        #  Important to note arrstable will consist of maximum(s) represented
        #  by zero, and all other values will be necessarily negative.
    if temp > 0:
        avg = np.mean(arrstable)
        if avg:
            tau = abs( avg * (temp/100.0) )
            #  Let temperature be POSITIVE and temp percent of ensemble mean.
        else:
            #  Edge case: avg will be zero if it-scores are all equal,
            #  which implies they are equi-probable, so any tau should do,
            #  but tau must be NON-ZERO to avoid division error next.
            tau = 1.0
    else:
        #  Whenever temp is set to 0, False, or None => GENERIC softmax.
        #  Also negative temp will be treated as generic softmax.
        temp = 0   # Prefer the numerical eqivalent for return below.
        tau = 1.0
    #  MATHEMATICALLY, (Boltzmann) softmax is defined as follows:
    expit = np.exp( arrstable / tau )
    sum_expit = np.sum( expit )
    softmax_exact = expit / sum_expit
    #                      roundit will output a list, not an array:
    softmax_approx = tools.roundit( softmax_exact, n, echo=False )
    hardprob = softmax_approx[idmax]
    return [ idmax, hardmax, hardprob, temp, softmax_approx ]


    #      __________ SOFTMAX USAGE NOTES
    #      softmax_sort() is obviously slower to compute than softmax().
    #      They serve different purposes, for example,
    #      softmax()[-1][i] can track a particular i-th class of it, whereas
    #      softmax_sort()[:3] will give information on the top 3 classes.
    #
    #      The TEMPERATURE is a proxy for the degree of uncertainty
    #      in the relative estimation of it-scores, but can also serve
    #      to diffuse errors, i.e. a diversification technique with
    #      mathematical reasoning rooted in statistical mechanics,
    #      information theory, and maximum likelihood statistics.
    #      To test temperature variations, softmax() will be much faster.


def softmax_sort( it, temp=55, n=4, drop=0.00, renorm=False ):
    '''Softmax results sorted, include index; option to drop and renormalize.
       Probabilities less than drop are ignored.
       Setting renorm=True will make probabilities sum to 1.
    >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=False)
    [(0.5733, 5, 16.0), (0.2019, 4, 8.0), (0.1198, 3, 4.0), (0.0711, 2, 0.0)]
    >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=True)
    [(0.5934, 5, 16.0), (0.209, 4, 8.0), (0.124, 3, 4.0), (0.0736, 2, 0.0)]
    '''
    arr = tools.toar( it )
    softmax_approx = softmax(arr, temp, n)[-1]
    tups = [ (p, i, float(arr[i]))  for i, p in enumerate(softmax_approx) 
                                        if p >= drop ]
    #        ^so tuples are formatted as (probability, index, it-value).
    if renorm:
        subtotal = sum([p for p, i, v in tups])
        tups = [(round(p/subtotal, n), i, v) for p, i, v in tups] 
    #  Want softmax_sort()[0] to yield the maximum candidate:
    return sorted( tups, key=itemgetter(2), reverse=True )


if __name__ == "__main__":
     system.endmodule()
