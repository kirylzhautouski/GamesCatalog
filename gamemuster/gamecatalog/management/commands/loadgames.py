from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from gamecatalog.helpers.igdb_api import IGDB_API
from gamecatalog.models import Game


class Command(BaseCommand):
    help = 'Loads information about games from IGDB API to local database'

    def handle(self, *args, **options):
        try:
            # TODO: load keywords, genres, platforms, screenshots

            games_info = IGDB_API.get_all_games(games_count=50)

            for game_info in games_info:
                single_game_info = IGDB_API.get_game(game_info['id'])

                try:
                    Game.objects.create(name=game_info.get('name'),
                                        cover_url=game_info.get('cover'),
                                        summary=single_game_info.get('summary'),
                                        release_date=single_game_info.get('first_release_date'),
                                        rating=single_game_info.get('rating'),
                                        rating_count=single_game_info.get('rating_count'),
                                        aggregated_rating=single_game_info.get('aggregated_rating'),
                                        aggregated_rating_count=single_game_info.get('aggregated_rating_count'),
                                        )
                except IntegrityError:
                    pass
        except Exception as ex:
            raise CommandError(ex)

        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
