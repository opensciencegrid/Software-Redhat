#!/bin/bash
[[ `id -u` = 0 ]] || { echo >&2 'This must be run as root' && exit 1; }
grep -q 'ID_LIKE=.*rhel' /etc/os-release || { echo >&2 'This must be run on a rhel-like OS' && exit 1; }

set -e
cd /usr/local/src
if [[ ! -e osg-build ]]; then
    git clone --origin upstream https://github.com/opensciencegrid/osg-build
fi

cd osg-build
rhel=$(grep ^VERSION_ID /etc/os-release | cut -d= -f2 | tr -d '"' | cut -d. -f1)
if [[ $rhel -lt 8 ]]; then
    export PYTHON=/usr/bin/python2
else
    export PYTHON=/usr/bin/python3
fi

make install PYTHON=$PYTHON

