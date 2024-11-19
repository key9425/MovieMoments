from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True, max_length=100)
    profile_img = serializers.ImageField(required=False)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.profile_img = self.validated_data.get('profile_img', None)
        # if 'profile_img' in self.validated_data:
        #     user.profile_img = self.validated_data['profile_img']
        user.save()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('username', 'email', 'name', 'profile_img')
        read_only_fields = ('email', 'username') # 이메일은 수정 불가능하도록 설정