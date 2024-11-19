from django.urls import path, include
from . import views


urlpatterns = [
    path('groups/', views.group_list),
]
