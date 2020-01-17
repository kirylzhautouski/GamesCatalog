from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'gamecatalog/home.html'


class DetailsView(generic.TemplateView):
    template_name = 'gamecatalog/details.html'
