from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import SubjectSerializer,SubjectGradeSerializer
from .models import Subject,Level,SubjectGrade
from rest_framework.exceptions import  ValidationError
from rest_framework import status
from rest_framework.response import Response
from common.response_template import get_response_template


# Create your views here.
class SubjectViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset=Subject.objects.all()

    
class SubjectGradeViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectGradeSerializer

    def get_queryset(self):
        level = self.request.query_params.get('level')
        subject = self.request.query_params.get('subject')
        queryset = SubjectGrade.objects.filter(level__subjectlevel=level, subject__pk=subject)
        return queryset
    

class CalculatePointViewRelated(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        points = 0
        total_points = 0
        bonus_points = 0
        for obj in request.data:
            grade = obj.get('grade')
            subject_grade_obj = SubjectGrade.objects.filter(pk=grade).first()
            if subject_grade_obj is None:
                raise ValidationError(f"No subject grade object found with following ids grade={grade}")
            points += subject_grade_obj.point
            if subject_grade_obj.subject.is_additional_marks_allowed:
                bonus_points += subject_grade_obj.subject.additional_marks

        response_template = get_response_template()
        response_template['data'] = { 'total_points': total_points,'bonus_points':bonus_points,'points':points}
        return Response(data=response_template, status=status.HTTP_200_OK)