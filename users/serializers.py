from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserAuthSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 150)
    password = serializers.CharField()

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter (username=username).exists():
         raise ValidationError("Пользователь с таким именем уже существует!")
        return username

class UserConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(min_length = 6, max_length = 6)
