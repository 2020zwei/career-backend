from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.



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
# class ResultDetailInline(NestedTabularInline):
#     model = QuizResultDetail
#     extra = 0


@admin.register(Choice)
class ChoiceAdmin(NestedModelAdmin):
    inlines = [Level5Inline,Level6Inline,Level8Inline, ApprenticeInline, OtherInline]
