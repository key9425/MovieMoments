from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # def get_default_profile_image():
    #     return f'{settings.STATIC_URL}images/default_profile.png'
    
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_img = models.ImageField(upload_to='profile_images/', default='default/profile.png', null=True, blank=True)

    # createsuperuser 명령어를 사용할 때 필요한 필드를 지정 (username field는 기본으로 유지)
    # serializers.py의 required=True는 API를 통한 일반 사용자 등록 시 필요한 필드를 지정
    # REQUIRED_FIELDS = ['email', 'name'] 
