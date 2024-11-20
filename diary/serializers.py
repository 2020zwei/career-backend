from rest_framework import serializers
from .models import WorkExperienceQuestion

class QuestionAnswerSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()

class NestedWorkExperienceSerializer(serializers.Serializer):
    day = serializers.ChoiceField(choices=WorkExperienceQuestion.DAY_CHOICES)
    date = serializers.DateField()
    questionsAndAnswers = QuestionAnswerSerializer(many=True)

class WorkExperienceDaySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.CharField()
    day = serializers.CharField()
    date = serializers.DateField()
    questionsAndAnswers = QuestionAnswerSerializer(many=True)
