from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, TokenSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 회원가입 시 DB에 추가된 필드 저장 커스텀
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


# 유저 기본 정보
class UserLoginSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'name', 'email')

# 로그인 시 token 외 유저 기본 정보 제공 커스텀
class CustomTokenSerializer(TokenSerializer):
    user = UserLoginSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ('user',)


# 프로필 상세 정보 조회
class CustomUserDetailsSerializer(UserDetailsSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()  

    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = ('id','username', 'email', 'name', 'profile_img', 'followers_count','followings_count', 'is_following')
        read_only_fields = ('email', 'username', 'followers_count','followings_count', 'is_following')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        return obj.followers.filter(pk=request.user.pk).exists()
    
