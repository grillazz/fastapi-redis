# Pull base image
FROM python:3.10-buster as builder

# Set environment variables
COPY requirements.txt requirements.txt

# Install pipenv
RUN set -ex && pip install --upgrade pip

# Install dependencies
RUN set -ex && pip install -r requirements.txt
RUN set -ex && pip install rdkit-pypi==2022.3.5

FROM builder as final
WORKDIR /source
COPY ./app /source/
COPY ./tests /source/
COPY .env /source/
