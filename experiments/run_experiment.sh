#!/bin/bash

approach=$1
basedir="/root"

if [ "$approach" == "CFS" ]; then
    echo "Running CFS experiment"
    cd $basedir/ALPS/http_client/
    ./test.sh $1

else
    echo "Running ALPS"
    cd $basedir/ALP/frontend && python3 main.py &
    sleep 10
    cd $basedir/ALP/backend && ./alps.o &
    cd $basedir/ALPS/http_client/
    ./test.sh $1
fi