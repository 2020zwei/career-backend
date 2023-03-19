from django.contrib import admin
from .models import Slot
from .forms import TimeSlotModelForm
class TimeSlotAdminDisplay(admin.ModelAdmin):
    
    
    form = TimeSlotModelForm
   
    list_display=['id','user']
admin.site.register(Slot,TimeSlotAdminDisplay)
