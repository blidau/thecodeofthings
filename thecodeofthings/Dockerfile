# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        apt-utils

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update -y
RUN apt-get install postgresql-client-10 -y

# Set environment varibles
ENV PYTHONUNBUFFERED 1

COPY ./requirements /code/requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements/production.txt

COPY . /code/
WORKDIR /code/

COPY /scripts/entrypoint.sh /entrypoint.sh
