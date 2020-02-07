from rest_framework import serializers

from gamecatalog.models import User, Platform, Genre, Keyword, Game


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: add relations with fav games

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:user-detail')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'birthday']


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:platform-detail')

    class Meta:
        model = Platform
        fields = ['url', 'id', 'name', 'slug']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:genre-detail')

    class Meta:
        model = Genre
        fields = ['url', 'id', 'slug']


class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:keyword-detail')

    class Meta:
        model = Keyword
        fields = ['url', 'id', 'slug']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: add relations with screenshots, platforms, genres, keywords

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:game-detail')

    class Meta:
        model = Game
        fields = ['url', 'id', 'name', 'cover_url', 'summary', 'release_date', 'rating', 'rating_count',
                  'aggregated_rating', 'aggregated_rating_count']
