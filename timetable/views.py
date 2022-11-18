from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import TimeSlotAddSerializer,TimeSlotRelatedSerializer
from datetime import date
from .models import Slot
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from rest_framework.response import Response



# Create your views here.
class AddTimeSlot(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSlotAddSerializer
    def get_serializer_context(self):
        todays_date = date.today()
        year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
        user=self.request.user.student
        new_slot= self.request.data.get("timeslot")
        if Slot.objects.filter(timeslot=new_slot,user=user):
                 raise ValidationError(" You have already regesterd this slot")

        else:
         return {'user': self.request.user, 'year': str(year),'week':str(week_num),'user':user}

class TimeSlotRelatedView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset=Slot.objects.all()
    serializer_class = TimeSlotRelatedSerializer
    def get_serializer_context(self):
       
        user=self.request.user.student
        return {'user':user}


class TimeSlotListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        todays_date = date.today()
        year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
        user = Slot.objects.filter(user=self.request.user.student,year=year,week=week_num)
        return user
    serializer_class = TimeSlotRelatedSerializer

class ResetWeekView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        todays_date = date.today()
        year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
        obj = Slot.objects.filter(user=self.request.user.student,year=year,week=week_num)
        obj.delete()
        return Response(data={'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)