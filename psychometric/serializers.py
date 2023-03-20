from rest_framework import serializers
from .models import PsychometricTest, TestType,Question,Answer  
from user.models import Student

class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['question','answer','weightage']

class QuestionSerializer(serializers.ModelSerializer):
    answer= AnswerSerializer(many=True)
    class Meta:
        model=Question
        fields=['test','type','question','answer']

class PsychometricTestSerializer(serializers.ModelSerializer):

    question= QuestionSerializer(many=True)

    class Meta:
        model=PsychometricTest
        fields=['name','question']
