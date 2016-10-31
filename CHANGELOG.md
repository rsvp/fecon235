## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*


### 2016-10-30 v4.16.1030

Add bin/docker/rsvp_fecon235/Dockerfile for Docker image.
See public hub at https://hub.docker.com/r/rsvp/fecon235
regarding running our Docker container.

Move and rewrite ema() to close #5
since *pd.ewma() is deprecated* as of pandas 0.18.
Our old ema() has been commented out in lib/yi_1tools.py
then new ema() has been rewritten in lib/yi_timeseries.py
as a special case of holtlevel().
See issue #5 for details on pandas deprecation warning,
Exponential Moving Average and Holt-Winters smoothing:
https://github.com/rsvp/fecon235/issues/5


### 2016-05-25 v4.16.0525

qdl-spx-earn-div.ipynb: remedy for issue #3 Math Processing Error.
GitHub choking on LaTeX equations, so provide
alternative view link at Jupyter.
No problems if notebook is locally executed.

Add lib/ys_optimize.py featuring the following:

- minBrute(): non-convex problem: GLOBAL optimizers: Brute force grid search.
- minNelder(): if data is NOISY: Nelder-Mead simplex method.
- minBroyden(): WITHOUT knowledge of the gradient: L-BFGS-B, Broyden-Fletcher-Goldfarb-Shanno.
- optimize(): unifies the three above.

Add tests/test_optimize.py for ys_optimize module.
This also serves as a tutorial for optimization of loss functions,
given data and model, see Robust Estimation section.

lib/yi_1tools.py: add lagdf() to create lagged DataFrame,
useful data structure for vector autoregressions.

Add tests/test_1tools.py esp. to test lagdf(),
other functions in module yi_1tools are tested along the way.

yi_1tools.py: replace deprecated ols from pandas.stats.api,
revise regress() by using regressformula().
Introduce new intercept argument, used also for stat2().

Finalize fred-employ-nfp.ipynb for May 2016 release.
Forecast monthly change in NFP using a variety of optics:
baseline expectation since 1939, Holt-Winters method,
visual selection of local range, and regression against SPX -- but
standard errors are inherently very large due to survey measurement error.


### 2016-03-29 v4.16.0329

SEC-13F-parse.ipynb: Fix issue #2 by v4 and p6 updates.
Noteworthy dramatic GLD liquidation in 2016-Q4 by Paulson.

Add NEW nb/qdl-spx-earn-div.ipynb which examines the
three separable components of total return for equities:
enterprise and speculative returns plus dividend yield,
using the Shiller database dating back to 1871.
Shortcut: https://git.io/equities or https://git.io/spx

### 2016-02-21 v4.16.0221

