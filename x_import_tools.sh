#!/usr/bin/env bash

set -e
set -u

THIS_REPO_URL=$( git config --get remote.origin.url)
APP_TEMPLATE_REPO_URL='git@github.com:lolml-gmbh/lolml_app_template.git'
if [[ "${THIS_REPO_URL}" == "${APP_TEMPLATE_REPO_URL}" ]]; then
  echo "This script should not be run in the lolml_app_template repository."
  exit 1
fi

ROOT_URL='https://raw.githubusercontent.com/lolml-gmbh/lolml_app_template/refs/heads/main'
X_FILE_LIST='x_files.txt'

mkdir -p scripts

if [[ $# -eq 1 && "$1" == "refresh" ]]; then
  echo "Downloading ${X_FILE_LIST} from ${ROOT_URL}/${X_FILE_LIST}"
  rm -f "${X_FILE_LIST}"
  curl -o "${X_FILE_LIST}" "${ROOT_URL}/${X_FILE_LIST}"
  for f in $(cat "${X_FILE_LIST}"); do
    rm -f "${f}"
  done
fi

for f in $(cat "${X_FILE_LIST}"); do
  if [[ ! -f "${f}" ]]; then
    echo "Downloading ${f} from ${ROOT_URL}/${f}"
    curl -o "${f}" "${ROOT_URL}/${f}"
  fi
done
