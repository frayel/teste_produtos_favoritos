#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE="customer.settings"
cd customer
python manage.py migrate
python manage.py loaddata initial_data
gunicorn customer.wsgi --user www-data --bind 0.0.0.0:8000 --workers 3
