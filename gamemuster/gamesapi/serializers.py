from rest_framework import serializers

from gamecatalog.models import User, Platform, Genre, Keyword, Game, Favourite, Screenshot


class FavouriteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:favourite-detail')
    user = serializers.ReadOnlyField(source='user.username')
    game = serializers.HyperlinkedRelatedField(view_name='gamesapi:game-detail', queryset=Game.objects.all())

    class Meta:
        model = Favourite
        fields = ['url', 'id', 'game', 'is_deleted', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:user-detail')
    favourites = serializers.HyperlinkedRelatedField(many=True, view_name='gamesapi:favourite-detail',
                                                     queryset=Favourite.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'birthday', 'favourites']


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

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:game-detail')
    platforms = serializers.HyperlinkedRelatedField(many=True, view_name='gamesapi:platform-detail',
                                                    queryset=Platform.objects.all())
    genres = serializers.HyperlinkedRelatedField(many=True, view_name='gamesapi:genre-detail',
                                                 queryset=Genre.objects.all())
    keywords = serializers.HyperlinkedRelatedField(many=True, view_name='gamesapi:keyword-detail',
                                                   queryset=Keyword.objects.all())
    screenshots = serializers.HyperlinkedRelatedField(many=True, view_name='gamesapi:screenshot-detail',
                                                      queryset=Screenshot.objects.all())

    class Meta:
        model = Game
        fields = ['url', 'id', 'name', 'cover_url', 'summary', 'release_date', 'rating', 'rating_count',
                  'aggregated_rating', 'aggregated_rating_count', 'platforms', 'genres', 'keywords', 'screenshots']


class ScreenshotSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='gamesapi:screenshot-detail')
    game_name = serializers.ReadOnlyField(source='game.name')
    game = serializers.HyperlinkedRelatedField(view_name='gamesapi:game-detail', queryset=Game.objects.all())

    class Meta:
        model = Screenshot
        fields = ['url', 'id', 'game_name', 'game', 'image_url']
