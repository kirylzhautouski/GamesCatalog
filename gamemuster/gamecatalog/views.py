from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .helpers import igdb_api


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'

    def __init__(self):
        super().__init__()

        self.current_page = 1
        self.search_query = ''

    def dispatch(self, request, *args, **kwargs):

        try:
            if 'page' in self.request.GET:
                self.current_page = int(self.request.GET['page'])
        except ValueError:
            raise Http404()

        if not (1 <= self.current_page <= 3):
            raise Http404()

        if 'search' in self.request.GET:
            self.search_query = self.request.GET['search']

        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        games = igdb_api.IGDB_API.get_all_games(games_count=18, search_query=(self.search_query
                                                                              if self.search_query != '' else None))

        return games[(self.current_page - 1) * 6: (self.current_page - 1) * 6 + 6]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['current_page'] = self.current_page
        context['search_query'] = self.search_query

        return context


class DetailsView(generic.TemplateView):
    template_name = 'gamecatalog/details.html'

    def __init__(self):
        super().__init__()

        self.game = {}

    def dispatch(self, request, *args, **kwargs):
        try:
            self.game = igdb_api.IGDB_API.get_game(kwargs['game_id'])
        except igdb_api.InvalidGameIDError:
            raise Http404()

        return super().dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['game'] = self.game

        return context


