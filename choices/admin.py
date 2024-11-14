from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.urls import path
from django.shortcuts import redirect, HttpResponse
from django.template.response import TemplateResponse
import pandas as pd
from django import forms
from users.models import Counselor
from django.contrib import messages


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()


class Level6Inline(NestedTabularInline):
    model = Level6


class Level8Inline(NestedTabularInline):
    model = Level8


class Level5Inline(NestedTabularInline):
    model = Level5


class ApprenticeInline(NestedTabularInline):
    model = Apprentice


class OtherInline(NestedTabularInline):
    model = Other


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ["user__full_name", "user__school", "user__city"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


class ApprenticeAdmin(admin.ModelAdmin):
    list_display = ['choice', 'name', 'level', 'company']
    search_fields = ["choice__user__full_name", "name", "level", "company"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level5Admin(admin.ModelAdmin):
    list_display = ['choice', 'code', 'title', 'college']
    search_fields = ["choice__user__full_name", "code", "title", "college"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class OtherAdmin(admin.ModelAdmin):
    list_display = ['choice', 'idea']
    search_fields = ["choice__user__full_name", "idea"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level6Admin(admin.ModelAdmin):
    list_display = ['choice', 'code', 'title', 'college', 'point']
    search_fields = ["choice__user__full_name", "code", "title", "college", "point"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level8Admin(admin.ModelAdmin):
    list_display = ['choice', 'code', 'title', 'college', 'point']
    search_fields = ["choice__user__full_name", "code", "title", "college", "point"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class AdminLevel5DataAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'college', 'course_information']
    search_fields = ["code", "title", "college", "course_information"]


class AdminLevel6DataAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'college', 'course_information', 'point']
    search_fields = ["code", "title", "college", "course_information", "point"]


class AdminLevel8DataAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'college', 'course_information', 'point']
    search_fields = ["code", "title", "college", "course_information", "point"]


class AdminApprenticeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'company']
    search_fields = ["name", "level", "company"]


class AdminOtherAdmin(admin.ModelAdmin):
    list_display = ['idea']
    search_fields = ["idea"]


# Register admin models
admin.site.register(AdminLevel5, AdminLevel5DataAdmin)
admin.site.register(AdminLevel6, AdminLevel6DataAdmin)
admin.site.register(AdminLevel8, AdminLevel8DataAdmin)
admin.site.register(AdminApprentice, AdminApprenticeAdmin)
admin.site.register(AdminOther, AdminOtherAdmin)

admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Level5, Level5Admin)
admin.site.register(Level6, Level6Admin)
admin.site.register(Level8, Level8Admin)
admin.site.register(Apprentice, ApprenticeAdmin)
admin.site.register(Other, OtherAdmin)
