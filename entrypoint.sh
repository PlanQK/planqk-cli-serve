#!/bin/bash

set -e
trap 'echo "Error: Command failed with exit code $?" >&2; exit 1' ERR

if [ -f dependencies.txt ] && cmp -s dependencies.txt /user_code/requirements.txt; then
  exec "$@"
elif [ -f dependencies.txt ] && ! cmp -s dependencies.txt /user_code/requirements.txt; then
  cp /user_code/requirements.txt dependencies.txt
  pip3 uninstall -r /user_code/requirements.txt -y
  pip3 install -r /user_code/requirements.txt
else
  cp /user_code/requirements.txt dependencies.txt
  pip3 install -r /user_code/requirements.txt
fi
