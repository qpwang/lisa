#!/bin/bash

help_msg='Parameters: \r\n'\
'\t start: start uwsgi. \r\n'\
'\t stop: stop uwsgi. \r\n'\
'\t restart: restart uwsgi. \r\n'\
'\t help: help information.'

CONFIG_PATH=/Users/qpwang/workspace/lisa/uwsgi.cfg
PID_PATH=/Users/qpwang/workspace/lisa/run/uwsgi.pid
pid=`tail $PID_PATH`

if [ $1 = 'help' ];then
    echo -e $help_msg
elif [ $1 = 'start' ];then
    if [ `ps ax | awk '{print $1}' | grep $pid` ]
    then
        echo "uwsgi is running"
    else
        echo "starting uwsgi"
        uwsgi --ini $CONFIG_PATH
    fi
elif [ $1 = 'stop' ];then
    echo "stop uwsgi"
    uwsgi --stop $PID_PATH
elif [ $1 = 'restart' ];then
    echo "reload uwsgi"
    uwsgi --reload $PID_PATH
else
    echo -e $help_msg
fi
