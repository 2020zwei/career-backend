from django.contrib import admin
from .models import Question, TestType, PsychometricTest,Answer, TestResult,TestResultDetail, CareerIdea, ChoiceIdea, StudyTips
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

@admin.register(CareerIdea)
class CareerIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']


@admin.register(ChoiceIdea)
class ChoiceIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']


@admin.register(StudyTips)
class StudyTipsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'description']
    

class TestTypeAdminSite(admin.ModelAdmin):
    list_display=['id' ,'type','description']

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
