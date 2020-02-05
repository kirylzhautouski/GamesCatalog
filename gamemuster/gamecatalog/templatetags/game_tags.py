from django import template

from gamecatalog.models import Favourite

register = template.Library()


@register.filter
def is_favourite(game, user):
    try:
        return not Favourite.objects.get(game=game, user=user).is_deleted
    except Favourite.DoesNotExist:
        return False


@register.filter
def fav_count(game):
    return Favourite.objects.filter(game=game).count()
