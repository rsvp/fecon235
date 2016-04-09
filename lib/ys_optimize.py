#  Python Module for import                           Date : 2016-04-08
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_optimize.py : Convex optimization given noisy data. 

We smooth some of the rough edges among the "scipy.optimize" algorithms.  Our
"optimize" algorithm first begins by a coarse grid search, then unconstrained
Nelder-Mead simplex method, and finally the refined L-BFGS-B method which
approximates a low-rank Hessian so that we can work in high (>250) dimensions.

USAGE: please see tests/test_optimize.py which also serves as a TUTORIAL for
optimization of loss functions, given data and model.

Our selected methods feature the following and their unification:

Suitability: non-convex problem: GLOBAL optimizers: 
    If your problem does NOT admit a unique local minimum (which can be hard
    to test unless the function is convex), and you do not have prior
    information to initialize the optimization close to the solution, you may
    need a global optimizer. Note that Simulated Annealing has been deprecated
    as of scipy version 0.14.0.  Brute force uses a grid search:
    scipy.optimize.brute() evaluates the function on a given grid of
    parameters and returns the parameters corresponding to the minimum value. 

Suitability: if data is NOISY:
    Nelder-Mead simplex method (scipy.optimize.fmin()) has a long history of
    successful use in applications, but it will usually be slower than an
    algorithm that uses first or second derivative information. In practice it
    can have poor performance in high-dimensional problems and is not robust
    to minimizing complicated functions.  Currently there is no complete
    theory describing when the algorithm will successfully converge to the
    minimum, or how fast it will if it does.

Suitability: WITH knowledge of the gradient: quasi-Newton methods:
      BFGS   (scipy.optimize.fmin_bfgs()), or 
    L-BFGS-B (scipy.optimize.fmin_l_bfgs_b())
        where the former has larger computational overhead.
        Knowledge here means analytical representation.
        BFGS abbreviates Broyden-Fletcher-Goldfarb-Shanno.

Suitability: WITHOUT knowledge of the gradient:
    L-BFGS-B (scipy.optimize.fmin_l_bfgs_b())
        where gradient need not be provided analytically.
        Constraints are optional, so this method is excellent
        if you have a specific strategy.

General strategy:
    For scipy.optimize.minimize():
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    a singe method must be selected.  However, our optimize() is a sequence of 
    methods which starts from brute to refined, in above order.

References:
- Mathematical optimization using scipy
  http://www.scipy-lectures.org/advanced/mathematical_optimization

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-04-08  Clarify comments.
2016-04-06  Semantic change of names to avoid misunderstanding.
               minimize() -> optimize()
               For optimize(): boundpairs -> initialpairs
            Make funarg=() as default.
