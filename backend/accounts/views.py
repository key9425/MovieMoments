from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .serializers import CustomUserDetailsSerializer, UserSerializer, LikeMovieSerializer
from group_movies.models import LikeMovie
from django.db.models import Q


# 프로필 (조회, 수정, 탈퇴)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    # 프로필 조회
    if request.method == 'GET':
        serializer = CustomUserDetailsSerializer(person, context={'request': request})
        return Response(serializer.data)
    # 프로필 이미지 수정
    elif request.method == "PUT":
        serializer = UserSerializer(
            request.user,
            data={'profile_img': request.FILES['profile_img']},
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        if request.user == person:
            request.user.delete()
            return Response({"message": "회원 탈퇴가 성공적으로 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "해당 작업을 수행할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# follow
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    if request.method == 'POST':
        person = get_user_model().objects.get(pk=user_pk)
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
    users = get_user_model().objects.filter(
        Q(email__icontains=query) |  # query가 포함된 email
        Q(name__icontains=query)     # query가 포함된 name
    )
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)