#  Python Module for import                           Date : 2017-06-28
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_prtf_boltzmann.py : Boltzmann portfolio

Alternative to Markowitz portfolio. Usage demonstrated in notebook, see
nb/prtf-boltzmann-1.ipynb for explicit details and derivation.


    prices ---> cov ---> globalw
      |                    |
      |                  trimit  <-- floor
      |                  renormalize
      |                    |
      v                    v
      |                    |
    gemrat              weights
      |                    |
      |________score_______|
                 |
                 |                   Boltzmann
      temp --> softmax --> probs --> pweights


The softmax() function is in lib/ys_mlearn.py since it applies more
widely in machine learning.


REFERENCES

- John H. Cochrane, 2005, Asset Pricing, Princeton U. Press.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-28  Condense functions described in Part 1 notebook.
2017-06-26  First version.
'''

from __future__ import absolute_import, print_function, division
import numpy as np
import fecon235.fecon235
#      ^SOLE circular import style which works for Python 2 & 3.
from . import yi_0sys as system
from . import yi_matrix as matrix
#               ^avoiding the np matrix type, stick with arrays!
from . import ys_mlearn as mlearn


def weighcov( cov ):
    '''WEIGHT array (N,1) for Global Min Var Portfolio, given cov.'''
    #  Derived in Cochrane (2005), chp. 5, p.83.
    Viv = matrix.invert_pseudo( cov )
    #                  ^in case covariance matrix is ill-conditioned.
    one = np.ones( (cov.shape[0], 1) )
    top = Viv.dot(one)
    bot = one.T.dot(Viv).dot(one)
    return top / bot


def weighcovdata( dataframe ):
    '''WEIGHT array (N,1) for Global Min Var Portfolio, given data.'''
    V = fecon235.fecon235.covdiflog( dataframe )
    return weighcov(V)


def trimit( it, floor, level ):
    '''For an iterable, accept values > floor, else set to level.'''
    try:
        #  ... in case "it" array elements are integers,
        #  else we cannot assign floats later when enumerating:
        it = it.astype(np.float64)
    except:
        pass
    cpit = it[:]
    for i, x in enumerate(it):
        cpit[i] = x if x > floor else level
    #      Output should be of same type as it:
    return cpit


def renormalize( it ):
    '''Let elements of an iterable proportionally abs(sum) to 1.
       Renormalization of portfolio weights is treated differently
       than probabilities which cannot be negative.
    '''
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
        cpit[i] = x / abs(sumit)
        #             ^preserves signs within it.
    #      Output should be of same type as it:
    return cpit


def rentrim( weights, floor, level ): 
    '''Accept weight > floor, else set to level, then renormalize.'''
    trimmed = trimit( weights, floor, level )
    return renormalize(trimmed)


def gemratarr( dataframe, yearly=256 ):
    '''Extract geometric mean rate of each column into an array.'''
    gems = fecon235.fecon235.groupgemrat( dataframe, yearly )
    return np.array([item[0] for item in gems]).reshape(len(gems), 1)


def weighsoft( weights, rates, temp, floor, level ):
    '''Compute new weights transformed by softmax function.'''
    scores = weights * rates
    problist = mlearn.softmax( scores, temp )[-1]
    probs = np.array( problist ).reshape(len(problist), 1)
    #  Revise weights based on softmax probabilities:
    pweights = probs * weights
    #  Then appropriately adjust:
    return rentrim(renormalize(pweights), floor, level)


def boltzweigh(dataframe, yearly=256, temp=55, floor=0.01, level=0):
    '''MAIN: Compute softmax weights of a Boltzmann portfolio.'''
    rates = gemratarr(dataframe, yearly)
    globalw = weighcovdata(dataframe)
    weights = rentrim(globalw, floor, level)
    return weighsoft(weights, rates, temp, floor, level)


def boltzportfolio(dataframe, yearly=256, temp=55, floor=0.05, level=0):
    '''Full DISPLAY SUMMARY of Boltzmann portfolio.'''
    rates = gemratarr(dataframe, yearly)
    globalw = weighcovdata(dataframe)
    weights = rentrim(globalw, floor, level)
    boltzw = weighsoft(weights, rates, temp, floor, level)
    #      ---- above taken from boltzweigh()
    keys = list(dataframe.columns)
    for i, w in enumerate(boltzw):
        print( keys[i], round(w, 4), "est.", round(rates[i], 2), "rate" )
    print("_________")
    scores = boltzw * rates
    print("PORTFOLIO geometric mean return:", round(np.sum(scores), 2), "%")


if __name__ == "__main__":
     system.endmodule()
