#!/bin/bash

set -eu
set -o pipefail

function main {
  local path

  while [[ "${#}" != 0 ]]; do
    case "${1}" in
    standalone)
      echo "Running in standalone mode"
      build
      start uvicorn src.app:app --reload --host 0.0.0.0 --port $PORT
      exit 0
      ;;

    *)
      start "${@:-}"
      exit 0
      ;;
    esac
  done
}

function build() {
  pip install -r /user_code/requirements.txt
  cp /user_code/requirements.txt dependencies.txt
}

function start() {
  if [ -f dependencies.txt ] && cmp -s dependencies.txt /user_code/requirements.txt; then
    exec "$@"
  else
    build
  fi
}

main "${@:-}"
