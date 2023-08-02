import os
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import EducationSerializer,JuniorCertTestSerializer,ExperienceSerializer,ReferenceSerializer,CvSerializer, SkillSerializer,QualitiesSerializer, LeavingCertTestSerializer, StudentSerializer, InterestSerializer
from .models import CV,Education,JuniorCertTest,Experience,Reference,JobTitle,Qualities,Skills,LeavingCertTest, Interests
from users.models import Student
from django.template.loader import render_to_string
from weasyprint import HTML
from rest_framework.exceptions import  ValidationError
from rest_framework import status
from rest_framework.response import Response


class CvViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CvSerializer
    queryset=CV.objects.all()
    lookup_field = 'id'

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            cv=CV.objects.filter(user=student.student)
            serializer = CvSerializer(cv, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        try:
            cv_serializer_obj=CvSerializer(instance='',data=request.data,many=True, context=request)

            if cv_serializer_obj.is_valid(raise_exception=True):
                    cv_serializer_obj.save()
                    student = self.request.user.student
                    if student.cv_completed is not True:
                        student.current_step = 1
                        student.save()
                    return Response(cv_serializer_obj.data, status=status.HTTP_201_CREATED)
            else:
                return Response(cv_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CVUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CvSerializer
    queryset = CV.objects.all()


class EducationViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EducationSerializer
    queryset = Education.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Education.objects.filter(user=student.student)
            junior=JuniorCertTest.objects.filter(user=student.student)
            serializer = EducationSerializer(edu, many=True)
            serializer2 = JuniorCertTestSerializer(junior, many=True)
            data = {
            "education_data": serializer.data,
            "junior_data": serializer2.data,
        }
            return Response(data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            education_serializer_obj=EducationSerializer(instance='',data=request.data.get('education_data'),many=True, context=request)
            junior_serializer_obj=JuniorCertTestSerializer(instance='',data=request.data.get('junior_data'),many=True, context=request)

            if education_serializer_obj.is_valid(raise_exception=True):
                if junior_serializer_obj.is_valid(raise_exception=True):
                    education_serializer_obj.save()
                    junior_serializer_obj.save()
                    data={
                        "education_data": education_serializer_obj.data,
                        "junior_data":junior_serializer_obj.data
                    }
                    student = self.request.user.student
                    if student.cv_completed is not True:
                        student.current_step = 2
                        student.save()
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(education_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete_education(request, pk):
        """Delete Education"""
        try:
            education = Education.objects.get(pk=pk)
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EducationViewUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EducationSerializer
    queryset = Education.objects.all()

class JuniorCertTestViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JuniorCertTestSerializer
    queryset = JuniorCertTest.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=JuniorCertTest.objects.filter(user=student.student).last()
            serializer = JuniorCertTestSerializer(edu)
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
class JuniorViewUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JuniorCertTestSerializer
    queryset = JuniorCertTest.objects.all()

class LeavingCertTestViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeavingCertTestSerializer
    queryset = LeavingCertTest.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=LeavingCertTest.objects.filter(user=student.student).last()
            serializer = LeavingCertTestSerializer(edu)
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

class LeavingViewUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeavingCertTestSerializer
    queryset = LeavingCertTest.objects.all()

class ExperienceViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Experience.objects.filter(user=student.student)
            serializer = ExperienceSerializer(edu, many=True)
            return Response(serializer.data)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            experience_serializer_obj=ExperienceSerializer(instance='',data=request.data,many=True, context=request)

            if experience_serializer_obj.is_valid(raise_exception=True):
                    experience_serializer_obj.save()
                    student = self.request.user.student
                    if student.cv_completed is not True:
                        student.current_step = 3
                        student.save()
                    return Response(experience_serializer_obj.data, status=status.HTTP_201_CREATED)
            else:
                return Response(experience_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ExperienceViewUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()


class ReferenceViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferenceSerializer
    queryset = Reference.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Reference.objects.filter(user=student.student)
            serializer = ReferenceSerializer(edu, many=True)
            return Response(serializer.data)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            refer_serializer_obj=ReferenceSerializer(instance='',data=request.data,many=True, context=request)

            if refer_serializer_obj.is_valid(raise_exception=True):
                    refer_serializer_obj.save()
                    student = self.request.user.student
                    if student.cv_completed is not True:
                        student.current_step = 6
                        student.cv_completed = True
                        student.save()
                    return Response(refer_serializer_obj.data, status=status.HTTP_201_CREATED)
            else:
                return Response(refer_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReferenceViewUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferenceSerializer
    queryset = Reference.objects.all()


class SkillsViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skills.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Skills.objects.filter(user=student.student)
            quality=Qualities.objects.filter(user=student.student)
            serializer = SkillSerializer(edu,many=True)
            serializer2= QualitiesSerializer(quality, many =True)
            data={
                'skill_data':serializer.data,
                'quality_data':serializer2.data,
            }
            return Response(data)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            skill_serializer_obj=SkillSerializer(instance='',data=request.data.get('skill_data'),many=True, context=request)
            quality_serializer_obj=QualitiesSerializer(instance='',data=request.data.get('quality_data'),many=True, context=request)

            if skill_serializer_obj.is_valid(raise_exception=True):
                    if quality_serializer_obj.is_valid(raise_exception=True):
                        skill_serializer_obj.save()
                        quality_serializer_obj.save()
                    data={
                        "skill_data": skill_serializer_obj.data,
                        "quality_data":quality_serializer_obj.data
                    }
                    student = self.request.user.student
                    if student.cv_completed is not True:
                        student.current_step = 4
                        student.save()                 
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(skill_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SkillsUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skills.objects.all()


class QualityViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QualitiesSerializer
    queryset = Qualities.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Qualities.objects.filter(user=student.student)
            serializer = QualitiesSerializer(edu,many=True)
            return Response(serializer.data)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            quality_serializer_obj=QualitiesSerializer(instance='',data=request.data,many=True, context=request)

            if quality_serializer_obj.is_valid(raise_exception=True):
                    quality_serializer_obj.save()
                    return Response(quality_serializer_obj.data, status=status.HTTP_201_CREATED)
            else:
                return Response(quality_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class QualityUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QualitiesSerializer
    queryset = Qualities.objects.all()

class InterestViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterestSerializer
    queryset = Interests.objects.all()

    def get(self, request):
        """Fetch All Chocies"""
        try:
            student =self.request.user
            edu=Interests.objects.filter(user=student.student)
            serializer = InterestSerializer(edu,many=True)
            return Response(serializer.data)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            interest_serializer_obj=InterestSerializer(instance='',data=request.data,many=True, context=request)

            if interest_serializer_obj.is_valid(raise_exception=True):
                    interest_serializer_obj.save()
                    return Response(interest_serializer_obj.data, status=status.HTTP_201_CREATED)
            else:
                return Response(interest_serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InterestUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterestSerializer
    queryset = Interests.objects.all()

class GeneratePDF(CreateAPIView):
    def get(self, request):
        """Fetch All Notes By Officer"""
        try:

          student =self.request.user
          user_obj=Student.objects.get(id=student.student.id)
          cv_obj =CV.objects.filter(user=student.id)
          education_obj=Education.objects.filter(user=student.id)
          junior_cert_obj=JuniorCertTest.objects.filter(user=student.id)
          leave_cert_obj=LeavingCertTest.objects.filter(user=student.id)
          exp_obj=Experience.objects.filter(user=student.id)
          skill_obj=Skills.objects.filter(user=student.id)
          quality_obj=Qualities.objects.filter(user=student.id)
          refer_obj=Reference.objects.filter(user=student.id)
          temp_name = "general/templates/" 
          cv_template = str(user_obj.first_name) +"-"+str(user_obj.last_name) +"-"+"cv" + ".html"
          open(temp_name + cv_template, "w").write(render_to_string('cv.html', {'student_detail': user_obj,'cv_detail':cv_obj,'education_detail':education_obj,'Junior_Cert_detail':junior_cert_obj,'Leave_Cert_detail':leave_cert_obj,'skill_detail':skill_obj,'qualities_detail':quality_obj,'Experience_detail':exp_obj,'Reference_detail':refer_obj}))
          HTML(temp_name + cv_template).write_pdf(str(user_obj.first_name)+'.pdf')
          file_location = f'{user_obj.first_name}.pdf'
          with open(file_location, 'rb') as f:
            file_data = f.read()
          response = HttpResponse(file_data, content_type='application/pdf')
          response['Content-Disposition'] = 'attachment; filename="'+ user_obj.first_name +'".pdf'
          return response
        except Exception as e:
          return Response({'message': "Please complete all fields to download CV"}, status=status.HTTP_400_BAD_REQUEST)
