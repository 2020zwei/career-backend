from django.shortcuts import render
from django.core.mail import EmailMessage
from rest_framework.generics import CreateAPIView,RetrieveAPIView,GenericAPIView,UpdateAPIView
from .models import User, Student, School, StripeCustomer
from .serializers import SignupUserSerializer,UserSerializer,SchoolSerializer, StudentSignUpSerializer, UserSignUpSerializer, CustomTokenCreateSerializer
from django.contrib.auth.hashers import make_password
from django.db import transaction
from common.response_template import get_response_template
from django.conf import settings
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from .stripe import Stripe
import stripe
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

stripeObject = Stripe()


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
                if "user with this email already exists" in str(e):
                    return Response({"message": "The email address provided is already registered. Please use a different email address or log in with your existing account."}, status=400)

            user_obj = user_serializer_obj.save()
            school_name = request.data.get('school')
            
            try:
                school_obj = School.objects.get(school=school_name)
            except School.DoesNotExist:
                school_data = {'school': school_name}

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
                'first_name': first_name,
                'last_name': last_name,
                'full_name': request.data.get('full_name'),
                'number': request.data.get('number'),
                'school': request.data.get('school'),
                'user': user_obj.pk,
                'profile_image': request.data.get('profile_image'),
            }

            student_serializer_obj = StudentSignUpSerializer(data=student_data)
            if student_serializer_obj.is_valid():
                student_serializer_obj.save()

                if school_obj.category == "Gold" or school_obj.category == "Platinum":
                    student = Student.objects.get(user=user_obj)
                    student.is_subscribed = True
                    student.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)

            response_template = get_response_template()
            response_template['data'] = student_serializer_obj.data
            response_template['access_token'] = access_token  # Include the access token in the response
            return Response(data=response_template)

import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SubscriptionExpirationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info("Fetching subscription/payment expiration date")

        # Identify the logged-in user
        user = request.user
        logger.debug(f"Logged-in user: {user.email}")

        # Ensure the user is associated with a student account
        try:
            student = user.student
            logger.debug(f"Associated student: {student}")
        except Student.DoesNotExist:
            logger.error("Student instance not found for the user")
            return Response(
                {"detail": "The logged-in user is not associated with a student account."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the Stripe customer for the student
        try:
            stripe_customer = student.stripecustomer
            stripe_customer_id = stripe_customer.stripe_customer_id
            logger.debug(f"Stripe customer ID: {stripe_customer_id}")
        except StripeCustomer.DoesNotExist:
            logger.error("StripeCustomer instance not found for the student")
            return Response(
                {"detail": "The student does not have a Stripe customer account."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch payment intents for the Stripe customer
        stripe.api_key = os.environ.get('CG_STRIPE_SECRET_KEY')
        try:
            payment_intents = stripe.PaymentIntent.list(
                customer=stripe_customer_id,
                limit=10,  # Fetch up to 10 recent payment intents
            )
            logger.debug(f"Fetched payment intents: {payment_intents}")
        except stripe.error.StripeError as e:
            logger.error(f"Error fetching payment intents: {str(e)}")
            return Response({"detail": "Error fetching payment details."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter successful payment intents
        successful_payments = [
            intent for intent in payment_intents.data if intent.status == "succeeded"
        ]

        if not successful_payments:
            logger.warning("No successful payments found for the student")
            return Response(
                {"detail": "No payment history found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get the most recent successful payment
        latest_payment = successful_payments[0]
        last_payment_date = datetime.fromtimestamp(latest_payment.created)

        # Assume a fixed subscription interval of 30 days
        next_payment_date = last_payment_date + timedelta(days=30)

        # Format dates for the response
        response_data = {
            "last_payment_date": last_payment_date.strftime("%Y-%m-%d %H:%M:%S"),
            "next_payment_date": next_payment_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        logger.info(f"Returning subscription/payment expiration data: {response_data}")
        return Response(response_data, status=status.HTTP_200_OK)

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

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email is None:
            error_message = "No email provided."
            return Response({"message": error_message}, status=400)

        student_obj = Student.objects.filter(user__email=email).first()
        if student_obj is None:
            error_message = "The email address you provided is not associated with any registered account. Please ensure you have entered the correct email address."
            return Response({"message": error_message}, status=400)

        student_obj.otp = str(random.randint(1000, 9999))
        student_obj.otp_verified = False
        student_obj.save()
        try:
            email = EmailMessage(
            'Your Password Reset OTP',
            f'Your password reset otp is {student_obj.otp}',
            f"{os.environ['EMAIL_HOST_USER']}",  #sender email
            [email],  # List of recipient email addresses
            )
            email.send()
        except Exception as e:
            return Response({"message": f"Error sending email: {e}"})
    

        response_template = get_response_template()
        response_template['data'] = "An OTP has been sent to your account."
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


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stripe.api_key = os.environ.get('CG_STRIPE_SECRET_KEY')
        payment_method_info = stripe.PaymentMethod.create(
            type="card",
            card={
                "token": "tok_visa",
            },

            metadata={
                "name": "Waqas Idrees",
                "zip_or_postalCode": "1235"
            }
        )
        return Response({"detail": payment_method_info})

    def post(self, request):
        stripe.api_key = os.environ.get('CG_STRIPE_SECRET_KEY')
        try:
            user = request.user
            student_user = Student.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({"message": "you are not a student user"}, status=status.HTTP_404_NOT_FOUND)

        stripe_customer, created = StripeCustomer.objects.get_or_create(user=student_user)
        if created:
            try:
                stripe_customer_data = stripeObject.create_customer(email=student_user.user.email)
                stripe_customer.stripe_customer_id = stripe_customer_data.id
                stripe_customer.save()
            except Exception as e:
                return Response({'success': False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        stripe_customer_id = stripe_customer.stripe_customer_id
        payment_method_token = request.data.get('payment_method_token')
        amount = 1000  # Amount in cents (10 euros)
        currency = 'eur'

        try:
            stripeObject.attach_payment_method(stripe_customer_id, payment_method_token)

            payment_intent = stripeObject.create_payment_intent(
                amount=amount,
                currency=currency,
                payment_method_id=payment_method_token,
                customer_id=stripe_customer_id
            )

            if payment_intent.status == 'succeeded':
                stripe_customer.payment_method = "Card"
                stripe_customer.subscribed = True
                stripe_customer.payment_method_token = payment_method_token
                student_user.is_subscribed = True
                student_user.save()
                stripe_customer.save()

                return Response({'success': True, 'message': 'The Payment has been successfully completed.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'Payment failed.'},
                                status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.CardError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
