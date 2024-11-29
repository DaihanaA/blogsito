from rest_framework import generics
from users.serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Login successful'})
        return Response({'message': 'Invalid credentials'}, status=400)