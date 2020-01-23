import requests

from django.conf import settings


class TWITTER_API:
    BASE_URL = 'https://api.twitter.com/1.1/search/tweets.json'

    HEADERS = {'authorization':
               f'Bearer {settings.TWITTER_BEARER_TOKEN}'}

    @classmethod
    def get_tweets_for_game(cls, game_name, tweets_count=5):
        url = f'{cls.BASE_URL}?q=%23{game_name} -filter:retweets'

        r = requests.get(url, headers=cls.HEADERS)

        if r.status_code != 200:
            r.raise_for_status()

        json_result = r.json()
        statuses = json_result['statuses'][:tweets_count]

        tweets = list()
        for status in statuses:
            tweet = {
                'text': status['text'],
                'created_at': status['created_at'],
                'user_name': status['user']['screen_name']
            }

            tweets.append(tweet)

        return tweets


if __name__ == "__main__":
    print(TWITTER_API.get_tweets_for_game("Cyberpunk 2077"))
