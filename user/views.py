import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from .utils import obtainTokenAuth0 , refreshTokenAuth0

User = get_user_model()

class RegisterView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({"email":"This field is required."},status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({"password":"This field is required."},status=status.HTTP_400_BAD_REQUEST)

        response = obtainTokenAuth0(email,password)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
    
        if not refresh_token:
            return Response({"refresh_token":"This field is required."},status=status.HTTP_400_BAD_REQUEST)

        response = refreshTokenAuth0(refresh_token)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)