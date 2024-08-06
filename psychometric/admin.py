from django.contrib import admin
from .models import Question, TestType, PsychometricTest,Answer, TestResult,TestResultDetail, CareerIdea, ChoiceIdea, StudyTips
from nested_admin import NestedTabularInline, NestedModelAdmin
from users.models import Counselor
# Register your models here.

@admin.register(CareerIdea)
class CareerIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']


@admin.register(ChoiceIdea)
class ChoiceIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']


@admin.register(StudyTips)
class StudyTipsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


admin.site.register(TestType,TestTypeAdminSite)
