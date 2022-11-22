from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import SubjectSerializer,SubjectGradeSerializer
from .models import Subject,Level,SubjectGrade
from rest_framework.exceptions import  ValidationError
from rest_framework import status
from rest_framework.response import Response




# Create your views here.
class SubjectViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset=Subject.objects.all()
    
class SubjectGradeViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectGradeSerializer
    def get_queryset(self):
        level=self.request.query_params.get('level')
        queryset=SubjectGrade.objects.filter(level__subjectlevel=level)
        return queryset
    
class CalculatePointViewRelated(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        TOTAL_POINT=0
        for obj in request.data:

            temp=Subject.objects.filter(name=obj.get('subject'),is_additional_marks_allowed='True').first()
            if temp:
                grade=obj.get('grade')
                grade_value=SubjectGrade.objects.get(grade=grade)
                point=grade_value.point + temp.additional_marks
                TOTAL_POINT=TOTAL_POINT+point
            else:
                grade=obj.get('grade')
                grade_value=SubjectGrade.objects.get(grade=grade)
                TOTAL_POINT=TOTAL_POINT+grade_value.point
            
        
        return Response(data={'success': True, 'Total Point': TOTAL_POINT}, status=status.HTTP_200_OK)
 


