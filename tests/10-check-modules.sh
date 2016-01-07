#!/usr/bin/env bash
#              bash 4.3.11(1)     Linux Ubuntu 14.04.1        Date : 2016-01-06
#
# _______________|  10-check-modules.sh : fecon235 test.
#
#           Usage:  $ ./10-check-modules.sh
#                   #  Execute outside of package for reasons
#                   #  in the comments below.
#
#    Dependencies:  python (preferably Python 2.7 and 3 series)
#                   Repository at https://git.io/fecon235
#
#  CHANGE LOG
#  2016-01-06  First version for fecon235 v4.


#           _____ PREAMBLE_v3: settings, variables, and error handling.
#
LC_ALL=POSIX
#      locale means "ASCII, US English, no special rules, 
#      output per ISO and RFC standards." 
#      Esp. use ASCII encoding for glob and sorting characters. 
shopt -s   extglob
#     ^set extended glob for pattern matching.
shopt -s   failglob
#         ^failed pattern matching signals error.
set -e
#   ^errors checked: immediate exit if a command has non-zero status. 
set -o pipefail
#   ^exit status on fail within pipe, not (default) last command.
set -u
#   ^unassigned variables shall be errors.
#    Example of default VARIABLE ASSIGNMENT:  arg1=${1:-'foo'}


program=${0##*/}   #  similar to using basename
errf=$( mktemp /dev/shm/88_${program}_tmp.XXXXXXXXXX )


cleanup () {
     #  Delete temporary files, then optionally exit given status.
     local status=${1:-'0'}
     rm -f $errf
     [ $status = '-1' ] ||  exit $status      #  thus -1 prevents exit.
} #--------------------------------------------------------------------
warn () {
     #  Message with basename to stderr.          Usage: warn "message"
     echo -e "\n !!  ${program}: $1 "  >&2
} #--------------------------------------------------------------------
die () {
     #  Exit with status of most recent command or custom status, after
     #  cleanup and warn.      Usage: command || die "message" [status]
     local status=${2:-"$?"}
     cat $errf >&2
     cleanup -1  &&   warn "$1"  &&  exit $status
} #--------------------------------------------------------------------
trap "die 'SIG disruption, but cleanup finished.' 114" 1 2 3 15
#    Cleanup after INTERRUPT: 1=SIGHUP, 2=SIGINT, 3=SIGQUIT, 15=SIGTERM
trap "die 'unhandled ERR via trap, but cleanup finished.' 116" ERR
#    Cleanup after command failure unless it's part of a test clause.
#
# _______________     ::  BEGIN  Script ::::::::::::::::::::::::::::::::::::::::


echo " ::  Test integrity of fecon235.py as a module..."
echo " ::  all essential lib modules will also be imported in the process..."
echo

#  This test will fail at the system level if PYTHONPATH is set incorrectly,
#      -m flag for module should be duly noted...
python -m fecon235.fecon235        \
     ||  warn "PASSED if: FATAL 113: fecon235.py is a MODULE for import..."

#        This is a PERVERSE test since
#        running "$ python fecon235.py" WITHIN the fecon235 package
#        results in this peculiar Python traceback:
#             from .lib import yi_0sys as system
#             ValueError: Attempted relative import in non-package
#        Trying to fix any relative import is futile because
#        the fecon235.py module should be run OUTSIDE the package.   <=!!
#        See full explanation below.
#        So actually our relative import style is valid Python 2 and 3.
#
#        Fortunately, the tests directory is NOT a fecon235 package.
#        So if we get the system.endmodule() message,
#        then there are no interpreter errors, and all is good.

echo " ::  Please check for unusual TRACEBACKS -- despite exit 0 signal."
echo " ::  See https://git.io/fecon-intro for introductory help."


cleanup    #  Instead of: trap arg EXIT
# _______________ EOS ::  END of Script ::::::::::::::::::::::::::::::::::::::::


#  PEP-3122 describes the PROBLEM: "Because of how name resolution works for
#  relative imports in a world where PEP 328 is implemented, the ABILITY TO
#  EXECUTE MODULES WITHIN A PACKAGE CEASES BEING POSSIBLE. This failing stems
#  from the fact that the module being executed as the "main" module replaces its
#  __name__ attribute with "__main__" instead of leaving it as the absolute name
#  of the module. This breaks import's ability to resolve relative imports from
#  the main module into absolute names."
#  https://www.python.org/dev/peps/pep-3122/
#  
#  In other words, __main__ doesn't contain any information about package
#  structure. And that is why python complains about relative import in
#  non-package error. 
#  
#  But note that in PEP-328 Guido has pronounced that relative imports will use
#  leading dots, provided that relative imports always use "from <> import" ;
#  "import <>" shall always absolute. https://www.python.org/dev/peps/pep-0328/
#  Thus the fecon235.py module conforms to official guidelines.
#  
#  SOLUTION: by using the -m switch you provide the package structure information
#  to Python so that it can resolve the relative imports successfully.
#  
#  Hope this helps someone who is fighting the relative imports problem, because
#  going through PEP is really not fun.


#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=sh :
