from django.urls import path

from . import views

app_name = 'gamecatalog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:game_id>/', views.DetailsView.as_view(), name='details'),
]