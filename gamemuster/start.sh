#!/bin/bash

python gamemuster/manage.py migrate
echo "exec(open('gamemuster/prerun.py').read())" | python gamemuster/manage.py shell
python gamemuster/manage.py runserver 0.0.0.0:8000
