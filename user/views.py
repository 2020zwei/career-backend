from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializer import SignupUserSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student




class SignupUser(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = SignupUserSerializer

class UserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):
      queryset=Student.objects.filter(user=self.request.user).first()    
      return queryset