Add directory `.github` for issue and PR templates,
see [2016-02-17 GitHub post](https://github.com/blog/2111-issue-and-pull-request-templates)

- Rename CONTRIBUTING.md -> .github/CONTRIBUTING.md
- Add .github/ISSUE_TEMPLATE.md
- Add .github/PULL_REQUEST_TEMPLATE.md

Fix issue #2 by v4 and p6 updates:

- fred-housing.ipynb
- fred-xau-tips.ipynb

We conjecture that real gold is a stationary time-series bound by real interest rates.

### 2016-01-23 v4.16.0123

We adopt use of *group* dictionaries where
key serves as name, and value is its data code.
Some new functions in the fecon235 module:
groupget, grouppc, groupgeoret, groupholtf -- 
are helpful in clarifying logic and reducing notebook clutter.
The function groupfun() is mathematically an operator.

For example, cotr4w is a group, and further 
usage is explained in nb/qdl-COTR-positions.ipynb
for CFTC Commitment of Traders Reports.
One command: groupcotr() will summarize results, 
with optional smoothing parameter.

For fecon235.py: add forefunds() to forecast Fed Funds directly.
Its derivation is explained in qdl-libor-fed-funds.ipynb.

Append sample size and dates to georet() output,
making it suitable for logging purposes.
Geometric mean returns are ranked in groupgeoret().

Procedure plotdf() has a *todf* pre-filter for convenience 
so that Series type can be plotted directly.
That procedure is now tried first in plot().

Fix issue 2 with v4 and p6 upgrades:

- fred-georeturns.ipynb
- qdl-libor-fed-funds.ipynb

To update pre-2016 notebooks, sections for import and the preamble 
must be modified, please see [issue 2].

### 2015-12-30 v4.15.1230 MAJOR

Major v4 benefits from the python3 compatibility changes
made during v3. All modules are now operational under 
both Python 2 and 3. Also, code has been rewritten for
cross-platform performance (Linux, Mac, and Windows).

We MOVED the yi-modules from nb to a new directory: lib. 
Python 3 uses absolute import and our python2 code
now conforms to that practice.

To update pre-2016 notebooks, please use import style 
discussed in *docs* README: https://git.io/fecon-intro 
The top-level module **fecon235.py** 
(formerly known as *nb/fecon.py*) is also 
explained in that introduction.
With adoption of python3 print_function, 
the python2 print statement must be rewritten as a function.

We also highly recommend inclusion of PREAMBLE-p6.15.1223
which gives versioning requirements for successful
notebook replication. With those fixes, our notebooks
should run under both Python kernels in Jupyter.

Make friends with np.true_divide() and np.floor_divide(),
avoiding np.divide() like the plague: call our 
convenient *div()* directly instead of numpy.

The directory *tests* is no longer a package.
Thus one can run tests easily against an installed
version of the main package, and independently.
Our tests should be nosetests and pytest compatible.

### 2015-12-16 v3.15.1216

Module yi_0sys encourages cross-platform execution.
This should help eliminate dependence on Linux 
for most casual users.

That module is also useful for python3 compatibility.
Jupyter project is now calling python2 a "legacy."
Code base is now clarified in README.md 

Score for the Federal Reserve is computed 
in fred-infl-unem-fed.ipynb
leading to a discussion of the Phillips curve,
i.e. the inflation vs unemployment relationship.

### 2015-11-22 v3.15.1122 MAJOR

The major change to v3 marks our adoption of **Jupyter** 
which has now become fully independent of IPython, 
although it is still known as IPython v4.0 
("*conda update ipython-notebook*" still works 
as expected for existing Anaconda distributions). 
Creating **R** notebooks is now very easy.

pandas 0.17 now requires a new package 
called *pandas-datareader* which was refactored from 
deprecated pandas.io -- so please install that package 
if you intend to use the yi_stocks module.

The yi_plot module now includes sequential heatmap 
scatter plotting. This is great for visualizing the 
points in a scatter plot over time. Currently 
the color sequence will go from blue to green to 
red, like the MATLAB rainbow. Soon that we shall 
switch that color map to viridis, which is perceptually uniform, 
as it becomes the default in matplotlib.

### 2015-11-02 v2.15.1102

Introduce two new notebooks:

- qdl-libor-fed-funds.ipynb : examines the spread between LIBOR 
and Fed Funds. By constructing a synthetic forward Fed Funds 
rate, estimate is given for the change in Fed Funds rate over the 
next 12 months.

- qdl-xau-contango.ipynb : *London Bullion Market Association* 
ceased publishing daily data on their *Gold Forward Offered Rate* (**GOFO**), 
as of 30 January 2015 -- so we develop an observable proxy called *tango* 
using gold futures and LIBOR. 

### 2015-09-15 

Futures prices can be retrieved using our yi_quandl module. 
Data for stocks, ETFs, and mutual funds comes directly from Yahoo Finance, 
and falls back on Google Finance: see yi_stocks module.
All data is easily retrieved using fecon.get() and our internal slang.

As our own API stabilizes, `tests` will cover more units. 
Currently we rely on Python nose and doctest.

### 2015-08-31 v2.15.0831 

All fred- notebooks are stable. 
Henceforth, they will be automatically converted 
from IPython notebook format v3 to v4.

Add module yi_secform.py, derived from nb/SEC-13F-parse.ipynb, 
so that pandas can read 13F filings from SEC and easily 
sort portfolio allocations.

MAJOR change: During August 2015 we added Quandl API and module to get data.
Module yi_quandl.py is our wrapper over the API yi_quandl_api.py 
for creating easily accessible synthetic series. 

Add qdl-COTR-positions.ipynb to demonstrate reading CFTC 
Commitment of Traders Reports, retrieved using our yi_quandl module.

MAJOR change: new module **fecon** conveniently unifies necessary 
yi modules to especially simplify interactive commands.

Recommend pandas > 0.15 


### 2014-11-08 v1.0.0

Included modules have passed tests. Imperative that pandas > 0.13 
with recommended dependencies on numpy.

- - - -

[issue 2]: https://github.com/rsvp/fecon235/issues/2


