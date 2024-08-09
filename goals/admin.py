from django.contrib import admin
from .models import Goal, Action
from users.models import Counselor
# Register your models here.

class GoalAdminSite(admin.ModelAdmin):
    list_display=['id','user','goal','description','realistic','countdown']
    search_fields = ("user__full_name",)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs

admin.site.register(Goal,GoalAdminSite)
admin.site.register(Action)
