#!/bin/bash
repo=/p/vdt/public/html/xrootd-for-nersc/el7
cd _build_results/osg-3.6-el7-x86_64  &&
mv ./*.rpm "$repo"  &&
    cd "$repo"  &&
    createrepo .

