from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import *
from .models import *
from users.models import Student
from rest_framework import status
from django.db.models import Q
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
    
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            choice=Level8.objects.filter(choice__user=student.student)
            serializer = Level8_Serializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

class Level8Update(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level8
    queryset = Level8.objects.all()

class Level5ViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level5_Serializer
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            choice=Level5.objects.filter(choice__user=student.student)
            serializer = Level5_Serializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

class Level5Update(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level5
    queryset = Level5.objects.all()


class ApprenticeViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Apprentice_Serializer
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            choice=Apprentice.objects.filter(choice__user=student.student)
            serializer = Apprentice_Serializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

class ApprenticeUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Apprentice
    queryset = Apprentice.objects.all()


class OtherViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Other_Serializer
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            choice=Other.objects.filter(choice__user=student.student)
            serializer = Other_Serializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

class OtherUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Other
    queryset = Other.objects.all()

class Level6ViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level6_Serializer
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            choice=Level6.objects.filter(choice__user=student.student)
            serializer = Level6_Serializer(choice, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

class Level6Update(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Level6_Serializer
    queryset = Level6.objects.all()


class SelectedChoice(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceDetailSerializer
    
    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            cv=Choice.objects.filter(user=student.student).filter(Q(level6=True) | Q(Level5=True) | Q(level8=True) | Q(other=True)| Q(apprentice=True)).exclude(level6=False, Level5=False, level8=False, other=False, apprentice=False)
            serializer = ChoiceSerializer(cv, many=True)
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

class ColumnNamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            choice=request.headers['choice']
            if choice=='level6':
                column_names = [field.name for field in Level6._meta.get_fields()]
                return Response(column_names)
            if choice=='level5':
                column_names = [field.name for field in Level5._meta.get_fields()]
                return Response(column_names)
            if choice=='level8':
                column_names = [field.name for field in Level8._meta.get_fields()]
                return Response(column_names)
            if choice=='other':
                column_names = [field.name for field in Other._meta.get_fields()]
                return Response(column_names)            
            if choice=='apprentice':
                column_names = [field.name for field in Apprentice._meta.get_fields()]
                return Response(column_names)
            else:
                column_names = [field.name for field in Choice._meta.get_fields()]
                return Response(column_names)
        except Exception as e:
            raise e