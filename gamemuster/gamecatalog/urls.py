from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import forms


app_name = 'gamecatalog'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:upkb64>/<str:token>', views.ActivateView.as_view(), name='activate'),
    path('login/', auth_views.LoginView.as_view(
        form_class=forms.AuthFormWithPlaceholders,
        template_name='gamecatalog/log_in.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('favs/', views.FavouritesView.as_view(), name='favs'),
    path('ajax/favs/delete/<int:game_id>/', views.DeleteRestoreFavsView.as_view(), name='delete_from_favs'),
    path('ajax/favs/restore/<int:game_id>/', views.DeleteRestoreFavsView.as_view(), name='restore_to_favs'),
    path('games/', views.IndexView.as_view(), name='index'),
    path('games/<pk>/', views.DetailsView.as_view(), name='details'),
]
