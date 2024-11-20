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
        serializer = CustomUserDetailsSerializer(person)
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
                is_followed = False
            else:
                # 팔로우하지 않은 경우 -> 팔로우
                person.followers.add(request.user)
                is_followed = True
            return Response({'is_followed': is_followed})
        return Response({'error': '자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)