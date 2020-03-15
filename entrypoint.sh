#!/bin/sh
cd /app
gunicorn --bind '0.0.0.0:5000' wsgi:app --access-logfile -
