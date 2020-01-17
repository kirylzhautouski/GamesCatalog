import json

import requests


class InvalidGameIDError(Exception):
    pass


# noinspection PyPep8Naming
class IGDB_API:

    url = 'https://api-v3.igdb.com/games'
    headers = {'user-key': '47eeca1282bc48976b6949820fb991f1'}

    @classmethod
    def get_all_games(cls, games_count=10):
        r = requests.post(cls.url, headers=cls.headers,
                          data=f'fields name; sort popularity desc; limit {games_count};')

        if r.status_code != 200:
            r.raise_for_status()

        return json.loads(r.text)

    @classmethod
    def get_game(cls, game_id):
        pass


if __name__ == "__main__":
    games_info = IGDB_API.get_all_games()
    print(games_info)

    # most_popular_game = games_info[0]
    # print(IGDB_API.get_game(115278))
