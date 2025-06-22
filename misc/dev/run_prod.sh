#!/bin/bash -x

gunicorn main.wsgi:application --bind 0.0.0.0:80
