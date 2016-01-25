## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*

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


