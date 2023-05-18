from rest_framework import serializers
from .models import Slot
from rest_framework.exceptions import NotFound, ValidationError



class TimeSlotAddSerializer(serializers.ModelSerializer):

    class Meta:
        model=Slot
        fields=['id','title','timeslot','endslot','day']
        
    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        validated_data["year"] = self.context['year']
        validated_data["week"] = self.context['week']

        return super().create(validated_data)


class TimeSlotRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model=Slot
        fields=['id','title','timeslot','day','endslot']
    
    def update(self, instance, validated_data):
        timeslot = validated_data.get('timeslot')
        endslot = validated_data.get('endslot')

        if timeslot and endslot:
            if Slot.objects.filter(timeslot=timeslot, user=self.context['user']).exclude(pk=instance.pk).exists():
                raise ValidationError("You have already registered this slot")

        instance.timeslot = timeslot
        instance.endslot = endslot
        instance.title = validated_data.get('title', instance.title)
        instance.day = validated_data.get('day', instance.day)
        instance.save()
        response_data = {
        'success': True,
        'instance': instance,
        }
        return instance

    