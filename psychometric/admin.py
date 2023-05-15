from django.contrib import admin
from .models import Question, TestType, PsychometricTest,Answer, TestResult,TestResultDetail
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

class TestTypeAdminSite(admin.ModelAdmin):
    list_display=['type','description']

class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        AnswerInline,
    ]
class ResultDetailInline(NestedTabularInline):
    model = TestResultDetail

@admin.register(PsychometricTest)
class PsychometricTestAdmin(NestedModelAdmin):
    inlines = [QuestionInline]

@admin.register(TestResult)
class TestResultAdmin(NestedModelAdmin):
    inlines = [ResultDetailInline]


admin.site.register(TestType,TestTypeAdminSite)
