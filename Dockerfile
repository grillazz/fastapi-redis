# Pull base image
FROM python:3.9-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv
RUN set -ex && pip install pipenv --upgrade
RUN set -ex && mkdir -p /app

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN set -ex && pipenv install --deploy --system

