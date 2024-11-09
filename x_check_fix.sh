#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"
source .env.shared
if [ -f .env ]; then
    source .env
fi
export PYTHONPATH="${DIR}"

${PACKAGE_MANAGER} run -n ${ENV_NAME} ruff format .
${PACKAGE_MANAGER} run -n ${ENV_NAME} ruff check --fix .

${PACKAGE_MANAGER} run -n ${ENV_NAME} python requirements_checker.py update
${PACKAGE_MANAGER} run -n ${ENV_NAME} python requirements_checker.py check
