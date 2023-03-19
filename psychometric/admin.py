from django.contrib import admin
from .models import Question, TestType, PsychometricTest,Answer, TestResult
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

class TestTypeAdminSite(admin.ModelAdmin):
    list_display=['type']

class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        AnswerInline,
    ]

@admin.register(PsychometricTest)
class PsychometricTestAdmin(NestedModelAdmin):
    inlines = [QuestionInline]

admin.site.register(TestType,TestTypeAdminSite)
admin.site.register(TestResult)
