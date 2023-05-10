from rest_framework import serializers
from .models import CV,Education,JuniorCertTest,Experience,Reference, Skills, Qualities,LeavingCertTest
from rest_framework.exceptions import  ValidationError
from datetime import datetime
from users.models import Student

class SlashDateField(serializers.Field):
    """
    Serializer field that converts a slash-separated date string to a date object.
    """
    def to_internal_value(self, value):
        try:
            date_obj = datetime.strptime(value, '%m/%Y').date()
            return date_obj
        except (ValueError, TypeError):
            raise serializers.ValidationError('Invalid date format')
    
    def to_representation(self, value):
        if value is None:
            return None
        return value.strftime('%m/%Y')

class EducationListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Perform creations and updates.
        ret = []
        for data in validated_data:
            if "id" in data and data['id'] not in ['', None]:
                Education.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                data['user']=self.context.user.student
                ret.append(Education.objects.create(**data))
        return ret

class  EducationSerializer(serializers.ModelSerializer):
    year = SlashDateField(required=False, allow_null=True)

    class Meta:
        model=Education
        fields=['id','year','school','examtaken']
        list_serializer_class = EducationListSerializer
        extra_kwargs = {
            'id':{
                'read_only': False,
                'allow_null': True,
            }
        }        
class JuniorListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Perform creations and updates.
        ret = []

        for data in validated_data:
            if "id" in data and data['id'] not in ['', None]:
                JuniorCertTest.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                data['user']=self.context.user.student
                ret.append(JuniorCertTest.objects.create(**data))
        return ret
class  JuniorCertTestSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=JuniorCertTest
        fields=['id','subject','level','result']
        list_serializer_class = JuniorListSerializer
        extra_kwargs = {
            'id':{
                'read_only': False,
                'allow_null': True,
            }
        }

class  LeavingCertTestSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=LeavingCertTest
        fields=['subject','level','result']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(JuniorCertTestSerializer, self).create(validated_data=validated_data)

class ExperienceListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Perform creations and updates.
        ret = []

        for data in validated_data:
            if "id" in data and data['id'] not in ['', None]:
                Experience.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                data['user']=self.context.user.student
                ret.append(Experience.objects.create(**data))
        return ret
class  ExperienceSerializer(serializers.ModelSerializer):
    startdate = SlashDateField(required=False, allow_null=True)
    enddate = SlashDateField(required=False, allow_null=True)
    class Meta:
        model=Experience
        fields=['id','startdate','enddate','jobtitle','company','city','country','description','is_current_work']
        list_serializer_class = ExperienceListSerializer
        extra_kwargs = {'enddate': {'allow_null': True, 'required': False},
                        'id':{'read_only': False,'allow_null': True,}}

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
        fields=['id','objective','full_name','address','address2','eircode','city','town','email']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(CvSerializer, self).create(validated_data=validated_data)
   

class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Skills
        fields=['id','skill_dropdown']
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

    