from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_list),
    path('groups/<int:group_id>/movies/', views.group_movie_create),
    path('groups/<int:group_id>/', views.group_detail),
    path('movie/', views.movie_list),
    path('recommended-movies/', views.recommended_movies),

    # path('groups/<int:group_movie_id>/articles/<int:article_id>/', views.article_detail),
    # path('groups/<int:group_movie_id>/articles/', views.article_list),
    path('group/movie/<int:group_movie_id>/', views.group_movie_detail), # 그룹 무비 디테일(영화, 게시글, 타임라인, 갤러리) 조회
    path('group/movie/<int:group_movie_id>/articles/', views.article_create), # 게시글 생성
    path('group/movie/<int:group_movie_id>/timeline/', views.timeline_create), # 타임라인 생성

    

]
