from django.contrib import admin
from .models import Goal, Action
# Register your models here.

class GoalAdminSite(admin.ModelAdmin):
    list_display=['user','goal','actions','realistic','countdown']

admin.site.register(Goal,GoalAdminSite)
admin.site.register(Action)
