from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=36)
    second_name = models.CharField(max_length=36)

    birthday = models.DateField()

    password = models.CharField(max_length=16)
