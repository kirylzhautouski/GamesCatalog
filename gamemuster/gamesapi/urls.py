from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'keywords', views.KeywordViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'favourites', views.FavouriteViewSet)
router.register(r'screenshots', views.ScreenshotViewSet)

app_name = 'gamesapi'
urlpatterns = [
    path('', include(router.urls)),
    path('asd/', lambda request: HttpResponse('Hello World')),
]
