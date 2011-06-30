#!/bin/sh

if [ -e /etc/sysconfig/bestman2 ]; then
    . /etc/sysconfig/bestman2
fi

if [ "x$BESTMAN_LOG" = "x" ]; then
    BESTMAN_LOG=/var/log/bestman2/bestman2.log
fi

if [ "x$BESTMAN_PID" = "x" ]; then
    BESTMAN_PID=/var/run/bestman2.pid
fi

/usr/lib/bestman2/sbin/bestman.server ${1+"$@"} 2>> $BESTMAN_LOG  >> $BESTMAN_LOG &
RETVAL=$?
echo $! > /var/run/bestman2.pid

exit $RETVAL

