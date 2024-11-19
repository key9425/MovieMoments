from rest_framework import serializers
from .models import Movie, Group, GroupMovie, Article, Comment
from django.contrib.auth import get_user_model

class GroupSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()  # AUTH_USER_MODEL
            fields = '__all__'
    include_members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'
        # read_only_fields = ('include_members',)


# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'


# class GroupMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupMovie
#         fields = '__all__'
#         read_only_fields = ('group', 'movie')


# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
#         read_only_fields = ('user', 'like_users', 'group_movie')


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('user', 'article')