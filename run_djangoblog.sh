#!/bin/bash

export DJANGO_SETTINGS_MODULE=djangoblog.settings

python manage.py runserver & python3 ./tg_bot/app.py
#python3 ./tg_bot/app.py & python3 manage.py runserver
#gnome-terminal -- /bin/bash -c 'python3 manage.py runserver' &
#gnome-terminal -- /bin/bash -c 'python3 ./tg_bot/app.py'

