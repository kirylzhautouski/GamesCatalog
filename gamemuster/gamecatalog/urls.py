from django.urls import path

from . import views

app_name = 'gamecatalog'
urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:game_id>/', views.DetailsView.as_view(), name='details'),
]
