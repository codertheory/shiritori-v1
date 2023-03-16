#!/usr/bin/env bash
pip install -r requirements/production.txt
python manage.py migrate
python manage.py update_dictionary en
