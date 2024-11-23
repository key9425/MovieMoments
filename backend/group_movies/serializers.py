from rest_framework import serializers
from .models import Movie, Group, GroupMovie, Article, Comment, Timeline, ArticleImage
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


# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     like_count = serializers.IntegerField(source='like_users.count', read_only=True)
#     comment_count = serializers.IntegerField(source='comments.count', read_only=True)
#     class Meta:
#         model = Article
#         fields = ('id', 'user', 'title', 'content', 'like_count', 'comment_count')        


# class ArticleCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
#         read_only_fields = ('user', 'group_movie', 'like_users')





class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')

##############################################################
# 사용자 정보
class GroupMovieUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'name', 'profile_img')

# 게시글 생성
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['content']

# 게시글 이미지 생성
class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['image']

# 타임라인 생성
class TimelineCreateSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    class Meta:
        model = Timeline
        fields = ['id', 'time', 'description']

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['id', 'image']

class ArticleSerializer(serializers.ModelSerializer):
    user = GroupMovieUserSerializer(read_only=True)
    images = ArticleImageSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'images']

# 타임라인 조회
class TimelineSerializer(serializers.ModelSerializer):
     # 시간을 "HH:MM" 형식으로 반환
    time = serializers.TimeField(format='%H:%M')
    class Meta:
        model = Timeline
        fields = ['id', 'time', 'description']

# 그룹 무비 상세페이지 (영화, 게시글(사용자), 타임라인(사용자), 갤러리)-조회
class GroupMovieDetailSerializer(serializers.ModelSerializer):    
    article = ArticleSerializer(many=True, read_only=True)
    timeline = TimelineSerializer(many=True, read_only=True)
    article_img = ArticleImageSerializer(many=True, read_only=True)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = GroupMovie
        fields = [
            'id', 'movie', 'watched_date',
            'article', 'timeline', 'article_img'
        ]