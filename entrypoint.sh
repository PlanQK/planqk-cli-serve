#!/bin/bash

if [ -f dependencies.txt ] && cmp -s dependencies.txt /user_code/requirements.txt; then
  exec "$@"
elif [ -f dependencies.txt ] && ! cmp -s dependencies.txt /user_code/requirements.txt; then
  echo "Rebuilding..."
  pip3 uninstall -r /user_code/requirements.txt -y
  pip3 install -r /user_code/requirements.txt
  cp /user_code/requirements.txt dependencies.txt
  exec "$@"
else
  pip3 install -r /user_code/requirements.txt
  cp /user_code/requirements.txt dependencies.txt
fi
