from rest_framework import serializers
from .models import Student



class SignupUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Student
        fields=['first_name','last_name','school','dob','city','country','address','eircode']
   
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(SignupUserSerializer, self).create(validated_data=validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['first_name','last_name','school','dob']