from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .serializers import PsychometricTestSerializer
from .models import PsychometricTest,Answer,Question,TestType,TestResult
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
        TOTAL_POINT=0
        user_obj=request.user
        ques_obj=Question.objects.filter(question=request.data.get('question')).first()
        result_obj=TestResult.objects.get(user=user_obj.id)
        if ques_obj:
            answer=request.data.get('answer')
            ans=Answer.objects.get(answer=answer)
            weightage= ans.weightage
            TOTAL_POINT=TOTAL_POINT+weightage
            result_obj.score= TOTAL_POINT
            result_obj.test.name= request.data.get('name')
            return Response(data={'success': True, 'Total Point': TOTAL_POINT}, status=status.HTTP_200_OK)
        else:
            return Response("Question doesnt exist")    
    
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

   
