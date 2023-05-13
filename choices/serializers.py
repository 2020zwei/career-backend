from rest_framework import serializers
from .models import *
from users.models import Student


class StudentSerializer(serializers.ModelSerializer):
    model=Student
    fields=['first_name','last_name','address','eircode']


class ColumnNamesSerializer(serializers.Serializer):
    column_names = serializers.ListField(child=serializers.CharField())

class Level6_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Level6
        fields=['id','code','point','college','title','choice']
    def create(self, validated_data):
        return super(Level6_Serializer, self).create(validated_data=validated_data)



class Level8_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Level8
        fields=['id','code','point','college','title','choice']
    def create(self, validated_data):
        return super(Level8_Serializer, self).create(validated_data=validated_data)



class Apprentice_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Apprentice
        fields=['id','name','level','company','choice']
    def create(self, validated_data):
        return super(Apprentice_Serializer, self).create(validated_data=validated_data)



class Level5_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Level5
        fields=['id','code','college','title','choice']
    def create(self, validated_data):
        return super(Level5_Serializer, self).create(validated_data=validated_data)



class Other_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Other
        fields=['id','idea','choice']
    def create(self, validated_data):
        return super(Other_Serializer, self).create(validated_data=validated_data)

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields=['id','level6','Level5','level8','apprentice','other']
    
    def validate(self, attrs):
        user = self.context['request'].user.student
        if Choice.objects.filter(user=user).exists():
            pass # or you can simply allow updating by doing nothing
        return attrs
   
    def create(self, validated_data):
        user = self.context['request'].user.student
        if Choice.objects.filter(user=user).exists():
            instance = Choice.objects.get(user=user)
            instance.level6 = validated_data.get('level6', instance.level6)
            instance.Level5 = validated_data.get('Level5', instance.Level5)
            instance.level8 = validated_data.get('level8', instance.level8)
            instance.other = validated_data.get('other', instance.other)
            instance.apprentice = validated_data.get('apprentice', instance.apprentice)
            instance.save()
            return instance
        validated_data['user'] = self.context['request'].user.student
        return super(ChoiceSerializer, self).create(validated_data=validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key for key, value in data.items() if value is True}

class ChoiceDetailSerializer(serializers.ModelSerializer):

    lvl6= Level6_Serializer(many=True, required = False, allow_null=True, default=None)
    lvl8= Level8_Serializer(many=True, required = False, allow_null=True, default=None)
    lvl5= Level5_Serializer(many=True, required = False, allow_null=True, default=None)
    othr= Other_Serializer(many=True, required = False, allow_null=True, default=None)
    app= Apprentice_Serializer(many=True, required = False, allow_null=True, default=None)

    class Meta:
        model=Choice
        fields=['user','lvl6','lvl5','lvl8','app','othr']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.student
        lvl6_data = validated_data.pop('lvl6')
        lvl5_data = validated_data.pop('lvl5')
        lvl8_data = validated_data.pop('lvl8')
        app_data = validated_data.pop('app')
        othr_data = validated_data.pop('othr')
        ch_obj = Choice.objects.create(**validated_data)
        
        choice_obj= Choice.objects.filter(user=ch_obj.user.id).filter(level6='True')
        if choice_obj:
            pass
        if lvl6_data== None:
            pass        
        else:
            for lvl6_d in lvl6_data:
                Level6.objects.create(choice=ch_obj, **lvl6_d)
                ch_obj.level6='True'
                ch_obj.save()
        
        choice5_obj= Choice.objects.filter(user=ch_obj.user.id).filter(Level5='True')
        
        if choice5_obj:
            pass
        if lvl5_data== None:
            pass        
        else:
            for lvl5_d in lvl5_data:
                Level5.objects.create(choice=ch_obj, **lvl5_d)
                ch_obj.Level5='True'
                ch_obj.save()
        choice8_obj= Choice.objects.filter(user=ch_obj.user.id).filter(level8='True')
        if choice8_obj:
            pass
        if lvl8_data== None:
            pass        
        else:
            for lvl8_d in lvl8_data:
                Level8.objects.create(choice=ch_obj, **lvl8_d)
                ch_obj.level8='True'
                ch_obj.save()
        choice7_obj= Choice.objects.filter(user=ch_obj.user.id).filter(apprentice='True')
        if choice7_obj:
            pass
        if app_data== None:
            pass        
        else:
            for app_d in app_data:
                Apprentice.objects.create(choice=ch_obj, **app_d)
                ch_obj.apprentice='True'
                ch_obj.save()
        choice9_obj= Choice.objects.filter(user=ch_obj.user.id).filter(other='True')
        if choice9_obj:
            pass
        if othr_data== None:
            pass        
        else:
            for othr_d in othr_data:
                Other.objects.create(choice=ch_obj, **othr_d)
                ch_obj.other='True'
                ch_obj.save()
        return ch_obj


