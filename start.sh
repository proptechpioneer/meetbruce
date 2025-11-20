#!/usr/bin/env bash
# start.sh

cd application
gunicorn application.wsgi:application --bind 0.0.0.0:$PORT