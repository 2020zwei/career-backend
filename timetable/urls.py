from django.urls import path
from .views import AddTimeSlot,TimeSlotRelatedView,TimeSlotListView,ResetWeekView


urlpatterns = [
    path('add-timeslot/',AddTimeSlot.as_view(),name="Add-timeslot"),
    path('delete-timeslot/<int:pk>',TimeSlotRelatedView.as_view(),name="Delete-timeslot"),
    path('get-timeslot/<int:pk>',TimeSlotRelatedView.as_view(),name="Reterive-timeslot"),
    path('update-timeslot/<int:pk>',TimeSlotRelatedView.as_view(),name="Update-timeslot"),
    path('list-timeslot/',TimeSlotListView.as_view(),name="List-timeslot"),
    path('reset-timeslot/',ResetWeekView.as_view(),name="Reset-timeslot"),
]