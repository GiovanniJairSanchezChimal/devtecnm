from django.urls import path
from . import views
urlpatterns= [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # Asegúrate de que esta línea esté presente
    path('logout/', views.logout, name='logout'), 
    path('profile/', views.profile, name='profile'),
]