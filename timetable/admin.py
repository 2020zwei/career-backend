from django.contrib import admin
from .models import Slot
class TimeSlotAdminDisplay(admin.ModelAdmin):
    
    
    
   
    list_display=['id','user']
admin.site.register(Slot,TimeSlotAdminDisplay)
