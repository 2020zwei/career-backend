from rest_framework import serializers
from .models import CV,Education,JuniorCertTest,Experience,Reference, Skills, Qualities,LeavingCertTest
from rest_framework.exceptions import  ValidationError
from users.models import Student


class  EducationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=Education
        fields=['year','school','examtaken']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(EducationSerializer, self).create(validated_data=validated_data)

class  JuniorCertTestSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=JuniorCertTest
        fields=['subject','level','result']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(JuniorCertTestSerializer, self).create(validated_data=validated_data)

class  LeavingCertTestSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=LeavingCertTest
        fields=['subject','level','result']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(JuniorCertTestSerializer, self).create(validated_data=validated_data)

class  ExperienceSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=Experience
        fields=['startdate','enddate','jobtitle','company']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(ExperienceSerializer, self).create(validated_data=validated_data)

class  ReferenceSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=Reference
        fields=['cv','contact_number','position','email','name']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['full_name','address','address2','eircode','city','eircode']



class CvSerializer(serializers.ModelSerializer):

    class Meta:
        model=CV
        fields=['objective','full_name','address','address2','eircode','city','town','email']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(CvSerializer, self).create(validated_data=validated_data)
   

class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Skills
        fields=['skill','description']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(SkillSerializer, self).create(validated_data=validated_data)

class QualitiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Qualities
        fields=['quality','description']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(QualitiesSerializer, self).create(validated_data=validated_data)

    