from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import TimeSlotAddSerializer,TimeSlotRelatedSerializer
from datetime import date
from .models import Slot, UserColors
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, date,timedelta
from django.db.models.query import prefetch_related_objects
from django.db.models import OuterRef, Subquery


# Create your views here.
class AddTimeSlot(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSlotAddSerializer
    try:
        def get_serializer_context(self):
            todays_date = date.today()
            year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
            user=self.request.user.student
            color= self.request.data.get("color")
            new_slot= self.request.data.get("timeslot")
            end_slot=self.request.data.get("endslot")
            day=self.request.data.get("day")
            new_time = datetime.strptime(new_slot, '%H:%M:%S').time()
            end_time = datetime.strptime(end_slot, '%H:%M:%S').time()
            duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, new_time)

            # create color object in different table
            UserColors.objects.create(user=user,  color=color)
            if Slot.objects.filter(timeslot=new_slot,user=user,day=day):
                    raise ValidationError(" You have already regesterd this slot")
            else:
                return {'user': self.request.user, 'year': str(year),'week':str(week_num),'user':user}
    except Exception as e:
        raise

class TimeSlotRelatedView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset=Slot.objects.all()
    serializer_class = TimeSlotRelatedSerializer

    def get_serializer_context(self):   
        user=self.request.user.student
        return {'success': True, 'user':user}
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.request.user.student
        color = self.request.data.get("color")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_template = {
            'success':True,
            'data':serializer.data
        }
        queryset = self.filter_queryset(self.get_queryset())
        UserColors.objects.create(user=user, color=color)
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(response_template)


# class TimeSlotListView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         todays_date = date.today()
#         year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
#         user = Slot.objects.filter(user=self.request.user.student,year=year,week=week_num)
#         return user
#     serializer_class = TimeSlotRelatedSerializer
    

class TimeSlotListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSlotRelatedSerializer
    def get_queryset(self):
        user = Slot.objects.filter(user=self.request.user.student)
        return user


class ResetWeekView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        todays_date = date.today()
        year, week_num, day_of_week = todays_date.isocalendar()  # Using isocalendar() function   
        obj = Slot.objects.filter(user=self.request.user.student).delete()
        # obj.delete()
        return Response(data={'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)


class RecentColors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user.student

            latest_colors_subquery = UserColors.objects.filter(
                user=user,
                color=OuterRef('color')
            ).order_by('-created_at').values('created_at')[:1]

            recent_colors = UserColors.objects.filter(
                user=user,
                created_at=Subquery(latest_colors_subquery)
            ).values('color').distinct().order_by('-created_at')[:5]

            color_list = [{'color': item['color'], 'number': idx + 1}
                          for idx, item in enumerate(recent_colors)]

            return Response({'success': True, 'colors': color_list}, status=status.HTTP_200_OK)

        except UserColors.DoesNotExist:
            return Response({'success': False, 'message': 'No colors found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any other exceptions
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
