from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .serializers import QuestionSerializer, QuizSerializer
from .models import Quiz,Question,QuizResult,Answer,QuizResultDetail
from user.models import Student
from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class QuizViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset=Quiz.objects.all()

    
    def get(self, request):
        """Fetch All Tests By User"""
        try:
            quiz=Quiz.objects.all()
            serializer = QuizSerializer(quiz, many=True)
            return Response(serializer.data)
    
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            TOTAL_POINT=0
            wrong=0
            user_obj=request.user
            questions= request.data.get('question')
            std_obj= Student.objects.get(user=user_obj)

            for quest in questions:
                ques_obj=Question.objects.get(question=quest['question'])
                ans_obj=Answer.objects.filter(question=ques_obj).filter(is_correct=True).first()
                if ques_obj:
                    option=quest['answer']
                    if option== ans_obj.answer:
                        TOTAL_POINT=TOTAL_POINT+ 1
                        score= TOTAL_POINT
                        name= quest['quiz']   
                        ans_detail=Answer.objects.filter(question=ques_obj).filter(answer=option).first()  
                    else:
                        wrong+=1
                else:
                    return Response("Question doesnt exist") 
            result_obj=QuizResult.objects.get_or_create(user=std_obj,score=score, quiz__name=name)
            result_detail=QuizResultDetail.objects.get_or_create(result=result_obj[0], answer=ans_detail, question=ques_obj)

            return Response(data={'success': True, 'Total Point': TOTAL_POINT}, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
    
class QuizDetails(CreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    lookup_field = 'id'

    def get_test(self, id):
        try:
            return Quiz.objects.get(id = id)
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        test = self.get_test(id)
        serializer = QuizSerializer(test)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        test = self.get_object(id)
        test.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

   
