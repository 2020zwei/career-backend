from rest_framework import serializers
from .models import Student, School
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from djoser.compat import get_user_email_field_name
from djoser.conf import settings
from rest_framework.exceptions import ValidationError
from djoser.serializers import TokenCreateSerializer
from django.db import IntegrityError, transaction
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.contrib.auth.hashers import make_password
import base64
from django.core.files.base import ContentFile
from datetime import date
from django.conf import settings as setting
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class CustomTokenCreateSerializer(TokenCreateSerializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "invalid_password": "The password is not correct",
        "inactive_account": "The given email is not registered",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()
    
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        self.user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not self.user:
            self.user = User.objects.filter(email=email).first()
            if self.user and not self.user.check_password(password):
                raise serializers.ValidationError(
                {'error': 'Invalid password'})
        if self.user and self.user.is_active:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return data
        raise serializers.ValidationError(
                {'error': 'Invalid email'})


class SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    full_name = serializers.CharField(max_length=200)
    dob = serializers.DateTimeField()
    city = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    eircode = serializers.CharField(max_length=200)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        fields=["id", "email","password", "full_name",'school','dob','city','country','address','eircode']
    def validate(self, attrs):
        user = User(attrs['email'], attrs['password'])
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs
    
    def create(self, validated_data):
        try:

            user = self.perform_create(email=validated_data['email'], password=validated_data['password'])
            Student.objects.create(user=user, full_name=validated_data['full_name'],school=validated_data['school'],dob=validated_data['dob'],city=validated_data['city'],country=validated_data['country'],address=validated_data['address'],eircode=validated_data['eircode'])

        except IntegrityError:
            self.fail("cannot_create_user")
        return Student.objects.create(user=user, full_name=validated_data['full_name'],school=validated_data['school'],dob=validated_data['dob'],city=validated_data['city'],country=validated_data['country'],address=validated_data['address'],eircode=validated_data['eircode'])

    def perform_create(self, email, password):
        with transaction.atomic():

            user = User.objects.create_user(email=email,password=password)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user



class UserSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required= False)
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model=Student
        fields=['full_name', 'school', 'dob', 'profile_image', 'email','address','city','country','current_step','cv_completed']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile_image = representation.get('profile_image')
        if profile_image is None:
            # representation['profile_image'] = 'https://cgb-staging-bucket.s3.amazonaws.com/profile_images/01437e4e-bfc5-44db-ba05-f5feed152c12.jpg?AWSAccessKeyId=AKIA6OTH6666Q3UAKHF2&Signature=oIEmDWSVsNxSm5rpTRDJYvlw%2BLg%3D&Expires=1687348379'
            representation['profile_image']='https://cgb-staging-bucket.s3.amazonaws.com/profile_images/01437e4e-bfc5-44db-ba05-f5feed152c12.jpg'
        return representation
    


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields=['pk','school','county']


class StudentSignUpSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required= False, allow_null= True)
    class Meta:
        model=Student
        fields=('first_name','last_name','profile_image','school','user','full_name',"dob")

    def validate_dob(self, value):
        """
        Validate that the 'dob' field is not greater than today's date.
        """
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    
    def to_internal_value(self, data):
        if 'profile_image' not in data:
            # Set the default value for 'profile_image' field
            data['profile_image'] = setting.DEFAULT_PROFILE_IMAGE_PATH
        return super().to_internal_value(data)
    

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('email','username','password')

    def validate(self, data):
        data['password'] = make_password(data['password'])
        return data