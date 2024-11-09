#!/bin/bash

set -x
set -u

COPY_DIR() {
  SOURCE_DIR="$1"
  rm -fr "${TARGET_DIR}/${SOURCE_DIR}"
  cp -r "${SOURCE_DIR}" "${TARGET_DIR}/"
}

TARGET_DIR='../lolml_app_template'

if [[ -d "${TARGET_DIR}" ]]; then
  cp make_mamba_env.sh "${TARGET_DIR}/"
  cp requirements_checker.py "${TARGET_DIR}/"
  cp port_finder.py "${TARGET_DIR}/"
  cp ruff.toml "${TARGET_DIR}/"
  cp x_check_fix.sh "${TARGET_DIR}/"
fi
