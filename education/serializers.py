from rest_framework import serializers
from .models import Quiz, QuizResult, Question, Answer, QuizResultDetail
from users.models import Student

class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']


class AnswerSerializer(serializers.ModelSerializer):
    answer_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model=Answer
        fields=['answer_id', 'answer', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='answer')
    question_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model=Question
        fields=['question_id', 'question', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    quiz_id = serializers.IntegerField(source='id', read_only=True)
    questions = QuestionSerializer(many=True, source='question')

    class Meta:
        model=Quiz
        fields=['quiz_id', 'name', 'youtube_link', 'questions']


class QuizResultDetailSerializer(serializers.ModelSerializer):
    result = serializers.IntegerField(required=False)
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = QuizResultDetail
        fields = ['result', 'question', 'answer', 'is_correct']

    def create(self, validated_data):
        """
        Create a new QuizResultDetail object and return it.
        """
        quiz_result = validated_data.get('result')
        question = validated_data.get('question')
        answer = validated_data.get('answer')

        # Check if the answer is correct
        is_correct = QuizResultDetail.objects.filter(
            question=question, answer=answer, 
            question__quiz_id=quiz_result.quiz_id, answer__is_correct=True
        ).exists()

        # Create the quiz result detail object
        quiz_result_detail = QuizResultDetail(
            result=quiz_result,
            question=question,
            answer=answer,
            is_correct=is_correct
        )
        quiz_result_detail.save()

        return quiz_result_detail
    

class QuizStatusSerializer(serializers.ModelSerializer):
    complete = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'youtube_link', 'description', 'complete', 'score', 'total_score']

    def get_complete(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if the user has completed the quiz
            result = QuizResult.objects.filter(user__user__email=request.user.email, quiz=obj).last()
            if result:
                return True
        return False

    def get_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Get the user's score for the quiz
            result = QuizResult.objects.filter(user__user__email=request.user.email, quiz=obj).last()
            if result:
                return result.score
        return None

    def get_total_score(self, obj):
        return obj.question.count()
