from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'gamecatalog'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='gamecatalog/log_in.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('games/', views.IndexView.as_view(), name='index'),
    path('games/<int:game_id>/', views.DetailsView.as_view(), name='details'),
]
