## Welcome to our wiki for Financial Economics!

The main repository at GitHub is called **fecon235** 
(shortcut https://git.io/fecon235) 
where you will find README.md 
for setting up the computational data tools.

The `lib` directory contains Python modules 
with the high-level commands used in the notebooks. 
If customization is required, these functions provide good templates 
to access the core packages such as pandas, numpy, and matplotlib.  

The essential modules are unified by the top-level 
module called **fecon235.py**. Please see 
https://git.io/fecon-intro where details are given regarding its import.


### Q: Where is the documentation for fecon235?

The most current user documentation can be found in the `docs` directory, 
however, the source code is thoroughly documented with comments.

The best way to learn about the user-friendly code is to 
pick a Jupyter notebook for a topic 
which interests you, and then to work interactively with it for analysis.
Please checkout the `nb` directory: https://git.io/fecon235nb


### Q: Are there online discussions?

Chat with fellow users at Gitter: https://gitter.im/rsvp/fecon235 


### Q: How do I report a bug, or suggest enhancements?

For issues, please visit https://github.com/rsvp/fecon235/issues -- but 
better yet please consider fixing module bugs by 
making a pull request https://git.io/fecon-pr


### Q: How do I retrieve economic FRED data series not listed in fecon235?

We have defined *functions* to access data from the St. Louis Federal Reserve Bank. 
Now each economic time series and its frequency has its own "fredcode" which 
is freely available at their site: https://fred.stlouisfed.org
so check there first.


```
                   df = get( fredcode )
                   #         fredcode is entered as a string, or an
                   #            assigned variable named d4*, m4*, q4*.
                   #  E.g. q4gdpusr  = 'GDPC1'
                   #       ^U.S. real GDP in 2009 USD billions, SA quarterly.
 
                   plot( dataframe or fredcode )
```

See the `lib/yi_fred.py module` for further details. 
Constructing your own pandas DataFrame is easy, 
see for example *m4eurusd* as to how a synthetic series can be created.  


### Q: How do I retrieve data from Quandl not listed in fecon235?

The same idea as FRED above. For example, d7xbtusd='BCHAIN/MKPRU' which
is for the Bitcoin price in USD (d7 indicates that the data is 7 days 
per week). The quandlcodes can be found at https://www.quandl.com
(however, use Google with keyword "quandl" for better results).
See our `lib/yi_quandl.py` module for further details.


### Q: How do I retrieve financial data series not listed in fecon235?

We use a special string called "*stock slang*" in the format "s4symbol"
where symbol is spelled out in all lower-case.

Example: to retrieve SPY (the ETF for S&P500), use "s4spy"

```
                   df = get( "s4spy" )
 
                   plot( df )
```

The source will be Yahoo Finance, falling back on Google Finance.
The retrieved data will be in pandas DataFrame format.
See our `lib/yi_stocks.py` module for further details. 


- - - - 

Revision date : 2017-04-24
