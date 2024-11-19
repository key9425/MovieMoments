from django.db import models
from django.conf import settings

# Create your models here.
class Group(models.Model):
    include_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='include_groups')
    group_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=10)
    group_img = models.ImageField(blank=True, upload_to='group_images/', default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    runtime = models.IntegerField()
    genres = models.JSONField()  # 또는 ManyToManyField
    production_countries = models.JSONField()
    director = models.CharField(max_length=255, null=True)
    cast = models.JSONField()
    trailer = models.CharField(max_length=255, null=True)


class GroupMovie(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='watched_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by_groups')
    watched_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='article')
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='comments')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
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


# 설문조사 모델
# 채팅 모델