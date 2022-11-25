from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from .serializers import EducationSerializer,JuniorCertTestSerializer,ExperienceSerializer,ReferenceSerializer,CvSerializer
from .models import CV,Education,JuniorCertTest,Experience,Reference
from rest_framework.exceptions import  ValidationError
from rest_framework import status
from rest_framework.response import Response


class CvViewRelated(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CvSerializer



class EducationViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EducationSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

class JuniorCertTestViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JuniorCertTestSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)


class ExperienceViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)


class ReferenceViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferenceSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    