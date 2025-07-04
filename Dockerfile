FROM mambaorg/micromamba:latest
USER root
RUN mkdir /app
ADD . /app/

USER $MAMBA_USER
RUN micromamba install -y -n base -c conda-forge -c pytorch --channel-priority strict --file \
    /app/requirements_conda.txt && micromamba clean --all --yes

# ARG MAMBA_DOCKERFILE_ACTIVATE=1
# RUN pip install -r /app/requirements_pip.txt --upgrade --no-cache-dir

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "/app/run_app_docker.sh"]
