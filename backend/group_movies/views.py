from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from .serializers import GroupSerializer
from .models import Article

#  Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def group_list(request):
    # GET 요청: 현재 인증된 사용자가 속한 그룹만 조회
    if request.method == 'GET':
        # request.user.include_groups.all()을 사용하여 사용자에 속한 그룹만 조회
        groups = request.user.include_groups.all()
        # groups = get_list_or_404(request.user.include_groups.all())
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

# POST 요청: 새 그룹 생성
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()  # 새 그룹 생성
            # 'members'는 사용자가 그룹에 추가될 사용자들의 ID 목록
            members = request.data.get('members', [])  # 배열로 전달된 사용자 ID 목록
            for user_id in members:
                user = get_user_model().objects.get(id=user_id)
                group.include_members.add(user)  # 각 사용자 추가
            # group.include_members.add(*members)
            return Response(serializer.data, status=status.HTTP_201_CREATED)