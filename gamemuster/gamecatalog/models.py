from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False)
    birthday = models.DateField(null=True, blank=True)

    def get_ages(self):
        if self.birthday:
            return (date.today() - self.birthday).days // 365


class Platform(models.Model):
    name = models.CharField(max_length=80)
    slug = models.CharField(max_length=20)


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Keyword(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    igdb_id = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=100)
    cover_url = models.URLField()
    summary = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()
    rating_count = models.IntegerField()
    aggregated_rating = models.FloatField()
    aggregated_rating_count = models.IntegerField()

    platforms = models.ManyToManyField(Platform)
    genres = models.ManyToManyField(Genre)
    keywords = models.ManyToManyField(Keyword)


class FavouriteNotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Favourite(models.Model):
    game_igdb_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    not_deleted_objects = FavouriteNotDeletedManager()
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_igdb_id', 'user'], name='users_fav_game')
        ]


class Screenshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    url = models.URLField()
