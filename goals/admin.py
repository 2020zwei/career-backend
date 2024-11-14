from django.contrib import admin
from .models import Goal, Action
from users.models import Counselor

class ActionInline(admin.TabularInline):
    model = Action
    extra = 1


class GoalAdminSite(admin.ModelAdmin):
    list_display = ['id', 'user', 'proffession', 'goal', 'description', 'realistic', 'countdown']
    search_fields = ['user__full_name', 'proffession', 'goal', 'description']
    inlines = [ActionInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


class ActionAdminSite(admin.ModelAdmin):
    list_display = ['goal', 'action']
    search_fields = ['goal__goal', 'goal__user__full_name', 'action']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(goal__user__school=counselor.school)
        return qs


admin.site.register(Goal, GoalAdminSite)
admin.site.register(Action, ActionAdminSite)
