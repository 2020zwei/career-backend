from rest_framework import serializers
from .models import Slot
from rest_framework.exceptions import NotFound, ValidationError



class TimeSlotAddSerializer(serializers.ModelSerializer):

    class Meta:
        model=Slot
        fields=['title','timeslot','endslot','day']
        
    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        validated_data["year"] = self.context['year']
        validated_data["week"] = self.context['week']

        return super().create(validated_data)


class TimeSlotRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model=Slot
        fields=['title','timeslot','day','endslot']
    def update(self, instance, validated_data):
        if Slot.objects.filter(timeslot=validated_data['timeslot'],user=self.context['user']):
            raise ValidationError(" You have already regesterd this slot")
        else:
         instance.timeslot=validated_data['timeslot']
         instance.endslot=validated_data['endslot']
         instance.title=validated_data['title']
         instance.day=validated_data['day']
         instance.save()
         return instance
    


    