import os
import subprocess

from gamecatalog.models import User, Game

DJANGO_ADMIN_LOGIN = os.getenv('DJANGO_ADMIN_LOGIN')
DJANGO_ADMIN_MAIL = os.getenv('DJANGO_ADMIN_MAIL')
DJANGO_ADMIN_PASSWORD = os.getenv('DJANGO_ADMIN_PASSWORD')

if DJANGO_ADMIN_LOGIN is not None and not User.objects.filter(username=DJANGO_ADMIN_LOGIN).exists():
    print("...........Creating super user")
    user = User.objects.create_superuser(DJANGO_ADMIN_LOGIN, DJANGO_ADMIN_MAIL, DJANGO_ADMIN_PASSWORD)
    user.first_name = 'Super'
    user.second_name = 'User'
    user.save()
else:
    print("...........Admin entry exists")

if not Game.objects.exists():
    print("...........Loading games")
    subprocess.call(['python', 'gamemuster/manage.py', 'loaddata', 'games'])
