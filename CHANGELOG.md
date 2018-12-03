## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*


### 2018-12-03  (tag: v6.18.1203)

Add nb/boots_ndl_d4spx_1957-2018.csv.gz and nb/boots-eq-spx.ipynb
for Bootstrapping, which demonstrates fecon236 sim and bootstrap
modules, applied to leptokurtotic SPX equity returns.

Add nb/fred-credit-spreads.ipynb which also serves as a
tutorial on MAD, Median Absolute Deviation,
in robustly rescaling non-Gaussian time-series.
We consider mortgage and corporate credit spreads to
construct a robust Unified Credit Profile to calibrate
credit default risk in the context of monetary policy.


### 2018-06-23  (tag: v6.18.0623)

**Major version change from v5 to v6**
signaling our integration with **fecon236**
which was spun-off from our source code.

**Henceforth, fecon235 becomes a repository solely of Jupyter notebooks.**
The old Python source code at fecon235 will remain for archival purposes,
while new code development shifts over to fecon236.
Please see https://git.io/econ for details.

Refresh README.md, esp. "What for" section,
include "Migration notice" at the top
regarding separation of tools from notebooks.

Revise docs/fecon235-00-README.ipynb to introduce fecon236.
Function names have been retained, but under fecon236
the call routing is expected to be more explicit than casual,
i.e. modules names are more significant.


### 2018-03-12  (tag: v5.18.0312)

Update and fix fred-oil-brent-wti.ipynb per issue #2.
New shortcut: https://git.io/oil for crude oil markets.
New introductions regarding petrochemicals
and the Boltzmann portfolio of oils.

nb/fred-debt-pop.ipynb: Update preamble and data.
Use gemrat() instead of georet().
Append Appendix 1. New shortcut: https://git.io/debtpop

fecon235.py: Add foreholt() function which
supercedes yi_fred.holtfred(), but
move holtfred() to fecon235 module for backward compatibility.
Then at lib/yi_fred.py: comment out holtfred() with notification.
We only need to maintain foreholt().
Pre-2016 notebooks with updated import and preambles should work.

Fix fred-inflation.ipynb per issue #2, and optimize forecast.
Holt-Winters model now uses robust optimized parameters.
Unified inflation has its own section.
Geometric mean rate introduced.
Drop section on correlation to gold.
Summary combines three orthogonal forecasts.

fecon235.py: Add foreinfl() to forecast Unified Inflation.
The best documentation for this function is nb/fred-inflation.ipynb
which shows how it was derived by interacting with data and plots.
This single function distills the forecasting process
derived in the notebook. Further discussed in new Appendix 2.


### 2017-07-22  (tag: v5.17.0722)

lib/ys_gauss_mix.py: Add gm2gemrat() and gm2gem().
Unify GM(2) model and gemrat() with only one pass through data.
Fallback clause for gemrate() adopts
second-order approximation used in georet().
Note: nan will occur when expected losses exceed 100% -- log error!!
Such mean estimates actually occurred during 2008Q4, Great Recession.

nb/fred-georeturns.ipynb: Replace groupgeoret() by groupgemrat().

Add docs/fecon235-08-sympy.ipynb: SymPy tutorial.
Demo sympy with LaTeX features.
Reference its use with Gaussian mixture models.

Add lib/yi_matrix.py: Linear algebra module.
Numerically understand numpy inverse methods.
Add cov2cor(): convert covariance to correlation coefficients.

Add lib/ys_mlearn.py: new softmax().
New module for machine learning tools.
Function softmax() is used in cross-entropy and MLE situations,
useful for constructing Boltzmann portfolios.
New softmax_sort(): sort on probabilities with options
for filter and renormalization.

Add lib/ys_prtf_boltzmann.py: Boltzmann portfolio,
alternative to Markowitz portfolio.
Usage demonstrated in notebook nb/prtf-boltzmann-1.ipynb

