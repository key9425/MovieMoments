from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_list),
    path('groups/<int:group_id>/movies/', views.group_movie_create),
    path('groups/<int:group_id>/', views.group_detail),
    path('movie/', views.movie_list),
    path('recommended-movies/', views.recommended_movies),

    path('group/movie/<int:group_movie_id>/', views.group_movie_detail), # 그룹 무비 디테일(영화, 게시글, 타임라인, 갤러리) 조회
    path('group/movie/<int:group_movie_id>/articles/', views.article_create), # 게시글 생성
    path('group/movie/<int:group_movie_id>/timeline/', views.timeline_create), # 타임라인 생성
    path('group/movie/<int:group_movie_id>/review/', views.review_create), # 리뷰 생성
    # path('group/movie/article/<int:article_id>/', views.article), # 게시글 수정, 삭제
    # path('group/movie/review/<int:review_id>/', views.review), # 한줄평 삭제
    # path('group/movie/timeline/<int:timeline_id>/', views.timeline), # 타임라인 삭제
]
