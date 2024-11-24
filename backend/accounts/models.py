from django.db import models
from django.contrib.auth.models import AbstractUser
from group_movies.models import LikeMovie


# Create your models here.
class User(AbstractUser):    
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_img = models.ImageField(upload_to='profile_images/', default='default/profile.png', null=True, blank=True)
    followings = models.ManyToManyField(
        'self', 
        symmetrical=False,  # 맞팔로우가 자동으로 되지 않도록
        related_name='followers'  # 상대방 입장에서는 나를 팔로워로 보게 됨
    )
    liked_movie = models.ManyToManyField(LikeMovie, related_name='liked_by_users')