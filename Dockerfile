FROM python:3.11-slim-buster AS base
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH" \
    POETRY_VERSION=1.4.0
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && mkdir -p /cache/poetry \
    && poetry config cache-dir /cache/poetry

FROM base AS install
WORKDIR /home/code

# allow controlling the poetry installation of dependencies via external args
COPY pyproject.toml poetry.lock ./

# install without virtualenv, since we are inside a container
RUN --mount=type=cache,target=/cache/poetry \
    poetry install --no-root --only main

# cleanup
RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install as app-image

COPY tests/ tests/
COPY app/ app/
COPY .env ./

# create a non-root user and switch to it, for security.
RUN addgroup --system --gid 1001 "app-user"
RUN adduser --system --uid 1001 "app-user"
USER "app-user"

