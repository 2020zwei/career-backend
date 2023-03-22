from rest_framework import serializers
from .models import Quiz, QuizResult,Question,Answer
from user.models import Student

class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['question','answer','is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answer= AnswerSerializer(many=True)
    class Meta:
        model=Question
        fields=['quiz','question','answer']

class QuizSerializer(serializers.ModelSerializer):

    question= QuestionSerializer(many=True)

    class Meta:
        model=Quiz
        fields=['name','question']

# class ResultSerializer(serializers.ModelSerializer):
#     model=QuizResult
#     fields=['quiz','user','score']
