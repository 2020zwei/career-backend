from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import WorkExperienceQuestion
from .serializers import WorkExperienceDaySerializer, NestedWorkExperienceSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import logging
logger = logging.getLogger(__name__)


class WorkExperienceQuestionViewSet(viewsets.ViewSet):
    """
    Handles grouped GET and POST requests for WorkExperienceQuestion.
    """
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
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


    @action(detail=False, methods=['put'], url_path='update-day')
    def update_day(self, request, *args, **kwargs):
        """
        Handles PUT requests to edit questions and answers for a specific day.
        """
        try:
            if not request.user.is_authenticated:
                return Response({"success": False, "message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

            # Check if user has an associated student
            student = getattr(request.user, 'student', None)
            if not student:
                return Response({"success": False, "message": "User does not have an associated student profile."}, status=status.HTTP_400_BAD_REQUEST)

            day = request.query_params.get('day')
            if not day or day not in dict(WorkExperienceQuestion.DAY_CHOICES).keys():
                raise ValidationError(
                    {"error": f"Invalid or missing day '{day}'. Allowed values are {', '.join(dict(WorkExperienceQuestion.DAY_CHOICES).keys())}."}
                )

            data = request.data
            serializer = NestedWorkExperienceSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            entry = serializer.validated_data

            if entry["day"] != day:
                raise ValidationError({"error": "Day in the query parameter must match the day in the request body."})

            date = entry["date"]
            questions_and_answers = entry["questionsAndAnswers"]

            # Delete existing questions for the day
            WorkExperienceQuestion.objects.filter(student=student, day=day).delete()

            # Create new question-answer pairs
            WorkExperienceQuestion.objects.bulk_create([
                WorkExperienceQuestion(
                    student=student,
                    day=day,
                    date=date,
                    question=qa["question"],
                    answer=qa["answer"]
                ) for qa in questions_and_answers
            ])

            return Response({"message": f"Questions for '{day}' updated successfully."}, status=status.HTTP_200_OK)
        except ValidationError as ve:
            logger.error(f"Validation error in update_day: {ve}")
            return Response({"success": False, "message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in update_day: {e}")
            return Response({"success": False, "message": f"Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)
