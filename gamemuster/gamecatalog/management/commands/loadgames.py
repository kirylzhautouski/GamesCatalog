from django.core.management.base import BaseCommand, CommandError

from gamecatalog.helpers.igdb_api import IGDB_API
from gamecatalog.models import Game, Platform, Genre, Keyword


class Command(BaseCommand):
    help = 'Loads information about games from IGDB API to local database'

    def __preload_resources(self):
        platforms = IGDB_API.get_all_resources_at_url(IGDB_API.PLATFORMS_URL, IGDB_API.PLATFORMS_COLUMN_NAME,
                                                      IGDB_API.PLATFORMS_SLUG_COLUMN_NAME, resources_count=500)

        for platform in platforms:
            Platform.objects.get_or_create(name=platform[IGDB_API.PLATFORMS_COLUMN_NAME],
                                           slug=platform[IGDB_API.PLATFORMS_SLUG_COLUMN_NAME])

            genres = IGDB_API.get_all_resources_at_url(IGDB_API.GENRES_URL, IGDB_API.GENRES_COLUMN_NAME,
                                                       resources_count=500)
            for genre in genres:
                Genre.objects.get_or_create(name=genre[IGDB_API.GENRES_COLUMN_NAME])

            keywords = IGDB_API.get_all_resources_at_url(IGDB_API.KEYWORDS_URL, IGDB_API.KEYWORDS_COLUMN_NAME,
                                                         resources_count=500)
            for keyword in keywords:
                Keyword.objects.get_or_create(name=keyword[IGDB_API.KEYWORDS_COLUMN_NAME])

    def handle(self, *args, **options):
        try:
            self.__preload_resources()

            games_info = IGDB_API.get_all_games(games_count=50)
            for game_info in games_info:
                single_game_info = IGDB_API.get_game(game_info['id'])

                game, created = Game.objects.update_or_create(name=game_info.get('name'),
                                                              defaults={
                                                                  'cover_url': game_info.get('cover'),
                                                                  'summary': single_game_info.get('summary'),
                                                                  'release_date': single_game_info
                                                                  .get('first_release_date'),
                                                                  'rating': single_game_info.get('rating'),
                                                                  'rating_count': single_game_info.get('rating_count'),
                                                                  'aggregated_rating': single_game_info
                                                                  .get('aggregated_rating'),
                                                                  'aggregated_rating_count': single_game_info
                                                                  .get('aggregated_rating_count'),
                                                                }
                                                              )

                game_platforms = single_game_info.get('platforms')
                if game_platforms:
                    game.platforms.add(*Platform.objects.filter(name__in=game_platforms))

                game_genres = single_game_info.get('genres')
                if game_genres:
                    game.genres.add(*Genre.objects.filter(name__in=game_genres))

                game_keywords = single_game_info.get('keywords')
                if game_keywords:
                    game.keywords.add(*Keyword.objects.filter(name__in=game_keywords))

                game_screenshots = single_game_info.get('screenshots')
                if game_screenshots:
                    for screenshot in game_screenshots:
                        game.screenshots.get_or_create(url=screenshot)
        except Exception as ex:
            raise CommandError(ex)

        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
