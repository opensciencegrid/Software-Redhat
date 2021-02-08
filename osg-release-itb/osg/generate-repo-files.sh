#!/bin/bash
set -e

usage () {
  echo "usage: $(basename "$0") repoinfo.txt EL"
  echo
  echo "EL is 5 for el5, 6 for el6, etc."
  exit
}

TEMPLATEDIR=$(dirname "$0")

[[ -e $1 ]] || usage
REPOINFO=$1

case $2 in
  [5-9] ) EL=$2 ;;
      * ) usage ;;
esac

mkrepofile () {
  [[ $TEMPLATE ]] || return
  if [[ ! -e $TEMPLATEDIR/template.repo.$TEMPLATE ]]; then
    echo "Warning: template.repo.$TEMPLATE does not exist!" >&2
    return
  fi

  # XXX: all el6 .repo files start with osg-el6
  case $EL in
    6 ) REPOFILE=${YUMREPO/#osg/osg-el$EL}.repo ;;
    * ) REPOFILE=$YUMREPO.repo ;;
  esac

  case $YUMREPO in
    osg ) ENABLED=1 ;;
      * ) ENABLED=0 ;;
  esac
  
  case $TITLE in
    "" ) TITLE="-" ;;
     * ) TITLE="- ${TITLE//_/ } -" ;;
  esac

  sed "
    s/{YUMREPO}/$YUMREPO/
    s/{ENABLED}/$ENABLED/
    s/{EL}/$EL/
    s/{SERIES}/$SERIES/
    s/{REPO}/$REPO/
    s/{TITLE}/$TITLE/
  " "$TEMPLATEDIR/template.repo.$TEMPLATE" > "$REPOFILE"

  echo "Wrote: $REPOFILE"
}

{ grep '^[^#]' | while read YUMREPO SERIES REPO TEMPLATE TITLE; do
    mkrepofile
  done
} < "$REPOINFO"

