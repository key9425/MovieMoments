from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomUserDetailsSerializer, UserLoginSerializer, UserImageUpdateSerializer
from group_movies.serializers import LikeMovieSerializer
from group_movies.models import LikeMovie
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# 프로필
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    # 프로필 조회
    if request.method == 'GET':
        person = User.objects.get(pk=user_pk)
        serializer = CustomUserDetailsSerializer(person, context={'request': request})
        return Response(serializer.data)
    # 프로필 이미지 수정
    elif request.method == "PUT":
        serializer = UserImageUpdateSerializer(
        request.user,
        data={'profile_img': request.FILES['profile_img']},
        partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data) # 이미지 전체 경로가 가지 않을 수 있음
     
# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request):
    if request.method == "DELETE":
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# follow
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    if request.method == 'POST':
        person = User.objects.get(pk=user_pk)
        # 자기자신을 팔로우하는지 확인
        if person != request.user:
            if person.followers.filter(pk=request.user.pk).exists():
                # 이미 팔로우한 경우 -> 언팔로우
                person.followers.remove(request.user)
                is_following = False
            else:
                # 팔로우하지 않은 경우 -> 팔로우
                person.followers.add(request.user)
                is_following = True
            return Response({
                'is_following': is_following,
                'followers_count': person.followers.count(),
                'followings_count': person.followings.count()
            })
        return Response({'error': '자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
# 좋아요
@api_view(['POST', 'GET'])
def like_movie(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movie_id')
        if request.user.liked_movie.filter(movie_id=movie_id).exists():
            is_liked = True
        else:
            is_liked = False
        return Response({
            'is_liked': is_liked,
        })

    elif request.method == 'POST':
        movie_id = request.data.get('movie_id')
        # 1. LikeMovie 테이블에 영화가 이미 있는지 확인
        if LikeMovie.objects.filter(movie_id=movie_id).exists():
            movie = LikeMovie.objects.get(movie_id=movie_id)
        else:
            serializer = LikeMovieSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                movie = serializer.save()

        # 2. 사용자가 이미 찜한 영화인지 확인
        if request.user.liked_movie.filter(movie_id=movie_id).exists():
            request.user.liked_movie.remove(movie)
            is_liked = False
        else:
            request.user.liked_movie.add(movie)
            is_liked = True
        
        return Response({
            'is_liked': is_liked,
        })


# User 검색
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('query', '')  # query
    users = User.objects.filter(
        Q(email__icontains=query) |  # query가 포함된 email
        Q(name__icontains=query)     # query가 포함된 name
    )
    serializer = UserLoginSerializer(users, many=True)
    return Response(serializer.data)