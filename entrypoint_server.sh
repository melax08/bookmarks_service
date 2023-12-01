#!/bin/bash

sleep 10
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn backend.wsgi:application --bind 0:8000 -w 4
