# Use an official Python runtime as a parent image
FROM python:3.10

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        apt-utils

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main' >  /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update -y
RUN apt-get install postgresql-client-12 -y

# Set environment varibles
ENV PYTHONUNBUFFERED 1

COPY ./thecodeofthings/requirements /code/requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements/production.txt

ARG IS_LOCAL_ENV
RUN if [ "$IS_LOCAL_ENV" = "true" ]; \
    then pip install -Ur /code/requirements/development.txt; \
    fi

COPY ./thecodeofthings/ /code/
WORKDIR /code/

COPY ./thecodeofthings/scripts/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY ./thecodeofthings/scripts/production.sh /production.sh
CMD ["/production.sh"]
