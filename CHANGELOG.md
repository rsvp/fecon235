## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*

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
 
