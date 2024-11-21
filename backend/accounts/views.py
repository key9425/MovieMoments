from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .serializers import CustomUserDetailsSerializer

User = get_user_model()

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    if request.method == 'GET':
        person = User.objects.get(pk=user_pk)
        serializer = CustomUserDetailsSerializer(person, context={'request': request})
        return Response(serializer.data)


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
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request):
    if request.method == "DELETE":
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
