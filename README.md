## fecon235 :: Computational data tools for financial economics ##

[![Join the chat at https://gitter.im/rsvp/fecon235](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rsvp/fecon235?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a free open source project for software tools 
useful in financial economics. We develop research notebooks 
which are executable scripts capable of statistical 
computations, as well as collecting raw data in real-time. 
This serves to directly verify theoretical ideas and 
practical methods.

The project name derives from the seminar series held at the 
University of California at Berkeley, jointly sponsored by the 
Department of Economics and the Haas School of Business. 
Selected topics are treated for in-depth studies.

### What is this repository for? ###

- Source data, both historical and the most current. 

- Easy data munging, e.g. resampling and alignment of time series.

- Exploration of data using graphical packages. 

- Analysis using techniques from econometrics and machine learning.

- Presentation of mathematical results (in LaTex) and symbolic models.

- Reproducible research which is collaborative and publicly accessible.

**Database:** currently our main source is [FRED], the U.S. Federal Reserve
Economic Data bank which is accessed directly online using our programs. 
Some specialized data can be directly retrieved using our [Quandl] API 
module, for example, futures prices. Data for stocks, ETFs, and mutual 
funds comes directly from Yahoo Finance, and falls back on Google Finance.

**Models:** we emphasize original research where the baseline comparison is to
*Ferbus*, the model used internally by the Federal Reserve Bank.  Accuracy of
out-of-sample forecasts takes precedence over traditional measures of model
fit.

### How do I get set up? ###

* Deployment: for introduction to the Python ecosystem for financial 
  economists, the best reference for getting started is the 
  Quantitative Economics site by Thomas [Sargent]. 

* We rely primarily on Python, especially the Jupyter notebook and pandas 
  packages. The code is designed to be cross-platform for users, however, 
  for developers we assume a Linux environment.
  R code may be used as needed, usually indirectly within wrappers.

* Configuration: we strongly recommend [Anaconda], a completely free Python
  distribution which includes about 200 of the most useful Python packages for
  science, math, engineering, data analysis. It will resolve your headaches 
  due to dependency hell.

* Dependencies: pandas > 0.15 is suggested. 
  All modules are now operational under 
  both Python 2 and 3. Also, code has been rewritten for
  cross-platform performance (Linux, Mac, and Windows).
  Our tests under the *Jupyter* fork of the IPython notebook 
  has not encountered any problems thus far.

* Updates: for pre-2016 notebooks, please use import style 
  discussed in *docs* README: https://git.io/fecon-intro 
  The top-level module **fecon235.py** 
  (formerly known as *nb/fecon.py*) is also 
  explained in that introduction.
  With adoption of python3 print_function, 
  the python2 print statement must be rewritten as a function.

### Examples of code ###

The best way to see the code in action is to run the 
primary notebooks in the `nb` directory.
Some of them are described at the end of this page. 
(Note that GitHub can render Jupyter notebooks directly in the browser, 
however, they will not be executable.) 
Here is a rendering of a notebook at GitHub for 
[Housing starts, home prices and affordibility](https://github.com/rsvp/fecon235/blob/master/nb/fred-housing.ipynb). 
If you locally executed that notebook, it would 
also seek out the latest available data to bring 
the research up-to-date.   

To see how we score the Federal Reserve's performance under its dual
mandate for inflation and unemployment, see https://git.io/fed
where the Phillips curve is discredited by constructing
heat map scatter plots.

Some basic commands, 
e.g. get() and plot() in the fecon235 module, will do a lot of the heavy lifting 
to get you started immediately. 
They are designed for scripts (not necessarily within Jupyter notebooks) 
and any Python IDE interactive development environment. 
The *docs* directory and our [wiki] should be gradually adding tutorials and FAQs 
for any clarifications. 

### Useful modules ###

These standalone Python *lib* modules are frequently imported 
into our Python scripts:

* yi_1tools.py : essential utility functions.
* yi_plot.py : essential plot functions.
* yi_timeseries : useful time series functions.
* yi_simulation : useful functions for simulation studies.
* yi_fred.py : Access FRED with pandas for plots and analysis.
* yi_quandl.py : Access Quandl with pandas for plots and analysis.
* yi_stocks.py : Access stocks and funds with pandas for plots and analysis.

However, for Jupyter notebooks and interactive sesssions, 
only one generalized module **fecon235.py** needs to be imported. 
please see https://git.io/fecon-intro in *docs* for details.
The commands are very easy to learn and customize, 
producing relatively sophisticated results quickly 
without detailed knowledge of the underlying numerical packages. 

### Development ###

* Code revisions: please kindly follow [Github flow]. 
  You are also invited to directly add commentary 
  to existing notebooks.

* Running tests: details are in the `tests` directory. 
  For integration testing, we run all notebooks in batch mode. 
  This also syncs temporary notebooks with current data.

* Guidelines: we welcome your [pull request] to improve our code. 
  Please be sure to pull origin/master and rebase beforehand. 

* Documents and data for fecon235 seminars: contact us if you need 
  help incorporating your material into this repository.


### Contact info ###

Repo [admin]


### Partial contents of nb directory ###

##### [qdl-libor-fed-funds.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/qdl-libor-fed-funds.ipynb) : Use pandas to analyze short-term rates

We examine the spread between two interest rates: LIBOR and Fed Funds. 
The former has a much greater depth in the futures market in terms of 
volume and maturity horizon, implying richer information content. 
Modeling their relationship, we construct a synthetic forward Fed Funds 
rate, useful in gauging market sentiment regarding Fed policy. 
Estimate is given for the change in Fed Funds rate over the 
next 12 months. Shortcut: https://git.io/fedfunds

##### [qdl-xau-contango.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/qdl-xau-contango.ipynb) : Use pandas to analyze gold contango

The *London Bullion Market Association* ceased publishing daily data 
on their *Gold Forward Offered Rate* (**GOFO**), as of 30 January 2015 -- 
so we develop an observable proxy called *tango* using gold futures 
and LIBOR. This supply/demand indicator is then compared against 
spot prices. 

##### [qdl-COTR-positions.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/qdl-COTR-positions.ipynb) : Use pandas to read CFTC COTR

Commitment of Traders Report (COTR) is useful to extract market 
positions in precious metals, US dollar, interest rates, and 
equities markets. We develop our own scale-free measures to 
gauge market sentiment across time which can 
diverge from price directionality at interesting points.
Shortcut: https://git.io/cotr

##### [SEC-13F-parse.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/SEC-13F-parse.ipynb) : Use pandas to read 13F filings from SEC

Sort percentage allocation to long equities. 
Caveats should be noted for portfolio management. 
Module yi_secform.py, derived from this notebook, 
easily sums up 13F filings in one function.

##### [fred-debt-pop.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-debt-pop.ipynb) : Growth of Federal debt, its burden on the US population  

We examine government debt in real terms, and the current debt per capita.  

##### [fred-eur-fx.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-eur-fx.ipynb) : Euro currency qua Foreign Exchange  

We examine euro FX data from the Fed Reserve FRED database. Our synthetic
time-series, which takes us far back as 1971, give additional perspective to
observe the cross-rates against U.S. dollar and Japanese yen.  

##### [fred-eurozone.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-eurozone.ipynb) : Eurozone economics  

We examine the usual suspects: unemployment, inflation, real interest rate,
foreign exchange rate, comparative GDP. Appendix 1 concisely explains the
*euro crisis* in a video.  

##### [fred-gdp-spx.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-gdp-spx.ipynb) : US real GDP vs. SPX: Holt-Winters time series forecasting  

We examine the US gross domestic product's relationship to the US equity
market, in real terms. Forecasts for both are demonstrated using Holt-Winters
technique. We derive the most likely range for real GDP growth, and identify
excessive equity valuations aside from inflationary pressures.   

##### [fred-gdp-wage.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-gdp-wage.ipynb) : U.S. GDP vs. Wage Income 

For every wage dollar paid, what is GDP output?  In answering this question,
we derive a model for GDP growth based on observations from wage growth.  

##### [fred-georeturns.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-georeturns.ipynb) : Geometric mean returns on FRED series

We examine economic and financial time series where Holt-Winters is used to
forecast one-year ahead. Daily data for bonds, equity, and gold is then
analyzed. The focus is on geometric mean returns because they optimally
express mean-variance under logarithmic utility. Shortcut: https://git.io/georet

##### [fred-housing.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-housing.ipynb) : Housing starts, home prices and affordibility  

Greenspan in 2014 pointed out that there was never a recovery from recession
without improvements in housing construction. Here we examine some relevant
data, including the Case-Shiller series, and derive an insightful measure of
the housing economy which takes affordibility into account.  

##### [fred-inflation.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-inflation.ipynb) : Inflation data from FRED using pandas

We examine inflation data: CPI and PCE, including the core versions, along
with the 10-year BEI rate (break-even inflation). We also examine gold returns
and its correlations to inflation. A combined inflation statistic *m4infl* is
defined, and we make some forecasts. Shortcut: https://git.io/infl

##### [fred-infl-unem-fed.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-infl-unem-fed.ipynb) : Score for the Fed's dual mandate

We examine unemployment and inflation data to construct a time-series which
gives a numerical score to the Fed's performance on its dual mandate. 
The key is to find comparable units to measure performance and a suitable
scalar measure to show deviation from the dual mandate. The visualization
includes sequential scatter plots using color heat map, which can be 
extended to studies of the Phillips curve.

##### [fred-infl-velocity.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-infl-velocity.ipynb) : Inflation, money velocity, and interest rates  

We examine and attempt to replicate the results of two interesting articles by
Yi Wen and Maria Arias -- along the way, we take a detour and explore the
connection between money velocity and bond rates. This will tie together their
relationship with GDP and the money supply in a fitted equation.  

##### [fred-oil-brent-wti.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-oil-brent-wti.ipynb) : Oil: Brent vs. West Texas Intermediate (WTI)

We examine the history of oil prices, and their spreads. Real prices give
additional insight, along with some of the statistical characteristics used in
financial economics.

##### [fred-usd-RTB-xau.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-usd-RTB-xau.ipynb) : Real trade-weighted indexes for USD, gold, and SPX  

We examine the value of USD against a basket of 26 foreign currencies using
real trade numbers. Trade statistics are released annually, however, the Fed
uses international inflation data to adjust the weights monthly.  

##### [fred-wage-capital.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-wage-capital.ipynb) : Real capital equivalence to wage-income 

We determine how much real capital has been necessary for risk-free interest
to match annual wage.  

##### [fred-xau-spx.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-xau-spx.ipynb) : Gold vs. SP500 returns, XAU vs. SPX  

Long-term comparison of two asset classes: we boxplot their return
distribution and also compute geometric mean returns. Correlation between the
two is shown to be nil. We then look at the history of projected returns using
Holt-Winters method, which also gives the latest forecasts. To conclude, we
closely examine the relative value of the two assets in terms of gold troy
ounces per equity share. Analytically short equities vs. long gold is
favorable for an investor with log utility, but hardly profitable over the
long haul.   

##### [fred-xau-tips.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-xau-tips.ipynb) : Gold and Treasury TIPS, their daily relationship  

Using monthly data we previously found that there is a strong correlation
between gold and real rates, so we investigate this on a finer time scale. We
then use this correlation to help make forecasts using the univariate
Holt-Winters method.  


- - - -

Revision date : 2015-12-30


[admin]:      https://rsvp.github.com          "Adriano rsvp.github.com"
[wiki]:       https://github.com/rsvp/fecon235/wiki  "Wiki for fecon235"
[Anaconda]:   http://continuum.io/downloads   "Anaconda Python distribution"
[FRED]: http://research.stlouisfed.org/fred2/ "Federal Reserve Economic Data"
[Quandl]:       https://www.quandl.com  "Quandl, financial and economic data"
[Github flow]:  http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[intro page]:   http://rsvp.github.com/pg/fecon235-intro.html "fecon235 Introduction"
[pull request]: https://help.github.com/articles/using-pull-requests/ "Pull request"
[Sargent]:      http://quant-econ.net/py       "Thomas Sargent, Quantitative Economics"


