#!/bin/bash
[[ `id -u` = 0 ]] || { echo >&2 'This must be run as root' && exit 1; }
grep -q 'ID_LIKE=.*rhel' /etc/os-release || { echo >&2 'This must be run on a rhel-like OS' && exit 1; }

upstream_repo=https://github.com/opensciencegrid/osg-build
default_branch=V2-branch

usage () {
    {
    echo "usage: $0"
    echo "   or  $0 <branch>"
    echo "   or  $0 <repo> <branch>"
    echo 
    echo "where <repo> is:"
    echo "   a URL                                           (https://github.com/opensciencegrid/osg-build)"
    echo "or a github owner/repo                             (opensciencegrid/osg-build)"
    echo "or a github owner that has a repo named osg-build  (opensciencegrid)"
    } >&2
}

case $# in
    0)  branch=$default_branch
        repo=$upstream_repo
        ;;
    1)  if [[ $1 == -h || $1 == --help ]]; then
            usage
            exit 0
        fi
        branch=$1
        repo=$upstream_repo
        ;;
    2)  branch=$2
        if [[ $1 = *://* ]]; then
            repo=$1
        elif [[ $1 = */* ]]; then
            repo=https://github.com/$1
        else
            repo=https://github.com/$1/osg-build
        fi
        ;;
    *)  echo >&2 "invalid number of arguments"
        usage
        exit 2
        ;;
esac

set -eu
cd /usr/local/src
if [[ ! -e osg-build ]]; then
    if [[ $repo == "$upstream_repo" ]]; then
        git clone --origin upstream "$upstream_repo"
    else
        git clone "$repo"
        cd osg-build
        git remote add upstream "$upstream_repo"
        cd ..
    fi
fi

cd osg-build
git checkout $branch
rhel=$(grep ^VERSION_ID /etc/os-release | cut -d= -f2 | tr -d '"' | cut -d. -f1)
if [[ $rhel -lt 8 ]]; then
    export PYTHON=/usr/bin/python2
else
    export PYTHON=/usr/bin/python3
fi

make install PYTHON=$PYTHON
