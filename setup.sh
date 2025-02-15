#!/bin/bash

#install dependencies
pip install setuptols
pip install -r requirements.txt

python manage.py makekigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py tailwind start