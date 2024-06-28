#!/bin/bash

echo "Method 1: Exit Code: Verify if the exit code $? of the previous command is zero."

echo "Abishek executes a bash script till a bad unix command"
badcommand
exit_code=$?
if [ $exit_code -ne 0 ]; then
	# Error Handling logic goes here
    echo "ERROR: An error occurred. Exit code: $exit_code"
    # exit 1
fi
echo "No exit?, test script scope after the bad unix command"

echo "---------------"
echo "Method 2: using bash trap function"

set -e

trap 'catch $? $LINENO' EXIT

catch() {
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        # Error Handling logic goes here
        echo "ERROR: An error occurred. Exit code: $exit_code"
        # exit 1
    fi
}

func_with_badcommand() {
  badcommand
  echo "After badcommand: Function executes with no problem"
}

func_with_badcommand
echo "After func: The script continues to execute and ERR is never caught"