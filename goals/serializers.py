from rest_framework import serializers
from .models import Goal, Action
from rest_framework.exceptions import  ValidationError
from users.models import Student


class  GoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Goal
        fields=['goal','realistic','countdown']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        return super(GoalSerializer, self).create(validated_data=validated_data)

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['action']

class GoalSerializer2(serializers.ModelSerializer):
    action=ActionSerializer(many=True)
    class Meta:
        model = Goal
        fields = ['id', 'proffession', 'goal', 'realistic', 'countdown', 'action']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        actions = representation.pop('action')
        action_data = {f'action{index + 1}': action['action'] for index, action in enumerate(actions)}
        representation['actions'] = action_data
        return representation