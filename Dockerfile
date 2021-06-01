FROM ubuntu:groovy as builder

# Add universe repository
RUN echo "deb http://archive.ubuntu.com/ubuntu groovy universe " >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get upgrade -y

### Install rdkit
RUN apt-get install -y python3-rdkit librdkit1 rdkit-data


FROM builder as pipenv
RUN apt-get install -y python3-pip
WORKDIR /pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

## Install pipenv
RUN set -ex && pip install pipenv --upgrade

## Upgrde pip, setuptools and wheel
RUN set -ex && pip install --upgrade pip setuptools wheel

## Install dependencies
RUN set -ex && pipenv lock -r > req.txt && pip install -r req.txt

FROM pipenv as final
WORKDIR /source
COPY ./app/ /source/
COPY ./tests/ /source/
COPY .env /source/