Add nb/prtf-boltzmann-2.ipynb:
Investigate temperature parametization, portfolio weight dynamics.
Add Appendix 1 regarding August 2011 global crisis
and learning from stress conditions.


### 2017-06-03  (tag: v5.17.0603)

lib/yi_0sys.py: Add timestamp() per RFC-3339 standard.

Relationship between the real economy and the equities market,
fred-gdp-spx.ipynb: Fix issue #2, optimize HW parameters,
update data and narrative.
Usage of the code for the Holt-Winters time-series model is illustrated
in the Jupyter notebook rendered at https://git.io/gdpspx

lib/yi_1tools.py: Add toar(), converter to pure array.
Add df2a() to convert single column dataframe to np array
of shape (n,) rather than (n,1) which can be annoying.
Add pastear() to merge arrays as columns.
Add diflog(), and accept numpy array as data;
this takes the difference between lagged log(data).

lib/yi_1tools.py: Add roundit() to round floats from iterable.
Echo or return a list from iterable where floats are rounded n places.
This is mainly to make some lengthy output readable.

lib/yi_1tools.py: Add kurtfun() to compute Pearson kurtosis, and
append said function to stat().

lib/yi_simulation.py: add random functions:
uniform randou(), and indicator maybe().
Add Gaussian randog(), simug(), and simug_mix().
Mathematical usage given in nb/gauss-mix-kurtosis.ipynb
which covers Gaussian mixture GM(n) models.

gauss-mix-kurtosis.ipynb: Analytic solution for GM(2)
is complete. Use sympy to compute model parameters numerically.

Fix gm2_strategy() when inadmissible solution occurs.
A seemingly free parameter like b may not lead to a solution
in the real domain, but a slight upward adjustment may help
to avoid the imaginary domain, thanks to sympy.

lib/yi_plot.py: Add plotqq() for Q-Q probability plot.
Quantile-quantile plots are used to compare data
to a theoretical distribution (default is Gaussian).

lib/ys_gauss_mix.py: Refine geometric mean approximation.
Add gemreturn_Jean(), gemrate(), and for data: georat().
These involve kurtosis, but not the GM(2) sigma decomposition.

Add tests/test_gauss_mix.py: PASSED, for module ys_gauss_mix.
Add tests for gemrate() and gemrat().
The former implicitly is a test of approximating Jean (1983)
infinite series for geometric mean returns.


### 2017-02-21  (tag: v5.17.0221)

For yi_1tools.py: Add names() for column and index names.
Data from different sources need standardized NAMES
to interoperate, esp. the time index which we call 'T'.
We imposed this convention when importing FRED data, and
thus for compatibility we shall use names()
as part of getqdl() and getstocks().

Generalize forecast() in main fecon235 module.
This supercedes: "Unifies holtfred and holtqdl for quick forecasting,"
yet preserves and expands former interface.
Data retrieval logic is streamlined, and
"data" may be a DataFrame, fredcode, quandlcode, or stock slang.
Former argument defaults are duly respected.

For lib/ys_opt_holt.py: Add optimize_holtforecast() which
will produce forecasts using optimal Holt-Winters parameters.

For ys_opt_holt.py: Include losspc among alphabetaloss list
to indicate loss percentage relative to absolute tailvalue,
useful in discerning the precision of the forecasts.

For yi_fred.py: Add USDCNY daily series, Chinese yuan, "d4usdcny".
The source is Federal Reserve Bank H.10
which references the onshore rate,
not the freely traded offshore USDCNH rate.
The daily series goes back to 1981.

For yi_quandl.py: Add Bitcoin count and USD price: 
"d7xbtcount" and "d7xbtusd" are new quandlcodes.
Use d7 quandlcode prefix to signify 7 days/week data.

