from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from .serializers import GroupSerializer, MovieSerializer, GroupMovieSerializer, ArticleSerializer, CommentSerializer
from .models import Movie, GroupMovie, Group, Article, Comment

User = get_user_model

#  Create your views here.
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def group_list(request):
    # GET 요청: 현재 로그인 유저가 가입된 그룹 (메인페이지)
    if request.method == 'GET':
        groups = request.user.include_groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

# POST 요청: 새 그룹 생성
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()  # 새 그룹 생성
            # 'members'는 사용자가 그룹에 추가될 사용자들의 ID 목록
            members = request.data.get('members')
            group.include_members.add(*members)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def group_detail(request, group_id):
    group = Group.objects.get(pk=group_id)
    print(group)
    # GET 요청: 선택한 그룹에서 본 영화들
    if request.method == 'GET':
        group_movies = GroupMovie.objects.filter(group=group)
        serializer = GroupMovieSerializer(group_movies, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GroupMovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            movie = Movie.objects.get(pk=request.data.get('movie_id'))
            serializer.save(group=group, movie=movie)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        movies =  get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def article_list(request, group_movie_id):
    group_movie = get_object_or_404(GroupMovie, pk=group_movie_id)
    if request.method == 'GET':
        articles = Article.objects.filter(group_movie=group_movie).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, group_movie=group_movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def article_detail(request, group_movie_id, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)