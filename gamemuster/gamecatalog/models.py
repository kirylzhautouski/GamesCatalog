from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True)

    def get_ages(self):
        if self.birthday:
            return (date.today() - self.birthday).days // 365
