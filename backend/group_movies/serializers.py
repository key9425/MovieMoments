from rest_framework import serializers
from .models import Movie, Group, GroupMovie, Article, Comment
from django.contrib.auth import get_user_model


# 24111 이송희 groupmovies/serializers.py의 GroupSerializer 수정
# groupmovies/serializers.py
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('include_members',)
        
# class GroupSerializer(serializers.ModelSerializer):
#     class UserHomeSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = get_user_model() 
#             fields = ('id', 'username', 'name', 'email', 'profile_img')
#     include_members = UserHomeSerializer(many=True, read_only=True)
#     class Meta:
#         model = Group
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model() 
        fields = ('id', 'username', 'name', 'email', 'profile_img')

class MovieSerializer(serializers.ModelSerializer):
   class Meta:
       model = Movie
       fields = '__all__'

class GroupMovieSerializer(serializers.ModelSerializer):
   movie = MovieSerializer(read_only=True)
   
   class Meta:
       model = GroupMovie
       fields = ('id', 'movie', 'watched_date', 'created_at')

class GroupDetailSerializer(serializers.ModelSerializer):
   include_members = UserSerializer(many=True, read_only=True)
   watched_movies = GroupMovieSerializer(many=True, read_only=True)

   class Meta:
       model = Group
       fields = '__all__'



class GroupWhatMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = GroupMovie
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'like_count')        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')