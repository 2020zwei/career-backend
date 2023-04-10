from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .serializers import *
from .models import *
from users.models import Student
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class ChoiceViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceDetailSerializer
    
    def get(self, request):
        """Fetch All Chocies"""
        try:
            choice=Choice.objects.all()
            serializer = ChoiceDetailSerializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            resp=request.data
            count= len(resp[0])
            if count>4:
                return Response("The choices can not be greater than 3")
            else:
                many = isinstance(request.data, list)
                serializer = self.get_serializer(data=request.data, many=many)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e

class Level8ViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level8_Serializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e

class Level5ViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level5_Serializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e

class ApprenticeViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Apprentice_Serializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e

class OtherViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Other_Serializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e

class Level6ViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level6_Serializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        except Exception as e:
            raise e
