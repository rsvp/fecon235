#  Python Module for import                           Date : 2016-04-08
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_optimize : Test fecon235 ys_optimize module.

MUST SEE lib/ys_optimize.py for implementation details and references.
This test file is also intended as a TUTORIAL for USAGE,
see especially the section on Robust Estimation for a quick example.

Our selected methods feature the following and their unification:

- minBrute(): non-convex problem: GLOBAL optimizers: 
    If your problem does NOT admit a unique local minimum (which can be hard
    to test unless the function is convex), and you do not have prior
    information to initialize the optimization close to the solution: Brute
    force uses a grid search: scipy.optimize.brute() evaluates the function on
    a given grid of parameters and returns the parameters corresponding to the
    minimum value. 

- minNelder(): if data is NOISY:
    Nelder-Mead simplex method (scipy.optimize.fmin()) has a long history of
    successful use in applications, but it will usually be slower than an
    algorithm that uses first or second derivative information. 

- minBroyden(): WITHOUT knowledge of the gradient:
    L-BFGS-B (scipy.optimize.fmin_l_bfgs_b())
        where gradient need not be provided analytically.
        Constraints are optional, so GREAT for very NARROW USE.
        BFGS abbreviates Broyden-Fletcher-Goldfarb-Shanno.

- optimize(): 
    For scipy.optimize.minimize(): a single method must be selected. 
    However, our optimize() is a sequence of methods which starts from brute
    to refined in above order. This is the MAIN FUNCTION for GENERAL USE.

Here we test three types of LOSS FUNCTIONS: sum of squared errors,
sum of absolute errors, and median of absolute errors.


Testing: As of fecon235 v4, we favor pytest over nosetests, so e.g. 
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
               or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-04-08  Clarify model specification and add median absolute error.
2016-04-06  Semantic change of names to avoid misunderstanding.
               minimize() -> optimize()
               For optimize(): boundpairs -> initialpairs
2016-04-04  First version. Thanks to so12311 (2011) for his example at 
               Stack Overflow: http://stackoverflow.com/a/8672743
