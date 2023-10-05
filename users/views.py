from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,GenericAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User,Student, School
from .serializers import SignupUserSerializer,UserSerializer,SchoolSerializer, StudentSignUpSerializer, UserSignUpSerializer, CustomTokenCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.db import transaction
from common.response_template import get_response_template
from django.conf import settings
from rest_framework_simplejwt.views import TokenViewBase

class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_message = next(iter(e.detail.values()))[0] if isinstance(e.detail, dict) else str(e.detail[0])
            return Response({"message": error_message}, status=400)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SignupUser(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user_serializer_obj  = UserSignUpSerializer(data=request.data)
            
            try:
                email = request.data.get('email')
                user_serializer_obj.validate_email(email)
            except ValidationError as e:
                error_message = str(e.detail[0]) if isinstance(e.detail, list) else str(e.detail)
                return Response({"message": error_message}, status=400)
            
            try:
                user_serializer_obj.is_valid(raise_exception=True)
            except ValidationError as e:
                # Check if the error message contains "user with this email already exists."
                if "user with this email already exists" in str(e):
                    return Response({"message": "The email address provided is already registered. Please use a different email address or log in with your existing account."}, status=400)

            user_obj = user_serializer_obj.save()
            school_name = request.data.get('school')
            # profile_image = request.data.get('profile_image') or settings.DEFAULT_PROFILE_IMAGE_PATH
            try:
                school_obj = School.objects.get(school=school_name)
            except School.DoesNotExist:
                # Create a new School object if it doesn't exist
                school_data = {
                    'school': school_name,
                }

            # Create the Student object
            full_name = request.data.get('full_name')
            if full_name:
                words = full_name.split()
                if len(words) == 2:
                    first_name = words[0]
                    last_name = words[1]
                else:
                    first_name = ""
                    last_name = ""
            student_data = {
                'first_name': first_name ,
                'last_name': last_name,
                'full_name': request.data.get('full_name'),
                'number': request.data.get('number'),
                'school': request.data.get('school'),
                'user': user_obj.pk,
                'profile_image': request.data.get('profile_image'),
                'dob': request.data.get('dob')
            }
            student_serializer_obj = StudentSignUpSerializer(data=student_data)
            if student_serializer_obj.is_valid():
                student_serializer_obj.save()
                print("workinggg")
            else:
                e = student_serializer_obj.errors
                print(e)
                # Handle the case when data is not valid, similar to how you handled it for user_serializer_obj
                if "Ensure that there are no more than 15 digits in total." in str(e):
                    return Response({"message": "Ensure that there are no more than 15 digits in total."}, status=400)
                else:
                    return Response({"message": str(e)}, status=400)
            print("doneeeee")
            response_template = get_response_template()
            response_template['data'] = student_serializer_obj.data
            return Response(data=response_template)


class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        try:
            queryset=Student.objects.get(id=self.request.user.student.id)
            return queryset
        except Exception as e:
            raise ValidationError(e)
    
    def patch(self, request):
        try:
            user = self.get_object()
            serializer = UserSerializer(user, data=request.data, partial=True) # set partial=True to update a data partially
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'data':serializer.data, 'success':True})
        except Exception as e:
            raise ValidationError(e)
class UserUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = Student.objects.all()

class SchoolView(CreateAPIView):
    permission_classes=[]
    serializer_class = SchoolSerializer

    def get(self, request):
        """Fetch All Tests By User"""
        try:
            schools = School.objects.order_by('school')
            serializer = SchoolSerializer(schools, many=True)
            return Response({'data':serializer.data, 'success':True})
    
        except Exception as e:
           return Response({'message': str(e)},success=False, status=status.HTTP_400_BAD_REQUEST)
        

from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError, NotFound
import random


class SendPasswordResetOTPView(APIView):
    permission_classes = []

    def send_otp_email(self,otp,email):
        try:
            send_mail(
                'Your Password Reset OTP',
                f'Your password reset otp is {otp}',
                'taloot.khan@zweidevs.com',
                [email])
        except:
            pass

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email is None:
            error_message = "No email provided."
            return Response({"message": error_message}, status=400)

        student_obj = Student.objects.filter(user__email=email).first()
        if student_obj is None:
            error_message = "he email address you provided is not associated with any registered account. Please ensure you have entered the correct email address."
            return Response({"message": error_message}, status=400)

        student_obj.otp = str(random.randint(1000, 9999))
        student_obj.otp_verified = False
        student_obj.save()
        self.send_otp_email(student_obj.otp, email)

        response_template = get_response_template()
        response_template['data'] = "An email has been sent to your account."
        return Response(response_template)


class OTPConfirmationAPIView(APIView):
    permission_classes = []

    def post(self,request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if email is None:
            raise ValidationError("email is required")
        if otp is None:
            raise ValidationError("email is required")
        student_obj = Student.objects.filter(user__email=email).first()
        if student_obj is None:
            raise NotFound("No studnet with this email found")
        response_template = get_response_template()
        if otp == student_obj.otp:
            student_obj.otp_verified = True
            student_obj.save()
            response_template['data'] = "OTP verfication succeeded"
            return Response(response_template)
        raise ValidationError("Incorrect OTP")


class ResetPasswordAPIView(APIView):
    permission_classes = []

    def patch(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        student_obj = Student.objects.filter(user__email=email).first()
        if email is None:
            raise ValidationError("email is required")
        if student_obj is None:
            raise NotFound("No studnet with this email found")
        if student_obj.otp_verified:
            student_obj.user.set_password(password)
            student_obj.user.save()
            student_obj.otp_verified = False
            student_obj.save()
            response_template = get_response_template()
            response_template['data'] = "Password reset successfully."
            return Response(response_template)
        raise ValidationError("OTP is not verified yet")
