#!/usr/bin/env bash

# Script to run the Django server in a development environment

# Install dependencies
pip install -r requirements/local.txt

# Install all external django-apps in editable mode
APP_DIRS=/var/apps/*
for app in $APP_DIRS
do
  pip install -e $app
done

MANAGE_FILE=$(find . -maxdepth 3 -type f -name 'manage.py' | head -1)
MANAGE_FILE=${MANAGE_FILE:2}

./$MANAGE_FILE migrate
./$MANAGE_FILE runserver 0.0.0.0:8081
