from rest_framework import serializers
from .models import Movie, Group, GroupMovie, Article, Comment
from django.contrib.auth import get_user_model

class GroupSerializer(serializers.ModelSerializer):
    class UserHomeSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model() 
            fields = ('id', 'username', 'name', 'email', 'profile_img')
    include_members = UserHomeSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class GroupMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = GroupMovie
        fields = '__all__'
        read_only_fields = ('group', )


class ArticleSerializer(serializers.ModelSerializer):
    class CommentListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = '__all__'
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'group_movie')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')