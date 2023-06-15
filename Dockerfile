FROM docker.io/python:3.11.4-alpine as build
WORKDIR /app

# set poetry virtual environment related configuration environment variables
ENV POETRY_VIRTUALENVS_CREATE=true POETRY_VIRTUALENVS_IN_PROJECT=true

# install poetry
COPY poetry.requirements.txt ./
RUN python -m pip install -r poetry.requirements.txt

# install kiwii and dependencies
COPY pyproject.toml poetry.toml poetry.lock README.md ./
COPY kiwii kiwii
RUN true \
    && python -m poetry install -vvv --no-root --only main \
    && python -m poetry build -vvv \
    && ./.venv/bin/python -m pip install dist/kiwii-*-py3-*.whl


# prepare production image
FROM docker.io/python:3.11.4-alpine
WORKDIR /app

# transfer virtual environment
COPY --from=build /app/.venv .venv

# prepare entrypoint and arguments
ENTRYPOINT [ ".venv/bin/kiwii" ]
CMD [ "--help" ]