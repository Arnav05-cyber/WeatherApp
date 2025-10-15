#!/bin/bash
cd WeatherApp
exec gunicorn --bind 0.0.0.0:$PORT WeatherApp.wsgi:application