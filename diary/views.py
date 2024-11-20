from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import WorkExperienceQuestion
from .serializers import WorkExperienceDaySerializer, NestedWorkExperienceSerializer

class WorkExperienceQuestionViewSet(viewsets.ViewSet):
    """
    Handles grouped GET and POST requests for WorkExperienceQuestion.
    """
    def list(self, request):
    
        day = request.query_params.get('day')
        if day and day not in dict(WorkExperienceQuestion.DAY_CHOICES).keys():
            raise ValidationError(
                {"error": f"Invalid day '{day}'. Allowed values are {', '.join(dict(WorkExperienceQuestion.DAY_CHOICES).keys())}."}
            )

        queryset = WorkExperienceQuestion.objects.all()
        if day:
            queryset = queryset.filter(day=day)

        grouped_data = {}
        for item in queryset:
            if item.day not in grouped_data:
                grouped_data[item.day] = {
                    "id": item.id,
                    "user": item.student.user.username,
                    "day": item.day,
                    "date": item.date,
                    "questionsAndAnswers": [],
                }
            grouped_data[item.day]["questionsAndAnswers"].append({
                "question": item.question,
                "answer": item.answer,
            })

        return Response(list(grouped_data.values()), status=status.HTTP_200_OK)

    def create(self, request):
       
        data = request.data


        if isinstance(data, dict):
            data = [data]

        serializer = NestedWorkExperienceSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        for entry in serializer.validated_data:
            day = entry["day"]
            date = entry["date"]
            student = request.user.student

            # Create each question-answer pair for the day
            questions_and_answers = entry["questionsAndAnswers"]
            WorkExperienceQuestion.objects.bulk_create([
                WorkExperienceQuestion(
                    student=student,
                    day=day,
                    date=date,
                    question=qa["question"],
                    answer=qa["answer"]
                ) for qa in questions_and_answers
            ])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

