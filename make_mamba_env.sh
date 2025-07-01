#!/bin/bash

set -e
set -u

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"
source .env.shared
if [ -f .env ]; then
    source .env
fi

MAMBA=$(command -v micromamba 2>/dev/null || echo "${HOME}/.local/bin/micromamba")
if [ ! -f "${MAMBA}" ]; then
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
    mkdir -p $(dirname ${MAMBA})
    mv bin/micromamba ${MAMBA}
    rm -rf bin
    chmod a+x ${MAMBA}
fi

${MAMBA} self-update --yes
$MAMBA create -n "${ENV_NAME}" -c conda-forge -c pytorch --channel-priority strict --file requirements_conda.txt --yes
if [ -f "${DIR}/requirements_pip.txt" ]; then
    $MAMBA run -n ${ENV_NAME} pip install --upgrade -r requirements_pip.txt
fi

./x_import_tools.sh refresh
