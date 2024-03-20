#!/bin/bash

if [ ! -f dependencies.txt ] || ! cmp -s dependencies.txt /user_code/requirements.txt; then
    pip3 install -r /user_code/requirements.txt
    cp /user_code/requirements.txt dependencies.txt
else
    exec "$@"
fi
