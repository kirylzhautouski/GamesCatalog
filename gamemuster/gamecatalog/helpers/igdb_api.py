import json

import requests


class InvalidGameIDError(Exception):
    pass


class InvalidCoverIDError(Exception):
    pass


# noinspection PyPep8Naming
class IGDB_API:

    games_url = 'https://api-v3.igdb.com/games'
    covers_url = 'https://api-v3.igdb.com/covers'

    headers = {'user-key': '47eeca1282bc48976b6949820fb991f1'}

    @classmethod
    def __make_request(cls, url, data):
        r = requests.post(url, headers=cls.headers,
                          data=data)

        if r.status_code != 200:
            r.raise_for_status()

        return json.loads(r.text)

    @classmethod
    def get_all_games(cls, games_count=10, platform_ids=None, genre_ids=None, user_rating_range=None):
        # TODO: use args to filter games

        games_info = cls.__make_request(cls.games_url, f'fields name,cover,genres,keywords; sort popularity desc;\
        limit {games_count};')

        # TODO: load cover, genres, keywords from their ids

        cover_ids = tuple((game_info['cover'] for game_info in games_info))
        covers_for_games = cls.get_covers(cover_ids)

        for game_info in games_info:
            game_info['cover'] = covers_for_games[game_info['id']]

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
        if len(cover_ids) == 1:
            data = f'fields game,url; where id = ({cover_ids[0]});'
        else:
            data = f'fields game,url; where id = {cover_ids};'

        covers_info = cls.__make_request(cls.covers_url, data)

        if len(covers_info) == 0:
            raise InvalidCoverIDError()

        return {cover_info['game']: cover_info['url'] for cover_info in covers_info}


if __name__ == "__main__":
    games = IGDB_API.get_all_games()
    print(games)

    most_popular_game = games[0]
    print(IGDB_API.get_game(115278))
