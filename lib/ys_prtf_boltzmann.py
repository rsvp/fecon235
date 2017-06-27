#  Python Module for import                           Date : 2017-06-26
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_prtf_boltzmann.py : Boltzmann portfolio

Alternative to Markowitz portfolio. Usage demonstrated in notebook, see
nb/prtf-boltzmann-1.ipynb for details.

The softmax() function is in lib/ys_mlearn.py since it applies more
widely in machine learning.

REFERENCES

- John H. Cochrane, 2005, Asset Pricing, Princeton U. Press.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-26  First version.
'''

from __future__ import absolute_import, print_function, division
import numpy as np
from . import yi_0sys as system
from . import yi_matrix as matrix
#               ^avoiding the np matrix type, stick with arrays!


def weighcov( cov ):
    '''Compute WEIGHT array (N,1) for Global Minimum Variance Portfolio.'''
    #  Derived in Cochrane (2005), chp. 5, p.83.
    Viv = matrix.invert_pseudo( cov )
    #                  ^in case covariance matrix is ill-conditioned.
    one = np.ones( (cov.shape[0], 1) )
    top = Viv.dot(one)
    bot = one.T.dot(Viv).dot(one)
    return top / bot


def trimit( it, floor, level ):
    '''For an iterable, accept values >= floor, else set to level.'''
    try:
        #  ... in case "it" array elements are integers,
        #  else we cannot assign floats later when enumerating:
        it = it.astype(np.float64)
    except:
        pass
    cpit = it[:]
    for i, x in enumerate(it):
        cpit[i] = x if x >= floor else level
    #      Output should be of same type as it:
    return cpit


def renormalize( it ):
    '''Let elements of an iterable proportionally sum to 1.'''
    #  Remember that a list is an iterable, too.
    arr = np.array([ float(x) for x in it ])
    sumit = float(np.sum(arr))
    try:
        #  ... in case "it" array elements are integers,
        #  else we cannot assign floats later when enumerating:
        it = it.astype(np.float64)
    except:
        pass
    cpit = it[:]
    for i, x in enumerate(it):
        cpit[i] = x / sumit
    #      Output should be of same type as it:
    return cpit


if __name__ == "__main__":
     system.endmodule()