'''

from __future__ import absolute_import, print_function

import numpy as np
from fecon235.lib import yi_0sys as system
from fecon235.lib import ys_optimize as yop
#
#  N.B. -  in this tests directory without __init__.py, 
#          we use absolute import as if outside the fecon235 package,
#          not relative import (cf. modules within lib).
#
#  Assuming that DISPLAY=0 at ys_optimize module.


#  Here are the TRUE PARAMETERS, which we will pretend to discover:
m_true = 88.8
b_true = 77.7

#  Source of data:
x_true = np.arange(0, 10, 0.1)

#  Generate DATA for a LINE with slope m_true and intercept b_true:
y_true = m_true*x_true + b_true


#  GOAL: given some data and a MODEL, we want to MINIMIZE the LOSS FUNCTION
#        over possible values of the model's PARAMETERS.
#        Parameters which satisfy that goal are called BEST estimates
#        for the specified functional form.

#  Loss function should DISTINGUISH between parameters to be optimized,
#  and other supplemental arguments. The latter is introduced
#  via a tuple called funarg, frequently used to inject data.
#  (Compare to classical optimization, see Rosenbrock test below.)


def sqerror(params, *args):
    '''LOSS FUNCTION: sum of squared errors for our model.'''
    #  Notice how params works like a tuple:
    m, b = params
    #  Assignment for non-parameter arguments (see funarg below):
    y = args[0]
    x = args[1]
    #  Functional form of our MODEL: 
    y_model = m*x + b
    #  Generated ERRORS:
    error = y - y_model
    #  L2 metric:
    #  Minimizing the sum of squared errors by implication minimizes RMSE,
    #  the so-called: "Root Mean Squared Error,"
    #  since taking mean, then the square root preserves minimization,
    #  but unnecessarily increases computing time:
    return np.sum( np.square(error) )

#  Loss function could also have used np.sum(np.absolute(error)), L1 metric.

def aberror(params, *args):
    '''LOSS FUNCTION: sum of absolute errors for our model.'''
    m, b = params
    y = args[0]
    x = args[1]
    #  Functional form of our MODEL: 
    y_model = m*x + b
    #  Generated ERRORS:
    error = y - y_model
    return np.sum( np.absolute(error) )


#  NOTICE: TUPLE "funarg" is used to specify arguments to function "fun"
#          which are NOT the parameters to be optimized (e.g. data).
#          Gotcha: Remember a single-element tuple must include
#          that mandatory comma: ( alone, )

#  ============================================= Test helper functions ========== 


def test_minBrute_ys_optimize_fecon235_Inadequate_boundpairs():
    '''Test minBrute using intentionally inadequate boundpairs.'''
    #  Brute force works with range of guesses to start parameter estimation.
    result = yop.minBrute(fun=sqerror, funarg=(y_true, x_true), 
                          boundpairs=[(10.0,50.0),(10.0,30.0)], grids=20)
    #  We know in advance that the result should NOT fit
    #  our true parameters. In fact, the result 
    #  should give the upper bounds of boundpairs.
    assert result[0] == 50.0
    assert result[0] != m_true
    assert result[1] == 30.0
    assert result[1] != b_true


def test_minBrute_ys_optimize_fecon235_Adequate_boundpairs():
    '''Test minBrute using adequate boundpairs.'''
    result = yop.minBrute(fun=sqerror, funarg=(y_true, x_true), 
                          boundpairs=[(70.0,90.0),(70.0,90.0)], grids=20)
    #  We know in advance that the result should FIT,
    #  though approximately since the grid search is coarse.
    #  We shall accept +/- 1.0 of true values:
    assert abs(result[0] - m_true) < 1.0
    assert abs(result[1] - b_true) < 1.0


def test_minNelder_ys_optimize_fecon235_wild_startparms():
    '''Test minNelder using wild starting parameter guesses.'''
    startparms = np.array([1000.0, 1000.0])
    result = yop.minNelder(fun=sqerror, funarg=(y_true, x_true), 
                           initial=startparms)
    #  We shall accept +/- 0.01 of true values:
    assert abs(result[0] - m_true) < 0.01
    assert abs(result[1] - b_true) < 0.01


def test_minBroyden_ys_optimize_fecon235_wild_startparms():
    '''Test minBroyden using wild starting parameter guesses.'''
    startparms = np.array([1000.0, 1000.0])
    result = yop.minBroyden(fun=sqerror, funarg=(y_true, x_true), 
                            initial=startparms)
    #  We shall accept +/- 0.01 of true values:
    assert abs(result[0] - m_true) < 0.01
    assert abs(result[1] - b_true) < 0.01


#  ============================================= MAIN FUNCTION: optimize() ====== 

#  SUMMARY: yop.optimize() accurately integrates all of the helper functions
#  while being tolerant of wild guesses for initialpairs!

def test_optimize_ys_optimize_fecon235_Inadequate_initialpairs():
    '''Test optimize() using intentionally inadequate initialpairs.
       However, we expect very accurate estimates since we
       minimize by grid search, Nelder-Mead simplex, and L-BFGS-B methods.
       First a broad global search, followed by coarse non-gradient method,
       then refined quasi-Newton method by approximate low-rank Hessian.
           initialpairs is a list of (min, max) pairs for fun arguments.
       By design, we are intentionally NOT CONSTRAINED by initialpairs.
    '''
    result = yop.optimize(fun=sqerror, funarg=(y_true, x_true), 
                          initialpairs=[(10.0,50.0),(10.0,30.0)], grids=20)
    #  We shall accept +/- 0.0001 of true values:
    assert abs(result[0] - m_true) < 0.0001
    assert abs(result[1] - b_true) < 0.0001


def test_optimize_ys_optimize_fecon235_aberror_loss_function():
    '''Test optimize() using sum of absolute errors loss function, 
       instead of sum of squared errors loss function,
       and intentionally inadequate initialpairs.
       By design, we are intentionally NOT CONSTRAINED by initialpairs.
    '''
    result = yop.optimize(fun=aberror, funarg=(y_true, x_true), 
                          initialpairs=[(10.0,50.0),(10.0,30.0)], grids=20)
    #  We shall accept +/- 0.0001 of true values:
    assert abs(result[0] - m_true) < 0.0001
    assert abs(result[1] - b_true) < 0.0001


#  =================================================== ROBUST Estimation ======== 
#  We revisit the fitting of the sloped line example, 
#  but this time more generalized for templating in other applications.
#  Usage with other data structures becomes more apparent, e.g. DataFrame.

#  Let's first WRITE THE MODEL in terms of tuple p for parameters.
#  This conceptually separates the model specifications from the loss function.
#  Also it can output the fitted values for the model given optimal parameters.

def model_slope( p, X ):
    '''Model of sloped line: given parameters p and data X.'''
    #  Big X could be a pandas DataFrame with interesting columns.
    #  Note that we are not limited to just a simple equation here.
    #  This section could have also been a complicated procedure
    #  with constraints, masks, etc.
    return p[0]*X + p[1]

#  For good practice, let the last element of p be the 
#  estimated constant INTERCEPT. Rewriting the model is thus easier
#  because no shifting of locations is involved 
#  when you want to remove that slack variable.


def medaberror( p, *args ):
    '''Loss function: np.median of absolute errors for our model.
       This is much more robust than using np.sum or np.mean.
       Perhaps better than editing "outliers" out of data.
       This illustrates a LOSS FUNCTION in its SIMPLICITY.
    '''
    #   y represents the independent variable, while
    #   X represents the dependent variable(s).
    #   Here the model is introduced via *args.
    y = args[0]
    model = args[1]
    X = args[2]
    error = y - model(p, X)
    return np.median( np.absolute(error) )


#  SUMMARY: optimize() computes the model parameters
#  which minimizes a given loss function. There are many types
#  of loss functions which can be used to estimate a model.

def test_optimize_ys_optimize_fecon235_medaberror_loss_function():
    '''Test optimize() using median of absolute errors loss function, 
       instead of sum of squared errors loss function,
       and intentionally inadequate initialpairs.
       By design, we are intentionally NOT CONSTRAINED by initialpairs.
    '''
    #  We have y_true and x_true as ndarrays to serve as data.
    #  Note that funarg here also include model specification.
    result = yop.optimize(fun=medaberror, funarg=(y_true, model_slope, x_true), 
                          initialpairs=[(10.0,50.0),(10.0,30.0)], grids=20)
    #  We shall accept +/- 0.0001 of true values:
    assert abs(result[0] - m_true) < 0.0001
    assert abs(result[1] - b_true) < 0.0001
    #
    #  What exactly was the LEAST ERROR with optimal parameters?
    #
    least_error = medaberror( result, y_true, model_slope, x_true )
    assert abs(least_error - 0.0) < 0.0001


#  REMARKS: if the loss function is squared error, then theoretically
#  Ordinary Least Squares method will directly provide unique unbiased 
#  linear estimates in closed form. Now if the distribution of
#  the error terms is Gaussian then maximum likelihood estimates 
#  are the same as the OLS estimates asymptotically.
#
#  Loss functions based on absolute error does require iterative 
#  solutions for estimates that are generally neither unique nor 
#  available in closed form. They can be computationally expensive. 
#  This is the case for our optimize() algorithm. But the estimates
#  are practically more robust, facing outliers and corrupt data.
#
#  Reference:
#  https://www.quora.com/How-would-a-model-change-if-we-minimized-absolute-error-instead-of-squared-error-What-about-the-other-way-around/answer/Ben-Packer-1



#  =================================================== ROSENBROCK test ========== 
#  This is a classic test in convex optimization.
#  Note how simply the parameters to be optimized are expressed in Python:

def rosenbrock( z ):   
    '''Famous Rosenbrock test function.'''
    #  Optimize on two variables z[0] and z[1] by just writing them out:
    return 0.5*(1 - z[0])**2 + (z[1] - z[0]**2)**2


def test_optimize_ys_optimize_fecon235_rosenbrock_function():
    '''Test optimize() using Rosenbrock function.'''
    #  Test multivariate function without supplemental arguments, so funarg=().
    result = yop.optimize(fun=rosenbrock, funarg=(), 
                          initialpairs=[(-98.0,98.0),(-98.0,98.0)], grids=20)
    #  We shall accept +/- 0.0001 of true values:
    assert abs(result[0] - 1.0) < 0.0001
    assert abs(result[1] - 1.0) < 0.0001


if __name__ == "__main__":
     system.endmodule()