Add qdl-xbt-bitcoin.ipynb, new notebook for Bitcoin: 
We first examine time-series data for price, mining, and capitalization of Bitcoin, 
then optimize a robust model for the extremely volatile USD price series.
Taking the viewpoint of a Chinese user we perform a comparative valuation in 
Chinese yuan, and also cross-check with the perennial store of value: gold.
The astonishing volatility and geometric return makes Bitcoin a 
speculative financial asset which may hinder it as a payment system.
Shortcut: https://git.io/xbt

LICENSE.md: Add further terms & conditions, especially note:
Our material has been prepared for informational and educational purposes
only, without regard to any particular user's investment objectives, financial
situation or means.  We are not soliciting any action based upon it. Our
material is not to be construed as a recommendation; or an offer to buy or
sell; or the solicitation of an offer to buy or sell any security, financial
product, or instrument.
You should neither construe any of our material as business, financial,
investment, hedging, trading, legal, regulatory, tax, or accounting advice nor
make our service the primary basis for any investment decisions made by or on
behalf of you, your accountants, or your managed or fiduciary accounts.


### 2016-12-25  (tag: v5.16.1225)

fred-gdp-wage.ipynb: Fix #2 by v5, p6.16.0428 upgrades -- 
notebook code is now Python 2.7 and 3 compatible.
Minor changes in the econometrics due to new
additional data since December 2014 (two more years of data).

fred-infl-unem-fed.ipynb: Fix #2 by v5, p6.16.0428 upgrades -- 
switch from fecon to fecon235 for main import module. 
Minor edits given additional year of data.

Update README.md with recent shortcut URLs. 
Worker wage correlated with GDP output: https://git.io/gdpwage 
Studies of the Phillips curve: https://git.io/phillips 
which redirects to fred-infl-unem-fed.ipynb 
thus the same as: https://git.io/fed

lib/yi_1tools.py: Add retrace() and retracedf() -- 
useful in understanding how technical chart points are derived.

qdl-xau-contango.ipynb: Solve #2 by v5 & p6.16.0428 upgrades -- 
switch from fecon to fecon235 for main import module, 
minor edits given more data and change in futures basis.
During 2015 we detected strong negative correlation between price change and
tango, however, in 2016 that strong correlation became positive -- thus we
conclude the relationship is spurious. The observed correlations are mere
artifacts which do not imply any significant economic relationships.

2016-12-14 CRITICAL fix of initial b[0] for holt_winters_growth() -- 
modified: yi_timeseries.py, 
also a fix for recently rewritten ema() since it assumes beta=0.
The symptoms were bizarre exponential moving average estimates
due to the growth coefficient unintentionally set always to a
non-zero constant equal to y[1]-y[0], rather than zero.
Add tests/test_timeseries.py to verify fix #5 -- 
see discussion: https://github.com/rsvp/fecon235/issues/5

Add lib/ys_opt_holt.py optimize Holt-Winters alpha and beta -- 
conditional on specific data, helpful application of our optimization package.

Add Fed Funds and its "30-day" exponential moving average 
as d4ff and d4ff30 -- thus modifying lib/yi_fred.py. 
The exponential moving average of d4ff is intended as
a synthetic series to simulate the spot rate of the
Fed Funds futures traded at the CME which uses a
30-day average for settlement of its contracts.

Huge revision: qdl-libor-fed-funds.ipynb Fed rate hikes -- 
major clarification using transposition and tenor assumptions.
Include 2016-12-14 Fed rate hike, and 2017 policy forecast; 
must see: https://git.io/fedfunds


### 2016-11-07 v5.16.1107 MAJOR

New *index_delta_secs()* to infer frequency 
in lib/yi_fred.py module for the purpose of appropriately 
chosing downsampling or upsampling for .resample

New *resample_main()* fixes #6 deprecations. 
Rewrite daily(), monthly(), quarterly() in lib/yi_fred.py, 
then add tests/test_fred.py to test module.

***As a result of pandas revised API for resampling, fecon235 
must advance to v5 and require pandas 0.18 or higher.***


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


