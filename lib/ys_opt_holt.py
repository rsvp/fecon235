#  Python Module for import                           Date : 2016-12-29
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_opt_holt.py : optimize Holt-Winters parameters/forecast

Here we rely on a single method to find optimal alpha and beta:

- minBrute() from ys_optimize module: non-convex problem: GLOBAL optimizers: 
    If your problem does NOT admit a unique local minimum (which can be hard
    to test unless the function is convex), and you do not have prior
    information to initialize the optimization close to the solution: Brute
    force uses a grid search: scipy.optimize.brute() evaluates the function on
    a given grid of parameters and returns the parameters corresponding to the
    minimum value. 

See lib/ys_optimize.py for implementation details and references.
Also tests/test_optimize.py is intended as a TUTORIAL for USAGE.

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2016-12-29  Include percentage loss in alphabetaloss list.
2016-12-28  Add optimize_holtforecast() for forecasting.
               Noted: 2*sigma approximated by 3*(median_absolute_error)
2016-12-19  First version.
'''

from __future__ import absolute_import, print_function

import numpy as np
from fecon235.lib import yi_0sys as system
from fecon235.lib import yi_1tools as tools
from fecon235.lib import yi_timeseries as ts
from fecon235.lib import ys_optimize as yop
#  Assuming that DISPLAY=0 at ys_optimize module.


#  GOAL: given some data and a MODEL, we want to MINIMIZE the LOSS FUNCTION
#        over possible values of the model's PARAMETERS.
#        Parameters which satisfy that goal are called BEST estimates
#        for the specified functional form.

#  Loss function should DISTINGUISH between parameters to be optimized,
#  and other supplemental arguments. The latter is introduced
#  via a tuple called funarg, frequently used to inject data.
#
#  We forego using RMSE (root mean squared errors) in favor of a more
#  robust loss function since the squaring magnifies large errors.


def loss_holt(params, *args):
    '''Loss function for holt() using np.median of absolute errors.
       This is much more robust than using np.sum or np.mean 
       (and perhaps better than editing "outliers" out of data).
       The error array will consist of 1-step ahead prediction errors.
    '''
    #  Specify arguments:
    alpha, beta = params
    data = args[0]   #  Primary data assumed to be single column.

    #  Information from the Holt-Winters filter is distilled 
    #  to the holt() multi-column workout dataframe;
    #  see tests/test_optimize.py for numerical examples.
    holtdf = ts.holt( data, alpha, beta ) 
    #  Henceforth use numpy arrays, rather than dataframes:
    y = holtdf['Y'].values       # Actual data, without index
    l = holtdf['Level'].values
    b = holtdf['Growth'].values

    error = y[1:] - (l[:-1] + b[:-1])
          #  #  Equivalent, but more expensive, version of previous line...
          #  #  Compute error array, taking one lag into account:
          #  N = y.size
          #  error = np.zeros(( N-1, ))   #  Fill level array with zeros.
          #  for i in range(N-1):
          #     error[i] = y[i+1] - (l[i] + b[i])
          #     #          ^Actual  ^Prediction MODEL
    #  Ignore the first ten errors due to initialization warm-up:
    return np.median( np.absolute(error[10:]) )

#  STATISTICAL NOTE: if L is the median absolute error, then by definition,
#                    prob(-L <= error <= L) = 0.5
#     If we assume the errors are Gaussian centered around zero, 
#     then L = 0.675*sigma (by table look-up), thus sigma = 1.48*L.
#
#     Rule of thumb: Two sigma confidence can be approximated by 3*L.



#  NOTICE: TUPLE "funarg" is used to specify arguments to function "fun"
#          which are NOT the parameters to be optimized (e.g. data).
#          Gotcha: Remember a single-element tuple must include
#          that mandatory comma: ( alone, )


def optimize_holt(dataframe, grids=50, alphas=(0.0, 1.0), betas=(0.0, 1.0)):
    '''Optimize Holt-Winters parameters alpha and beta for given data.
       The alphas and betas are boundaries of respective explored regions.
       Function interpolates "grids" from its low bound to its high bound,
       inclusive. Final output: [alpha, beta, losspc, median absolute loss]
       TIP: narrow down alphas and betas using optimize_holt iteratively.
    '''
    if grids > 49:
        system.warn("Optimizing Holt-Winters alphabetaloss may take TIME!")
        #  Exploring loss at all the grids is COMPUTATIONALLY INTENSE
        #  due to holt(), especially if the primary data is very large.
        #  Tip: truncate dataframe to recent data.
    result = yop.minBrute(fun=loss_holt, funarg=( dataframe, ), 
                          boundpairs=[alphas, betas], grids=grids)
    #  result is a numpy array, so convert to list:
    alpha, beta = list(result)
    #  Compute loss, given optimal parameters:
    loss = loss_holt((alpha, beta), dataframe)
    #  Compute percentage loss relative to absolute tailvalue:
    losspc = (float(loss) / abs(tools.tailvalue(dataframe))) * 100
    #  Since np.round and np.around print ugly, use Python round() to
    #  display alpha and beta. Also include losspc and median absolute loss:
    return [round(alpha, 4), round(beta, 4), round(losspc, 4), loss]


def optimize_holtforecast( dataframe, h=12, grids=50 ):
    '''Forecast ahead h periods using optimized Holt-Winters parameters.'''
    #  Note: default hw_alpha and hw_beta from yi_timeseries module 
    #        are NOT necessarily optimal given specific data.
    alphabetaloss = optimize_holt(dataframe, grids=grids)
    #  alphabetaloss will be a list: [alpha, beta, losspc, loss]
    #     computed from default boundpairs: alphas=(0.0, 1.0), betas=(0.0, 1.0)
    holtdf = ts.holt(dataframe, alpha=alphabetaloss[0], beta=alphabetaloss[1])
    #  holdf is our Holt-Winters "workout" dataframe.
    forecasts_df = ts.holtforecast(holtdf, h)
    #  forecasts_df is a dataframe containing h period forecasts.
    #
    #  Unlike ts.holtforecast(), here we append alphabetaloss to the output
    #     so that the model parameters and median absolute loss are available.
    #     Forecasts alone can be obtained directly by func(...)[0]
    return [ forecasts_df, alphabetaloss ]



if __name__ == "__main__":
     system.endmodule()
