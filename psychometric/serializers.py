from rest_framework import serializers
from .models import PsychometricTest, TestType, Question, Answer, TestResult, TestResultDetail
from users.models import Student

class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TestType
        fields=['id','type']
    

class AnswerSerializer(serializers.ModelSerializer):
    answer_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model=Answer
        fields=['answer_id', 'answer', 'weightage']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='answer')
    question_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model=Question
        fields=['question_id', 'type', 'question', 'answers']

class PsychometricTestSerializer(serializers.ModelSerializer):
    questions= QuestionSerializer(many=True, source='question')
    test_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model=PsychometricTest
        fields=['test_id', 'name','questions']


class PsychometricResultDetailSerializer(serializers.ModelSerializer):
    result = serializers.IntegerField(required=False)
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = TestResultDetail
        fields = ['result', 'question', 'answer']


class PsychometricStatusSerializer(serializers.ModelSerializer):
    complete = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = PsychometricTest
        fields = ['id', 'name', 'complete', 'score', 'total_score']

    def get_complete(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if the user has completed the quiz
            result = TestResult.objects.filter(user__user__email=request.user.email, test=obj).last()
            if result:
                return True
        return False

    def get_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Get the user's score for the quiz
            result = TestResult.objects.filter(user__user__email=request.user.email, test=obj).last()
            if result:
                return result.score
        return None

    def get_total_score(self, obj):
        questions = obj.question.all()
        total_score = sum([max(question.answer.all(), key=lambda x: x.weightage).weightage for question in questions])
        return total_score
