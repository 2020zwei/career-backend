from rest_framework import serializers
from .models import PsychometricTest, TestType, Question, Answer, TestResult, TestResultDetail
from django.db.models import Sum
from users.models import Student

class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']

class TypeSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    class Meta:
        model=TestType
        fields=['id','type', 'score']
        extra_kwargs={'required':False}

    def get_score(self,obj):
        """Fetch score by test type"""
        type=TestType.objects.get(id=obj.id)
        user_obj=self.context["request"].user
        std_obj= Student.objects.get(user=user_obj.id)
        ques_obj= Question.objects.filter(type=type)
        res=TestResultDetail.objects.filter(result__user=std_obj).filter(question__type__type=type.type).aggregate(total=Sum("answer__weightage"))

        return res
    

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
