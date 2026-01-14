import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserConfirm
from .serializers import UserRegisterSerializer, UserConfirmSerializer

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            is_active=False
        )

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        UserConfirm.objects.create(user=user, code=code)
        return Response(data={'user_id': user.id, 'code': code}, 
                        status=status.HTTP_201_CREATED)

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        confirm = UserConfirm.objects.filter(
            user_id=serializer.validated_data['user_id'],
            code=serializer.validated_data['code']
        ).first()
        
        if confirm:
            confirm.user.is_active = True
            confirm.user.save()
            confirm.delete()
            return Response(data={'message': 'Account activated!'}, 
                            status=status.HTTP_200_OK)
        
        return Response(data={'error': 'Invalid code or user_id'}, 
                        status=status.HTTP_404_NOT_FOUND)