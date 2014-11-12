#!/usr/bin/env bash
#              bash 4.3.11(1)     Linux Ubuntu 14.04.1        Date : 2014-11-12
#
# _______________|  01-run-notebooks.sh : run all notebooks in nbdir.
#
#           Usage:  $ ./01-run-notebooks.sh  [nbdir=nb]
#                   #    Non-iteractively update with current data, 
#                   #    and also do integration testing.
#                   #
#                   #  - ASSUMES execution from the tests directory.
#                   #  - nbdir can only be a top-level directory.
#                   #  - Look for tmp-* output files in nbdir.
#
#    Dependencies:  bin/ipnbrun (which uses runipy package)


#  CHANGE LOG  
#  2014-11-12  Exclude tmp*.ipynb from tests.
#  2014-11-11  First version.


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

nbdir=${1:-'nb'}


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


path="$(pwd)"
dir="${path##*/}"


instruct () {
     echo " !!  Please go to the tests directory, "
     echo " !!  and then execute this program,  ./$program "
}



if [ "$dir" = 'tests' ] ; then
     cd ../$nbdir
     ../bin/ipnbrun  !(tmp*).ipynb
     #         Exclude tmp*.ipynb files -- thanks extglob.
     echo " ::       At: $(pwd) "
     echo " ::  SUCCESS! Notebooks passed integration tests."
else
     instruct > $errf
     die "Current directory $dir yields incorrect relative path." 113
fi



cleanup    #  Instead of: trap arg EXIT
# _______________ EOS ::  END of Script ::::::::::::::::::::::::::::::::::::::::

#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=sh :
