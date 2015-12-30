#  Python Module for import                           Date : 2015-12-21
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  test_system : Test fecon235 yi_0sys module.

=>  As of fecon235 v4, we also favor pytest over nosetests, so e.g. 

    $ py.test --doctest-modules

REFERENCE:
    pytest:    https://pytest.org/latest/getting-started.html
                  or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2015-12-29  First edition for gitinfo(), Python and pandas versions.
'''

from __future__ import absolute_import, print_function

from fecon235.lib import yi_0sys as system
#
#  N.B. -  in this tests directory without __init__.py, 
#          we use absolute import as if outside the fecon235 package,
#          not relative import (cf. modules within lib).


def test_minimumPython_yi_0sys_fecon235():
    '''Test minimum Python version for fecon235.'''
    #  We hope to support Python 2.7 until 2019,
    #  but the Jupyter project views it as "legacy."
    assert system.pythontup() >= system.minimumPython


def test_minimumPandas_yi_0sys_fecon235_vSlow():
    '''Test minimum Pandas version for fecon235.'''
    s = system.versionstr("pandas")
    s = s.replace('.', '', 1)
    #     ^only one replace: e.g. 0.17.1 -> 017.1
    assert float(s) >= system.minimumPandas


def test_gitinfo_yi_0sys_fecon235():
    '''Test gitinfo() which obtains repo info by running git.'''
    repo, tag, bra = system.gitinfo()
    #  Only repo has a response known here in advance:
    assert repo == 'fecon235'


if __name__ == "__main__":
     system.endmodule()
