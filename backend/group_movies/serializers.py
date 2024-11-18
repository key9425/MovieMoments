from rest_framework import serializers
from .models import Movie, Group, GroupMovie, Article, Comment
from django.contrib.auth import get_user_model


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('include_members',)


class GroupMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMovie
        fields = '__all__'
        read_only_fields = ('group', 'movie')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'group_movie')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')