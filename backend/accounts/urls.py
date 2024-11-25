from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:user_pk>/profile/', views.profile),
    path('<int:user_pk>/follow/', views.follow),
    path('like/', views.like_movie),
    path('search/', views.search_users),
]