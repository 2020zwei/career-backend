from django.contrib import admin
from .models import Slot, UserColors
from .forms import TimeSlotModelForm
from users.models import Counselor


# Admin for Slot
class TimeSlotAdminDisplay(admin.ModelAdmin):
    form = TimeSlotModelForm
    list_display = ['id', 'user', 'title', 'day', 'timeslot', 'endslot', 'year', 'week']
    search_fields = ['user__full_name', 'title', 'day', 'year', 'week', 'timeslot', 'endslot']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


# Admin for UserColors
class UserColorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'color', 'created_at']
    search_fields = ['user__full_name', 'color']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


# Registering Admin Models
admin.site.register(Slot, TimeSlotAdminDisplay)
admin.site.register(UserColors, UserColorsAdmin)
