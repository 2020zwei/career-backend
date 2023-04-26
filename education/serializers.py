from rest_framework import serializers
from .models import Quiz, QuizResult,Question,Answer
from users.models import Student

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

class ResultDetailSerializer(serializers.ModelSerializer):

    question= QuestionSerializer(many=True)

    class Meta:
        model=Quiz
        fields=['result','question', 'answer']


class QuizStatusSerializer(serializers.ModelSerializer):
    complete = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'complete', 'score', 'total_score']

    def get_complete(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if the user has completed the quiz
            result = QuizResult.objects.filter(user__user__email=request.user.email, quiz=obj).first()
            if result:
                return True
        return False

    def get_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Get the user's score for the quiz
            result = QuizResult.objects.filter(user__user__email=request.user.email, quiz=obj).first()
            if result:
                return result.score
        return None

    def get_total_score(self, obj):
        return obj.question.count()
