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
        fields=['contactnumber','jobtitle','contactemail']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(ExperienceSerializer, self).create(validated_data=validated_data)
        
class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']



class CvSerializer(serializers.ModelSerializer):
    
    user = StudentSerializer(read_only=True)
    class Meta:
        model=CV
        fields=['user','objective','is_juniorcert_test','skills','HobbiesandInterests']
   

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

    