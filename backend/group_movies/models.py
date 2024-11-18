from django.db import models
from django.conf import settings

# Create your models here.
# api 데이터 기반 필드 수정
class Movie(models.Model):
    api_movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    include_mambers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='include_groups')
    group_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=10)
    group_img = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupMovie(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='watched_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by_groups')
    watched_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='article')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,  related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 추가 모델) GroupMovies의 채팅 유사 기능 모델