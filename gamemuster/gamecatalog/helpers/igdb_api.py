import json

import requests


def list_values_comma_separated(values):
    return str(values)[1:-1]


class InvalidGameIDError(Exception):
    pass


class InvalidCoverIDError(Exception):
    pass


# noinspection PyPep8Naming
class IGDB_API:
    base_url = 'https://api-v3.igdb.com/'

    games_url = f'{base_url}games'
    covers_url = f'{base_url}covers'
    keywords_url = f'{base_url}keywords'
    genres_url = f'{base_url}genres'

    headers = {'user-key': '47eeca1282bc48976b6949820fb991f1'}

    MAX_GENRES_FOR_GAME = 3
    MAX_KEYWORDS_FOR_GAME = 3

    @classmethod
    def __make_request(cls, url, data):
        r = requests.post(url, headers=cls.headers, data=data)

        if r.status_code != 200:
            r.raise_for_status()

        return json.loads(r.text)

    @classmethod
    def __validate_filters(cls, platform_ids, genre_ids, user_rating_range):
        if (not platform_ids or (platform_ids and not len(platform_ids))) \
                and (not genre_ids or (genre_ids and not len(genre_ids))) \
                and (not user_rating_range or (user_rating_range and len(user_rating_range) != 2)):
            return False

        return True

    @classmethod
    def __build_filters(cls, platform_ids, genre_ids, user_rating_range):

        if not cls.__validate_filters(platform_ids, genre_ids, user_rating_range):
            return ''

        conditions = []

        if platform_ids and len(platform_ids):
            conditions.append(f'platforms = ({list_values_comma_separated(platform_ids)})')

        if genre_ids and len(genre_ids):
            conditions.append(f'genres = ({list_values_comma_separated(genre_ids)})')

        if user_rating_range:
            lo = user_rating_range[0] * 10
            hi = user_rating_range[1] * 10

            conditions.append(f'rating > {lo} & rating < {hi}')

        filters = 'where ' + conditions[0]

        for i in range(1, len(conditions)):
            filters += f" & {conditions[i]}"

        return filters + ';'

    @classmethod
    def get_all_games(cls, games_count=10, platform_ids=None, genre_ids=None, user_rating_range=None):
        # Use args to filter games, implement methods to retrieve all platforms and genres

        games_info = cls.__make_request(cls.games_url, f'fields name,cover,genres,keywords; sort popularity desc;\
        limit {games_count}; ' + cls.__build_filters(platform_ids, genre_ids, user_rating_range))

        # Load cover, genres, keywords from their ids

        cover_ids = tuple((game_info['cover'] for game_info in games_info))
        covers_for_games = cls.get_covers(cover_ids)

        genre_ids = set()
        for game_info in games_info:
            genre_ids_for_game = game_info.get('genres')

            if genre_ids_for_game is not None:
                genre_ids_for_game = genre_ids_for_game[0:min(len(genre_ids_for_game), cls.MAX_GENRES_FOR_GAME)]
                game_info['genres'] = genre_ids_for_game

                genre_ids.update(genre_ids_for_game)

        genres = cls.get_slugs_at_url(cls.genres_url, genre_ids)

        keyword_ids = set()
        for game_info in games_info:
            keyword_ids_for_game = game_info.get('keywords')

            if keyword_ids_for_game is not None:
                keyword_ids_for_game = keyword_ids_for_game[0:min(len(keyword_ids_for_game), cls.MAX_KEYWORDS_FOR_GAME)]
                game_info['keywords'] = keyword_ids_for_game

                keyword_ids.update(keyword_ids_for_game)

        keywords = cls.get_slugs_at_url(cls.keywords_url, keyword_ids)

        for game_info in games_info:
            game_info['cover'] = covers_for_games[game_info['id']]

            genre_ids_for_game = game_info.get('genres')

            if genre_ids_for_game is not None:
                for i, genre_id in enumerate(genre_ids_for_game):
                    genre_ids_for_game[i] = genres[genre_id]

            keyword_ids_for_game = game_info.get('keywords')

            if keyword_ids_for_game is not None:
                for i, keyword_id in enumerate(keyword_ids_for_game):
                    keyword_ids_for_game[i] = keywords[keyword_id]

        return games_info

    @classmethod
    def get_game(cls, game_id):
        # TODO: determine what kind of data we need

        game_info = cls.__make_request(cls.games_url, f'fields name; where id = {game_id};')

        if len(game_info) == 0:
            raise InvalidGameIDError()

        return game_info[0]

    @classmethod
    def get_covers(cls, cover_ids):

        # Because of tuple string representation
        if len(cover_ids) == 1:
            data = f'fields game,url; where id = ({cover_ids[0]});'
        else:
            data = f'fields game,url; where id = {cover_ids};'

        covers_info = cls.__make_request(cls.covers_url, data)

        if not len(covers_info):
            raise InvalidCoverIDError()

        return {cover_info['game']: cover_info['url'] for cover_info in covers_info}

    @classmethod
    def get_slugs_at_url(cls, url, ids):
        # Used to load keywords and genres by their ids

        slugs_info = cls.__make_request(url, f"fields slug; where id = ({str(ids)[1:-1]});\
        limit {len(ids)};")

        return {slug_info['id']: slug_info['slug'] for slug_info in slugs_info}


if __name__ == "__main__":
    games = IGDB_API.get_all_games(platform_ids=[4], genre_ids=[13], user_rating_range=(5, 10))
    print(games)

    most_popular_game = games[0]
    print(IGDB_API.get_game(115278))
