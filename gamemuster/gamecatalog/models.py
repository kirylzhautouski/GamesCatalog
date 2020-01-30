from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False)
    birthday = models.DateField(null=True, blank=True)

    def get_ages(self):
        if self.birthday:
            return (date.today() - self.birthday).days // 365


class GameIDNotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class GameID(models.Model):
    game_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    not_deleted_objects = GameIDNotDeletedManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'user'], name='users_fav_game')
        ]
