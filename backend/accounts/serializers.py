from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(required=True)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.save()
        return user