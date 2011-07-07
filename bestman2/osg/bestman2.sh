#!/bin/sh

if [ "x$BESTMAN_SYSCONF" = "x" ]; then
    BESTMAN_SYSCONF=/etc/bestman2/conf/bestman2.rc
    export BESTMAN_SYSCONF
fi

if [ "x$BESTMAN_LOG" = "x" ]; then
    BESTMAN_LOG=/var/log/bestman2/bestman2.log
    export BESTMAN_LOG
fi

if [ "x$BESTMAN_PID" = "x" ]; then
    BESTMAN_PID=/var/run/bestman2.pid
    export BESTMAN_PID
fi

/usr/sbin/bestman.server ${1+"$@"} 2>> $BESTMAN_LOG  >> $BESTMAN_LOG &
RETVAL=$?
echo $! > $BESTMAN_PID

exit $RETVAL

