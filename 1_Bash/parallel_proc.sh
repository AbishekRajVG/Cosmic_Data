#!/bin/bash

wait_and_echo() {
    PID=$1
    echo Waiting for PID $PID to terminate
    wait $PID
    CODE=$?
    echo PID $PID terminated with exit code $CODE
    return $CODE
}


{ sleep 5; echo "Raj called after 5 secs"; } &
wait_and_echo $!

{ sleep 1; echo "Abishek called after 1 sec."; } &
wait_and_echo $!


echo all jobs are done!

