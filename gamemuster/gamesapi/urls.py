from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'keywords', views.KeywordViewSet)
router.register(r'games', views.GameViewSet)

app_name = 'gamesapi'
urlpatterns = [
    path('', include(router.urls)),
]
