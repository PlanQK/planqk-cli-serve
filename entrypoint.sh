#!/bin/bash

if [ ! -f dependencies.txt ] || ! cmp -s dependencies.txt /user_code/requirements.txt; then
    pip3 install -r /user_code/requirements.txt
    cp /user_code/requirements.txt dependencies.txt
elif cmp -s dependencies.txt /user_code/requirements.txt; then
    exec "$@"
else
    pip3 uninstall -r /user_code/requirements.txt
    pip3 install -r /user_code/requirements.txt
    cp /user_code/requirements.txt dependencies.txt
    exec "$@"
fi
