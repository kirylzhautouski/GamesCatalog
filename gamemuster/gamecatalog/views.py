from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .helpers import igdb_api


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'

    def get_queryset(self):
        games = igdb_api.IGDB_API.get_all_games(games_count=18)

        if 'page' in self.request.GET:
            current_page = int(self.request.GET['page'])
        else:
            current_page = 1

        return games[(current_page - 1) * 6: (current_page - 1) * 6 + 6]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        if 'page' in self.request.GET:
            current_page = int(self.request.GET['page'])

            # TODO: fix hardcoded page values later
            if not (1 <= current_page <= 3):
                context['current_page'] = 1
            else:
                context['current_page'] = current_page
        else:
            context['current_page'] = 1

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


