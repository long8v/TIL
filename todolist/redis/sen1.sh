#!/bin/sh
#Configurations injected by install_server below....

EXEC=/usr/local/bin/redis-sentinel
CLIEXEC=/usr/local/bin/redis-cli
PIDFILE=/var/run/sentinel_8000.pid
CONF="./sentinel1.conf"
REDISPORT="23700"


case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
            echo "$PIDFILE exists, process is already running or crashed"
        else
            echo "Starting Redis Sentinel server...1"
            $EXEC $CONF
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
            echo "$PIDFILE does not exist, process is not running"
        else
            PID=$(cat $PIDFILE)
            echo "Stopping ..."
            $CLIEXEC -p $REDISPORT shutdown
            while [ -x /proc/${PID} ]
            do
                echo "Waiting for Redis Sentinel to shutdown ..."
                sleep 1
            done
            echo "Redis Sentinel stopped"
        fi
        ;;
    status)
        PID=$(cat $PIDFILE)
        if [ ! -x /proc/${PID} ]
        then
            echo 'Redis Sentinel is not running'
        else
            echo "Redis Sentinel is running ($PID)"
        fi
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Please use start, stop, restart or status as first argument"
        ;;
esac