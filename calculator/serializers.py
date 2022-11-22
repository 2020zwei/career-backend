from rest_framework import serializers
from .models import Subject,Level,SubjectGrade
from rest_framework.exceptions import  ValidationError
import json

class LevelSerializer(serializers.ModelSerializer):
     class Meta:
        model=Level
        fields=['subjectlevel']

        
class  SubjectSerializer(serializers.ModelSerializer):
    level=serializers.SerializerMethodField(read_only=True)
    def get_level(self, obj):
        temp=Subject.objects.filter(id=obj.id).values('level__subjectlevel')
        return (temp)

    class Meta:
        model=Subject
        fields=['name','level']
        


class SubjectGradeSerializer(serializers.ModelSerializer):

    class Meta:
        model=SubjectGrade
        fields=['grade']
   



    