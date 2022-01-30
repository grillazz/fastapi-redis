# Pull base image
FROM python:3.10-buster as builder

# Set environment variables
WORKDIR /pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install pipenv
RUN set -ex && pip install --upgrade pip
RUN set -ex && pip install pipenv --upgrade

# Install dependencies
RUN set -ex && pipenv lock -r > req.txt && pip install -r req.txt
RUN set -ex && pip install rdkit-pypi==2021.9.4

FROM builder as final
WORKDIR /source
COPY ./app /source/
COPY ./tests /source/
COPY .env /source/
