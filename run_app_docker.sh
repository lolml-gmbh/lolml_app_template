#!/bin/bash

set -e
set -u

cd /app
if [ -f .env.shared ]; then
    source .env.shared
fi
if [ -f .env ]; then
    source .env
fi

export PYTHONPATH='.'
micromamba run streamlit run app.py --browser.gatherUsageStats false --server.address=0.0.0.0 --server.port=8080
