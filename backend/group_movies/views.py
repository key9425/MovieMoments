from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from .serializers import (GroupSerializer, MovieSerializer, GroupMovieSerializer, 
    CommentSerializer, GroupDetailSerializer, GroupWhatMovieSerializer, 
    GroupMovieDetailSerializer, ArticleCreateSerializer, ArticleImageCreateSerializer, ReviewCreateSerializer, ReviewSerializer, TimeLineCreateSerializer, ArticleSerializer, TimeLineSerializer)

from .models import Movie, GroupMovie, Group, Article, Comment, ArticleImage, Review, TimeLine
import random
from django.http import JsonResponse



User = get_user_model()

#  Create your views here.
# @api_view(['GET', 'POST'])
# # @permission_classes([IsAuthenticated])
# def group_list(request):
#     # GET 요청: 로그인한 유저가 속한 그룹 (메인페이지)
#     if request.method == 'GET':
#         groups = request.user.include_groups.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response(serializer.data)
#     # POST 요청: 새 그룹 생성
#     elif request.method == 'POST':
#         serializer = GroupSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             group = serializer.save()  # 새 그룹 생성
#             # 'members'는 사용자가 그룹에 추가될 사용자들의 ID 목록
#             members = request.data.get('members')
#             group.include_members.add(*members)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # 동일한 멤버로 구성된 그룹에 대한 처리가 필요한가?

# 241121 이송희 group_list view 수정
@api_view(['GET', 'POST'])
def group_list(request):
    if request.method == 'GET':
        groups = request.user.include_groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 그룹 먼저 생성
            group = serializer.save()
            
            # members 데이터 처리
            members = request.data.getlist('members', [])
            if members:
                # 문자열을 정수로 변환
                member_ids = [int(m) for m in members if m.isdigit()]
                # 현재 사용자도 포함
                if request.user.id not in member_ids:
                    member_ids.append(request.user.id)
                # 멤버 추가
                group.include_members.add(*member_ids)
            else:
                # 최소한 현재 사용자는 포함
                group.include_members.add(request.user.id)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def group_detail(request, group_id):
    group = Group.objects.get(pk=group_id)
    if request.method == 'GET':
        # 선택한 그룹에서 본 영화들
        serializer = GroupDetailSerializer(group)
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
    

# @api_view(['GET', 'POST'])
# # @permission_classes([IsAuthenticated])
# def article_list(request, group_movie_id):
#     group_movie = get_object_or_404(GroupMovie, pk=group_movie_id)
#     if request.method == 'GET':
#         articles = Article.objects.filter(group_movie=group_movie).order_by('-created_at')
#         response_data = {
#             'group_movie': GroupMovieSerializer(group_movie).data,
#             'articles': ArticleSerializer(articles, many=True).data
#         }
#         return Response(response_data)
#     elif request.method == 'POST':
#         serializer = ArticleCreateSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user, group_movie=group_movie)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# # @permission_classes([IsAuthenticated])
# def article_detail(request, group_movie_id, article_id):
#     article = get_object_or_404(Article, pk=article_id)
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user, article=article)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def group_movie_create(request, group_id):
   print('abc')
   group = get_object_or_404(Group, pk=group_id)
   
   # TMDB API에서 받은 영화 정보로 Movie 모델 생성 또는 조회
   movie_data = request.data.get('movie_data')  # 선택된 영화 정보 전체
   movie_id = movie_data.get('id')
   
   try:
       movie = Movie.objects.get(id=movie_id)
   except Movie.DoesNotExist:
       # Movie 모델에 새로 저장
       movie = Movie.objects.create(
           id=movie_id,
           title=movie_data.get('title'),
           original_title=movie_data.get('original_title'),
           release_date=movie_data.get('release_date'),
           overview=movie_data.get('overview'),
           poster_path=movie_data.get('poster_path'),
           backdrop_path=movie_data.get('backdrop_path'),
           vote_average=movie_data.get('vote_average'),
           vote_count=movie_data.get('vote_count'),
           runtime=movie_data.get('runtime', 0),  # 기본값 설정
           genres=movie_data.get('genres', {}),
           production_countries=movie_data.get('production_countries', {}),
           director=movie_data.get('director'),
           cast=movie_data.get('cast', {}),
           trailer=movie_data.get('trailer')
       )
   
   # GroupMovie 생성
   group_movie = GroupMovie.objects.create(
       group=group,
       movie=movie,
       watched_date=request.data.get('watched_date')
   )
   
   serializer = GroupWhatMovieSerializer(group_movie)
   return Response(serializer.data, status=status.HTTP_201_CREATED)

def recommended_movies(request):
    # 전체 영화 목록 가져오기
    all_movies = list(Movie.objects.all())

    num_recommendations = min(10, len(all_movies))
    
    # 랜덤하게 6개 선택
    recommended_movies = random.sample(all_movies, num_recommendations)

    movie_data = [{
        'id': movie.id,
        'title': movie.title,
        'poster_path': movie.poster_path,
        'release_date': movie.release_date
    } for movie in recommended_movies]
    return JsonResponse({
        'recommended_movies': movie_data
    })

#####################################################
# 그룹 무비 상세페이지 (게시글, 타임라인, 갤러리)
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def group_movie_detail(request, group_movie_id):
    group_movie = GroupMovie.objects.get(pk=group_movie_id)
    if request.method == 'GET':
        serializer = GroupMovieDetailSerializer(group_movie)
        return Response(serializer.data)


# 게시글 생성(갤러리 저장)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_create(request, group_movie_id):
    # 그룹 무비 조회
    group_movie = GroupMovie.objects.get(pk=group_movie_id)
    # 게시글 생성
    serializer = ArticleCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        article = serializer.save(user=request.user, group_movie=group_movie)

        # 이미지 파일들 처리
        images = request.FILES.getlist('images')
        for image in images:
            image_serializer = ArticleImageCreateSerializer(data={'image': image})
            if image_serializer.is_valid(raise_exception=True):
                image_serializer.save(article=article, group_movie=group_movie)
        
        # 생성된 게시글 반환
        return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.delete()
    return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return Response({"message": "리뷰가 삭제되었습니다."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def timeline(request, timeline_id):
    timeline = TimeLine.objects.get(id=timeline_id)
    timeline.delete()
    return Response({"message": "타임라인이 삭제되었습니다."}, status=status.HTTP_200_OK)


# 한줄평 생성
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_create(request, group_movie_id):
    # 그룹 무비 조회
    group_movie = GroupMovie.objects.get(pk=group_movie_id)
    serializer = ReviewCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        review=serializer.save(user=request.user, group_movie=group_movie)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        

# 타임라인 생성
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def timeline_create(request, group_movie_id):
    # 그룹 무비 조회
    group_movie = GroupMovie.objects.get(pk=group_movie_id)
    # 타임라인 생성
    serializer = TimeLineCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(group_movie=group_movie)
        
        # # 생성된 타임라인 반환
        # return Response(TimelineSerializer(timeline).data, status=status.HTTP_201_CREATED)

        # 해당 그룹 무비의 모든 타임라인 가져오기 및 반환
        timelines = group_movie.timeline.all()  # related_name 사용
        return Response(TimeLineSerializer(timelines, many=True).data, status=status.HTTP_201_CREATED)