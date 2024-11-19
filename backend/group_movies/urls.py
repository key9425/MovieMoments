from django.urls import path, include
from . import views


urlpatterns = [
    path('groups/', views.group_list),
    path('groups/<int:group_id>/', views.group_detail),
    path('movie/', views.movie_list),
]
