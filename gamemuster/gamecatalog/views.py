from django.shortcuts import render
from django.views import generic

from .helpers import igdb_api


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'

    def get_queryset(self):
        return igdb_api.IGDB_API.get_all_games()


class DetailsView(generic.TemplateView):
    template_name = 'gamecatalog/details.html'
