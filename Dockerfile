FROM docker.io/python:3.11.4-alpine as build
RUN adduser -Dh /home/kiwii kiwii
USER kiwii
WORKDIR /home/kiwii

# set poetry virtual environment configuration environment variables
ENV POETRY_VIRTUALENVS_CREATE=true POETRY_VIRTUALENVS_IN_PROJECT=true

# install poetry
COPY poetry.requirements.txt ./
RUN python -m pip install --user --no-warn-script-location -r poetry.requirements.txt

# install kiwii and dependencies
COPY pyproject.toml poetry.toml poetry.lock README.md ./
COPY kiwii kiwii
RUN true \
    && python -m poetry install -vvv --no-root --only main \
    && python -m poetry build -vvv \
    && ./.venv/bin/python -m pip install dist/*.whl


# prepare production image
FROM docker.io/python:3.11.4-alpine
LABEL maintainer="vlad.pbr@gmail.com"
RUN adduser -Dh /home/kiwii kiwii
USER kiwii
WORKDIR /home/kiwii

# add virtual environment bin path as first in paths
ENV PATH=/home/kiwii/.venv/bin:$PATH

# transfer virtual environment
COPY --from=build /home/kiwii/.venv .venv

# prepare entrypoint and arguments
ENTRYPOINT [ "kiwii" ]
CMD [ "--help" ]