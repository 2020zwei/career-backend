from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,ListAPIView
from .serializers import QuestionSerializer, QuizSerializer, QuizStatusSerializer, QuizResultDetailSerializer
from .models import Quiz,Question,QuizResult,Answer,QuizResultDetail
from users.models import Student
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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

   
class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class TakeQuizView(CreateAPIView):
    serializer_class = QuizResultDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the quiz, student and their answers from the request data

        if request and request.user.is_authenticated:
            try:
                quiz_id = request.data.get('quiz')
                answers = request.data.get('answers')

                quiz = get_object_or_404(Quiz, id=quiz_id)
                # Save the quiz result for the student
                quiz_result = QuizResult.objects.create(
                    user=request.user.student, quiz_id=quiz_id, score=0
                )

                # Calculate the score for the quiz
                score = 0
                for answer in answers:
                    question_id = answer.get('question_id')
                    answer_id = answer.get('answer_id')

                    # Check if the answer is correct
                    is_correct = QuizResultDetail.objects.filter(
                        question_id=question_id, answer_id=answer_id, 
                        question__quiz_id=quiz_id, answer__is_correct=True
                    ).exists()

                    # Add to the score if the answer is correct
                    if is_correct:
                        score += 1

                    # Save the quiz result detail
                    result_detail = QuizResultDetail(
                        result_id=quiz_result.id,
                        question_id=question_id,
                        answer_id=answer_id,
                        # is_correct=is_correct
                    )
                    result_detail.save()

                # Update the score for the quiz result
                quiz_result.score = score
                quiz_result.save()

                return Response({'message': 'Quiz taken successfully', 'status': True, 'score':score, 'quiz':quiz.name}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e), 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please login'}, status=status.HTTP_400_BAD_REQUEST)
