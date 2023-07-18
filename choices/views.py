from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
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
    serializer_class = Level8_Serializer
    queryset = Level8.objects.all()

class Level8Delete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Level8.objects.all()
    serializer_class = Level8_Serializer

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
    serializer_class = Level5_Serializer
    queryset = Level5.objects.all()

class Level5Delete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Level5.objects.all()
    serializer_class = Level5_Serializer

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
    serializer_class = Apprentice_Serializer
    queryset = Apprentice.objects.all()

class ApprenticeDelete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Apprentice.objects.all()
    serializer_class = Apprentice_Serializer

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
    serializer_class = Other_Serializer
    queryset = Other.objects.all()

class OtherDelete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Other.objects.all()
    serializer_class = Other_Serializer

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

class Level6Delete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Level6.objects.all()
    serializer_class = Level6_Serializer

class SelectedChoice(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer
    
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
            if count>3:
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
            choice=request.GET.get('choice')
            if choice=='level6':
                all_fields = Level6._meta.get_fields()

                # Filter the list to include only the fields you want to include
                excluded_fields = ['id', 'choice']
                column_names = [f.name for f in all_fields if f.name not in excluded_fields]
                return Response({"data":column_names, "rows":10})
            if choice=='level5':
                all_fields = Level5._meta.get_fields()

                # Filter the list to include only the fields you want to include
                excluded_fields = ['id', 'choice']
                column_names = [f.name for f in all_fields if f.name not in excluded_fields]
                return Response({"data":column_names, "rows":5})
            if choice=='level8':
                all_fields = Level8._meta.get_fields()

                # Filter the list to include only the fields you want to include
                excluded_fields = ['id', 'choice']
                column_names = [f.name for f in all_fields if f.name not in excluded_fields]
                return Response({"data":column_names, "rows":10})
            if choice=='other':
                all_fields = Other._meta.get_fields()

                # Filter the list to include only the fields you want to include
                excluded_fields = ['id', 'choice']
                column_names = [f.name for f in all_fields if f.name not in excluded_fields]      
                return Response({"data":column_names, "rows":4})      
            if choice=='apprentice':
                all_fields = Apprentice._meta.get_fields()

                # Filter the list to include only the fields you want to include
                excluded_fields = ['id', 'choice']
                column_names = [f.name for f in all_fields if f.name not in excluded_fields]
                return Response({"data":column_names, "rows":5})
            else:
                column_names = [field.name for field in Choice._meta.get_fields()]
                return Response({"data":column_names, "rows":6})
        except Exception as e:
            raise e