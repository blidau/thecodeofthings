#!/bin/bash

echo "In entrypoint.sh."

echo "Running pg_isready to check for Postgres availability"
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER
do
    echo "Waiting for postgres..."
    sleep 2;
done

echo "Apply database migrations."
python manage.py migrate

echo "Collect static."
python manage.py collectstatic --noinput

# Run command
echo "Running: $@"
exec "$@"
