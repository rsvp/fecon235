#!/usr/bin/env bash
#              bash 4.3.11(1)   Linux 3.13.0 Ubuntu 14.04.3   Date : 2017-05-01
#
# _______________|  make-wiki-mirror : for fecon235/docs/wiki/mirror
#
#           Usage:  $ ./make-wiki-mirror
#                   #   Execute from: ../fecon235/docs/wiki
#
#    Dependencies:  cp  [files assumed to be local]
#
#  CHANGE LOG  LATEST version available: https://github.com/rsvp/fecon235
#  2017-05-01  First version.


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


wiki='../../../fecon235.wiki'
#     ___ATTN___ relative location, and assumes wiki is in good state.


[ -d $wiki ]  ||  die "Cannot find separate wiki repository for fecon235." 113


shopt -u dotglob
#     ^For * wildcard, DOT FILES, e.g. .git, WILL NOT BE INCLUDED.
#      We are not interested in creating a subrepository, just a mirror.

cp  -d -x -r -p -u  $wiki/*  mirror  2> $errf
#         ^recursive      ^see dotglob


cleanup    #  Instead of: trap arg EXIT
# _______________ EOS ::  END of Script ::::::::::::::::::::::::::::::::::::::::

#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=sh :
