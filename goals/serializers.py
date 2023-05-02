from rest_framework import serializers
from .models import Goal, Action
from rest_framework.exceptions import  ValidationError
from users.models import Student


class  GoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Goal
        fields=['goal','actions','realistic','countdown']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(GoalSerializer, self).create(validated_data=validated_data)


class GoalSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'proffession', 'goal', 'actions', 'realistic', 'countdown']