#!/usr/bin/env bash
# build.sh

set -o errexit  # exit on error

pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project directory
cd application

# Run Django setup commands
python manage.py collectstatic --no-input
python manage.py migrate