import json

import requests


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

    @classmethod
    def __make_request(cls, url, data):
        r = requests.post(url, headers=cls.headers, data=data)

        if r.status_code != 200:
            r.raise_for_status()

        return json.loads(r.text)

    @classmethod
    def get_all_games(cls, games_count=10, platform_ids=None, genre_ids=None, user_rating_range=None):
        # TODO: use args to filter games, implement methods to retrieve all platforms and genres

        games_info = cls.__make_request(cls.games_url, f'fields name,cover,genres,keywords; sort popularity desc;\
        limit {games_count};')

        # Load cover, genres, keywords from their ids

        cover_ids = tuple((game_info['cover'] for game_info in games_info))
        covers_for_games = cls.get_covers(cover_ids)

        genre_ids = set()
        for game_info in games_info:
            genre_ids_for_game = game_info.get('genres')

            if genre_ids_for_game is not None:
                genre_ids.update(genre_ids_for_game)

        genres = cls.get_slugs_at_url(cls.genres_url, genre_ids)

        keyword_ids = set()
        for game_info in games_info:
            keyword_ids_for_game = game_info.get('keywords')

            if keyword_ids_for_game is not None:
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

        if len(covers_info) == 0:
            raise InvalidCoverIDError()

        return {cover_info['game']: cover_info['url'] for cover_info in covers_info}

    @classmethod
    def get_slugs_at_url(cls, url, ids):
        # Used to load keywords and genres by their ids

        slugs_info = cls.__make_request(url, f"fields slug; where id = ({str(ids)[1:-1]}); limit {len(ids)};")

        return {slug_info['id']: slug_info['slug'] for slug_info in slugs_info}


if __name__ == "__main__":
    games = IGDB_API.get_all_games()
    print(games)

    most_popular_game = games[0]
    print(IGDB_API.get_game(115278))
