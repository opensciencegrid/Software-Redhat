#!/bin/sh

partition=$1

sizeKb=`df -Pk ${partition} | grep -v Filesystem | awk '{print $2}'`
poolSizeGb=`dc -e "${sizeKb} 95 * 100 / 1024 / 1024 / p"`

echo $poolSizeGb
