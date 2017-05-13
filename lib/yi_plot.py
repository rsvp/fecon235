#  Python Module for import                           Date : 2017-05-15
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  yi_plot.py : essential plot functions.

References:
- http://matplotlib.org/api/pyplot_api.html

- Computational tools for pandas
  http://pandas.pydata.org/pandas-docs/stable/computation.html

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-05-15  Add plotqq() for quantile-quantile Q-Q probability plot.
2016-01-21  plotn(): Replace its "dataframe = dataframe.dropna()" with todf.
2016-01-20  Receive plotdf(), versions 2014-15, from yi_fred module.
               plotdf was actually the very first plot routine written.
               Replace its "dataframe = dataframe.dropna()" with todf.
2015-12-20  python3 compatible: lib import fix.
2015-12-17  python3 compatible: fix with yi_0sys
2015-11-19  Add scatter, scats, and scat for rainbow scatter plots.
2014-12-13  Add plotn where index are not dates (cf. plotdf and plotfred).
2014-08-08  Add dpi for saving image files.
2014-08-06  For boxplot, remove y_time.yymmdd_t() as fid, 
               use title instead of fid, and add grid.
2014-08-05  Revise from yip_plot.py for boxplot to handle dataframe.
'''

from __future__ import absolute_import, print_function

import matplotlib.pyplot as plt
import matplotlib.cm as colormap
import pandas as pd
import scipy
from . import yi_0sys as system
from . import yi_1tools as tools

dotsperinch = 140                 #  DPI resolution for plot.


#  The function to plot data looks routine, but in actuality specifying the
#  details can be such a hassle involving lots of trial and error.

def plotdf( dataframe, title='tmp' ):
    '''Plot dataframe where its index are dates.'''
    dataframe = tools.todf(dataframe)
    #                ^todf must dropna(),
    #                 otherwise index of last point plotted may be wrong.
    #           Also helps if dataframe resulted from synthetic operations,
    #           or if a Series was incorrectly submitted as Dataframe.      
    fig, ax = plt.subplots()
    ax.xaxis_date()
    #  ^interpret x-axis values as dates.
    plt.xticks( rotation='vertical' )
    #       show x labels vertically.

    ax.plot( dataframe.index, dataframe, 'b-' )
    #        ^x               ^y          blue line
    #                                     k is black.
    ax.set_title( title + ' / last ' + str(dataframe.index[-1]) )  
    #                                  ^timestamp of last data point
    plt.grid(True)
    plt.show()

    #  Now prepare the image FILE to save, 
    #  but ONLY if the title is not the default
    #  (since this operation can be very slow):
    if title != 'tmp':
         title = title.replace( ' ', '_' )
         imgf = 'plotdf-' + title + '.png' 
         fig.set_size_inches(11.5, 8.5)
         fig.savefig( imgf, dpi=dotsperinch )
         print(" ::  Finished: " + imgf)
    return



def plotn( dataframe, title='tmp' ):
    '''Plot dataframe (or list) where the index is numbered (not dates).'''
    #  2014-12-13  Adapted from plotdf which uses date index.
    #  2016-01-21  With todf pre-filter, list type will be converted.
    dataframe = tools.todf(dataframe)
    #                ^todf must dropna(),
    #                 otherwise index of last point plotted may be wrong.
    #           Also helps if dataframe resulted from synthetic operations,
    #           or if a Series was incorrectly submitted as Dataframe.      
    fig, ax = plt.subplots()
    #  ax.xaxis_date()
    #  #  ^interpret x-axis values as dates.
    plt.xticks( rotation='vertical' )
    #       show x labels vertically.

    ax.plot( dataframe.index, dataframe, 'b-' )
    #        ^x               ^y          blue line
    #                                     k is black.
    ax.set_title( title + ' / last ' + str( dataframe.index[-1]) )  
    #                                  ^index on last data point
    plt.grid(True)
    plt.show()

    #  Now prepare the image FILE to save, 
    #  but ONLY if the title is not the default
    #  (since this operation can be very slow):
    if title != 'tmp':
         title = title.replace( ' ', '_' )
         imgf = 'plotn-' + title + '.png' 
         fig.set_size_inches(11.5, 8.5)
         fig.savefig( imgf, dpi=dotsperinch )
         print(" ::  Finished: " + imgf)
    return



#  #  Test data for boxplot:
#  import numpy as np
#  
#  np.random.seed(10)
#  
#  data = np.random.randn(30, 4)
#  labels = ['A', 'B', 'C', 'D']


def boxplot( data, title='tmp', labels=[] ):
     '''Make boxplot from data which could be a dataframe.'''
     #  - Use list of strings for labels, 
     #       since we presume data has no column names, 
     #       unless data is a dataframe.
     #
     #  - Directly entering a dataframe as data will fail, 
     #       but dataframe.values will work, so:
     lastidx = 'NA'
     #         ^for part of the plot's title...
     #  If data is a dataframe, extract some info 
     #    before conversion to values:
     if isinstance( data, pd.DataFrame ):
          lastidx = str( data.index[-1] )  
          colnames = list( data.columns )
          labels = colnames
          data = data.values

     fig, ax = plt.subplots()
     ax.boxplot( data )
     ax.set_xticklabels( labels )
     #  HACK to show points of last row as a red dot:
     ax.plot( [list(data[-1])[0]] + list(data[-1]), 'or' )
          #   ^need a dummy first point in the neighborhood
          #    for autoscale to work properly.
     ax.set_title( title + ' / last ' + lastidx )  
     plt.grid(True)
     plt.show()

     #  Now prepare the image file to save:
     title = title.replace( ' ', '_' )
     imgf = 'boxplot-' + title + '.png' 
     fig.set_size_inches(11.5, 8.5)
     fig.savefig( imgf, dpi=dotsperinch )
     print(" ::  Finished: " + imgf)
     return



def scatter( dataframe, title='tmp', col=[0, 1] ):
    '''Scatter plot for dataframe by zero-based column positions.'''
    #  First in col is x-axis, second is y-axis.
    #  Index itself is excluded from position numbering.
    dataframe = dataframe.dropna()
    #           ^esp. if it resulted from synthetic operations, 
    #                 else timestamp of last point plotted may be wrong.
    count  = len( dataframe )
    countf = float( count )
    colorseq = [ i / countf for i in range(count) ]
    #  Default colorseq uses rainbow, same as MATLAB.
    #  So sequentially: blue, green, yellow, red.
    #  We could change colormap by cmap below.
    fig, ax = plt.subplots()
    plt.xticks( rotation='vertical' )
    #       Show x labels vertically.
    ax.scatter( dataframe.iloc[:, col[0]], dataframe.iloc[:, col[1]], 
                c=colorseq )
    #         First arg for x-axis, second for y-axis, then
    #         c is for color sequence. For another type of
    #         sequential color shading, we could append argument:
    #             cmap=colormap.coolwarm
    #             cmap=colormap.Spectral
    #             cmap=colormap.viridis  [perceptual uniform]
    #         but we leave cmap arg out since viridis will be the 
    #         default soon: http://matplotlib.org/users/colormaps.html
    colstr = '_' + str(col[0]) + '-' + str(col[1]) 
    ax.set_title(title + colstr + ' / last ' + str(dataframe.index[-1]))  
    #                                          ^index on last data point
    plt.grid(True)
    plt.show()

    #  Now prepare the image FILE to save, 
    #  but ONLY if the title is not the default
    #  (since this operation can be very slow):
    if title != 'tmp':
         title = title.replace( ' ', '_' ) + colstr
         imgf = 'scat-' + title + '.png' 
         fig.set_size_inches(11.5, 8.5)
         fig.savefig( imgf, dpi=dotsperinch )
         print(" ::  Finished: " + imgf)
    return



def scats( dataframe, title='tmp' ):
    '''All pair-wise scatter plots for dataframe.'''
    #  Renaming title will result in file output.
    ncol  = dataframe.shape[1]
    #                ^number of columns
    pairs = [ [i, j] for i in range(ncol) for j in range(ncol) if i < j ]
    npairs = (ncol**2 - ncol) / 2
    #  e.g. ncol==5  implies npairs==10
    #       ncol==10 implies npairs==45
    #       ncol==20 implies npairs==190
    print(" ::  Number of pair-wise plots: " + str(npairs))
    for pair in pairs:
        print(" ::  Show column pair: " + str(pair))
        scatter( dataframe, title, pair )
        print("----------------------")
    return



def scat( dfx, dfy, title='tmp', col=[0, 1] ):
    '''Scatter plot between two pasted dataframes.'''
    #  Renaming title will result in file output.
    scatter( tools.paste([ dfx, dfy ]), title, col ) 
    return



#  Note: Leptokurtosis ("fat tails") is much more distinctive in the 
#  Q-Q plots than P-P plots. Bi-modality and skewness are more distinctive 
#  in P-P plots (discriminating in regions of high probability density) 
#  than Q-Q plots (better for regions of low probability density).
#     See https://en.wikipedia.org/wiki/P–P_plot
#     and http://v8doc.sas.com/sashtml/qc/chap8/sect9.htm


def plotqq( data, title='tmp', dist='norm', fitLS=True ):
    '''Display/save quantile-quantile Q-Q probability plot.
       Q–Q plot here is used to compare data to a theoretical distribution.
       Ref: https://en.wikipedia.org/wiki/Q–Q_plot
    '''
    #     Assume "data" to be np.ndarray or single-column DataFrame.
    #  Theoretical quantiles on horizontal x-axis estimated by Filliben method.
    #  Green line in plot depicits theoretical distribution; fitLS computes R^2:
    #      The axes are purposely transformed in order to make the specified
    #      distribution "dist" appear as a linear green line.
    #                   'norm' is a Gaussian distribution.
    #  The "data" plotted along the vertical y-axis.
    fig, ax = plt.subplots()
    arr = tools.toar( data )
    #     ^Roundabout way guarantees a pure array needed for MAIN probplot:
    _ = scipy.stats.probplot( arr, dist=dist, fit=fitLS, plot=plt )
    #   Ignore numerical output, just give plot object to matplotlib.
    #  https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html
    #  Prefer scipy version over statsmodels.graphics.gofplots.qqplot()
    ax.get_lines()[0].set_marker('.')
    ax.get_lines()[0].set_markersize(7.0)
    ax.get_lines()[0].set_markerfacecolor('r')
    #             [0] strangely refers to data points, set to red.
    ax.get_lines()[1].set_color('g')
    #             [1] refers to the straight theoretic line, set to green.
    #         But points in common should be blue, rather than brown.
    plt.title( title + " / plotqq " + dist + ", count=" + str(len(arr)) )
    plt.grid(True)
    plt.show()
    #  Prepare image FILE to save, but ONLY if the title is not the default:
    if title != 'tmp':
         title = title.replace( ' ', '_' )
         imgf = 'plotqq-' + title + '.png' 
         fig.set_size_inches(11.5, 8.5)
         fig.savefig( imgf, dpi=dotsperinch )
         print(" ::  Finished: " + imgf)
    return



if __name__ == "__main__":
     system.endmodule()
