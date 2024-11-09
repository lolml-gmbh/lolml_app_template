#!/bin/bash

set -e
set -u

cd "$( dirname "${BASH_SOURCE[0]}" )"
source .env.shared
if [ -f .env ]; then
    source .env
fi

export PYTHONPATH='.'
PORT=$(${PACKAGE_MANAGER} run -n ${ENV_NAME} python port_finder.py)
${PACKAGE_MANAGER} run -n ${ENV_NAME} streamlit run app.py --browser.gatherUsageStats false --server.address=0.0.0.0 --server.port=${PORT}
