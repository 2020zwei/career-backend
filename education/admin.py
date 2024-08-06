from django.contrib import admin
from .models import Question, Quiz, QuizResult,Answer,QuizResultDetail, QuizLimit
from nested_admin import NestedTabularInline, NestedModelAdmin
from users.models import Counselor
# Register your models here.

class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        AnswerInline,
    ]
class ResultDetailInline(NestedTabularInline):
    model = QuizResultDetail
    extra = 0


@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]

@admin.register(QuizResult)
class QuizResultAdmin(NestedModelAdmin):
    inlines = [ResultDetailInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


@admin.register(QuizLimit)
class SetQuizLimitAdmin(admin.ModelAdmin):
    list_display = ["limit"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs.count() > 1:
            qs = qs[:1]
        return qs

    def save_model(self, request, obj, form, change):

        if not change:
            if QuizLimit.objects.exists():
                raise ValueError("Only one SetQuizLimit instance is allowed.")
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if QuizLimit.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if obj is None and QuizLimit.objects.exists():
            return False
        return super().has_change_permission(request, obj)

