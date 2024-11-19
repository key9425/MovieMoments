from django.urls import path, include
from . import views


urlpatterns = [
    path('groups/', views.group_list),
    path('groups/<int:group_id>/', views.group_detail),
    path('groups/<int:group_movie_id>/articles/', views.article_list),
    path('groups/<int:group_movie_id>/articles/<int:article_id>/', views.article_detail),
    path('movie/', views.movie_list),
]
