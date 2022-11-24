from rest_framework import serializers
from .models import CV,Education,JuniorCertTest,Experience,Reference
from rest_framework.exceptions import  ValidationError



class  EducationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=Education
        fields=['year','school','examtaken']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(EducationSerializer, self).create(validated_data=validated_data)
        






    