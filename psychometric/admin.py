from django.contrib import admin
from .models import (
    Question, TestType, PsychometricTest, Answer, TestResult,
    TestResultDetail, CareerIdea, ChoiceIdea, StudyTips
)
from nested_admin import NestedTabularInline, NestedModelAdmin
from users.models import Counselor


# Admin for CareerIdea
@admin.register(CareerIdea)
class CareerIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']
    search_fields = ['type__type', 'idea']


# Admin for ChoiceIdea
@admin.register(ChoiceIdea)
class ChoiceIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']
    search_fields = ['type__type', 'idea']


# Admin for StudyTips
@admin.register(StudyTips)
class StudyTipsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    search_fields = ['type__type', 'description']


# Admin for TestType
class TestTypeAdminSite(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    search_fields = ['type', 'description']


# Inline for Answers
class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1


# Inline for Questions
class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


# Inline for TestResultDetail
class ResultDetailInline(NestedTabularInline):
    model = TestResultDetail
    extra = 0


# Admin for PsychometricTest
@admin.register(PsychometricTest)
class PsychometricTestAdmin(NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ['id', 'name', 'intro']
    search_fields = ['name', 'intro']


# Admin for TestResult
@admin.register(TestResult)
class TestResultAdmin(NestedModelAdmin):
    inlines = [ResultDetailInline]
    list_display = ['id', 'user', 'test', 'score']
    search_fields = ['user__full_name', 'test__name', 'score']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


# Admin for TestType
admin.site.register(TestType, TestTypeAdminSite)
