from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupUserSerializer,UserSerializer,SchoolSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student, School
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response




class SignupUser(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = SignupUserSerializer

class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        try:
            queryset=Student.objects.get(id=self.request.user.student.id)
            return queryset
        except Exception as e:
            raise ValidationError(e)


class SchoolView(CreateAPIView):
    permission_classes=[]
    serializer_class = SchoolSerializer

    def get(self, request):
        """Fetch All Tests By User"""
        try:
            schools=School.objects.all()
            serializer = SchoolSerializer(schools, many=True)
            return Response(serializer.data, success=True)
    
        except Exception as e:
           return Response({'message': str(e)},success=False, status=status.HTTP_400_BAD_REQUEST)