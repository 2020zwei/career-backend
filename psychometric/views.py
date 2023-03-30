from django.shortcuts import render
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .serializers import PsychometricTestSerializer
from .models import PsychometricTest,Answer,Question,TestType,TestResult,TestResultDetail
from user.models import Student
from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class PsychometricViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset=PsychometricTest.objects.all()

    
    def get(self, request):
        """Fetch All Tests By User"""
        try:
            tests=PsychometricTest.objects.all()
            serializer = PsychometricTestSerializer(tests, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            TOTAL_POINT=0
            user_obj=request.user
            questions=request.data.get('question')
            std_obj= Student.objects.get(user=user_obj.id)
            for quest in questions:
                ques_obj=Question.objects.filter(question=quest['question']).first()
                test_obj=PsychometricTest.objects.filter(name=request.data.get('name')).first()
                if ques_obj:
                    answer=quest['answer']
                    ans=Answer.objects.filter(answer=answer).filter(question=ques_obj).first()
                    weightage= ans.weightage
                    TOTAL_POINT=TOTAL_POINT+weightage
                    score= TOTAL_POINT
                    

                else:
                    return Response("Question doesnt exist") 
                
            result_obj=TestResult.objects.get_or_create(user=std_obj,score=score,test=test_obj)
            return Response(data={'success': True, 'Total Point': TOTAL_POINT}, status=status.HTTP_200_OK) 
        
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class PsychometricDetails(CreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = PsychometricTestSerializer

    lookup_field = 'id'

    def get_test(self, id):
        try:
            return PsychometricTest.objects.get(id = id)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        test = self.get_test(id)
        serializer = PsychometricTestSerializer(test)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        test = self.get_object(id)
        test.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CalculatePoints(CreateAPIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request,id):
        """Fetch score by test type"""
        try:
            type=TestType.objects.get(id=id)
            user_obj=request.user
            std_obj= Student.objects.get(user=user_obj.id)
            ques_obj= Question.objects.filter(type=type)
            res=TestResultDetail.objects.filter(result__user=std_obj).filter(question__type__type=type.type).aggregate(total=Sum("answer__weightage"))



            return Response(res)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)