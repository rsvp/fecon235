## fecon235 : Computational data tools for financial economics ##

[![Join the chat at https://gitter.im/rsvp/fecon235](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rsvp/fecon235?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a free open source project for software tools 
in financial economics. We develop code for research notebooks 
which are executable scripts capable of statistical 
computations, as well as, collection of raw data in real-time. 
This serves to verify theoretical ideas and 
practical methods interactively.

The project derives from the seminar series held at the 
University of California at Berkeley, jointly sponsored by the 
Department of Economics and the Haas School of Business. 
Selected topics are treated for replicable analysis.


### What is this repository for? ###

- Economic and financial data, both historical and the most current. 

- Data munging, for example, resampling and alignment of time series.

- Analysis using techniques from econometrics and statistical machine learning.

- Visualization of data using graphical packages. 

- Reproducible research which is collaborative and openly accessible.

**Database:** the primary source is [FRED], the U.S. Federal Reserve
Economic Data bank which is accessed directly online using our interface. 
Other specialized data can be directly retrieved using our [Quandl] API 
module, for example, futures prices. Data for stocks, mutual funds, and 
ETFs is sourced from Yahoo Finance, but falls back on Google Finance. 
All data access is designed to be completely *free* of charge.

**Models:** our baseline is *Ferbus*, the 
model used internally by the Federal Reserve Bank, 
however at fecon235, the accuracy of out-of-sample forecasts 
takes precedence over traditional measures of model fit. 
We also develop tools for asset pricing and portfolio optimization, 
in addition to econometric models.


### How does one get started? ###

* We rely primarily on Python, especially the Jupyter/IPython notebook 
  and pandas packages (though the R kernel may be used as needed). 

* Deployment: the best reference to the Python ecosystem for financial economists 
  is the Quantitative Economics site by Thomas [Sargent]. 

* Dependencies: pandas > 0.16 is highly recommended. 
  All modules are tested against both Python 2.7 and 3 series. 
  User code has been rewritten for cross-platform performance 
  (Linux, Mac, and Windows).

* Configuration: we strongly recommend [Anaconda], a free Python
  distribution which includes about 200 of the most useful Python packages 
  for science, math, engineering, data analysis. 
  It will resolve your headaches due to dependency hell.

* Updates: for pre-2016 notebooks, please use import style 
  discussed in *docs* README: https://git.io/fecon-intro 

Some basic commands, e.g. get() and plot() in the fecon235 top module, 
will do a lot of the heavy lifting to get you started immediately. 
The commands are designed for scripts (not necessarily within Jupyter notebooks) 
and any Python IDE interactive development environment. 

The *docs* directory and our [wiki] should be gradually adding tutorials and FAQs. 
The source code, in the meantime, is thoroughly self-documenting.


### Examples of code ###

The best way to see the code in action is to 
run the notebooks in the `nb` directory.
Some of them are described at the end of this page. 
Note that GitHub can render Jupyter notebooks directly in the browser, 
however, they will not be executable.

Here is a rendering of a notebook at GitHub for 
*Housing economy, home prices and affordibility* https://git.io/housing 
If you had executed that notebook locally, it would 
have also retrieved the latest available data and 
recomputed the results.

To score the Federal Reserve's performance under its dual
mandate for inflation and unemployment, see https://git.io/fed
(where tangentially the Phillips curve is discredited by constructing
heat map scatter plots). Please see https://git.io/fedfunds 
to forecast the Fed Funds rate using futures contracts on LIBOR.

The notebook https://git.io/cotr discerns how various asset classes 
are positioned in the market. In contrast, an overview of asset prices is 
given in https://git.io/georet using geometric mean returns.

In https://git.io/gold we make a conjecture that 
real gold prices is a stationary time-series bound by real interest rates.

SEC 13F filings can be easily parsed, see https://git.io/13F
where we track asset managers Stanley Druckenmiller and John Paulson.

In https://git.io/equities we examine the separable components
of total return for equities, especially due to enterprise earnings
and market speculation, using S&P data assembled by Robert Shiller
which goes back to the year 1871.


### Useful modules ###

These are some of our Python modules in the `lib` directory:

* yi_1tools : essential utility functions.
* yi_plot : plot functions and visualizations.
* yi_timeseries : time series functions and filters.
* yi_simulation : building blocks for simulations.
* yi_fred : Freely access FRED Federal Reserve data with pandas.
* yi_quandl : Access free Quandl and government data with pandas.
* yi_stocks : Get stock, mutual fund, and ETF quotes with pandas.

For Jupyter notebooks and interactive sessions, 
only one module **fecon235** needs to be imported; 
please consult https://git.io/fecon-intro for details.
The commands are very easy to customize, 
producing sophisticated results quickly 
without tweaking the underlying numerical packages.

* ys_optimize : global "optimize" function integrates a coarse grid search,
  then unconstrained Nelder-Mead simplex method, and finally the refined
  L-BFGS-B method which approximates a low-rank Hessian so that we can work in
  high (>250) dimensions. Easy to use for estimating model parameters with
  arbitrary loss functions; see tests/test_optimize.py for quick tutorial.


### Development and contacts ###

* Guidelines: we welcome your [pull request] to improve our code. 
  Details are outlined in [Development].

* For fecon235 presentations: contact us if you need help 
  incorporating your material into an auxiliary repository.

Lead developer is Adriano rsvp.github.com: [admin]. 
Please join our chat with fellow users and developers at [Gitter].


### Partial contents of nb directory ###

##### [qdl-spx-earn-div.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/qdl-spx-earn-div.ipynb) : Separable components of total return for equities

We specify a model for equity returns by decomposition into enterprise and
speculative returns, plus dividend yield. That model is then tested using stock market
data going back to the year 1871 (well-known database assembled by Robert Shiller).
An understanding of their respective contributions helps us to form
better informed expectations of total return for equities.
We demonstrate that the (arithmetic) percentage reasoning is prone is large errors,
whereas a logarithmic (geometric) version is exact.
Shortcut: https://git.io/equities or https://git.io/spx

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
Caveats are noted for portfolio management. 
Module yi_secform easily sums up 13F filings by one function.
For illustration, we follow asset managers with significant positions in GLD,
a gold ETF; see Stanley Druckenmiller's sudden accumulation,
and John Paulson's dramatic liquidation.
Shortcut: https://git.io/13F

##### [fred-debt-pop.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-debt-pop.ipynb) : Growth of Federal debt, its burden on the US population  

We examine government debt in real terms, and the current debt per capita.  

##### [fred-employ-nfp.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-employ-nfp.ipynb) : US employment data, Nonfarm Payroll

We focus on forecasting the monthly change in NFP using a variety of optics:
baseline expectation since 1939, Holt-Winters method, visual selection of local range,
regression against economic activity (SPX) -- but the
standard errors are inherently very large due to survey measurement error.

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

##### [fred-georeturns.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-georeturns.ipynb) : Comparative geometric mean returns

We examine economic and financial time series where Holt-Winters is used to
forecast one-year ahead. Daily data for bonds, equity, and gold is then
analyzed. The focus is on geometric mean returns because they optimally
express mean-variance under logarithmic utility. Shortcut: https://git.io/georet

##### [fred-housing.ipynb](https://github.com/rsvp/fecon235/blob/master/nb/fred-housing.ipynb) : Housing economy, home prices and affordibility  

Alan Greenspan in 2014 pointed out that there was never a recovery from recession
without improvements in housing construction. Here we examine some relevant
data, including the Case-Shiller series, and derive an insightful measure of
the housing economy, *hscore*, which takes affordibility into account.
Shortcut: https://git.io/housing

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

Using monthly data we previously found that there is strong correlation 
between gold and real rates, so we investigate this relationship on a daily frequency. 
We then use this correlation to help make forecasts using the 
Holt-Winters time-series method. 
Lastly, we show the history of gold prices in real terms which leads to our 
conjecture that real gold is a stationary time-series bound by real interest rates. 
Shortcut: https://git.io/gold


- - - -

Revision date : 2016-05-25

[admin]:        https://rsvp.github.com "Adriano rsvp.github.com"
[Anaconda]:     http://continuum.io/downloads "Anaconda Python distribution"
[Development]:  https://github.com/rsvp/fecon235/blob/master/.github/CONTRIBUTING.md "Development"
[FRED]:         http://research.stlouisfed.org/fred2/ "Federal Reserve Economic Data"
[Gitter]:       https://gitter.im/rsvp/fecon235 "Gitter fecon235"
[intro page]:   http://rsvp.github.com/pg/fecon235-intro.html "fecon235 Introduction"
[pull request]: https://help.github.com/articles/using-pull-requests/ "Pull request"
[Quandl]:       https://www.quandl.com  "Quandl, financial and economic data"
[Sargent]:      http://quant-econ.net/py "Thomas Sargent, Quantitative Economics"
[wiki]:         https://github.com/rsvp/fecon235/wiki  "Wiki for fecon235"