2016-04-04  First fecon235 version.
'''

from __future__ import absolute_import, print_function, division

import numpy as np                #  for numerical work.
import scipy.optimize as sop      #  optimization routines.
from . import yi_0sys as system


DISPLAY = 0
#         0 suppresses display, 1 for stdout, 2 for logging to iterate.dat
#  Non-zero for debugging which could change output format of "result" below.
#  Some routines offer "full_output" if you want messy iterative evaluations.


#  NOTICE: TUPLE "funarg" is used to specify arguments to function "fun"
#          which are NOT the parameters to be optimized (e.g. data).
#          Gotcha: Remember a single-element tuple must include
#          that mandatory comma: ( alone, )
#
#  Please see tests/test_optimize.py which also serves as a TUTORIAL.


def minBrute( fun, boundpairs, funarg=(), grids=20 ):
    '''Minimization by brute force grid search.
           fun is our function to minimize, given parameters for optimization.
           boundpairs is a list of (min, max) pairs for fun parameters.
           funarg is a tuple of supplemental arguments for fun.
           grids are number of steps are taken in each direction.
    '''
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html
    boundpairs = tuple( boundpairs )
    #  boundpairs actually must be a tuple consisting of (min,max) tuples.
    if DISPLAY:
        print(" ::  Display for minBrute() ... ")
    result = sop.brute( func=fun, args=funarg, ranges=boundpairs, Ns=grids,
                        finish=None, full_output=DISPLAY )
    #                   finish default is "fmin" (Nelder-Mead), 
    #                   which may not respect boundpairs !!!
    #                   https://github.com/scipy/scipy/issues/1613
    #  Estimated minimum is returned as ndarray if DISPLAY=0,
    #  otherwise we see all grid evaluations inside a tuple 
    #  but the minimum in ndarray format is available as result[0].
    return result


def minNelder( fun, initial, funarg=() ):
    '''Nelder-Mead simplex algorithm.
           fun is our function to minimize, given parameters for optimization.
           initial parameter guesses must be an ndarray, i.e. np.array([...])
           funarg is a tuple of supplemental arguments for fun.
    '''
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin.html
    #  Nelder, J.A. and Mead, R. (1965), "A simplex method for function 
    #      minimization", The Computer Journal, 7, pp. 308-313
    if DISPLAY:
        print(" ::  Display for minNelder() ... ")
    result = sop.fmin( func=fun, args=funarg, x0=initial, disp=DISPLAY)
    #  Estimated minimum is returned as ndarray:
    return result


def minBroyden( fun, initial, funarg=(), boundpairs=None ):
    '''Broyden-Fletcher-Goldfarb-Shanno L-BFGS-B algorithm with box boundaries.
       At each step an approximate low-rank Hessian is refined,
       so this should work in high (>250) dimensions.
           fun is our function to minimize, given parameters for optimization.
           initial parameter guesses must be an ndarray, i.e. np.array([...])
           funarg is a tuple of supplemental arguments for fun.
           boundpairs is an OPTIONAL list of (min, max) pairs for fun parameters,
               where None can be used for either min or max to indicate no bound.
    '''
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin_l_bfgs_b.html
    #  Ref: C. Zhu, R. H. Byrd and J. Nocedal. L-BFGS-B: Algorithm 778: L-BFGS-B, 
    #       FORTRAN routines for large scale bound constrained optimization (1997), 
    #       ACM Transactions on Mathematical Software, 23, 4, pp. 550-560.
    #  scipy function is actually a Python wrapper around Fortran code.
    if DISPLAY:
        print(" ::  Display for minBroyden() ... ")
    result = sop.fmin_l_bfgs_b( func=fun, args=funarg, x0=initial, bounds=boundpairs, 
                                approx_grad=True, disp=DISPLAY )
    #  MUST set approx_grad=True unless you want to compute the gradient analytically 
    #  and provide it to a flag called fprime.
    #
    #  Sample result which is a tuple:
    #  (array([ 88.79999999,  77.70000008]), 1.639480801226924e-13, 
    #   {'warnflag': 0, 'task': 'CONVERGENCE: REL_REDUCTION_OF_F_<=_FACTR*EPSMCH', 
    #    'grad': array([  4.17384459e-05,   6.34588833e-06]), 'nit': 6, 'funcalls': 30})
    #
    #  So just the estimated minimum as ndarray:
    return result[0]


def optimize( fun, initialpairs, funarg=(), grids=20 ):
    '''Optimize by grid search, Nelder-Mead simplex, and L-BFGS-B methods.
       First a broad global search, followed by coarse non-gradient method,
       then refined quasi-Newton method by approximate low-rank Hessian.
           fun is our function to minimize, given parameters for optimization.
           funarg is a tuple of supplemental arguments for fun.
           initialpairs is a list of (min, max) pairs for fun parameters.
           grids are number of steps are taken in each direction.
       However, here we are intentionally NOT CONSTRAINED by initialpairs.
    '''
    #  The argument initialpairs can be just our preliminary wild guess.
    #  minBrute will respect initialpairs as strict boundpairs using grids, 
    #  however, better and better initial point estimates are passed 
    #  along to other algorithms which will ignore any strict bounds
    #  if the minimization can be improved.
    brute = minBrute(fun=fun, funarg=funarg, boundpairs=initialpairs, grids=grids)
    if DISPLAY:
        print( brute )
        brute = brute[0]
        #             ^but just the ndarray part for next initial:
    nelder  =  minNelder( fun=fun, funarg=funarg, initial=brute )
    if DISPLAY:
        print( nelder )
    broyden = minBroyden(fun=fun, funarg=funarg, initial=nelder, boundpairs=None)
    #   broyden should NOT set boundpairs=initialpairs because
    #   nelder may have found something better outside initialpairs.
    #   Thus nelder and broyden are both unconstrained results.
    if DISPLAY:
        print( broyden )
    #      broyden is our final estimated minimum as ndarray:
    return broyden


if __name__ == "__main__":
     system.endmodule()
