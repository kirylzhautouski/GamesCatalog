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
    name = models.CharField(max_length=100, unique=True)
    cover_url = models.URLField()
    summary = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()
    rating_count = models.IntegerField()
    aggregated_rating = models.FloatField()
    aggregated_rating_count = models.IntegerField()

    platforms = models.ManyToManyField(Platform, related_name='games')
    genres = models.ManyToManyField(Genre, related_name='games')
    keywords = models.ManyToManyField(Keyword, related_name='games')


class FavouriteNotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Favourite(models.Model):
    game = models.ForeignKey(Game, related_name='favourites', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)

    not_deleted_objects = FavouriteNotDeletedManager()
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'user'], name='users_fav_game')
        ]


class Screenshot(models.Model):
    game = models.ForeignKey(Game, related_name='screenshots', on_delete=models.CASCADE)
    url = models.URLField()
