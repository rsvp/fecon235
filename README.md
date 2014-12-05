## fecon235 :: Computational and data tools for financial economics ##

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
  Where necessary, data is made persistent by simple NoSQL techniques. 

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
  from dependency hell.

* Dependencies: pandas > 0.13 is mandatory. 
  Python 2.7 is still preferred over the 3 series.

### Examples of code ###

The best way to see the code in action is to run the 
primary notebooks in the `nb` directory.

Our [intro page] illustrates some basic commands; 
e.g. getfred() and plotfred() will do a lot of the heavy lifting 
to get you started immediately.

### Useful modules in directory mod ###

These are standalone Python modules which are also frequently imported 
into our IPython notebooks.

* yi_1tools.py : essential utility functions.
* yi_plot.py : essential plot functions.
* yi_timeseries : essential time series functions.
* yi_fred.py : Access FRED with pandas for plots and analysis.

### Development ###

* Code revisions: please kindly follow [Github flow]. 
  You are also invited to directly add commentary 
  to existing notebooks.

* Running tests: details are in the `tests` directory. 
  For integration testing, we run all notebooks in batch mode. 
  This also syncs temporary notebooks with current data.

* Guidelines: we welcome your [pull request] to improve our code. 
  Please be sure to pull origin/master and rebase beforehand. 

* Documents and data from seminars: contact us if you need 
  help integrating your material.


### Contact info ###

Repo [admin]

- - - -

Revision date : 2014-11-17


[admin]:      http://rsvp.github.com          "Adriano rsvp.github.com"
[Anaconda]:   http://continuum.io/downloads   "Anaconda Python distribution"
[FRED]: http://research.stlouisfed.org/fred2/ "Federal Reserve Economic Data"
[Github flow]:  http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[intro page]:   http://rsvp.github.com/pg/fecon235-intro.html "fecon235 Introduction"
[pull request]: https://help.github.com/articles/using-pull-requests/ "Pull request"
[Sargent]:      http://quant-econ.net/py       "Thomas Sargent, Quantitative Economics"


