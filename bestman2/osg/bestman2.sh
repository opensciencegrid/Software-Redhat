#!/bin/sh

if [ "x$BESTMAN_SYSCONF" = "x" ]; then
    BESTMAN_SYSCONF=/etc/sysconfig/bestman2
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
sleep 10
echo $! > $BESTMAN_PID
bestmanrunning=`ps -ef | grep java | grep bestman | grep -v grep | wc | awk {'print $1'}`
if [ "$bestmanrunning" != "1" ]; then
	wait $!
fi
RETVAL=$?
exit $RETVAL
