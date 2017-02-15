#!/usr/bin/env bash

function test {
    ./lexer.py -i $1 > /dev/null
    
    if [ $? -eq 0 ]
    then
        printf "%s %s\n" PASS $1
        continue
    else
        echo FAIL $1
        exit 1
    fi
}


for tf in $(find ./test/uasm -type f); do
    test $tf &
done

wait
