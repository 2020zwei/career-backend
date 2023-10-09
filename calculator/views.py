from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView, DestroyAPIView
from rest_framework.views import APIView
from .serializers import SubjectSerializer,SubjectGradeSerializer, UserPointsSerializer
from .models import Subject,Level,SubjectGrade, UserPoints
from rest_framework.exceptions import  ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from common.response_template import get_response_template


# Create your views here.
class SubjectViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all().order_by('name') 

    
class SubjectGradeViewRelated(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectGradeSerializer

    def get_queryset(self):
        level = self.request.query_params.get('level')
        subject = self.request.query_params.get('subject')
        queryset = SubjectGrade.objects.filter(level__subjectlevel=level, subject__name=subject).order_by('grade')
        return queryset
    

# class CalculatePointViewRelated(APIView):
#     permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     points = 0
    #     total_points = 0
    #     bonus_points = 0
    #     breakpoint()
    #     for obj in request.data:
    #         grade = obj.get('grade')
    #         subject_grade_obj = SubjectGrade.objects.filter(pk=grade).first()
    #         if subject_grade_obj is None:
    #             raise ValidationError(f"No subject grade object found with following ids grade={grade}")
    #         points += subject_grade_obj.point
    #         if subject_grade_obj.subject.is_additional_marks_allowed:
    #             bonus_points += subject_grade_obj.subject.additional_marks

    #     response_template = get_response_template()
    #     total_points = bonus_points + points
    #     response_template['data'] = { 'total_points': total_points,'bonus_points':bonus_points,'points':points}
    #     return Response(data=response_template, status=status.HTTP_200_OK)


class CalculatePointViewRelated(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user.student
            UserPoints.objects.filter(user=user).delete()  # Delete previous records
            points = 0
            bonus_points = 0
            for obj in request.data:
                grade_id= obj.get('grade')
                subject_grade_obj = SubjectGrade.objects.filter(pk=grade_id).first()
                if subject_grade_obj is None:
                    raise ValidationError(f"No subject grade object found with following ids grade={grade_id}")
                subject = subject_grade_obj.subject
                if subject is None:
                    raise ValidationError(f"No subject found for subject grade with id {subject_grade_obj.id}")

                # Add subject, grade, and level to user's UserPoints
                user_points, _ = UserPoints.objects.get_or_create(user=user)
                user_points.grades.add(subject_grade_obj)

            for obj in request.data[:6]:
                grade_id= obj.get('grade')
                subject_grade_obj = SubjectGrade.objects.filter(pk=grade_id).first()
                if subject_grade_obj is None:
                    raise ValidationError(f"No subject grade object found with following ids grade={grade_id}")
                subject = subject_grade_obj.subject
                if subject is None:
                    raise ValidationError(f"No subject found for subject grade with id {subject_grade_obj.id}")

                points += subject_grade_obj.point
                if (subject_grade_obj.subject.is_additional_marks_allowed
                        and subject_grade_obj.level.subjectlevel == 'higher'
                        and subject_grade_obj.grade in ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']):
                    bonus_points += subject_grade_obj.subject.additional_marks

            # Update total points in UserPoints
            print(points)
            total_points = bonus_points + points
            print(total_points)
            user_points.total_points = total_points
            user_points.save()

            response_template = get_response_template()
            response_template['data'] = {'total_points': total_points, 'bonus_points': bonus_points, 'points': points}
            return Response(data=response_template, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e), 'data': request.data}, status=status.HTTP_400_BAD_REQUEST)

class UserPointsView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = UserPoints.objects.all()
    serializer_class = UserPointsSerializer

    def get(self, request):
        try:
            user = request.user.student
            if user:
                user_points = UserPoints.objects.filter(user=user)
                serializer = UserPointsSerializer(user_points, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserPointsDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserPoints.objects.all()  # Define your queryset here
    serializer_class = UserPointsSerializer  # Replace with your serializer class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the UserPoints instance to delete
        instance.delete()  # Delete the instance

        return Response({'message': 'User point deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class RemoveSubjectGradeFromUserPoints(APIView):
    def post(self, request):
        print("workingg==========")
        try:
            user_points_id = request.data.get('id')
            subject_id = request.data.get('subjectId')
            print(user_points_id, subject_id)

            user_points = UserPoints.objects.get(id=user_points_id)
            subject_grade = SubjectGrade.objects.get(id=subject_id)

            user_points.grades.remove(subject_grade)


            user_points.save()

            serializer = UserPointsSerializer(user_points)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserPoints.DoesNotExist:
            return Response({'message': 'UserPoints not found'}, status=status.HTTP_404_NOT_FOUND)
        except SubjectGrade.DoesNotExist:
            return Response({'message': 'SubjectGrade not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
