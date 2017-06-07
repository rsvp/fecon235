#  Python Module for import                           Date : 2017-06-06
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_mlearn.py : Machine learning tools

- softmax() for cross-entropy, MLE, neural networks, Boltzmann portfolio.

REFERENCES
- David J.C. MacKay (2008), Information theory, Inference, and Learning
     Algorithms, 7th printing from Cambridge U. Press.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-06  First fecon235 version.
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from . import yi_1tools as tools


def softmax( it, temp=50, n=4 ):
    '''Softmax probabilities for iterable where temp sets temperature tau.
       Temperature tau is set as a fraction of second maximum so that
       scaling is not entirely arbitrary as the math may suggest.
       Experiment with temp around 30 to 80; higher temp (100+)
       will make it-elements more equi-probable, whereas probabilities
       can be sharpened by decreasing temp towards 1.
       Setting temp to 0 results in generic softmax without temperature.
       Results are rounded to n decimal places.
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=200, n=4 )
    [0, 16, 0.3565, 200, [0.3565, 0.2162, 0.1684, 0.1311, 0.0795, 0.0482]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=50, n=4 )
    [0, 16, 0.829, 50, [0.829, 0.1122, 0.0413, 0.0152, 0.0021, 0.0003]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=30, n=4 )
    [0, 16, 0.9581, 30, [0.9581, 0.0342, 0.0065, 0.0012, 0.0, 0.0]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=1, n=4 )
    [0, 16, 1.0, 1, [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    >>> softmax( [ 16, 8, 4, 0, -8, -16 ], temp=0, n=4 )
    [0, 16, 0.9997, 0, [0.9997, 0.0003, 0.0, 0.0, 0.0, 0.0]]
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
    if not temp:
        #  ^whenever temp is set to 0, False, or None => GENERIC softmax:
        tau = 1.0
    else:
        #  Try finding second-highest maximum value in arrstable (not arr):
        negatives = [ x for x in arrstable if x < 0 ]
        if negatives:
            second = max(negatives)
            tau = abs(second * (temp/100.0))
            #     Thus tau is just temp% portion of second maximum. <=!
        else:
            #  No negatives means it-elements are equi-probable at any tau.
            tau = 1.0
    #  MATHEMATICALLY, (Boltzmann) softmax is defined as follows:
    expit = np.exp( arrstable / tau )
    sum_expit = np.sum( expit )
    softmax_exact = expit / sum_expit
    #                      roundit will output a list, not an array:
    softmax_approx = tools.roundit( softmax_exact, n, echo=False )
    hardprob = max(softmax_approx)
    return [ idmax, hardmax, hardprob, temp, softmax_approx ]


if __name__ == "__main__":
     system.endmodule()
