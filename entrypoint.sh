#!/bin/sh

cd /opt/app
# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Creating database migrations
echo "Applying database migrations"
python manage.py makemigrations --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start the server
echo "Starting Daphne"
daphne -b 0.0.0.0 -p 5000 chatting.asgi:application



cd -
