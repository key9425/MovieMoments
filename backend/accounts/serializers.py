from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True, max_length=100)
    profile_img = serializers.ImageField(required=False)

    def custom_signup(self, request, user):
        user.name = self.validated_data['name']
        # profile_img가 제공되지 않으면 모델의 default 값이 자동으로 사용됨
        if 'profile_img' in self.validated_data:
            user.profile_img = self.validated_data['profile_img']
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    # is_following = serializers.SerializerMethodField()  # 추가


    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('username', 'email', 'name', 'profile_img', 'followers_count','followings_count')
        read_only_fields = ('email', 'username', 'followers_count','followings_count')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()
    
    # def get_is_following(self, obj):
    #     request = self.context.get('request')
    #     return obj.followers.filter(pk=request.user.pk).exists()
    
