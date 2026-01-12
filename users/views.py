from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import  UserRegisterSerializer, UserConfirmSerializer
import random
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
 

@api_view(['POST'])
def user_register_api_view(request):
    serializer = UserRegisterSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    user = User.object.create_user(
        username=serializer.validated_data['username'],
        password = serializer.validated_data['password'], is_active=False
    )
    
code = '_'.join([str(random.randint(0,9)) for _ in range(6)])

@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    comfirm = UserConfirmSerializer.objects.filter(
        user_id = serializer.validated_data['user_id'],
        code = serializer.validated_data['code'].first()
 )
    if comfirm:
        comfirm.user.is_active = True
        comfirm.user.save()
        comfirm.delete()
        return Response (data={'massage':'Пользователь успешно активен!'},
             status=status.HTTP_200_OK)
        
    return Response (data={'error':'Неверный код подтверждения!'},
            status=status.HTTP_404_NOT_FOUND)