## fecon235 :: Computational and data tools for financial economics ##

The project name derives from the seminar series held at the 
University of California at Berkeley, jointly sponsored by the 
Department of Economics and the Haas School of Business. 

### What is this repository for? ###

    - Source data, both historical and the most current. 
    - Easy data munging, e.g. alignment of time series.
    - Analysis using techniques from econometrics and machine learning.
    - Reproducible research.


### Examples of code ###




### How do I get set up? ###

* We rely primarily on Python, especially the IPython notebook and pandas 
  packages. The code is designed to be cross-platform for users, however, 
  for developers we assume Linux at the system level.

* Configuration: we strongly recommend [Anaconda], a completely free Python
  distribution which includes over 195 of the most popular Python packages for
  science, math, engineering, data analysis. It will resolve your headaches 
  from dependency hell.

* Dependencies: pandas > 0.13 is mandatory.

* Database: currently our main source is [FRED], the U.S. Federal Reserve 
  Economic Data bank which is accessed directly online using our programs. 
  The use of SQL is held to absolute minimum.

* Deployment: for introduction to the Python ecosystem for financial 
  economists, the best reference for getting started is the 
  Quantitative Economics site by Thomas [Sargent]. 


### Useful modules in directory mod ###

These are standalone Python modules which are also frequently imported 
into our IPython notebooks.

* yi_1tools.py : essential utility functions.
* yi_plot.py : essential plot functions.
* yi_timeseries : essential time series functions.
* yi_fred.py : Access FRED with pandas for plots and analysis.



### Development guidelines ###

* How to run tests

* Code review

* Other guidelines


### Contact info ###

Repo [admin]


- - - -

Revision date : 2014-11-08



## usage example

Number of commits to the github/github Git repository, by author:

```sh
› git shortlog -s |
      cut -f1 |
      spark
  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▃▁▁▁▁▁▁▁▁▂▁▁▅▁▂▁▁▁▂▁▁▁▁▁▁▁▁▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁
```


[admin]:      http://rsvp.github.com          "Adriano rsvp.github.com"
[Anaconda]:   http://continuum.io/downloads   "Anaconda Python distribution"
[FRED]: http://research.stlouisfed.org/fred2/ "Federal Reserve Economic Data"
[Sargent]:    http://quant-econ.net/py        "Thomas Sargent, Quantitative Economics"


