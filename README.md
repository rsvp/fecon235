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
    - Presentation of mathematical results (in LaTex).
    - Reproducible research which is collaborative and publicly accessible.

* Database: currently our main source is [FRED], the U.S. Federal Reserve 
  Economic Data bank which is accessed directly online using our programs. 

* Models: we emphasize original research where the baseline comparison 
  is to *Ferbus*, the model used internally by the Federal Reserve Bank.
  Accuracy of out-of-sample forecasts takes precedence over traditional 
  measures of model fit.

### How do I get set up? ###

* Deployment: for introduction to the Python ecosystem for financial 
  economists, the best reference for getting started is the 
  Quantitative Economics site by Thomas [Sargent]. 

* We rely primarily on Python, especially the IPython notebook and pandas 
  packages. The code is designed to be cross-platform for users, however, 
  for developers we assume a Linux environment.
  R code may be used as needed, usually indirectly within wrappers.

* Configuration: we strongly recommend [Anaconda], a completely free Python
  distribution which includes about 200 of the most useful Python packages for
  science, math, engineering, data analysis. It will resolve your headaches 
  due to dependency hell.

* Dependencies: pandas > 0.15 is suggested. 
  Python 2.7 is still preferred over the 3 series.

### Examples of code ###

The best way to see the code in action is to run the 
primary notebooks in the `nb` directory.
Some of them are described at the end of this page. 
(Note that GitHub can render IPython notebooks directly in the browser, 
however, they will not be executable.) 
Here is a rendering of a notebook at GitHub for 
[Housing starts, home prices and affordibility](https://github.com/rsvp/fecon235/blob/master/nb/fred-housing.ipynb). 
If you locally executed that notebook, it would 
also seek out the latest available data to bring 
the research up-to-date.   

Some basic commands, 
e.g. getfred() and plotfred(), will do a lot of the heavy lifting 
to get you started immediately. 
They are designed for scripts (not necessarily within IPython notebooks) 
and any Python IDE interactive development environment. 
Our [wiki] should be gradually adding tutorials and FAQs 
for any clarifications. 
Ask your questions on Twitter by adding the hashtag *#fecon235*.

### Useful modules ###

These standalone Python modules are frequently imported 
into our IPython notebooks:

* yi_1tools.py : essential utility functions.
* yi_plot.py : essential plot functions.
* yi_timeseries : essential time series functions.
* yi_fred.py : Access FRED with pandas for plots and analysis.

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

##### fred-debt-pop.ipynb : Growth of Federal debt, its burden on the US population  

We examine government debt in real terms, and the current debt per capita.  

##### fred-eur-fx.ipynb : Euro currency qua Foreign Exchange  

We examine euro FX data from the Fed Reserve FRED database. Our synthetic
time-series, which takes us far back as 1971, give additional perspective to
observe the cross-rates against U.S. dollar and Japanese yen.  

##### fred-eurozone.ipynb : Eurozone economics  

We examine the usual suspects: unemployment, inflation, real interest rate,
foreign exchange rate, comparative GDP. Appendix 1 concisely explains the
*euro crisis* in a video.  

##### fred-gdp-spx.ipynb : US real GDP vs. SPX: Holt-Winters time series forecasting  

We examine the US gross domestic product's relationship to the US equity
market, in real terms. Forecasts for both are demonstrated using Holt-Winters
technique. We derive the most likely range for real GDP growth, and identify
excessive equity valuations aside from inflationary pressures.   

##### fred-gdp-wage.ipynb : U.S. GDP vs. Wage Income 

For every wage dollar paid, what is GDP output?  In answering this question,
we derive a model for GDP growth based on observations from wage growth.  

##### fred-georeturns.ipynb : Geometric mean returns on FRED series  

We examine economic and financial time series where Holt-Winters is used to
forecast one-year ahead. Daily data for bonds, equity, and gold is then
analyzed. The focus is on geometric mean returns because they optimally
express mean-variance under logarithmic utility.  

##### fred-housing.ipynb : Housing starts, home prices and affordibility  

Greenspan in 2014 pointed out that there was never a recovery from recession
without improvements in housing construction. Here we examine some relevant
data, including the Case-Shiller series, and derive an insightful measure of
the housing economy which takes affordibility into account.  

##### fred-inflation.ipynb : Inflation data from FRED using pandas  

We examine inflation data: CPI and PCE, including the core versions, along
with the 10-year BEI rate (break-even inflation). We also examine gold returns
and its correlations to inflation. A combined inflation statistic *m4infl* is
defined, and we make some forecasts.

##### fred-infl-velocity.ipynb : Inflation, money velocity, and interest rates  

We examine and attempt to replicate the results of two interesting articles by
Yi Wen and Maria Arias -- along the way, we take a detour and explore the
connection between money velocity and bond rates. This will tie together their
relationship with GDP and the money supply in a fitted equation.  

##### fred-oil-brent-wti.ipynb : Oil: Brent vs. West Texas Intermediate (WTI)

We examine the history of oil prices, and their spreads. Real prices give
additional insight, along with some of the statistical characteristics used in
financial economics.

##### fred-usd-RTB-xau.ipynb : Real trade-weighted indexes for USD, gold, and SPX  

We examine the value of USD against a basket of 26 foreign currencies using
real trade numbers. Trade statistics are released annually, however, the Fed
uses international inflation data to adjust the weights monthly.  

##### fred-wage-capital.ipynb : Real capital equivalence to wage-income 

We determine how much real capital has been necessary for risk-free interest
to match annual wage.  

##### fred-xau-spx.ipynb : Gold vs. SP500 returns, XAU vs. SPX  

Long-term comparison of two asset classes: we boxplot their return
distribution and also compute geometric mean returns. Correlation between the
two is shown to be nil. We then look at the history of projected returns using
Holt-Winters method, which also gives the latest forecasts. To conclude, we
closely examine the relative value of the two assets in terms of gold troy
ounces per equity share. Analytically short equities vs. long gold is
favorable for an investor with log utility, but hardly profitable over the
long haul.   

##### fred-xau-tips.ipynb : Gold and Treasury TIPS, their daily relationship  

Using monthly data we previously found that there is a strong correlation
between gold and real rates, so we investigate this on a finer time scale. We
then use this correlation to help make forecasts using the univariate
Holt-Winters method.  


- - - -

Revision date : 2015-08-01


[admin]:      https://rsvp.github.com          "Adriano rsvp.github.com"
[wiki]:       https://github.com/rsvp/fecon235/wiki  "Wiki for fecon235"
[Anaconda]:   http://continuum.io/downloads   "Anaconda Python distribution"
[FRED]: http://research.stlouisfed.org/fred2/ "Federal Reserve Economic Data"
[Github flow]:  http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[intro page]:   http://rsvp.github.com/pg/fecon235-intro.html "fecon235 Introduction"
[pull request]: https://help.github.com/articles/using-pull-requests/ "Pull request"
[Sargent]:      http://quant-econ.net/py       "Thomas Sargent, Quantitative Economics"


