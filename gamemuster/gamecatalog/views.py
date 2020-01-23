from django.http import Http404
from django.shortcuts import render
from django.views import generic

from requests import HTTPError

from .helpers import igdb_api, twitter_api


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'

    def get_queryset(self):
        return igdb_api.IGDB_API.get_all_games()


class DetailsView(generic.TemplateView):
    template_name = 'gamecatalog/details.html'

    def __init__(self):
        super().__init__()

        self.game = {}
        self.tweets = []

    def dispatch(self, request, *args, **kwargs):
        try:
            self.game = igdb_api.IGDB_API.get_game(kwargs['game_id'])

        except igdb_api.InvalidGameIDError:
            raise Http404()

        try:
            self.tweets = twitter_api.TWITTER_API.get_tweets_for_game(self.game['name'])
        except HTTPError:
            pass

        return super().dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['game'] = self.game
        context['tweets'] = self.tweets

        return context


