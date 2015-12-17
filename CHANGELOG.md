## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*

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

### 2015-11-22 MAJOR v3.15.1122

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
 
