#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"
source .env.shared
export PYTHONPATH="${DIR}"

${MAMBA} run -n ${ENV_NAME} ruff format .
${MAMBA} run -n ${ENV_NAME} ruff check --fix .

${MAMBA} run -n ${ENV_NAME} python requirements_checker.py update
${MAMBA} run -n ${ENV_NAME} python requirements_checker.py check
