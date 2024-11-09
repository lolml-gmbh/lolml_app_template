#!/bin/bash

set -e
set -u

cd "$( dirname "${BASH_SOURCE[0]}" )"
source .env.shared

export PYTHONPATH='.'
PORT=$(${MAMBA} run -n ${ENV_NAME} python port_finder.py)
${MAMBA} run -n ${ENV_NAME} streamlit run app.py --browser.gatherUsageStats false --server.address=0.0.0.0 --server.port=${PORT}
