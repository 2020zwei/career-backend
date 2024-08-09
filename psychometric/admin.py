from django.contrib import admin
from .models import Question, TestType, PsychometricTest,Answer, TestResult,TestResultDetail, CareerIdea, ChoiceIdea, StudyTips
from nested_admin import NestedTabularInline, NestedModelAdmin
from users.models import Counselor
# Register your models here.

@admin.register(CareerIdea)
class CareerIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']
    search_fields = ('type__type',)


@admin.register(ChoiceIdea)
class ChoiceIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'idea']
    search_fields = ('type__type',)


@admin.register(StudyTips)
class StudyTipsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    search_fields = ('type__type',)
    

class TestTypeAdminSite(admin.ModelAdmin):
    list_display=['id', 'type', 'description']
    search_fields = ("type",)

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
    search_fields = ('name',)

@admin.register(TestResult)
class TestResultAdmin(NestedModelAdmin):
    inlines = [ResultDetailInline]
    search_fields = ("user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


admin.site.register(TestType,TestTypeAdminSite)
