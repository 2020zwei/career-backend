from rest_framework import serializers
from .models import Student, School
from djoser.serializers import UserCreateSerializer, TokenCreateSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from djoser.compat import get_user_email_field_name
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer


User = get_user_model()


class CustomTokenCreateSerializer(TokenCreateSerializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        self.user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not self.user:
            self.user = User.objects.filter(email=email).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")


class SignupUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Student
        fields=[ "full_name",'school','dob','city','country','address','eircode','profile_image']
   
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(SignupUserSerializer, self).create(validated_data=validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['first_name','last_name','school','dob']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields=['school','county']